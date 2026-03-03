from pydantic import BaseModel

class Item(BaseModel):
    id: int
    name: str
    item_type: str  # FK to ItemType