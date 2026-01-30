from pydantic import BaseModel

class TipoItem(BaseModel):
    id_item: int
    nm_item: str
    tipo_item: str # FK para TipoItem