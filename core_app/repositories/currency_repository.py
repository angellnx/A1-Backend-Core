"""Repository layer for persisting Currency domain models.

Converts between Domain Models (Currency) and Database Models (CurrencyModel).
"""
from core_app.database.models.currency_model import CurrencyModel
from core_app.domain.models.currency import Currency
from sqlalchemy.orm import Session

class CurrencyRepository:
    """Coordinates Currency domain model persistence."""

    def __init__(self, session: Session):
        self._session = session

    def create(self, currency: Currency) -> Currency:
        db = CurrencyModel(
            code=currency.code,
            name=currency.name,
            symbol=currency.symbol
        )
        self._session.add(db)
        self._session.commit()
        self._session.refresh(db)
        return currency

    def find_by_code(self, code: str) -> Currency | None:
        db = self._session.query(CurrencyModel).filter_by(code=code).first()
        if not db:
            return None
        return Currency(code=db.code, name=db.name, symbol=db.symbol)

    def find_all(self) -> list[Currency]:
        return [
            Currency(code=db.code, name=db.name, symbol=db.symbol)
            for db in self._session.query(CurrencyModel).all()
        ]

    def delete(self, code: str):
        db = self._session.query(CurrencyModel).filter_by(code=code).first()
        if db:
            self._session.delete(db)
            self._session.commit()