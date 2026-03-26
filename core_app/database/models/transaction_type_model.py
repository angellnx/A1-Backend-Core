from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from core_app.database.base import Base

class TransactionTypeModel(Base):
    __tablename__ = "transaction_type"

    name: Mapped[str] = mapped_column(String(20), primary_key = True)
    is_positive: Mapped[bool] = mapped_column(Boolean(), nullable = False)