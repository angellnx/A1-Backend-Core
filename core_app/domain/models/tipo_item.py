from pydantic import BaseModel

class TipoItem(BaseModel):
    nm_tipo_item: str
    ds_cor_tipo: str
