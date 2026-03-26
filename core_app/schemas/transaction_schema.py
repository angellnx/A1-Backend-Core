from pydantic import BaseModel, Field
from datetime import datetime

class TransactionRequest(BaseModel):
    user_id: int
    item_id: int
    transaction_type_name: str
    currency_code: str
    value: float
    date: datetime | None = None
    notes: str | None = None

class TransactionResponse(BaseModel):
    id: int
    date: datetime
    value: float
    transaction_type_name: str
    currency_code: str
    user_id: int
    item_id: int
    notes: str | None = None