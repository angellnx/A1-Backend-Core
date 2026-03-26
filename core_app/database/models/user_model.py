from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from core_app.database.base import Base

class UserModel(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    email: Mapped[str] = mapped_column(String(255), nullable = False)
    password: Mapped[str] = mapped_column(String(255), nullable = False)
    name: Mapped[str] = mapped_column(String(150), nullable = False)
    username: Mapped[str] = mapped_column(String(50), nullable = False)