from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core_app.database.base import Base

class CurrencyModel(Base):
    __tablename__ = "currency"

    code: Mapped[str] = mapped_column(String(3), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    symbol: Mapped[str] = mapped_column(String(5), nullable=False)