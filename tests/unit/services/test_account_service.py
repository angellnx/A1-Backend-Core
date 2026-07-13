"""Unit tests for AccountService.

Repositories are mocked so these tests exercise only the business rules
in the service layer (validation, ownership enforcement), not persistence.
"""
from unittest.mock import Mock

import pytest

from core_app.domain.models.account import Account
from core_app.domain.models.user import User
from core_app.repositories.account_repository import AccountRepository
from core_app.repositories.user_repository import UserRepository
from core_app.services.account_service import AccountService


@pytest.fixture()
def account_repo():
    return Mock(spec=AccountRepository)


@pytest.fixture()
def user_repo():
    return Mock(spec=UserRepository)


@pytest.fixture()
def service(account_repo, user_repo):
    return AccountService(repository=account_repo, user_repository=user_repo)


class TestCreateAccount:
    def test_create_account_missing_name_raises(self, service):
        with pytest.raises(ValueError, match="Name is required"):
            service.create_account(name="", account_type="Checking", user_id=1)

    def test_create_account_missing_type_raises(self, service):
        with pytest.raises(ValueError, match="Type is required"):
            service.create_account(name="Nubank", account_type="", user_id=1)

    def test_create_account_user_not_found_raises(self, service, user_repo):
        user_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="User with id 1 not found"):
            service.create_account(name="Nubank", account_type="Checking", user_id=1)

    def test_create_account_success(self, service, account_repo, user_repo):
        user_repo.find_by_id.return_value = User(
            id=1, email="a@a.com", name="A", username="a"
        )
        account_repo.create.side_effect = lambda acc: acc

        result = service.create_account(name="Nubank", account_type="Checking", user_id=1)

        assert result.name == "Nubank"
        assert result.account_type == "Checking"
        assert result.user_id == 1
        account_repo.create.assert_called_once()


class TestGetAccount:
    def test_get_account_not_found_raises(self, service, account_repo):
        account_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Account with id 99 not found"):
            service.get_account(account_id=99, current_user_id=1)

    def test_get_account_wrong_owner_raises_permission_error(self, service, account_repo):
        account_repo.find_by_id.return_value = Account(
            id=1, name="Nubank", account_type="Checking", user_id=1
        )
        with pytest.raises(PermissionError, match="do not have access"):
            service.get_account(account_id=1, current_user_id=2)

    def test_get_account_success(self, service, account_repo):
        account = Account(id=1, name="Nubank", account_type="Checking", user_id=1)
        account_repo.find_by_id.return_value = account
        assert service.get_account(account_id=1, current_user_id=1) is account


class TestListAccountsByUser:
    def test_list_accounts_user_not_found_raises(self, service, user_repo):
        user_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="User with id 1 not found"):
            service.list_accounts_by_user(user_id=1)

    def test_list_accounts_paginates_through_repository(self, service, account_repo, user_repo):
        user_repo.find_by_id.return_value = User(
            id=1, email="a@a.com", name="A", username="a"
        )
        account_repo.find_all_by_user.return_value = []

        service.list_accounts_by_user(user_id=1, skip=10, limit=5)

        account_repo.find_all_by_user.assert_called_once_with(1, skip=10, limit=5)


class TestDeleteAccount:
    def test_delete_account_not_found_raises(self, service, account_repo):
        account_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Account with id 1 not found"):
            service.delete_account(account_id=1, current_user_id=1)

    def test_delete_account_wrong_owner_raises_permission_error(self, service, account_repo):
        account_repo.find_by_id.return_value = Account(
            id=1, name="Nubank", account_type="Checking", user_id=1
        )
        with pytest.raises(PermissionError):
            service.delete_account(account_id=1, current_user_id=2)

    def test_delete_account_success(self, service, account_repo):
        account_repo.find_by_id.return_value = Account(
            id=1, name="Nubank", account_type="Checking", user_id=1
        )
        service.delete_account(account_id=1, current_user_id=1)
        account_repo.delete.assert_called_once_with(1)
