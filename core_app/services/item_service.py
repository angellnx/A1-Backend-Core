from core_app.domain.models.item import Item
from core_app.repositories.item_repository import ItemRepository
from core_app.repositories.item_type_repository import ItemTypeRepository

class ItemService:
    def __init__(self, repository: ItemRepository, item_type_repository: ItemTypeRepository):
        self.repository = repository
        self.item_type_repository = item_type_repository

    def create_item(self, name: str, item_type_name: str) -> Item:
        if not name:
            raise ValueError("Name is required")

        item_type = self.item_type_repository.find_by_name(item_type_name)
        if not item_type:
            raise ValueError(f"Item type '{item_type_name}' not found")

        item = Item(id=0, name=name, item_type=item_type)
        return self.repository.create(item)

    def get_item(self, item_id: int) -> Item:
        item = self.repository.find_by_id(item_id)
        if not item:
            raise ValueError(f"Item '{item_id}' not found")
        return item

    def list_items(self) -> list[Item]:
        return self.repository.find_all()

    def delete_item(self, item_id: int) -> None:
        item = self.repository.find_by_id(item_id)
        if not item:
            raise ValueError(f"Item '{item_id}' not found")
        self.repository.delete(item_id)
        
        