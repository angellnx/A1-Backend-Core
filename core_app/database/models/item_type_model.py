from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from core_app.database.base import Base

class ItemTypeModel(Base):
    __tablename__ = "item_type"

    name: Mapped[str] = mapped_column(String(30), primary_key = True)
    color: Mapped[str] = mapped_column(String(7), nullable = False)