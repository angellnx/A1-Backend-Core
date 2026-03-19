from core_app.domain.models.transaction_type import TransactionType

class TransactionTypeRepository:
    def __init__(self):
        self._db: list[TransactionType] = []

    def create(self, transaction_type: TransactionType) -> TransactionType:
        self._db.append(transaction_type)
        return transaction_type

    def find_by_name(self, name: str) -> TransactionType | None:
        for tt in self._db:
            if tt.name == name:
                return tt
        return None

    def find_all(self) -> list[TransactionType]:
        return list(self._db)

    def delete(self, name: str) -> None:
        self._db = [tt for tt in self._db if tt.name != name]