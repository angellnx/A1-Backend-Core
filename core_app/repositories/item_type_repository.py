from typing import List, Optional
from core_app.domain.models.type_item import ItemType

item_types_db: List[ItemType] = []

def add_item_type(item_type: ItemType) -> ItemType:
    item_types_db.append(item_type)
    return item_type

def get_item_types() -> List[ItemType]:
    return item_types_db


def get_item_type_by_name(name: str) -> Optional[ItemType]:
    for it in item_types_db:
        if it.name == name:
            return it
    return None

def update_item_type(name: str, updated_item_type: ItemType) -> Optional[ItemType]:
    for index, it in enumerate(item_types_db):
        if it.name == name:
            item_types_db[index] = updated_item_type
            return updated_item_type
    return None

def delete_item_type(name: str) -> bool:
    for index, it in enumerate(item_types_db):
        if it.name == name:
            del item_types_db[index]
            return True
    return False

# compatibility names for service layer
create = add_item_type
find_by_id = get_item_type_by_name
find_all = get_item_types
delete = delete_item_type
