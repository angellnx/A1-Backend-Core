"""Integration tests for UserRepository against a real (in-memory) SQLite DB."""
from core_app.domain.models.user import User
from core_app.repositories.user_repository import UserRepository


def make_user(email="a@a.com", username="alice", password="secret123"):
    user = User(id=0, email=email, name="Alice", username=username)
    user.set_password(password)
    return user


class TestCreate:
    def test_assigns_id_and_persists(self, db_session):
        repo = UserRepository(db_session)
        created = repo.create(make_user())
        assert created.id != 0

        found = repo.find_by_id(created.id)
        assert found is not None
        assert found.email == "a@a.com"
        assert found.username == "alice"

    def test_persists_password_hash_not_plaintext(self, db_session):
        repo = UserRepository(db_session)
        created = repo.create(make_user(password="secret123"))
        found = repo.find_by_id(created.id)
        assert found.check_password("secret123") is True
        assert found.check_password("wrong") is False


class TestFind:
    def test_find_by_id_missing_returns_none(self, db_session):
        repo = UserRepository(db_session)
        assert repo.find_by_id(999) is None

    def test_get_by_username(self, db_session):
        repo = UserRepository(db_session)
        repo.create(make_user(username="bob"))
        found = repo.get_by_username("bob")
        assert found is not None
        assert found.username == "bob"

    def test_get_by_username_missing_returns_none(self, db_session):
        repo = UserRepository(db_session)
        assert repo.get_by_username("nobody") is None

    def test_get_by_email(self, db_session):
        repo = UserRepository(db_session)
        repo.create(make_user(email="bob@bob.com"))
        found = repo.get_by_email("bob@bob.com")
        assert found is not None
        assert found.email == "bob@bob.com"

    def test_find_all(self, db_session):
        repo = UserRepository(db_session)
        repo.create(make_user(email="a@a.com", username="alice"))
        repo.create(make_user(email="b@b.com", username="bob"))
        assert len(repo.find_all()) == 2


class TestDelete:
    def test_delete_removes_user(self, db_session):
        repo = UserRepository(db_session)
        created = repo.create(make_user())
        repo.delete(created.id)
        assert repo.find_by_id(created.id) is None

    def test_delete_missing_user_is_noop(self, db_session):
        repo = UserRepository(db_session)
        repo.delete(999)  # should not raise
