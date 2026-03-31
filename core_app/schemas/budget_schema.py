"""Pydantic models defining the API contract for budget operations.

Request and response schemas handle the composite budget concept:
budgets are scoped to user + category + currency + month + year.
"""
from pydantic import BaseModel


class BudgetRequest(BaseModel):
    """Validates budget creation request from client."""
    amount: float
    month: int
    year: int
    user_id: int
    category_name: str
    currency_code: str


class BudgetResponse(BaseModel):
    """Serializes budget data in API response to client."""
    id: int
    amount: float
    month: int
    year: int
    user_id: int
    category_name: str
    currency_code: str
