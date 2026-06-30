"""Repository layer for persisting Transaction domain models.
Converts between Domain Models (Transaction) and Database Models (TransactionModel).
"""
from datetime import datetime
from sqlalchemy.orm import Session
from core_app.domain.models.transaction import Transaction
from core_app.domain.models.transaction_type import TransactionType
from core_app.database.models.transaction_model import TransactionModel

class TransactionRepository:
    """Coordinates Transaction domain model persistence.

    Manages complex relationships: transactions connect items, accounts,
    transaction types, users, currencies, and amounts.
    """

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
            currency_code=transaction.currency_code,
            account_id=transaction.account_id
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
        return self._to_domain(db)

    def find_all(self) -> list[Transaction]:
        return [
            self._to_domain(db)
            for db in self._session.query(TransactionModel).all()
        ]

    def find_by_user(
        self,
        user_id: int,
        transaction_type_name: str | None = None,
        currency_code: str | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        skip: int = 0,
        limit: int = 20
    ) -> list[Transaction]:
        """Retrieve transactions for a user with optional filters and pagination.

        Args:
            user_id: Owner user ID.
            transaction_type_name: Optional filter by transaction type.
            currency_code: Optional filter by currency.
            date_from: Optional start date filter (inclusive).
            date_to: Optional end date filter (inclusive).
            skip: Number of records to skip for pagination.
            limit: Maximum number of records to return.

        Returns:
            Filtered and paginated list of Transaction domain objects.
        """
        query = self._session.query(TransactionModel).filter_by(user_id=user_id)

        if transaction_type_name:
            query = query.filter(TransactionModel.transaction_type_name == transaction_type_name)
        if currency_code:
            query = query.filter(TransactionModel.currency_code == currency_code)
        if date_from:
            query = query.filter(TransactionModel.date >= date_from)
        if date_to:
            query = query.filter(TransactionModel.date <= date_to)

        query = query.order_by(TransactionModel.date.desc())

        return [
            self._to_domain(db)
            for db in query.offset(skip).limit(limit).all()
        ]

    def delete(self, transaction_id: int) -> None:
        db = self._session.query(TransactionModel).filter_by(id=transaction_id).first()
        if not db:
            raise ValueError("Transaction not found")
        self._session.delete(db)
        self._session.commit()

    def _to_domain(self, db: TransactionModel) -> Transaction:
        """Convert a TransactionModel ORM object to a Transaction domain object.

        Args:
            db: SQLAlchemy ORM instance.

        Returns:
            Transaction domain object.
        """
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
            account_id=db.account.id,
            notes=db.notes
        )
