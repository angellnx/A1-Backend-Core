"""Repository layer for persisting User domain models.

Converts between Domain Models (User) and Database Models (UserModel).
"""
from sqlalchemy.orm import Session
from core_app.database.models.user_model import UserModel
from core_app.domain.models.user import User

class UserRepository:
    """Coordinates User domain model persistence.
    
    Bridges domain password hashing methods with database storage of password hashes.
    """
    def __init__(self, session: Session):
        self._session: Session = session

    def create(self, user: User) -> User:
        db = UserModel(
            email=user.email,
            password=user._password_hash,
            name=user.name,
            username=user.username
        )
        self._session.add(db)
        self._session.commit()
        self._session.refresh(db)
        user.id = db.id
        return user

    def find_by_id(self, user_id: int) -> User | None:
        db = self._session.query(UserModel).filter_by(id=user_id).first()
        if not db:
            return None
        user = User(
            id=db.id,
            email=db.email,
            name=db.name,
            username=db.username
        )
        user._password_hash = db.password
        return user

    def find_all(self) -> list[User]:
        users = []
        for db in self._session.query(UserModel).all():
            user = User(
                id=db.id,
                email=db.email,
                name=db.name,
                username=db.username
            )
            user._password_hash = db.password
            users.append(user)
        return users

    def delete(self, user_id: int) -> None:
        db = self._session.query(UserModel).filter_by(id=user_id).first()
        if db:
            self._session.delete(db)
            self._session.commit()