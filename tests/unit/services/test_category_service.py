"""Unit tests for CategoryService (repository mocked)."""
from unittest.mock import Mock

import pytest

from core_app.domain.models.category import Category
from core_app.repositories.category_repository import CategoryRepository
from core_app.services.category_service import CategoryService


@pytest.fixture()
def repo():
    return Mock(spec=CategoryRepository)


@pytest.fixture()
def service(repo):
    return CategoryService(repository=repo)


class TestCreateCategory:
    def test_missing_name_raises(self, service):
        with pytest.raises(ValueError, match="Name is required"):
            service.create_category(name="", color="#FFFFFF")

    def test_missing_color_raises(self, service):
        with pytest.raises(ValueError, match="Color is required"):
            service.create_category(name="Food", color="")

    def test_duplicate_name_raises(self, service, repo):
        repo.find_by_name.return_value = Category(name="Food", color="#FFFFFF")
        with pytest.raises(ValueError, match="Category 'Food' already exists"):
            service.create_category(name="Food", color="#000000")

    def test_success(self, service, repo):
        repo.find_by_name.return_value = None
        repo.create.side_effect = lambda c: c
        result = service.create_category(name="Food", color="#FF5733")
        assert result == Category(name="Food", color="#FF5733")


class TestGetCategory:
    def test_not_found_raises(self, service, repo):
        repo.find_by_name.return_value = None
        with pytest.raises(ValueError, match="Category 'Food' not found"):
            service.get_category("Food")

    def test_success(self, service, repo):
        category = Category(name="Food", color="#FF5733")
        repo.find_by_name.return_value = category
        assert service.get_category("Food") == category


class TestListCategories:
    def test_delegates_to_repository(self, service, repo):
        repo.find_all.return_value = [Category(name="Food", color="#FF5733")]
        assert service.list_categories() == repo.find_all.return_value


class TestDeleteCategory:
    def test_not_found_raises(self, service, repo):
        repo.find_by_name.return_value = None
        with pytest.raises(ValueError, match="Category 'Food' not found"):
            service.delete_category("Food")

    def test_success(self, service, repo):
        repo.find_by_name.return_value = Category(name="Food", color="#FF5733")
        service.delete_category("Food")
        repo.delete.assert_called_once_with("Food")
