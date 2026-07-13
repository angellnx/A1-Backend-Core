"""Unit tests for TransactionService.list_transactions_by_user.

Complements the existing tests/test_transaction_service.py (which already
covers TestCreateTransaction, TestGetTransaction, TestDeleteTransaction)
by covering the filtering/pagination path that wasn't in that file.
"""
from datetime import datetime
from unittest.mock import Mock

import pytest

from core_app.repositories.currency_repository import CurrencyRepository
from core_app.repositories.item_repository import ItemRepository
from core_app.repositories.transaction_repository import TransactionRepository
from core_app.repositories.transaction_type_repository import TransactionTypeRepository
from core_app.services.transaction_service import TransactionService


@pytest.fixture()
def transaction_repo():
    return Mock(spec=TransactionRepository)


@pytest.fixture()
def service(transaction_repo):
    return TransactionService(
        repository=transaction_repo,
        transaction_type_repository=Mock(spec=TransactionTypeRepository),
        item_repository=Mock(spec=ItemRepository),
        currency_repository=Mock(spec=CurrencyRepository),
    )


class TestListTransactionsByUser:
    def test_passes_all_filters_and_pagination_through(self, service, transaction_repo):
        transaction_repo.find_by_user.return_value = []
        date_from = datetime(2026, 1, 1)
        date_to = datetime(2026, 1, 31)

        service.list_transactions_by_user(
            user_id=1,
            transaction_type_name="Expense",
            currency_code="BRL",
            date_from=date_from,
            date_to=date_to,
            skip=10,
            limit=5,
        )

        transaction_repo.find_by_user.assert_called_once_with(
            user_id=1,
            transaction_type_name="Expense",
            currency_code="BRL",
            date_from=date_from,
            date_to=date_to,
            skip=10,
            limit=5,
        )

    def test_defaults_to_no_filters_and_standard_pagination(self, service, transaction_repo):
        transaction_repo.find_by_user.return_value = []
        service.list_transactions_by_user(user_id=1)
        transaction_repo.find_by_user.assert_called_once_with(
            user_id=1,
            transaction_type_name=None,
            currency_code=None,
            date_from=None,
            date_to=None,
            skip=0,
            limit=20,
        )
