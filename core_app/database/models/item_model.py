"""SQLAlchemy ORM model for persisting Item entities.

Maps Item domain models to the 'item' database table with SQLite.
"""
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core_app.database.base import Base
from core_app.database.models.category_model import CategoryModel

class ItemModel(Base):
    """ORM model for Item persistence.
    
    Items belong to a Category and are used as line items in Transactions.
    The category relationship is eagerly loaded (lazy="joined") for performance.
    """
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(150), nullable = False)
    category_name: Mapped[str] = mapped_column(String(30), ForeignKey("category.name"), nullable = False)

    category: Mapped[CategoryModel] = relationship("CategoryModel", lazy="joined")