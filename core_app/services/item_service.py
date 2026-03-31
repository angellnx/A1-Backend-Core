"""Business logic service for managing Items.

Coordinates item operations by validating inputs and verifying category
existence before item creation.
"""
from core_app.domain.models.item import Item
from core_app.repositories.category_repository import CategoryRepository
from core_app.repositories.item_repository import ItemRepository

class ItemService:
    """Orchestrates item business logic and repository coordination.
    
    Responsibilities:
    - Validate item inputs (name required)
    - Verify category exists before creating item
    - Items provide line-item granularity for transactions
    """
    def __init__(self, repository: ItemRepository, category_repository: CategoryRepository):
        self.repository = repository
        self.category_repository = category_repository

    def create_item(self, name: str, category_name: str) -> Item:
        if not name:
            raise ValueError("Name is required")

        category = self.category_repository.find_by_name(category_name)
        if not category:
            raise ValueError(f"Category '{category_name}' not found")

        item = Item(id=0, name=name, category=category)
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
        
        