"""Pydantic models defining the API contract for transaction type operations.

Transaction types classify transactions as income (positive) or expense
(negative), determining the sign applied to transaction values.
"""
from pydantic import BaseModel


class TransactionTypeRequest(BaseModel):
    """Validates transaction type creation request from client."""
    name: str
    is_positive: bool


class TransactionTypeResponse(BaseModel):
    """Serializes transaction type data in API response to client."""
    name: str
    is_positive: bool