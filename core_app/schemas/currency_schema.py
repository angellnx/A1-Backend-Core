"""Pydantic models defining the API contract for currency operations.

Currencies are ISO 4217 reference data used by transactions and budgets.
"""
from pydantic import BaseModel


class CurrencyCreate(BaseModel):
    """Validates currency creation request from client."""
    code: str
    name: str
    symbol: str


class CurrencyResponse(BaseModel):
    """Serializes currency data in API response to client."""
    code: str
    name: str
    symbol: str

