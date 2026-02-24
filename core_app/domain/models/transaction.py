from pydantic import BaseModel
from datetime import date

class Transaction(BaseModel):
    id: int
    date: date
    value: float
    notes: str | None = None
    user_id: int  # FK to User
    item_id: int  # FK to ItemType
    transaction_type_id: int  # FK to TransactionType
