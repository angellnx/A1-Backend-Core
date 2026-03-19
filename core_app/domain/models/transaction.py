from dataclasses import dataclass
from datetime import datetime
from .transaction_type import TransactionType

@dataclass
class Transaction:
    id: int
    date: datetime
    value: float
    transaction_type: TransactionType
    user_id: int
    item_id: int
    notes: str | None = None

    def __post_init__(self):
        self._normalize_value()

    def _normalize_value(self):
        # Users always input positive values. The sign is determined
        # by the transaction type's is_positive flag, not by the user.
        if not self.transaction_type.is_positive:
            self.value = -abs(self.value)
        else:
            self.value = abs(self.value)