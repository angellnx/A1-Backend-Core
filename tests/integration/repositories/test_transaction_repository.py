"""Integration tests for TransactionRepository against a real (in-memory) SQLite DB."""
from datetime import datetime, timedelta

import pytest

from core_app.domain.models.account import Account
from core_app.domain.models.category import Category
from core_app.domain.models.currency import Currency
from core_app.domain.models.item import Item
from core_app.domain.models.transaction import Transaction
from core_app.domain.models.transaction_type import TransactionType
from core_app.domain.models.user import User
from core_app.repositories.account_repository import AccountRepository
from core_app.repositories.category_repository import CategoryRepository
from core_app.repositories.currency_repository import CurrencyRepository
from core_app.repositories.item_repository import ItemRepository
from core_app.repositories.transaction_repository import TransactionRepository
from core_app.repositories.transaction_type_repository import TransactionTypeRepository
from core_app.repositories.user_repository import UserRepository


@pytest.fixture()
def user(db_session):
    u = User(id=0, email="a@a.com", name="Alice", username="alice")
    u.set_password("secret123")
    return UserRepository(db_session).create(u)


@pytest.fixture()
def account(db_session, user):
    return AccountRepository(db_session).create(
        Account(id=0, name="Nubank", account_type="Checking", user_id=user.id)
    )


@pytest.fixture()
def category(db_session):
    return CategoryRepository(db_session).create(Category(name="Food", color="#FF5733"))


@pytest.fixture()
def item(db_session, category):
    return ItemRepository(db_session).create(Item(id=0, name="Apple", category=category))


@pytest.fixture()
def brl(db_session):
    return CurrencyRepository(db_session).create(Currency(code="BRL", name="Real", symbol="R$"))


@pytest.fixture()
def usd(db_session):
    return CurrencyRepository(db_session).create(Currency(code="USD", name="US Dollar", symbol="$"))


@pytest.fixture()
def expense_type(db_session):
    return TransactionTypeRepository(db_session).create(
        TransactionType(name="Expense", is_positive=False)
    )


@pytest.fixture()
def income_type(db_session):
    return TransactionTypeRepository(db_session).create(
        TransactionType(name="Salary", is_positive=True)
    )


def make_transaction(user, item, account, ttype, currency_code, value, date):
    return Transaction(
        id=0, date=date, value=value, transaction_type=ttype,
        user_id=user.id, item_id=item.id, account_id=account.id,
        currency_code=currency_code,
    )


class TestCreate:
    def test_assigns_id_and_normalizes_value_sign(
        self, db_session, user, item, account, brl, expense_type
    ):
        repo = TransactionRepository(db_session)
        txn = make_transaction(user, item, account, expense_type, "BRL", 200, datetime.now())
        created = repo.create(txn)

        assert created.id != 0
        assert created.value == -200  # expense stored negative by the domain model

        found = repo.find_by_id(created.id)
        assert found.value == -200
        assert found.transaction_type.name == "Expense"
        assert found.currency_code == "BRL"


class TestFindByUser:
    def test_scopes_results_to_user(self, db_session, user, item, account, brl, expense_type):
        repo = TransactionRepository(db_session)
        other_user_repo = UserRepository(db_session)
        other_user_repo.create(User(id=0, email="b@b.com", name="Bob", username="bob"))

        repo.create(make_transaction(user, item, account, expense_type, "BRL", 100, datetime.now()))

        results = repo.find_by_user(user_id=user.id)
        assert len(results) == 1

    def test_filters_by_transaction_type(
        self, db_session, user, item, account, brl, expense_type, income_type
    ):
        repo = TransactionRepository(db_session)
        repo.create(make_transaction(user, item, account, expense_type, "BRL", 50, datetime.now()))
        repo.create(make_transaction(user, item, account, income_type, "BRL", 1000, datetime.now()))

        results = repo.find_by_user(user_id=user.id, transaction_type_name="Salary")

        assert len(results) == 1
        assert results[0].transaction_type.name == "Salary"

    def test_filters_by_currency(self, db_session, user, item, account, brl, usd, expense_type):
        repo = TransactionRepository(db_session)
        repo.create(make_transaction(user, item, account, expense_type, "BRL", 50, datetime.now()))
        repo.create(make_transaction(user, item, account, expense_type, "USD", 50, datetime.now()))

        results = repo.find_by_user(user_id=user.id, currency_code="USD")

        assert len(results) == 1
        assert results[0].currency_code == "USD"

    def test_filters_by_date_range(self, db_session, user, item, account, brl, expense_type):
        repo = TransactionRepository(db_session)
        old_date = datetime.now() - timedelta(days=30)
        recent_date = datetime.now()
        repo.create(make_transaction(user, item, account, expense_type, "BRL", 10, old_date))
        repo.create(make_transaction(user, item, account, expense_type, "BRL", 20, recent_date))

        results = repo.find_by_user(
            user_id=user.id,
            date_from=recent_date - timedelta(days=1),
            date_to=recent_date + timedelta(days=1),
        )

        assert len(results) == 1
        assert results[0].value == -20

    def test_orders_by_most_recent_first(self, db_session, user, item, account, brl, expense_type):
        repo = TransactionRepository(db_session)
        earlier = datetime.now() - timedelta(days=1)
        later = datetime.now()
        repo.create(make_transaction(user, item, account, expense_type, "BRL", 10, earlier))
        repo.create(make_transaction(user, item, account, expense_type, "BRL", 20, later))

        results = repo.find_by_user(user_id=user.id)

        assert results[0].value == -20  # most recent first
        assert results[1].value == -10

    def test_respects_pagination(self, db_session, user, item, account, brl, expense_type):
        repo = TransactionRepository(db_session)
        for i in range(5):
            repo.create(make_transaction(user, item, account, expense_type, "BRL", i + 1, datetime.now()))

        page = repo.find_by_user(user_id=user.id, skip=2, limit=2)
        assert len(page) == 2


class TestDelete:
    def test_delete_removes_transaction(self, db_session, user, item, account, brl, expense_type):
        repo = TransactionRepository(db_session)
        created = repo.create(
            make_transaction(user, item, account, expense_type, "BRL", 10, datetime.now())
        )
        repo.delete(created.id)
        assert repo.find_by_id(created.id) is None

    def test_delete_missing_transaction_raises_value_error(self, db_session):
        repo = TransactionRepository(db_session)
        with pytest.raises(ValueError, match="Transaction not found"):
            repo.delete(999)
