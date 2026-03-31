"""SQLAlchemy ORM model for persisting User entities.

Maps User domain models to the 'user' database table with SQLite.
Enforces unique constraints on email and username columns.
"""
from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from core_app.database.base import Base

class UserModel(Base):
    """ORM model for User persistence.
    
    Stores authentication credentials and user profile information.
    Email and username must be unique across all users.
    """
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)

    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
        UniqueConstraint("username", name="uq_user_username"),
    )