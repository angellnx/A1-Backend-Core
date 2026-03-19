from pydantic import BaseModel

class ItemRequest(BaseModel):
    name: str
    item_type_name: str

class ItemResponse(BaseModel):
    id: int
    name: str
    item_type_name: str