"""Integration tests for ItemRepository against a real (in-memory) SQLite DB."""
import pytest

from core_app.domain.models.category import Category
from core_app.domain.models.item import Item
from core_app.repositories.category_repository import CategoryRepository
from core_app.repositories.item_repository import ItemRepository


@pytest.fixture()
def category(db_session):
    return CategoryRepository(db_session).create(Category(name="Food", color="#FF5733"))


class TestCreate:
    def test_assigns_id_and_persists_with_category(self, db_session, category):
        repo = ItemRepository(db_session)
        created = repo.create(Item(id=0, name="Apple", category=category))
        assert created.id != 0

        found = repo.find_by_id(created.id)
        assert found.name == "Apple"
        assert found.category.name == "Food"
        assert found.category.color == "#FF5733"


class TestFind:
    def test_find_by_id_missing_returns_none(self, db_session):
        repo = ItemRepository(db_session)
        assert repo.find_by_id(999) is None

    def test_find_all(self, db_session, category):
        repo = ItemRepository(db_session)
        repo.create(Item(id=0, name="Apple", category=category))
        repo.create(Item(id=0, name="Bus Ticket", category=category))
        names = {i.name for i in repo.find_all()}
        assert names == {"Apple", "Bus Ticket"}


class TestDelete:
    def test_delete_removes_item(self, db_session, category):
        repo = ItemRepository(db_session)
        created = repo.create(Item(id=0, name="Apple", category=category))
        repo.delete(created.id)
        assert repo.find_by_id(created.id) is None

    def test_delete_missing_item_is_noop(self, db_session):
        repo = ItemRepository(db_session)
        repo.delete(999)  # should not raise
