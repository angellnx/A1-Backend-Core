"""SQLAlchemy ORM model for persisting TransactionType entities.

Maps TransactionType domain models to the 'transaction_type' database table.
"""
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from core_app.database.base import Base

class TransactionTypeModel(Base):
    """ORM model for TransactionType persistence.
    
    Transaction types classify transactions as income (positive) or expense (negative).
    Type name is the primary key as types are reference data.
    """
    __tablename__ = "transaction_type"

    name: Mapped[str] = mapped_column(String(20), primary_key = True)
    is_positive: Mapped[bool] = mapped_column(Boolean(), nullable = False)