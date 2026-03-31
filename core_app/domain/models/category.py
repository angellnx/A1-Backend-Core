"""Category domain model for organizing expenses and income items."""
from dataclasses import dataclass

@dataclass
class Category:
    """Represents a spending/income category.
    
    Categories group related items and budgets (e.g., "Food", "Transportation").
    Name is the primary key as categories are referenced by their unique name.
    
    Attributes:
        name: Unique category identifier (e.g., "Groceries").
        color: Hex color code for UI display (e.g., "#FF5733").
    """
    name: str
    color: str