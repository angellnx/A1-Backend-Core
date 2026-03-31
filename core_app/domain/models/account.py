"""Account domain model for user financial accounts."""
from dataclasses import dataclass

@dataclass
class Account:
    """Represents a user's bank or wallet account.
    
    Accounts hold transactions and have a dynamic balance calculated from
    all linked transactions. Balance is computed in the Service Layer by
    summing transaction values, not stored directly.
    
    Attributes:
        id: Unique account identifier.
        name: Institution name (e.g., "Nubank", "Bank of America").
        account_type: Account type (e.g., "Checking", "Savings", "Wallet").
        user_id: Reference to the owning User.
    """
    id: int
    name: str
    account_type: str
    user_id: int

    @property
    def balance(self) -> float:
        """Placeholder for balance calculation.
        
        Actual balance is computed dynamically by summing all transactions
        linked to this account. Calculation is performed in the Service Layer.
        
        Returns:
            float: Always returns 0.0 as a placeholder.
        """
        return 0.0