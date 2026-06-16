"""User domain model representing an authenticated system user."""
from dataclasses import dataclass, field
from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12, truncate_error=False)

@dataclass
class User:
    """Represents an authenticated user in the personal finance system.

    Attributes:
        id: Unique user identifier.
        email: User's email address (unique).
        name: User's full name.
        username: Unique username for login.
        phone: Optional contact phone number.
        _password_hash: Bcrypt hash of user's password.
    """
    id: int
    email: str
    name: str
    username: str
    phone: str | None = None
    _password_hash: str = field(default="", repr=False)

    def set_password(self, raw_password: str) -> None:
        """Hash and store a raw password using bcrypt."""
        self._password_hash = _pwd_context.hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        """Verify a plaintext password against the stored bcrypt hash."""
        return _pwd_context.verify(raw_password, self._password_hash)