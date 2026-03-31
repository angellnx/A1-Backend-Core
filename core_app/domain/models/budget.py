"""Budget domain model for spending limits and planning."""
from dataclasses import dataclass
from .category import Category


@dataclass
class Budget:
    """Represents a user-defined spending limit for a category and currency.
    
    Budgets enforce spending limits per category per currency per month/year.
    A budget is uniquely identified by the combination of user + category +
    currency + month + year (no duplicate budgets allowed).
    
    Attributes:
        id: Unique budget identifier.
        amount: Spending limit as a decimal value.
        month: Calendar month (1-12).
        year: Calendar year.
        user_id: Reference to the owning User.
        category: Reference to the Category this budget applies to.
        currency_code: ISO 4217 currency code (no cross-currency conversion).
    """
    id: int
    amount: float
    month: int
    year: int
    user_id: int
    category: Category
    currency_code: str