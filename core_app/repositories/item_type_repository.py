from core_app.domain.models.item_type import ItemType

class ItemTypeRepository:
    def __init__(self):
        self._db: list[ItemType] = []

    def create(self, item_type: ItemType) -> ItemType:
        self._db.append(item_type)
        return item_type
    
    def find_by_name(self, name: str) -> ItemType | None:
        for item_type in self._db:
            if item_type.name == name:
                return item_type
        return None
    
    def find_all(self) -> list[ItemType]:
        return self._db.copy()
    
    def delete(self, name: str) -> None:
        self._db = [it for it in self._db if it.name != name]