from core_app.domain.models import Currency
from core_app.repositories.currency_repository import CurrencyRepository

class CurrencyService:
    def __init__(self, repository: CurrencyRepository):
        self.repository = repository

    def create_currency(self, code: str, name: str, symbol: str) -> Currency:
        if not code:
            raise ValueError("Code is required")

        code = code.upper()

        existing = self.repository.find_by_code(code)
        if existing:
            raise ValueError(f"Currency '{code}' already exists")

        currency = Currency(
            code=code,
            name=name,
            symbol=symbol
        )

        return self.repository.create(currency)

    def get_currency(self, code: str) -> Currency:
        code = code.upper()

        currency = self.repository.find_by_code(code)
        if not currency:
            raise ValueError(f"Currency '{code}' not found")
        return currency

    def list_currencies(self) -> list[Currency]:
        return self.repository.find_all()

    def delete_currency(self, code: str) -> None:
        code = code.upper()

        currency = self.repository.find_by_code(code)
        if not currency:
            raise ValueError(f"Currency '{code}' not found")
        self.repository.delete(code)