from pydantic import BaseModel, Field

class CurrencyCreate(BaseModel):
    code: str
    name: str
    symbol: str

class CurrencyResponse(BaseModel):
    code: str
    name: str
    symbol: str

