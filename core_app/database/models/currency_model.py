"""SQLAlchemy ORM model for persisting Currency entities.

Maps Currency domain models to the 'currency' database table with SQLite.
"""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core_app.database.base import Base

class CurrencyModel(Base):
    """ORM model for Currency persistence.
    
    Currencies are identified by ISO 4217 code (primary key) rather than ID,
    making them reference data for transactions and budgets.
    """
    __tablename__ = "currency"

    code: Mapped[str] = mapped_column(String(3), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    symbol: Mapped[str] = mapped_column(String(5), nullable=False)