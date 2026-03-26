from dataclasses import dataclass

@dataclass
class Currency:
    code: str # ISO 4217  
    name: str # Full name of the currency`
    symbol: str 