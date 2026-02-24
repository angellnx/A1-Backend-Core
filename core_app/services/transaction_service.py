from datetime import datetime
from core_app.domain.models.transaction import Transaction
from typing import Any

class TransactionService:
    def __init__(self, repository: Any):
        self.repository = repository

    def create_transaction(
        self,
        user_id: int,
        item_id: int,
        transaction_type: str,
        value: float,
        date: datetime | None = None,
        note: str | None = None
    ) -> Transaction:

        if value <= 0:
            raise ValueError("Value must be greater than zero")

        effective_date = date if date else datetime.now()

        transaction = Transaction(
            id=0,
            date=effective_date.date() if isinstance(effective_date, datetime) else effective_date,
            value=value,
            notes=note,
            user_id=user_id,
            item_id=item_id,
            transaction_type_id=0
        )

        return self.repository.create(transaction)

    def get_transaction_by_id(self, transaction_id: int) -> Transaction | None:
        return self.repository.find_by_id(transaction_id)

    def list_transactions(self) -> list[Transaction]:
        return self.repository.find_all()

    def delete_transaction(self, transaction_id: int) -> None:
        tr = self.repository.find_by_id(transaction_id)
        if not tr:
            raise ValueError("Transaction not found")
        self.repository.delete(tr)
