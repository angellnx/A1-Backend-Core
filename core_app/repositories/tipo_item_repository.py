from typing import List, Optional
from core_app.models.tipo_item import TipoItem

tipo_items_db: List[TipoItem] = []

def add_tipo_item(tipo_item: TipoItem) -> TipoItem:
    tipo_items_db.append(tipo_item)
    return tipo_item

def get_tipo_items() -> List[TipoItem]:
    return tipo_items_db

def get_tipo_item_by_nome(nome: str) -> Optional[TipoItem]:
    for tipo_item in tipo_items_db:
        if tipo_item.nome == nome:
            return tipo_item
    return None

def update_tipo_item(nome: str, updated_tipo_item: TipoItem) -> Optional[TipoItem]:
    for index, tipo_item in enumerate(tipo_items_db):
        if tipo_item.nome == nome:
            tipo_items_db[index] = updated_tipo_item
            return updated_tipo_item
    return None

def delete_tipo_item(nome: str) -> bool:
    for index, tipo_item in enumerate(tipo_items_db):
        if tipo_item.nome == nome:
            del tipo_items_db[index]
            return True
    return False