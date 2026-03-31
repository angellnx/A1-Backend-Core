"""SQLAlchemy ORM model for persisting Account entities.

Maps Account domain models to the 'account' database table with SQLite.
"""
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from core_app.database.base import Base


class AccountModel(Base):
    """ORM model for Account persistence.
    
    Accounts belong to a User and can have multiple Transactions.
    Account type and name are stored as free-text strings for flexibility.
    """
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    account_type: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable=False)
