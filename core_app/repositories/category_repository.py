"""Repository layer for persisting Category domain models.

Converts between Domain Models (Category) and Database Models (CategoryModel).
"""
from sqlalchemy.orm import Session
from core_app.database.models.category_model import CategoryModel
from core_app.domain.models.category import Category

class CategoryRepository:
    """Coordinates Category domain model persistence."""
    def __init__(self, session: Session):
        self._session: Session = session

    def create(self, category: Category) -> Category:
        db = CategoryModel(
            name=category.name,
            color=category.color
        )
        self._session.add(db)
        self._session.commit()
        self._session.refresh(db)
        return category
    
    def find_by_name(self, name: str) -> Category | None:
        db = self._session.query(CategoryModel).filter_by(name=name).first()
        if not db:
            return None
        return Category(name=db.name, color=db.color)

    def find_all(self) -> list[Category]:
        return [
            Category(name=db.name, color=db.color)
            for db in self._session.query(CategoryModel).all()
        ]
    
    def delete(self, name: str) -> None:
        db = self._session.query(CategoryModel).filter_by(name=name).first()
        if db:
            self._session.delete(db)
            self._session.commit()