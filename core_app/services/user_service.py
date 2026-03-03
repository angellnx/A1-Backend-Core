from core_app.domain.models.user import User
from typing import Any

class UserService:
    def __init__(self, repository: Any):
        self.repository = repository

    def create_user(self, email: str, username: str, name: str, password: str, phone: str | None = None) -> User:
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        if not name:
            raise ValueError("User name is required")
        if not password:
            raise ValueError("Password is required")
        # phone is optional on the User model; earlier code raised an error if
        # it was missing, which created an inconsistency.  Leave it alone so
        # callers may omit it.

        user = User(
            id=0,
            email=email,
            username=username,
            name=name,
            password=password,
            phone=phone
        )

        return self.repository.create(user)

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.repository.find_by_id(user_id)

    def list_users(self) -> list[User]:
        return self.repository.find_all()

    def delete_user(self, user_id: int) -> None:
        user = self.repository.find_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        self.repository.delete(user)
