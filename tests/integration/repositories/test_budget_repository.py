"""Integration tests for BudgetRepository against a real (in-memory) SQLite DB."""
import pytest
from sqlalchemy.exc import IntegrityError

from core_app.domain.models.budget import Budget
from core_app.domain.models.category import Category
from core_app.domain.models.currency import Currency
from core_app.domain.models.user import User
from core_app.repositories.budget_repository import BudgetRepository
from core_app.repositories.category_repository import CategoryRepository
from core_app.repositories.currency_repository import CurrencyRepository
from core_app.repositories.user_repository import UserRepository


@pytest.fixture()
def user(db_session):
    u = User(id=0, email="a@a.com", name="Alice", username="alice")
    u.set_password("secret123")
    return UserRepository(db_session).create(u)


@pytest.fixture()
def category(db_session):
    return CategoryRepository(db_session).create(Category(name="Food", color="#FF5733"))


@pytest.fixture()
def currency(db_session):
    return CurrencyRepository(db_session).create(Currency(code="BRL", name="Real", symbol="R$"))


def make_budget(user, category, month=1, year=2026):
    return Budget(
        id=0, amount=500, month=month, year=year,
        user_id=user.id, category=category, currency_code=category and "BRL",
    )


class TestCreate:
    def test_assigns_id_and_persists(self, db_session, user, category, currency):
        repo = BudgetRepository(db_session)
        created = repo.create(make_budget(user, category))
        assert created.id != 0

        found = repo.find_by_id(created.id)
        assert found.amount == 500
        assert found.category.name == "Food"
        assert found.currency_code == "BRL"

    def test_duplicate_composite_key_raises_integrity_error(self, db_session, user, category, currency):
        repo = BudgetRepository(db_session)
        repo.create(make_budget(user, category, month=1, year=2026))

        with pytest.raises(IntegrityError):
            repo.create(make_budget(user, category, month=1, year=2026))


class TestFind:
    def test_find_by_id_missing_returns_none(self, db_session):
        repo = BudgetRepository(db_session)
        assert repo.find_by_id(999) is None

    def test_find_all_by_user_respects_pagination(self, db_session, user, category, currency):
        repo = BudgetRepository(db_session)
        for month in range(1, 6):
            repo.create(make_budget(user, category, month=month))

        page = repo.find_all_by_user(user.id, skip=2, limit=2)
        assert len(page) == 2

    def test_find_by_user_category_currency_month_year(self, db_session, user, category, currency):
        repo = BudgetRepository(db_session)
        repo.create(make_budget(user, category, month=3, year=2026))

        found = repo.find_by_user_category_currency_month_year(
            user.id, "Food", "BRL", 3, 2026
        )
        assert found is not None

        missing = repo.find_by_user_category_currency_month_year(
            user.id, "Food", "BRL", 4, 2026
        )
        assert missing is None


class TestDelete:
    def test_delete_removes_budget(self, db_session, user, category, currency):
        repo = BudgetRepository(db_session)
        created = repo.create(make_budget(user, category))
        repo.delete(created.id)
        assert repo.find_by_id(created.id) is None

    def test_delete_missing_budget_raises_value_error(self, db_session):
        repo = BudgetRepository(db_session)
        with pytest.raises(ValueError, match="Budget with id 999 not found"):
            repo.delete(999)
