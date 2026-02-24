from pydantic import BaseModel

class ItemType(BaseModel):
    name: str
    color: str
