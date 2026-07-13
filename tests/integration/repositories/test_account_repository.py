"""Integration tests for AccountRepository against a real (in-memory) SQLite DB."""
import pytest

from core_app.domain.models.account import Account
from core_app.domain.models.user import User
from core_app.repositories.account_repository import AccountRepository
from core_app.repositories.user_repository import UserRepository


@pytest.fixture()
def user(db_session):
    u = User(id=0, email="a@a.com", name="Alice", username="alice")
    u.set_password("secret123")
    return UserRepository(db_session).create(u)


class TestCreate:
    def test_assigns_id_and_persists(self, db_session, user):
        repo = AccountRepository(db_session)
        account = Account(id=0, name="Nubank", account_type="Checking", user_id=user.id)
        created = repo.create(account)
        assert created.id != 0

        found = repo.find_by_id(created.id)
        assert found.name == "Nubank"
        assert found.user_id == user.id


class TestFind:
    def test_find_by_id_missing_returns_none(self, db_session):
        repo = AccountRepository(db_session)
        assert repo.find_by_id(999) is None

    def test_find_all_by_user_scopes_to_owner(self, db_session, user):
        repo = AccountRepository(db_session)
        other_user_repo = UserRepository(db_session)
        other = other_user_repo.create(
            User(id=0, email="b@b.com", name="Bob", username="bob")
        )
        repo.create(Account(id=0, name="Nubank", account_type="Checking", user_id=user.id))
        repo.create(Account(id=0, name="Itau", account_type="Savings", user_id=other.id))

        results = repo.find_all_by_user(user.id)

        assert len(results) == 1
        assert results[0].name == "Nubank"

    def test_find_all_by_user_respects_pagination(self, db_session, user):
        repo = AccountRepository(db_session)
        for i in range(5):
            repo.create(Account(id=0, name=f"Acc{i}", account_type="Checking", user_id=user.id))

        page = repo.find_all_by_user(user.id, skip=2, limit=2)

        assert len(page) == 2


class TestDelete:
    def test_delete_removes_account(self, db_session, user):
        repo = AccountRepository(db_session)
        created = repo.create(Account(id=0, name="Nubank", account_type="Checking", user_id=user.id))
        repo.delete(created.id)
        assert repo.find_by_id(created.id) is None

    def test_delete_missing_account_raises_value_error(self, db_session):
        repo = AccountRepository(db_session)
        with pytest.raises(ValueError, match="Account with id 999 not found"):
            repo.delete(999)
