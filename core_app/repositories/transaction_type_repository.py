from typing import List, Optional
from core_app.domain.models.transaction_type import TransactionType

transaction_types_db: List[TransactionType] = []

def add_transaction_type(transaction_type: TransactionType) -> TransactionType:
    transaction_types_db.append(transaction_type)
    return transaction_type

def get_transaction_types() -> List[TransactionType]:
    return transaction_types_db

def get_transaction_type_by_name(name: str) -> Optional[TransactionType]:
    for tt in transaction_types_db:
        if tt.name == name:
            return tt
    return None

def update_transaction_type(name: str, updated_transaction_type: TransactionType) -> Optional[TransactionType]:
    for index, tt in enumerate(transaction_types_db):
        if tt.name == name:
            transaction_types_db[index] = updated_transaction_type
            return updated_transaction_type
    return None

def delete_transaction_type(name: str) -> bool:
    for index, tt in enumerate(transaction_types_db):
        if tt.name == name:
            transaction_types_db.pop(index)
            return True
    return False
