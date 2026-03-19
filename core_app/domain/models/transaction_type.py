from dataclasses import dataclass

@dataclass
class TransactionType:
    name: str # PK textual
    is_positive: bool # True = Income, False = Expense