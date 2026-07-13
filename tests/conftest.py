"""Shared pytest fixtures for the A1 Backend Core test suite.

Provides an isolated in-memory SQLite database per test, so repository
and API integration tests never touch the real `a1.db` file and never
leak state between tests.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core_app.database.base import Base

# Import every ORM model module so its table registers with Base.metadata.
# Without this, Base.metadata.create_all() would create an empty schema.
from core_app.database.models import (  # noqa: F401
    account_model,
    budget_model,
    category_model,
    currency_model,
    item_model,
    transaction_model,
    transaction_type_model,
    user_model,
)


@pytest.fixture()
def engine():
    """Fresh in-memory SQLite engine per test.

    StaticPool keeps the same connection alive for the whole test so the
    in-memory database isn't wiped between statements (SQLite's default
    in-memory behavior is one DB per connection).
    """
    eng = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)
    eng.dispose()


@pytest.fixture()
def db_session(engine):
    """A SQLAlchemy session bound to the in-memory test engine."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
