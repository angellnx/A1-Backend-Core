"""Pydantic models defining the API contract for account operations.

Request schema accepts user-provided account details.
Response schema includes the calculated balance property.
"""
from pydantic import BaseModel


class AccountRequest(BaseModel):
    """Validates account creation request from client."""
    name: str
    account_type: str
    user_id: int


class AccountResponse(BaseModel):
    """Serializes account data in API response to client.
    
    Includes dynamically calculated balance from account service.
    """
    id: int
    name: str
    account_type: str
    user_id: int
    balance: float
