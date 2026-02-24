from core_app.domain.models.type_item import ItemType
from typing import Any

class ItemTypeService:
    def __init__(self, repository: Any):
        self.repository = repository

    def create_item_type(self, name: str, color: str) -> ItemType:
        if not name:
            raise ValueError("Type name is required")
        if not color:
            raise ValueError("Color is required")

        item_type = ItemType(
            name=name,
            color=color
        )

        return self.repository.create(item_type)

    def get_item_type_by_name(self, name: str) -> ItemType | None:
        return self.repository.find_by_id(name)

    def list_item_types(self) -> list[ItemType]:
        return self.repository.find_all()

    def delete_item_type(self, name: str) -> None:
        item_type = self.repository.find_by_id(name)
        if not item_type:
            raise ValueError("Item type not found")
        self.repository.delete(item_type)
