from datetime import datetime
from core_app.domain.models.transaction import Transaction
from core_app.repositories.transaction_repository import TransactionRepository
from core_app.repositories.transaction_type_repository import TransactionTypeRepository
from core_app.repositories.item_repository import ItemRepository

class TransactionService:
    def __init__(
        self,
        repository: TransactionRepository,
        transaction_type_repository: TransactionTypeRepository,
        item_repository: ItemRepository
    ):
        self.repository = repository
        self.transaction_type_repository = transaction_type_repository
        self.item_repository = item_repository

    def create_transaction(
        self,
        user_id: int,
        item_id: int,
        transaction_type_name: str,
        value: float,
        date: datetime | None = None,
        notes: str | None = None
    ) -> Transaction:
        if value <= 0:
            raise ValueError("Value must be greater than zero")

        transaction_type = self.transaction_type_repository.find_by_name(transaction_type_name)
        if not transaction_type:
            raise ValueError(f"Transaction type '{transaction_type_name}' not found")

        item = self.item_repository.find_by_id(item_id)
        if not item:
            raise ValueError(f"Item '{item_id}' not found")

        effective_date = date if date else datetime.now()

        transaction = Transaction(
            id=0,
            date=effective_date,
            value=value,
            transaction_type=transaction_type,
            user_id=user_id,
            item_id=item_id,
            notes=notes
        )

        return self.repository.create(transaction)

    def get_transaction(self, transaction_id: int) -> Transaction:
        transaction = self.repository.find_by_id(transaction_id)
        if not transaction:
            raise ValueError(f"Transaction '{transaction_id}' not found")
        return transaction

    def list_transactions(self) -> list[Transaction]:
        return self.repository.find_all()

    def delete_transaction(self, transaction_id: int) -> None:
        transaction = self.repository.find_by_id(transaction_id)
        if not transaction:
            raise ValueError(f"Transaction '{transaction_id}' not found")
        self.repository.delete(transaction_id)
        