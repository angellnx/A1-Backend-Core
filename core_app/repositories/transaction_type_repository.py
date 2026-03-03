from typing import List, Optional
from core_app.domain.models.transaction_type import TransactionType

transaction_types_db: List[TransactionType] = []
_next_id: int = 1

def add_transaction_type(transaction_type: TransactionType) -> TransactionType:
    global _next_id
    # ID is optional on the model; assign one here if not provided (or
    # overwrite any placeholder).
    transaction_type.id = _next_id
    _next_id += 1
    transaction_types_db.append(transaction_type)
    return transaction_type

def get_transaction_types() -> List[TransactionType]:
    return transaction_types_db

def get_transaction_type_by_id(tt_id: int) -> Optional[TransactionType]:
    for tt in transaction_types_db:
        if tt.id == tt_id:
            return tt
    return None


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

# compatibility helpers for service layer
create = add_transaction_type
find_by_id = get_transaction_type_by_id
find_all = get_transaction_types
delete = delete_transaction_type
