"""Pydantic models defining the API contract for transaction operations.

Transactions record financial movements (income/expense) affecting account
balances. Values are normalized based on transaction type.
"""
from pydantic import BaseModel, Field
from datetime import datetime

class TransactionRequest(BaseModel):
    """Validates transaction creation request from client."""
    user_id: int
    item_id: int
    account_id: int
    transaction_type_name: str
    currency_code: str
    value: float
    date: datetime | None = None
    notes: str | None = None

class TransactionResponse(BaseModel):
    """Serializes transaction data in API response to client."""
    id: int
    date: datetime
    value: float
    transaction_type_name: str
    currency_code: str
    user_id: int
    item_id: int
    account_id: int
    notes: str | None = None