from sqlalchemy import Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core_app.database.base import Base
from core_app.database.models.user_model import UserModel
from core_app.database.models.transaction_type_model import TransactionTypeModel
from core_app.database.models.item_model import ItemModel
from core_app.database.models.currency_model import CurrencyModel
from datetime import datetime

class TransactionModel(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone = True), nullable = False)
    value: Mapped[float] = mapped_column(Numeric(18, 4), nullable = False)
    notes: Mapped[str] = mapped_column(String(500), nullable = True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable = False)
    transaction_type_name: Mapped[str] = mapped_column(String(20), ForeignKey("transaction_type.name"), nullable = False)
    item_id: Mapped[int] = mapped_column(Integer, ForeignKey("item.id"), nullable = False)
    currency_code: Mapped[str] = mapped_column(String(3), ForeignKey("currency.code"), nullable=False)

    transaction_type: Mapped[TransactionTypeModel] = relationship("TransactionTypeModel", lazy="joined")
    item: Mapped[ItemModel] = relationship("ItemModel", lazy="joined")
    user: Mapped[UserModel] = relationship("UserModel", lazy="joined")  
    currency: Mapped[CurrencyModel] = relationship("CurrencyModel", lazy="joined")