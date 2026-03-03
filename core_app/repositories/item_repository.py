from typing import List, Optional
from core_app.domain.models.item import Item

items_db: List[Item] = []
_next_id: int = 1

def add_item(item: Item) -> Item:
    global _next_id
    # assign an auto-incremented id regardless of what was passed in
    item.id = _next_id
    _next_id += 1
    items_db.append(item)
    return item

def get_items() -> List[Item]:
    return items_db

def get_item_by_id(item_id: int) -> Optional[Item]:
    for item in items_db:
        if item.id == item_id:
            return item
    return None

def update_item(item_id: int, updated_item: Item) -> Optional[Item]:
    for index, item in enumerate(items_db):
        if item.id == item_id:
            items_db[index] = updated_item
            return updated_item
    return None

def delete_item(item_id: int) -> bool:
    for index, item in enumerate(items_db):
        if item.id == item_id:
            del items_db[index]
            return True
    return False

# compatibility aliases for service interface
create = add_item
find_by_id = get_item_by_id
find_all = get_items
delete = delete_item