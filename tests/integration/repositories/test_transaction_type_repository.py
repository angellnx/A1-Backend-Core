"""Integration tests for TransactionTypeRepository against a real (in-memory) SQLite DB."""
from core_app.domain.models.transaction_type import TransactionType
from core_app.repositories.transaction_type_repository import TransactionTypeRepository


class TestCreate:
    def test_persists_transaction_type(self, db_session):
        repo = TransactionTypeRepository(db_session)
        repo.create(TransactionType(name="Salary", is_positive=True))
        found = repo.find_by_name("Salary")
        assert found == TransactionType(name="Salary", is_positive=True)


class TestFind:
    def test_find_by_name_missing_returns_none(self, db_session):
        repo = TransactionTypeRepository(db_session)
        assert repo.find_by_name("Ghost") is None

    def test_find_all(self, db_session):
        repo = TransactionTypeRepository(db_session)
        repo.create(TransactionType(name="Salary", is_positive=True))
        repo.create(TransactionType(name="Grocery", is_positive=False))
        names = {t.name for t in repo.find_all()}
        assert names == {"Salary", "Grocery"}


class TestDelete:
    def test_delete_removes_transaction_type(self, db_session):
        repo = TransactionTypeRepository(db_session)
        repo.create(TransactionType(name="Salary", is_positive=True))
        repo.delete("Salary")
        assert repo.find_by_name("Salary") is None

    def test_delete_missing_is_noop(self, db_session):
        repo = TransactionTypeRepository(db_session)
        repo.delete("Ghost")  # should not raise
