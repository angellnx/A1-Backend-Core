"""Repository layer for persisting Budget domain models.

Converts between Domain Models (Budget) and Database Models (BudgetModel).
"""
from sqlalchemy.orm import Session
from core_app.database.models.budget_model import BudgetModel
from core_app.domain.models.budget import Budget
from core_app.domain.models.category import Category


class BudgetRepository:
    """Coordinates Budget domain model persistence.
    
    Composite uniqueness (user + category + currency + month + year) is enforced
    at the database level; find_by_user_category_currency_month_year() is used
    to check for duplicates before creation.
    """
    def __init__(self, session: Session):
        self._session = session

    def create(self, budget: Budget) -> Budget:
        db = BudgetModel(
            amount=budget.amount,
            month=budget.month,
            year=budget.year,
            user_id=budget.user_id,
            category_name=budget.category.name,
            currency_code=budget.currency_code
        )
        self._session.add(db)
        self._session.commit()
        self._session.refresh(db)
        budget.id = db.id
        return budget

    def find_by_id(self, budget_id: int) -> Budget | None:
        db = self._session.query(BudgetModel).filter_by(id=budget_id).first()
        if not db:
            return None
        return Budget(
            id=db.id,
            amount=db.amount,
            month=db.month,
            year=db.year,
            user_id=db.user_id,
            category=Category(
                name=db.category.name,
                color=db.category.color
            ),
            currency_code=db.currency_code
        )

    def find_all_by_user(self, user_id: int) -> list[Budget]:
        return [
            Budget(
                id=db.id,
                amount=db.amount,
                month=db.month,
                year=db.year,
                user_id=db.user_id,
                category=Category(
                    name=db.category.name,
                    color=db.category.color
                ),
                currency_code=db.currency_code
            )
            for db in self._session.query(BudgetModel).filter_by(user_id=user_id).all()
        ]

    def find_by_user_category_currency_month_year(
        self,
        user_id: int,
        category_name: str,
        currency_code: str,
        month: int,
        year: int
    ) -> Budget | None:
        db = self._session.query(BudgetModel).filter_by(
            user_id=user_id,
            category_name=category_name,
            currency_code=currency_code,
            month=month,
            year=year
        ).first()
        if not db:
            return None
        return Budget(
            id=db.id,
            amount=db.amount,
            month=db.month,
            year=db.year,
            user_id=db.user_id,
            category=Category(
                name=db.category.name,
                color=db.category.color
            ),
            currency_code=db.currency_code
        )

    def delete(self, budget_id: int) -> None:
        db = self._session.query(BudgetModel).filter_by(id=budget_id).first()
        if not db:
            raise ValueError(f"Budget with id {budget_id} not found")
        self._session.delete(db)
        self._session.commit()
