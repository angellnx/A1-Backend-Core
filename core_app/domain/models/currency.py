"""Currency domain model for exchange and transaction values."""
from dataclasses import dataclass

@dataclass
class Currency:
    """Represents an ISO 4217 currency.
    
    Currencies define the unit of value for transactions and budgets.
    Code is the primary key following ISO 4217 standard (e.g., "USD", "EUR").
    
    Attributes:
        code: ISO 4217 currency code (unique, e.g., "USD").
        name: Full name of currency (e.g., "United States Dollar").
        symbol: Currency symbol for display (e.g., "$").
    """
    code: str
    name: str
    symbol: str 