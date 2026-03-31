"""Item domain model for organizing transactions by line item."""
from dataclasses import dataclass
from .category import Category

@dataclass
class Item:
    """Represents a line item that can be used in transactions.
    
    Items (e.g., "Apple", "Bus Ticket") belong to categories and help
    organize transactions at a finer granularity than categories alone.
    
    Attributes:
        id: Unique item identifier.
        name: Item name.
        category: Reference to the Category this item belongs to.
    """
    id: int
    name: str
    category: Category