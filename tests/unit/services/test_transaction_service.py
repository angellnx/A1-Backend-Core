"""Unit tests for TransactionService.

Repositories are mocked so these tests exercise only the business rules
in the service layer (validation, related-entity checks), not persistence.
"""

from datetime import datetime
from unittest.mock import Mock

import pytest

from core_app.domain.models.currency import Currency
from core_app.domain.models.item import Item
from core_app.domain.models.category import Category
from core_app.domain.models.transaction_type import TransactionType
from core_app.repositories.currency_repository import CurrencyRepository
from core_app.repositories.item_repository import ItemRepository
from core_app.repositories.transaction_repository import TransactionRepository
from core_app.repositories.transaction_type_repository import TransactionTypeRepository
from core_app.services.transaction_service import TransactionService


@pytest.fixture()
def transaction_repo():
    return Mock(spec=TransactionRepository)


@pytest.fixture()
def transaction_type_repo():
    return Mock(spec=TransactionTypeRepository)


@pytest.fixture()
def item_repo():
    return Mock(spec=ItemRepository)


@pytest.fixture()
def currency_repo():
    return Mock(spec=CurrencyRepository)


@pytest.fixture()
def service(transaction_repo, transaction_type_repo, item_repo, currency_repo):
    return TransactionService(
        repository=transaction_repo,
        transaction_type_repository=transaction_type_repo,
        item_repository=item_repo,
        currency_repository=currency_repo,
    )


@pytest.fixture()
def valid_type():
    return TransactionType(name="Expense", is_positive=False)


@pytest.fixture()
def valid_item():
    return Item(id=1, name="Apple", category=Category(name="Food", color="#FF5733"))


@pytest.fixture()
def valid_currency():
    return Currency(code="BRL", name="Real", symbol="R$")


class TestCreateTransaction:
    def test_create_transaction_success(
        self,
        service,
        transaction_repo,
        transaction_type_repo,
        item_repo,
        currency_repo,
        valid_type,
        valid_item,
        valid_currency,
    ):
        transaction_type_repo.find_by_name.return_value = valid_type
        item_repo.find_by_id.return_value = valid_item
        currency_repo.find_by_code.return_value = valid_currency
        transaction_repo.create.side_effect = lambda t: t

        result = service.create_transaction(
            user_id=1,
            item_id=1,
            account_id=1,
            transaction_type_name="Expense",
            currency_code="BRL",
            value=200,
        )

        assert result.value == -200  # normalized by the domain model
        assert result.currency_code == "BRL"
        transaction_repo.create.assert_called_once()

    def test_create_transaction_invalid_value(self, service):
        with pytest.raises(ValueError, match="Value must be greater than zero"):
            service.create_transaction(
                user_id=1,
                item_id=1,
                account_id=1,
                transaction_type_name="Expense",
                currency_code="BRL",
                value=0,
            )

    def test_create_transaction_negative_value(self, service):
        with pytest.raises(ValueError, match="Value must be greater than zero"):
            service.create_transaction(
                user_id=1,
                item_id=1,
                account_id=1,
                transaction_type_name="Expense",
                currency_code="BRL",
                value=-50,
            )

    def test_create_transaction_type_not_found(self, service, transaction_type_repo):
        transaction_type_repo.find_by_name.return_value = None
        with pytest.raises(ValueError, match="Transaction type 'Expense' not found"):
            service.create_transaction(
                user_id=1,
                item_id=1,
                account_id=1,
                transaction_type_name="Expense",
                currency_code="BRL",
                value=200,
            )

    def test_create_transaction_item_not_found(
        self, service, transaction_type_repo, item_repo, valid_type
    ):
        transaction_type_repo.find_by_name.return_value = valid_type
        item_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Item '1' not found"):
            service.create_transaction(
                user_id=1,
                item_id=1,
                account_id=1,
                transaction_type_name="Expense",
                currency_code="BRL",
                value=200,
            )

    def test_create_transaction_currency_not_found(
        self,
        service,
        transaction_type_repo,
        item_repo,
        currency_repo,
        valid_type,
        valid_item,
    ):
        transaction_type_repo.find_by_name.return_value = valid_type
        item_repo.find_by_id.return_value = valid_item
        currency_repo.find_by_code.return_value = None
        with pytest.raises(ValueError, match="Currency 'BRL' not found"):
            service.create_transaction(
                user_id=1,
                item_id=1,
                account_id=1,
                transaction_type_name="Expense",
                currency_code="BRL",
                value=200,
            )

    def test_create_transaction_defaults_date_to_now_when_not_provided(
        self,
        service,
        transaction_repo,
        transaction_type_repo,
        item_repo,
        currency_repo,
        valid_type,
        valid_item,
        valid_currency,
    ):
        transaction_type_repo.find_by_name.return_value = valid_type
        item_repo.find_by_id.return_value = valid_item
        currency_repo.find_by_code.return_value = valid_currency
        transaction_repo.create.side_effect = lambda t: t

        before = datetime.now()
        result = service.create_transaction(
            user_id=1,
            item_id=1,
            account_id=1,
            transaction_type_name="Expense",
            currency_code="BRL",
            value=200,
        )
        after = datetime.now()

        assert before <= result.date <= after


class TestGetTransaction:
    def test_get_transaction_success(self, service, transaction_repo, valid_type):
        from core_app.domain.models.transaction import Transaction

        txn = Transaction(
            id=1,
            date=datetime.now(),
            value=200,
            transaction_type=valid_type,
            user_id=1,
            item_id=1,
            account_id=1,
            currency_code="BRL",
        )
        transaction_repo.find_by_id.return_value = txn

        assert service.get_transaction(1) is txn

    def test_get_transaction_not_found(self, service, transaction_repo):
        transaction_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Transaction '1' not found"):
            service.get_transaction(1)


class TestDeleteTransaction:
    def test_delete_transaction_success(self, service, transaction_repo, valid_type):
        from core_app.domain.models.transaction import Transaction

        txn = Transaction(
            id=1,
            date=datetime.now(),
            value=200,
            transaction_type=valid_type,
            user_id=1,
            item_id=1,
            account_id=1,
            currency_code="BRL",
        )
        transaction_repo.find_by_id.return_value = txn

        service.delete_transaction(1)

        transaction_repo.delete.assert_called_once_with(1)

    def test_delete_transaction_not_found(self, service, transaction_repo):
        transaction_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Transaction '1' not found"):
            service.delete_transaction(1)
