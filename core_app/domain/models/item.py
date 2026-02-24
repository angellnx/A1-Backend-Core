from pydantic import BaseModel

class Item(BaseModel):
    id_item: int
    item_name: str
    item_type: str  # FK to ItemType