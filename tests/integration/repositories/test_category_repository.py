"""Integration tests for CategoryRepository against a real (in-memory) SQLite DB."""
from core_app.domain.models.category import Category
from core_app.repositories.category_repository import CategoryRepository


class TestCreate:
    def test_persists_category(self, db_session):
        repo = CategoryRepository(db_session)
        repo.create(Category(name="Food", color="#FF5733"))
        found = repo.find_by_name("Food")
        assert found == Category(name="Food", color="#FF5733")


class TestFind:
    def test_find_by_name_missing_returns_none(self, db_session):
        repo = CategoryRepository(db_session)
        assert repo.find_by_name("Ghost") is None

    def test_find_all(self, db_session):
        repo = CategoryRepository(db_session)
        repo.create(Category(name="Food", color="#FF5733"))
        repo.create(Category(name="Transport", color="#00FF00"))
        names = {c.name for c in repo.find_all()}
        assert names == {"Food", "Transport"}


class TestDelete:
    def test_delete_removes_category(self, db_session):
        repo = CategoryRepository(db_session)
        repo.create(Category(name="Food", color="#FF5733"))
        repo.delete("Food")
        assert repo.find_by_name("Food") is None

    def test_delete_missing_category_is_noop(self, db_session):
        repo = CategoryRepository(db_session)
        repo.delete("Ghost")  # should not raise
