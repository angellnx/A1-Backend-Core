"""Business logic service for managing Accounts.

Coordinates account operations by validating inputs, verifying user
existence, delegating to repositories, and calculating balances.
"""
from core_app.domain.models.account import Account
from core_app.repositories.account_repository import AccountRepository
from core_app.repositories.user_repository import UserRepository


class AccountService:
    """Orchestrates account business logic and repository coordination.
    
    Responsibilities:
    - Validate account inputs (name and type required)
    - Verify user exists before account creation
    - Filter accounts by user for scoped access
    - Coordinate between routers and repository layer
    """
    def __init__(self, repository: AccountRepository, user_repository: UserRepository):
        self.repository = repository
        self.user_repository = user_repository

    def create_account(self, name: str, account_type: str, user_id: int) -> Account:
        """Create a new account with validation.
        
        Args:
            name: Institution name (required).
            account_type: Account type like 'Checking' (required).
            user_id: Owner user ID (must exist).
            
        Returns:
            Account: The created domain model.
            
        Raises:
            ValueError: If inputs invalid or user doesn't exist.
        """
        if not name:
            raise ValueError("Name is required")
        if not account_type:
            raise ValueError("Type is required")

        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")

        account = Account(id=0, name=name, account_type=account_type, user_id=user_id)
        return self.repository.create(account)

    def get_account(self, account_id: int) -> Account:
        """Retrieve an account by ID.
        
        Args:
            account_id: Account ID to find.
            
        Returns:
            Account: The found domain model.
            
        Raises:
            ValueError: If account not found.
        """
        account = self.repository.find_by_id(account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        return account

    def list_accounts_by_user(self, user_id: int) -> list[Account]:
        """Retrieve all accounts for a specific user.
        
        Args:
            user_id: Owner user ID (must exist).
            
        Returns:
            list[Account]: All accounts for the user.
            
        Raises:
            ValueError: If user doesn't exist.
        """
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return self.repository.find_all_by_user(user_id)

    def delete_account(self, account_id: int) -> None:
        """Delete an account by ID.
        
        Args:
            account_id: Account ID to delete.
            
        Raises:
            ValueError: If account not found.
        """
        account = self.repository.find_by_id(account_id)
        if not account:
            raise ValueError(f"Account with id {account_id} not found")
        self.repository.delete(account_id)
