"""Repository layer for persisting Item domain models.

Converts between Domain Models (Item) and Database Models (ItemModel).
"""
from sqlalchemy.orm import Session
from core_app.domain.models.item import Item
from core_app.domain.models.category import Category
from core_app.database.models.item_model import ItemModel

class ItemRepository:
    """Coordinates Item domain model persistence.
    
    Items include category references which are loaded eagerly from relationships.
    """
    def __init__(self, session: Session):
        self._session = session

    def create(self, item: Item) -> Item:
        db = ItemModel(
            name=item.name,
            category_name=item.category.name
        )
        self._session.add(db)
        self._session.commit()
        self._session.refresh(db)
        item.id = db.id
        return item

    def find_by_id(self, item_id: int) -> Item | None:
        db = self._session.query(ItemModel).filter_by(id=item_id).first()
        if not db:
            return None
        return Item(
            id=db.id,
            name=db.name,
            category=Category(
                name=db.category.name,
                color=db.category.color
            )
        )

    def find_all(self) -> list[Item]:
        return [
            Item(
                id=db.id,
                name=db.name,
                category=Category(
                    name=db.category.name,
                    color=db.category.color
                )
            )
            for db in self._session.query(ItemModel).all()
        ]

    def delete(self, item_id: int) -> None:
        db = self._session.query(ItemModel).filter_by(id=item_id).first()
        if db:
            self._session.delete(db)
            self._session.commit()
