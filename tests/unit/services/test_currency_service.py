"""Unit tests for CurrencyService (repository mocked)."""
from unittest.mock import Mock

import pytest

from core_app.domain.models.currency import Currency
from core_app.repositories.currency_repository import CurrencyRepository
from core_app.services.currency_service import CurrencyService


@pytest.fixture()
def repo():
    return Mock(spec=CurrencyRepository)


@pytest.fixture()
def service(repo):
    return CurrencyService(repository=repo)


class TestCreateCurrency:
    def test_missing_code_raises(self, service):
        with pytest.raises(ValueError, match="Code is required"):
            service.create_currency(code="", name="Real", symbol="R$")

    def test_normalizes_code_to_uppercase(self, service, repo):
        repo.find_by_code.return_value = None
        repo.create.side_effect = lambda c: c
        result = service.create_currency(code="brl", name="Real", symbol="R$")
        assert result.code == "BRL"
        repo.find_by_code.assert_called_once_with("BRL")

    def test_duplicate_raises(self, service, repo):
        repo.find_by_code.return_value = Currency(code="BRL", name="Real", symbol="R$")
        with pytest.raises(ValueError, match="Currency 'BRL' already exists"):
            service.create_currency(code="BRL", name="Real", symbol="R$")


class TestGetCurrency:
    def test_normalizes_code_before_lookup(self, service, repo):
        repo.find_by_code.return_value = Currency(code="USD", name="US Dollar", symbol="$")
        service.get_currency("usd")
        repo.find_by_code.assert_called_once_with("USD")

    def test_not_found_raises(self, service, repo):
        repo.find_by_code.return_value = None
        with pytest.raises(ValueError, match="Currency 'USD' not found"):
            service.get_currency("usd")


class TestListCurrencies:
    def test_delegates_to_repository(self, service, repo):
        repo.find_all.return_value = [Currency(code="USD", name="US Dollar", symbol="$")]
        assert service.list_currencies() == repo.find_all.return_value


class TestDeleteCurrency:
    def test_normalizes_code_before_lookup(self, service, repo):
        repo.find_by_code.return_value = Currency(code="USD", name="US Dollar", symbol="$")
        service.delete_currency("usd")
        repo.delete.assert_called_once_with("USD")

    def test_not_found_raises(self, service, repo):
        repo.find_by_code.return_value = None
        with pytest.raises(ValueError, match="Currency 'USD' not found"):
            service.delete_currency("usd")
