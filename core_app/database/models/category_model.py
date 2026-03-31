"""SQLAlchemy ORM model for persisting Category entities.

Maps Category domain models to the 'category' database table with SQLite.
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from core_app.database.base import Base

class CategoryModel(Base):
    """ORM model for Category persistence.
    
    Categories are identified by unique name (primary key) rather than ID,
    making them reference data for items and budgets.
    """
    __tablename__ = "category"

    name: Mapped[str] = mapped_column(String(30), primary_key = True)
    color: Mapped[str] = mapped_column(String(7), nullable = False)