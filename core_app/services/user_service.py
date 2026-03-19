from core_app.domain.models.user import User
from core_app.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, email: str, name: str, username: str, password: str, phone: str | None = None) -> User:
        if not email:
            raise ValueError("Email is required")
        if not name:
            raise ValueError("Name is required")
        if not username:
            raise ValueError("Username is required")
        if not password:
            raise ValueError("Password is required")

        user = User(id=0, email=email, name=name, username=username, phone=phone)
        user.set_password(password)
        return self.repository.create(user)

    def get_user(self, user_id: int) -> User:
        user = self.repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"User '{user_id}' not found")
        return user

    def list_users(self) -> list[User]:
        return self.repository.find_all()

    def delete_user(self, user_id: int) -> None:
        user = self.repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"User '{user_id}' not found")
        self.repository.delete(user_id)