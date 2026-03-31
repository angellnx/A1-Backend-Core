"""Repository layer for persisting Account domain models.

Converts between Domain Models (Account) and Database Models (AccountModel).
"""
from sqlalchemy.orm import Session
from core_app.database.models.account_model import AccountModel
from core_app.domain.models.account import Account


class AccountRepository:
    """Coordinates Account domain model persistence."""
    def __init__(self, session: Session):
        self._session = session

    def create(self, account: Account) -> Account:
        db = AccountModel(
            name=account.name,
            account_type=account.account_type,
            user_id=account.user_id
        )
        self._session.add(db)
        self._session.commit()
        self._session.refresh(db)
        account.id = db.id
        return account

    def find_by_id(self, account_id: int) -> Account | None:
        db = self._session.query(AccountModel).filter_by(id=account_id).first()
        if not db:
            return None
        return Account(
            id=db.id,
            name=db.name,
            account_type=db.account_type,
            user_id=db.user_id
        )

    def find_all_by_user(self, user_id: int) -> list[Account]:
        return [
            Account(
                id=db.id,
                name=db.name,
                account_type=db.account_type,
                user_id=db.user_id
            )
            for db in self._session.query(AccountModel).filter_by(user_id=user_id).all()
        ]

    def delete(self, account_id: int) -> None:
        db = self._session.query(AccountModel).filter_by(id=account_id).first()
        if not db:
            raise ValueError(f"Account with id {account_id} not found")
        self._session.delete(db)
        self._session.commit()
