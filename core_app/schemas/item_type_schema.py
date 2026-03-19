from pydantic import BaseModel

class ItemTypeRequest(BaseModel):
    name: str
    color: str

class ItemTypeResponse(BaseModel):
    name: str
    color: str