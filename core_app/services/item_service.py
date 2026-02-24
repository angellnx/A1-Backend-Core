from core_app.domain.models.item import Item
from core_app.repositories.item_repository import ItemRepository

class ItemService:

    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def create_item(self, name: str, price: float) -> Item:
        if not name:
            raise ValueError("Item name is required")

        if price <= 0:
            raise ValueError("Price must be greater than zero")

        item = Item(
            id=0,
            name=name,
            item_type="",
        )

        return self.repository.create(item)

    def get_item_by_id(self, item_id: int) -> Item | None:
        return self.repository.find_by_id(item_id)

    def list_items(self) -> list[Item]:
        return self.repository.find_all()

    def delete_item(self, item_id: int) -> None:
        item = self.repository.find_by_id(item_id)

        if not item:
            raise ValueError("Item not found")

        self.repository.delete(item)
