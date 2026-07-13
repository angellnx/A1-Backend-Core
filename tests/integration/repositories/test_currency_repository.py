"""Integration tests for CurrencyRepository against a real (in-memory) SQLite DB."""
from core_app.domain.models.currency import Currency
from core_app.repositories.currency_repository import CurrencyRepository


class TestCreate:
    def test_persists_currency(self, db_session):
        repo = CurrencyRepository(db_session)
        repo.create(Currency(code="BRL", name="Brazilian Real", symbol="R$"))
        found = repo.find_by_code("BRL")
        assert found == Currency(code="BRL", name="Brazilian Real", symbol="R$")


class TestFind:
    def test_find_by_code_missing_returns_none(self, db_session):
        repo = CurrencyRepository(db_session)
        assert repo.find_by_code("XYZ") is None

    def test_find_all(self, db_session):
        repo = CurrencyRepository(db_session)
        repo.create(Currency(code="BRL", name="Brazilian Real", symbol="R$"))
        repo.create(Currency(code="USD", name="US Dollar", symbol="$"))
        codes = {c.code for c in repo.find_all()}
        assert codes == {"BRL", "USD"}


class TestDelete:
    def test_delete_removes_currency(self, db_session):
        repo = CurrencyRepository(db_session)
        repo.create(Currency(code="BRL", name="Brazilian Real", symbol="R$"))
        repo.delete("BRL")
        assert repo.find_by_code("BRL") is None

    def test_delete_missing_currency_is_noop(self, db_session):
        repo = CurrencyRepository(db_session)
        repo.delete("XYZ")  # should not raise
