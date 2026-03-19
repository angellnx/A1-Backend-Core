from dataclasses import dataclass
from .item_type import ItemType

@dataclass
class Item:
    id: int
    name: str
    item_type: ItemType