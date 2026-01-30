from enum import Enum
from pydantic import BaseModel, Field


class TipoMovimentacaoEnum(str, Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"


class TipoMovi(BaseModel):
    id_tipo_movi: int | None = None
    nome: str = Field
    cor: str = Field
    tipo: TipoMovimentacaoEnum
