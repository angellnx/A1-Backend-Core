from core_app.domain.models.user import User

class UserRepository:
    def __init__(self):
        self._db: list[User] = []
        self._next_id: int = 1

    def create(self, user: User) -> User:
        user.id = self._next_id
        self._next_id += 1
        self._db.append(user)
        return user

    def find_by_id(self, user_id: int) -> User | None:
        for user in self._db:
            if user.id == user_id:
                return user
        return None

    def find_all(self) -> list[User]:
        return list(self._db)

    def delete(self, user_id: int) -> None:
        self._db = [u for u in self._db if u.id != user_id]