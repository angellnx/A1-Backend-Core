from core_app.domain.models.item_type import ItemType
from core_app.repositories.item_type_repository import ItemTypeRepository

class ItemTypeService:
    def __init__(self, repository: ItemTypeRepository):
        self.repository = repository

    def create_item_type(self, name: str, color: str) -> ItemType:
        if not name:
            raise ValueError("Name is required.")
        if not color:
            raise ValueError("Color is required.")
        
        existing = self.repository.find_by_name(name)
        if existing:
            raise ValueError(f"Item type '{name}' already exists.")
        
        item_type = ItemType(name=name, color=color)
        return self.repository.create(item_type)
    
    def get_item_type(self, name: str) -> ItemType:
        item_type = self.repository.find_by_name(name)
        if not item_type:
            raise ValueError(f"Item type '{name}' not found.")
        return item_type
    
    def list_item_types(self) -> list[ItemType]:
        return self.repository.list_all()
    
    def delete_item_type(self, name: str) -> None:
        item_type = self.repository.find_by_name(name)
        if not item_type:
            raise ValueError(f"Item type '{name}' not found.")
        self.repository.delete(name)
        