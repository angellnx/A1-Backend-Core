import hashlib
from dataclasses import dataclass, field

@dataclass
class User:
    id: int
    email: str
    name: str
    _password_hash: str = field(repr=False) 

    def set_password(self, raw_password: str): 
        self._password_hash = hashlib.sha256(raw_password.encode()).hexdigest()
    
    def check_password(self, raw_password: str) -> bool:
        return self._password_hash == hashlib.sha256(raw_password.encode()).hexdigest() 