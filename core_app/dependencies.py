from core_app.repositories.item_type_repository import ItemTypeRepository
from core_app.repositories.transaction_type_repository import TransactionTypeRepository
from core_app.repositories.item_repository import ItemRepository
from core_app.repositories.user_repository import UserRepository
from core_app.repositories.transaction_repository import TransactionRepository
from core_app.services.item_type_service import ItemTypeService
from core_app.services.transaction_type_service import TransactionTypeService
from core_app.services.item_service import ItemService
from core_app.services.user_service import UserService
from core_app.services.transaction_service import TransactionService

# Repositories — A single instance of each repository to be shared across the application
item_type_repository = ItemTypeRepository()
transaction_type_repository = TransactionTypeRepository()
item_repository = ItemRepository()
user_repository = UserRepository()
transaction_repository = TransactionRepository()

# Factories — Functions called by FastAPI for dependency injection
def get_item_type_service() -> ItemTypeService:
    return ItemTypeService(item_type_repository)

def get_transaction_type_service() -> TransactionTypeService:
    return TransactionTypeService(transaction_type_repository)

def get_item_service() -> ItemService:
    return ItemService(item_repository, item_type_repository)

def get_user_service() -> UserService:
    return UserService(user_repository)

def get_transaction_service() -> TransactionService:
    return TransactionService(
        transaction_repository,
        transaction_type_repository,
        item_repository
    )