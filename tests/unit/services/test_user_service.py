"""Unit tests for UserService.

Repository is mocked so these tests exercise only the business rules
in the service layer (required-field validation, duplicate checks,
password hashing delegation), not persistence.
"""
from unittest.mock import Mock

import pytest

from core_app.domain.models.user import User
from core_app.repositories.user_repository import UserRepository
from core_app.services.user_service import UserService


@pytest.fixture()
def repo():
    return Mock(spec=UserRepository)


@pytest.fixture()
def service(repo):
    return UserService(repository=repo)


class TestCreateUser:
    def test_create_user_success(self, repo, service):
        repo.get_by_username.return_value = None
        repo.get_by_email.return_value = None
        repo.create.side_effect = lambda u: u

        result = service.create_user(
            email="alice@example.com",
            name="Alice",
            username="alice",
            password="secret123",
        )

        assert result.email == "alice@example.com"
        assert result.username == "alice"
        assert result.check_password("secret123") is True
        repo.create.assert_called_once()

    def test_create_user_missing_email(self, service):
        with pytest.raises(ValueError, match="Email is required"):
            service.create_user(email="", name="Alice", username="alice", password="secret123")

    def test_create_user_missing_name(self, service):
        with pytest.raises(ValueError, match="Name is required"):
            service.create_user(email="alice@example.com", name="", username="alice", password="secret123")

    def test_create_user_missing_username(self, service):
        with pytest.raises(ValueError, match="Username is required"):
            service.create_user(email="alice@example.com", name="Alice", username="", password="secret123")

    def test_create_user_missing_password(self, service):
        with pytest.raises(ValueError, match="Password is required"):
            service.create_user(email="alice@example.com", name="Alice", username="alice", password="")

    def test_create_user_duplicate_username(self, repo, service):
        repo.get_by_username.return_value = User(
            id=1, email="existing@example.com", name="Existing", username="alice"
        )
        with pytest.raises(ValueError, match="Username 'alice' already exists"):
            service.create_user(
                email="alice@example.com", name="Alice", username="alice", password="secret123"
            )

    def test_create_user_duplicate_email(self, repo, service):
        repo.get_by_username.return_value = None
        repo.get_by_email.return_value = User(
            id=1, email="alice@example.com", name="Existing", username="existing"
        )
        with pytest.raises(ValueError, match="Email 'alice@example.com' already exists"):
            service.create_user(
                email="alice@example.com", name="Alice", username="alice", password="secret123"
            )


class TestGetUser:
    def test_get_user_success(self, repo, service):
        user = User(id=1, email="alice@example.com", name="Alice", username="alice")
        repo.find_by_id.return_value = user
        assert service.get_user(1) is user

    def test_get_user_not_found(self, repo, service):
        repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="User '1' not found"):
            service.get_user(1)


class TestDeleteUser:
    def test_delete_user_success(self, repo, service):
        repo.find_by_id.return_value = User(
            id=1, email="alice@example.com", name="Alice", username="alice"
        )
        service.delete_user(1)
        repo.delete.assert_called_once_with(1)

    def test_delete_user_not_found(self, repo, service):
        repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="User '1' not found"):
            service.delete_user(1)
