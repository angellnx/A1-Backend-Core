from pydantic import BaseModel, Field
from datetime import datetime

class TransactionRequest(BaseModel):
    user_id: int
    item_id: int
    transaction_type_name: str
    value: float = Field(gt=0, description="Value must be greater than zero")
    date: datetime | None = None
    notes: str | None = None

class TransactionResponse(BaseModel):
    id: int
    date: datetime
    value: float
    transaction_type_name: str
    user_id: int
    item_id: int
    notes: str | None = None