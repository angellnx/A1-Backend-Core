"""Transaction domain model for recording financial movements."""
from dataclasses import dataclass
from datetime import datetime
from .transaction_type import TransactionType

@dataclass
class Transaction:
    """Represents a financial transaction (income or expense).
    
    Transactions record money movements into or out of accounts. The sign of
    the value is normalized based on the transaction type: expenses are stored
    as negative values, income as positive. This normalization ensures that
    users can always input positive amounts and the system determines the sign.
    
    Attributes:
        id: Unique transaction identifier.
        date: When the transaction occurred.
        value: Transaction amount. Sign is normalized post-init based on type.
        transaction_type: Reference to TransactionType (determines expense vs income).
        user_id: Reference to the owning User.
        item_id: Reference to the Item being transacted.
        account_id: Reference to the Account the transaction affects.
        currency_code: ISO 4217 currency code for the value.
        notes: Optional additional details about the transaction.
    """
    id: int
    date: datetime
    value: float
    transaction_type: TransactionType
    user_id: int
    item_id: int
    account_id: int
    currency_code: str
    notes: str | None = None

    def __post_init__(self):
        """Normalize transaction value sign based on transaction type.
        
        Ensures expense transactions are negative and income transactions
        are positive, regardless of input sign. This allows users to always
        input positive amounts while the system determines the sign.
        """
        self._normalize_value()

    def _normalize_value(self):
        if not self.transaction_type.is_positive:
            self.value = -abs(self.value)
        else:
            self.value = abs(self.value)