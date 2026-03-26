from sqlalchemy.orm import Session
from core_app.domain.models.transaction import Transaction
from core_app.domain.models.transaction_type import TransactionType
from core_app.database.models.transaction_model import TransactionModel


class TransactionRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, transaction: Transaction) -> Transaction:
        db = TransactionModel(
            date=transaction.date,
            value=transaction.value,
            notes=transaction.notes,
            user_id=transaction.user_id,
            transaction_type_name=transaction.transaction_type.name,
            item_id=transaction.item_id,
            currency_code=transaction.currency_code
        )
        self._session.add(db)
        self._session.commit()
        self._session.refresh(db)
        transaction.id = db.id
        return transaction

    def find_by_id(self, transaction_id: int) -> Transaction | None:
        db = self._session.query(TransactionModel).filter_by(id=transaction_id).first()
        if not db:
            return None

        return Transaction(
            id=db.id,
            date=db.date,
            value=float(db.value),
            transaction_type=TransactionType(
                name=db.transaction_type.name,
                is_positive=db.transaction_type.is_positive
            ),
            user_id=db.user_id,
            item_id=db.item_id,
            currency_code=db.currency.code,
            notes=db.notes
        )

    def find_all(self) -> list[Transaction]:
        return [
            Transaction(
                id=db.id,
                date=db.date,
                value=float(db.value),
                transaction_type=TransactionType(
                    name=db.transaction_type.name,
                    is_positive=db.transaction_type.is_positive
                ),
                user_id=db.user_id,
                item_id=db.item_id,
                currency_code=db.currency.code,
                notes=db.notes
            )
            for db in self._session.query(TransactionModel).all()
        ]

    def delete(self, transaction_id: int) -> None:
        db = self._session.query(TransactionModel).filter_by(id=transaction_id).first()
        if not db:
            raise ValueError("Transaction not found")

        self._session.delete(db)
        self._session.commit()