"""Business logic service for managing Budgets.

Coordinates budget operations by validating inputs, verifying related
entities (user, category, currency), and enforcing uniqueness constraints.
"""
from core_app.domain.models.budget import Budget
from core_app.repositories.budget_repository import BudgetRepository
from core_app.repositories.user_repository import UserRepository
from core_app.repositories.category_repository import CategoryRepository
from core_app.repositories.currency_repository import CurrencyRepository


class BudgetService:
    """Orchestrates budget business logic and repository coordination.
    
    Responsibilities:
    - Validate budget inputs (amount > 0, month 1-12)
    - Verify user, category, and currency exist
    - Enforce unique constraint: user + category + currency + month + year
    - Filter budgets by user for scoped access
    """
    def __init__(
        self,
        repository: BudgetRepository,
        user_repository: UserRepository,
        category_repository: CategoryRepository,
        currency_repository: CurrencyRepository
    ):
        self.repository = repository
        self.user_repository = user_repository
        self.category_repository = category_repository
        self.currency_repository = currency_repository

    def create_budget(
        self,
        amount: float,
        month: int,
        year: int,
        user_id: int,
        category_name: str,
        currency_code: str
    ) -> Budget:
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        if month < 1 or month > 12:
            raise ValueError("Month must be between 1 and 12")

        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        category = self.category_repository.find_by_name(category_name)
        if not category:
            raise ValueError(f"Category '{category_name}' not found")

        currency = self.currency_repository.find_by_code(currency_code)
        if not currency:
            raise ValueError(f"Currency '{currency_code}' not found")

        existing = self.repository.find_by_user_category_currency_month_year(
            user_id, category_name, currency_code, month, year
        )
        if existing:
            raise ValueError(
                f"Budget already exists for user {user_id}, category '{category_name}', "
                f"currency '{currency_code}', month {month}, year {year}"
            )

        budget = Budget(
            id=0,
            amount=amount,
            month=month,
            year=year,
            user_id=user_id,
            category=category,
            currency_code=currency_code
        )
        return self.repository.create(budget)

    def get_budget(self, budget_id: int) -> Budget:
        budget = self.repository.find_by_id(budget_id)
        if not budget:
            raise ValueError(f"Budget with id {budget_id} not found")
        return budget

    def list_budgets_by_user(self, user_id: int) -> list[Budget]:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return self.repository.find_all_by_user(user_id)

    def delete_budget(self, budget_id: int) -> None:
        budget = self.repository.find_by_id(budget_id)
        if not budget:
            raise ValueError(f"Budget with id {budget_id} not found")
        self.repository.delete(budget_id)
