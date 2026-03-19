import hashlib #hashlib is used for password hashing
from dataclasses import dataclass, field

@dataclass
class User:
    id: int
    email: str
    name: str
    _password_hash: str = field(repr=False) # The password hash is stored in a private field
                       # and is not included in the string representation of the User object

    # This method hashes the raw password and stores it in the _password_hash field
    def set_password(self, raw_password: str): 
        self._password_hash = hashlib.sha256(raw_password.encode()).hexdigest()
    
    # This method checks if the provided raw password matches the stored password hash
    def check_password(self, raw_password: str) -> bool:
        return self._password_hash == hashlib.sha256(raw_password.encode()).hexdigest() 