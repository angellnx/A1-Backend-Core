"""Tests for the global IntegrityError -> 409 handler in main.py.

Rather than trying to guess which router endpoint might let a raw
IntegrityError bubble up (every service currently pre-checks duplicates
with its own ValueError before touching the DB, so triggering the real
409 path through the public API would require a genuine race condition
between two simultaneous requests -- flaky and not worth relying on for
CI), this tests the handler function itself directly. That's exactly
the unit under test and gives a deterministic, fast result.
"""
import pytest
from fastapi import Request
from sqlalchemy.exc import IntegrityError

from core_app.main import integrity_error_handler


def make_request() -> Request:
    """Minimal ASGI scope so Request() can be constructed for the handler."""
    scope = {
        "type": "http",
        "method": "POST",
        "path": "/api/v1/whatever/",
        "headers": [],
    }
    return Request(scope)


@pytest.mark.asyncio
async def test_integrity_error_returns_409():
    exc = IntegrityError("INSERT INTO ...", params={}, orig=Exception("UNIQUE constraint failed"))

    response = await integrity_error_handler(make_request(), exc)

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_integrity_error_response_body_does_not_leak_internals():
    """The handler must not expose raw SQL, params, or the original driver
    exception to the client -- only a clean, generic message."""
    sensitive_detail = "UNIQUE constraint failed: user.email VALUES('leaked@internal.example')"
    exc = IntegrityError(
        "INSERT INTO user ...",
        params={"email": "leaked@internal.example"},
        orig=Exception(sensitive_detail),
    )

    response = await integrity_error_handler(make_request(), exc)
    body = response.body.decode()

    assert "detail" in body
    assert "leaked@internal.example" not in body
    assert "UNIQUE constraint failed" not in body
    assert "INSERT INTO" not in body
