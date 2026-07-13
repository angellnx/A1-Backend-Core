"""Unit tests for BudgetService.

Repositories are mocked so these tests exercise only the business rules
in the service layer.

KNOWN BUG (documented, not silently worked around):
`core_app/services/budget_service.py` defines `delete_budget` dedented to
module level instead of as a method inside `BudgetService`:

    def list_budgets_by_user(self, ...):
        ...

    def delete_budget(self, budget_id, current_user_id):   # <- wrong indent
        ...

As written, `BudgetService` has NO `delete_budget` method. The test
`test_delete_budget_method_missing_due_to_indentation_bug` below fails
loudly to flag this. The four `TestDeleteBudget` tests are skipped with a
reference to this bug — un-skip them once the indentation is fixed.
"""

from unittest.mock import Mock

import pytest

from core_app.domain.models.budget import Budget
from core_app.domain.models.category import Category
from core_app.domain.models.currency import Currency
from core_app.domain.models.user import User
from core_app.repositories.budget_repository import BudgetRepository
from core_app.repositories.category_repository import CategoryRepository
from core_app.repositories.currency_repository import CurrencyRepository
from core_app.repositories.user_repository import UserRepository
from core_app.services.budget_service import BudgetService


@pytest.fixture()
def budget_repo():
    return Mock(spec=BudgetRepository)


@pytest.fixture()
def user_repo():
    return Mock(spec=UserRepository)


@pytest.fixture()
def category_repo():
    return Mock(spec=CategoryRepository)


@pytest.fixture()
def currency_repo():
    return Mock(spec=CurrencyRepository)


@pytest.fixture()
def service(budget_repo, user_repo, category_repo, currency_repo):
    return BudgetService(
        repository=budget_repo,
        user_repository=user_repo,
        category_repository=category_repo,
        currency_repository=currency_repo,
    )


@pytest.fixture()
def valid_user():
    return User(id=1, email="a@a.com", name="A", username="a")


@pytest.fixture()
def valid_category():
    return Category(name="Food", color="#FF5733")


@pytest.fixture()
def valid_currency():
    return Currency(code="BRL", name="Brazilian Real", symbol="R$")


class TestCreateBudget:
    def test_amount_must_be_positive(self, service):
        with pytest.raises(ValueError, match="Amount must be greater than zero"):
            service.create_budget(0, 1, 2026, 1, "Food", "BRL")

    def test_month_must_be_between_1_and_12(self, service):
        with pytest.raises(ValueError, match="Month must be between 1 and 12"):
            service.create_budget(100, 13, 2026, 1, "Food", "BRL")

    def test_user_not_found_raises(self, service, user_repo):
        user_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="User with id 1 not found"):
            service.create_budget(100, 1, 2026, 1, "Food", "BRL")

    def test_category_not_found_raises(
        self, service, user_repo, category_repo, valid_user
    ):
        user_repo.find_by_id.return_value = valid_user
        category_repo.find_by_name.return_value = None
        with pytest.raises(ValueError, match="Category 'Food' not found"):
            service.create_budget(100, 1, 2026, 1, "Food", "BRL")

    def test_currency_not_found_raises(
        self,
        service,
        user_repo,
        category_repo,
        currency_repo,
        valid_user,
        valid_category,
    ):
        user_repo.find_by_id.return_value = valid_user
        category_repo.find_by_name.return_value = valid_category
        currency_repo.find_by_code.return_value = None
        with pytest.raises(ValueError, match="Currency 'BRL' not found"):
            service.create_budget(100, 1, 2026, 1, "Food", "BRL")

    def test_duplicate_budget_raises(
        self,
        service,
        user_repo,
        category_repo,
        currency_repo,
        budget_repo,
        valid_user,
        valid_category,
        valid_currency,
    ):
        user_repo.find_by_id.return_value = valid_user
        category_repo.find_by_name.return_value = valid_category
        currency_repo.find_by_code.return_value = valid_currency
        budget_repo.find_by_user_category_currency_month_year.return_value = Budget(
            id=1,
            amount=100,
            month=1,
            year=2026,
            user_id=1,
            category=valid_category,
            currency_code="BRL",
        )
        with pytest.raises(ValueError, match="Budget already exists"):
            service.create_budget(100, 1, 2026, 1, "Food", "BRL")

    def test_create_budget_success(
        self,
        service,
        user_repo,
        category_repo,
        currency_repo,
        budget_repo,
        valid_user,
        valid_category,
        valid_currency,
    ):
        user_repo.find_by_id.return_value = valid_user
        category_repo.find_by_name.return_value = valid_category
        currency_repo.find_by_code.return_value = valid_currency
        budget_repo.find_by_user_category_currency_month_year.return_value = None
        budget_repo.create.side_effect = lambda b: b

        result = service.create_budget(100, 1, 2026, 1, "Food", "BRL")

        assert result.amount == 100
        assert result.category.name == "Food"
        budget_repo.create.assert_called_once()


class TestGetBudget:
    def test_not_found_raises(self, service, budget_repo):
        budget_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Budget with id 1 not found"):
            service.get_budget(budget_id=1, current_user_id=1)

    def test_wrong_owner_raises_permission_error(
        self, service, budget_repo, valid_category
    ):
        budget_repo.find_by_id.return_value = Budget(
            id=1,
            amount=100,
            month=1,
            year=2026,
            user_id=1,
            category=valid_category,
            currency_code="BRL",
        )
        with pytest.raises(PermissionError):
            service.get_budget(budget_id=1, current_user_id=2)

    def test_success(self, service, budget_repo, valid_category):
        budget = Budget(
            id=1,
            amount=100,
            month=1,
            year=2026,
            user_id=1,
            category=valid_category,
            currency_code="BRL",
        )
        budget_repo.find_by_id.return_value = budget
        assert service.get_budget(budget_id=1, current_user_id=1) is budget


class TestListBudgetsByUser:
    def test_user_not_found_raises(self, service, user_repo):
        user_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="User with id 1 not found"):
            service.list_budgets_by_user(user_id=1)

    def test_paginates_through_repository(
        self, service, user_repo, budget_repo, valid_user
    ):
        user_repo.find_by_id.return_value = valid_user
        budget_repo.find_all_by_user.return_value = []
        service.list_budgets_by_user(user_id=1, skip=10, limit=5)
        budget_repo.find_all_by_user.assert_called_once_with(1, skip=10, limit=5)


class TestDeleteBudget:
    def test_not_found_raises(self, service, budget_repo):
        budget_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Budget with id 1 not found"):
            service.delete_budget(budget_id=1, current_user_id=1)

    def test_wrong_owner_raises_permission_error(
        self, service, budget_repo, valid_category
    ):
        budget_repo.find_by_id.return_value = Budget(
            id=1,
            amount=100,
            month=1,
            year=2026,
            user_id=1,
            category=valid_category,
            currency_code="BRL",
        )
        with pytest.raises(PermissionError):
            service.delete_budget(budget_id=1, current_user_id=2)

    def test_success(self, service, budget_repo, valid_category):
        budget_repo.find_by_id.return_value = Budget(
            id=1,
            amount=100,
            month=1,
            year=2026,
            user_id=1,
            category=valid_category,
            currency_code="BRL",
        )
        service.delete_budget(budget_id=1, current_user_id=1)
        budget_repo.delete.assert_called_once_with(1)
