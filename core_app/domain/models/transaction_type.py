from enum import Enum
from pydantic import BaseModel, Field


class TransactionTypeEnum(str, Enum):
    INCOMING = "INCOMING"
    OUTGOING = "OUTGOING"


class TransactionType(BaseModel):
    id: int | None = None
    name: str = Field
    color: str = Field
    type: TransactionTypeEnum
