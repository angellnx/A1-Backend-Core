"""Unit tests for TransactionTypeService (repository mocked)."""
from unittest.mock import Mock

import pytest

from core_app.domain.models.transaction_type import TransactionType
from core_app.repositories.transaction_type_repository import TransactionTypeRepository
from core_app.services.transaction_type_service import TransactionTypeService


@pytest.fixture()
def repo():
    return Mock(spec=TransactionTypeRepository)


@pytest.fixture()
def service(repo):
    return TransactionTypeService(repository=repo)


class TestCreateTransactionType:
    def test_missing_name_raises(self, service):
        with pytest.raises(ValueError, match="Name is required"):
            service.create_transaction_type(name="", is_positive=True)

    def test_duplicate_raises(self, service, repo):
        repo.find_by_name.return_value = TransactionType(name="Salary", is_positive=True)
        with pytest.raises(ValueError, match="Transaction type 'Salary' already exists"):
            service.create_transaction_type(name="Salary", is_positive=True)

    def test_success(self, service, repo):
        repo.find_by_name.return_value = None
        repo.create.side_effect = lambda t: t
        result = service.create_transaction_type(name="Salary", is_positive=True)
        assert result == TransactionType(name="Salary", is_positive=True)


class TestGetTransactionType:
    def test_not_found_raises(self, service, repo):
        repo.find_by_name.return_value = None
        with pytest.raises(ValueError, match="Transaction type 'Salary' not found"):
            service.get_transaction_type("Salary")

    def test_success(self, service, repo):
        tt = TransactionType(name="Salary", is_positive=True)
        repo.find_by_name.return_value = tt
        assert service.get_transaction_type("Salary") == tt


class TestListTransactionTypes:
    def test_delegates_to_repository(self, service, repo):
        repo.find_all.return_value = []
        assert service.list_transaction_types() == []


class TestDeleteTransactionType:
    def test_not_found_raises(self, service, repo):
        repo.find_by_name.return_value = None
        with pytest.raises(ValueError, match="Transaction type 'Salary' not found"):
            service.delete_transaction_type("Salary")

    def test_success(self, service, repo):
        repo.find_by_name.return_value = TransactionType(name="Salary", is_positive=True)
        service.delete_transaction_type("Salary")
        repo.delete.assert_called_once_with("Salary")
