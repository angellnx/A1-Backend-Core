from pydantic import BaseModel

class TransactionTypeRequest(BaseModel):
    name: str
    is_positive: bool

class TransactionTypeResponse(BaseModel):
    name: str
    is_positive: bool