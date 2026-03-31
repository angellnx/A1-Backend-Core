"""User domain model representing an authenticated system user."""
import hashlib
from dataclasses import dataclass, field

@dataclass
class User:
    """Represents an authenticated user in the personal finance system.

    Attributes:
        id: Unique user identifier.
        email: User's email address (unique).
        name: User's full name.
        username: Unique username for login.
        phone: Optional contact phone number.
        _password_hash: SHA256 hash of user's password. Marked as non-repr
            to prevent sensitive data from appearing in logs or debugging output.
    """
    id: int
    email: str
    name: str
    username: str
    phone: str | None = None
    _password_hash: str = field(default="", repr=False)

    def set_password(self, raw_password: str):
        """Hash and store a raw password.

        Args:
            raw_password: Plaintext password to hash.
        """
        self._password_hash = hashlib.sha256(raw_password.encode()).hexdigest()

    def check_password(self, raw_password: str) -> bool:
        """Verify a plaintext password against the stored hash.

        Args:
            raw_password: Plaintext password to verify.
        Returns:
            bool: True if password matches, False otherwise.
        """
        return self._password_hash == hashlib.sha256(raw_password.encode()).hexdigest()