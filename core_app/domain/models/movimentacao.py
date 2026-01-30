from pydantic import BaseModel
from datetime import date

class MovimentacaoItem(BaseModel):
    id_movimentacao: int
    ds_data: date
    ds_valor: float
    ds_anotacao: str | None = None
    usuario_id: int  # FK para Usuario
    item_id: int  # FK para nm_tipo_item
    tipo_movi_id: int  # FK para TipoMovi
