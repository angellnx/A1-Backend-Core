"""Unit tests for ItemService (repositories mocked)."""
from unittest.mock import Mock

import pytest

from core_app.domain.models.category import Category
from core_app.domain.models.item import Item
from core_app.repositories.category_repository import CategoryRepository
from core_app.repositories.item_repository import ItemRepository
from core_app.services.item_service import ItemService


@pytest.fixture()
def item_repo():
    return Mock(spec=ItemRepository)


@pytest.fixture()
def category_repo():
    return Mock(spec=CategoryRepository)


@pytest.fixture()
def service(item_repo, category_repo):
    return ItemService(repository=item_repo, category_repository=category_repo)


class TestCreateItem:
    def test_missing_name_raises(self, service):
        with pytest.raises(ValueError, match="Name is required"):
            service.create_item(name="", category_name="Food")

    def test_category_not_found_raises(self, service, category_repo):
        category_repo.find_by_name.return_value = None
        with pytest.raises(ValueError, match="Category 'Food' not found"):
            service.create_item(name="Apple", category_name="Food")

    def test_success(self, service, category_repo, item_repo):
        category_repo.find_by_name.return_value = Category(name="Food", color="#FF5733")
        item_repo.create.side_effect = lambda i: i

        result = service.create_item(name="Apple", category_name="Food")

        assert result.name == "Apple"
        assert result.category.name == "Food"


class TestGetItem:
    def test_not_found_raises(self, service, item_repo):
        item_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Item '1' not found"):
            service.get_item(1)

    def test_success(self, service, item_repo):
        item = Item(id=1, name="Apple", category=Category(name="Food", color="#FF5733"))
        item_repo.find_by_id.return_value = item
        assert service.get_item(1) is item


class TestListItems:
    def test_delegates_to_repository(self, service, item_repo):
        item_repo.find_all.return_value = []
        assert service.list_items() == []


class TestDeleteItem:
    def test_not_found_raises(self, service, item_repo):
        item_repo.find_by_id.return_value = None
        with pytest.raises(ValueError, match="Item '1' not found"):
            service.delete_item(1)

    def test_success(self, service, item_repo):
        item_repo.find_by_id.return_value = Item(
            id=1, name="Apple", category=Category(name="Food", color="#FF5733")
        )
        service.delete_item(1)
        item_repo.delete.assert_called_once_with(1)
