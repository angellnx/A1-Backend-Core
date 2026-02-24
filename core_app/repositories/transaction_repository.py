from typing import List, Optional
from core_app.domain.models.transaction import Transaction

transactions_db: List[Transaction] = []

def add_transaction(tr: Transaction) -> Transaction:
    transactions_db.append(tr)
    return tr

def get_transactions() -> List[Transaction]:
    return transactions_db

def get_transaction_by_id(tr_id: int) -> Optional[Transaction]:
    for tr in transactions_db:
        if tr.id == tr_id:
            return tr
    return None

def update_transaction(tr_id: int, updated_tr: Transaction) -> Optional[Transaction]:
    for index, tr in enumerate(transactions_db):
        if tr.id == tr_id:
            transactions_db[index] = updated_tr
            return updated_tr
    return None

def delete_transaction(tr_id: int) -> bool:
    for index, tr in enumerate(transactions_db):
        if tr.id == tr_id:
            transactions_db.pop(index)
            return True
    return False
