from core_app.domain.models.item import Item

class ItemRepository:
    def __init__(self):
        self._db: list[Item] = []
        self._next_id = 1

    def create(self, item: Item) -> Item:
        item.id = self._next_id
        self._next_id += 1
        self._db.append(item)
        return item
    
    def find_by_id(self, id: int) -> Item | None:
        for item in self._db:
            if item.id == id:
                return item
        return None
    
    def find_all(self) -> list[Item]:
        return list(self._db)
    
    def delete(self, id: int) -> None:
        self._db = [i for i in self._db if i.id != id]