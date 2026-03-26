from sqlalchemy.orm import Session
from core_app.domain.models.item import Item
from core_app.domain.models.item_type import ItemType
from core_app.database.models.item_model import ItemModel

class ItemRepository:
    def __init__(self, session: Session):
        self._session = session

    def create(self, item: Item) -> Item:
        db = ItemModel(
            name=item.name,
            item_type_name=item.item_type.name
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
            item_type=ItemType(
                name=db.item_type.name,
                color=db.item_type.color
            )
        )

    def find_all(self) -> list[Item]:
        return [
            Item(
                id=db.id,
                name=db.name,
                item_type=ItemType(
                    name=db.item_type.name,
                    color=db.item_type.color
                )
            )
            for db in self._session.query(ItemModel).all()
        ]

    def delete(self, item_id: int) -> None:
        db = self._session.query(ItemModel).filter_by(id=item_id).first()
        if db:
            self._session.delete(db)
            self._session.commit()
