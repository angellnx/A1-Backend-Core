from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core_app.database.base import Base
from core_app.database.models.item_type_model import ItemTypeModel

class ItemModel(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(150), nullable = False)
    item_type_name: Mapped[str] = mapped_column(String(30), ForeignKey("item_type.name"), nullable = False)

    item_type: Mapped[ItemTypeModel] = relationship("ItemTypeModel", lazy="joined")