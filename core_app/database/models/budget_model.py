"""SQLAlchemy ORM model for persisting Budget entities.

Maps Budget domain models to the 'budget' database table with SQLite.
Enforces a composite unique constraint on user + category + currency + month + year.
"""
from sqlalchemy import Integer, Float, Numeric, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core_app.database.base import Base
from core_app.database.models.category_model import CategoryModel
from core_app.database.models.currency_model import CurrencyModel


class BudgetModel(Base):
    """ORM model for Budget persistence.
    
    Budgets define spending limits per user, category, currency, and month/year.
    The composite unique constraint prevents duplicate budgets for the same
    user + category + currency + month + year combination. Both category and
    currency relationships are eagerly loaded (lazy="joined") for performance.
    """
    __tablename__ = "budget"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
    category_name: Mapped[str] = mapped_column(String(30), ForeignKey("category.name"), nullable=False)
    currency_code: Mapped[str] = mapped_column(String(3), ForeignKey("currency.code"), nullable=False)

    category: Mapped[CategoryModel] = relationship("CategoryModel", lazy="joined")
    currency: Mapped[CurrencyModel] = relationship("CurrencyModel", lazy="joined")

    __table_args__ = (
            UniqueConstraint("user_id", "category_name", "currency_code", "month", "year",
                            name="uq_budget_user_category_currency_month_year"),
        )