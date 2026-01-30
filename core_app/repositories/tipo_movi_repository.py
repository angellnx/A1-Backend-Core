from typing import List, Optional
from core_app.domain.models.tipo_movi import TipoMovi

tipo_movi_db: List[TipoMovi] = []

def add_tipo_movi(tipo_movi: TipoMovi) -> TipoMovi:
    tipo_movi_db.append(tipo_movi)
    return tipo_movi

def get_tipo_movis() -> List[TipoMovi]:
    return tipo_movi_db

def get_tipo_movi_by_nome(nome: str) -> Optional[TipoMovi]:
    for tm in tipo_movi_db:
        if tm.ds_tipo_movi == nome:
            return tm
    return None

def update_tipo_movi(nome: str, updated_tipo_movi: TipoMovi) -> Optional[TipoMovi]:
    for index, tm in enumerate(tipo_movi_db):
        if tm.ds_tipo_movi == nome:
            tipo_movi_db[index] = updated_tipo_movi
            return updated_tipo_movi
    return None

def delete_tipo_movi(nome: str) -> bool:
    for index, tm in enumerate(tipo_movi_db):
        if tm.ds_tipo_movi == nome:
            tipo_movi_db.pop(index)
            return True
    return False
