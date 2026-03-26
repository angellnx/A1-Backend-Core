from sqlalchemy.orm import Session
from core_app.database.models.user_model import UserModel
from core_app.domain.models.user import User

class UserRepository:
    def __init__(self, session: Session):
        self._db: Session = session

    def create(self, user: User) -> User:
        db = UserModel(
            email=user.email,
            password=user._password_hash,
            name=user.name,
            username=user.username
        )
        self._db.add(db)
        self._db.commit()
        self._db.refresh(db)
        user.id = db.id
        return user

    def find_by_id(self, user_id: int) -> User | None:
        db = self._session.query(UserModel).filter_by(id=user_id).first()
        if not db:
            return None
        user = User(
            id=db.id,
            email=db.email,
            password=db._password_hash,
            name=db.name,
            username=db.username
        )
        return user

    def find_all(self) -> list[User]:
        users = []
        for db in self._session.query(UserModel).all():
            user =User(
                id=db.id,
                email=db.email,
                password=db.password,
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