"""Business logic service for managing Transaction Types.

Coordinates transaction type operations by validating inputs and
preventing duplicate type definitions.
"""
from core_app.domain.models.transaction_type import TransactionType
from core_app.repositories.transaction_type_repository import TransactionTypeRepository

class TransactionTypeService:
    """Orchestrates transaction type business logic and repository coordination.
    
    Responsibilities:
    - Validate transaction type inputs (name required)
    - Prevent duplicate transaction types
    - Reference data for classifying transactions as income/expense
    """
    def __init__(self, repository: TransactionTypeRepository):
        self.repository = repository

    def create_transaction_type(self, name: str, is_positive: bool) -> TransactionType:
        if not name:
            raise ValueError("Name is required")

        existing = self.repository.find_by_name(name)
        if existing:
            raise ValueError(f"Transaction type '{name}' already exists")

        transaction_type = TransactionType(name=name, is_positive=is_positive)
        return self.repository.create(transaction_type)

    def get_transaction_type(self, name: str) -> TransactionType:
        transaction_type = self.repository.find_by_name(name)
        if not transaction_type:
            raise ValueError(f"Transaction type '{name}' not found")
        return transaction_type

    def list_transaction_types(self) -> list[TransactionType]:
        return self.repository.find_all()

    def delete_transaction_type(self, name: str) -> None:
        transaction_type = self.repository.find_by_name(name)
        if not transaction_type:
            raise ValueError(f"Transaction type '{name}' not found")
        self.repository.delete(name)
        