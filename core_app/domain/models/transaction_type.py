"""Transaction type domain model for classifying income vs expense."""
from dataclasses import dataclass

@dataclass
class TransactionType:
    """Represents a transaction classification (income or expense).
    
    Determines the sign applied to transaction values. For example,
    "Salary" is positive (income) while "Grocery" is negative (expense).
    
    Attributes:
        name: Unique type identifier (e.g., "Salary", "Grocery").
        is_positive: True for income, False for expenses.
    """
    name: str
    is_positive: bool