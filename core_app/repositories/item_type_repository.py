from sqlalchemy.orm import Session
from core_app.database.models.item_type_model import ItemTypeModel
from core_app.domain.models.item_type import ItemType

class ItemTypeRepository:
    def __init__(self, session: Session):
        self._db: Session = session

    def create(self, item_type: ItemType) -> ItemType:
        db = ItemTypeModel(
            name=item_type.name,
            color=item_type.color
        )
        self.session.add(db)
        self.session.commit()
        self.session.refresh(db)
        return item_type
    
    def find_by_name(self, name: str) -> ItemType | None:
        db = self.session.query(ItemTypeModel).filter_by(name=name).first()
        if not db:
            return None
        return ItemType(name=db.name, color=db.color
                        )
    def find_all(self) -> list[ItemType]:
        return [
            ItemType(name=db.name, color=db.color)
            for db in self.session.query(ItemTypeModel).all()
        ]
    
    def delete(self, name: str) -> None:
        db = self.session.query(ItemTypeModel).filter_by(name=name).first()
        if db:
            self.session.delete(db)
            self.session.commit()