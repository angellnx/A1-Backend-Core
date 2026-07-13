"""Fixtures for API integration tests (FastAPI TestClient).

IMPORTANT — assumptions made here (routers/schemas were not shared):
- POST /api/v1/auth/register is assumed to accept JSON:
  {"email": ..., "name": ..., "username": ..., "password": ..., "phone": ...}
  matching UserService.create_user's parameters.
- POST /api/v1/auth/login is assumed to use FastAPI's standard
  OAuth2PasswordRequestForm (form-encoded "username" + "password"), since
  dependencies.py wires OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
  and core/security.py encodes {"sub": username} — the conventional pairing.

If either assumption is wrong, adjust `register_user` / `auth_headers` below
to match your actual router/schema — everything else in these API tests
(the client + in-memory DB wiring) will keep working unchanged.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from core_app.main import app
from core_app.database import session as db_session_module


@pytest.fixture()
def client(engine):
    """TestClient wired to the in-memory `engine` fixture from tests/conftest.py."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_session():
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[db_session_module.get_session] = override_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def register_user(client, email="alice@example.com", username="alice", password="secret123"):
    return client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "name": "Alice",
            "username": username,
            "password": password,
        },
    )


def login(client, username="alice", password="secret123"):
    return client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )


@pytest.fixture()
def registered_user(client):
    response = register_user(client)
    assert response.status_code in (200, 201), response.text
    return response.json()


@pytest.fixture()
def auth_headers(client, registered_user):
    response = login(client)
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
