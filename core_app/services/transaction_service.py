"""Business logic service for managing Transactions.

Coordinates transaction operations by validating inputs, verifying related
entities, and enforcing value normalization based on transaction type.
"""
from datetime import datetime
from core_app.domain.models.transaction import Transaction
from core_app.repositories.transaction_repository import TransactionRepository
from core_app.repositories.transaction_type_repository import TransactionTypeRepository
from core_app.repositories.item_repository import ItemRepository
from core_app.repositories.currency_repository import CurrencyRepository


class TransactionService:
    """Orchestrates transaction business logic and repository coordination.
    
    Responsibilities:
    - Validate transaction inputs (value > 0)
    - Verify transaction type, item, and currency exist
    - The domain model normalizes value sign based on transaction type
    - Default transaction date to current time if not provided
    """
    def __init__(
        self,
        repository: TransactionRepository,
        transaction_type_repository: TransactionTypeRepository,
        item_repository: ItemRepository,
        currency_repository: CurrencyRepository
    ):
        self.repository = repository
        self.transaction_type_repository = transaction_type_repository
        self.item_repository = item_repository
        self.currency_repository = currency_repository

    def create_transaction(
        self,
        user_id: int,
        item_id: int,
        account_id: int,
        transaction_type_name: str,
        currency_code: str,
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

        currency = self.currency_repository.find_by_code(currency_code)
        if not currency:
            raise ValueError(f"Currency '{currency_code}' not found")

        effective_date = date if date else datetime.now()

        transaction = Transaction(
            id=0,
            date=effective_date,
            value=value,
            transaction_type=transaction_type,
            user_id=user_id,
            item_id=item_id,
            account_id=account_id,
            currency_code=currency.code,
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