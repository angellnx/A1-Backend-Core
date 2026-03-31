"""Repository layer for persisting TransactionType domain models.

Converts between Domain Models (TransactionType) and Database Models (TransactionTypeModel).
"""
from sqlalchemy.orm import Session
from core_app.domain.models.transaction_type import TransactionType
from core_app.database.models.transaction_type_model import TransactionTypeModel

class TransactionTypeRepository:
    """Coordinates TransactionType domain model persistence."""
    def __init__(self, session: Session):
        self._session = session

    def create(self, transaction_type: TransactionType) -> TransactionType:
        db = TransactionTypeModel(
            name=transaction_type.name,
            is_positive=transaction_type.is_positive
        )
        self._session.add(db)
        self._session.commit()
        self._session.refresh(db)
        return transaction_type

    def find_by_name(self, name: str) -> TransactionType | None:
        db = self._session.query(TransactionTypeModel).filter_by(name=name).first()
        if not db:
            return None
        return TransactionType(name=db.name, is_positive=db.is_positive)

    def find_all(self) -> list[TransactionType]:
        return [
            TransactionType(name=db.name, is_positive=db.is_positive)
            for db in self._session.query(TransactionTypeModel).all()
        ]

    def delete(self, name: str) -> None:
        db = self._session.query(TransactionTypeModel).filter_by(name=name).first()
        if db:
            self._session.delete(db)
            self._session.commit()