from fastapi import Depends
from sqlalchemy.orm import Session
from core_app.database.session import get_session
from core_app.repositories.item_type_repository import ItemTypeRepository
from core_app.repositories.transaction_type_repository import TransactionTypeRepository
from core_app.repositories.item_repository import ItemRepository
from core_app.repositories.user_repository import UserRepository
from core_app.repositories.transaction_repository import TransactionRepository
from core_app.services.item_type_service import ItemTypeService
from core_app.repositories.currency_repository import CurrencyRepository
from core_app.services.transaction_type_service import TransactionTypeService
from core_app.services.item_service import ItemService
from core_app.services.user_service import UserService
from core_app.services.transaction_service import TransactionService
from core_app.services.currency_service import CurrencyService

def get_item_type_service(session: Session = Depends(get_session)) -> ItemTypeService:
    return ItemTypeService(ItemTypeRepository(session))

def get_transaction_type_service(session: Session = Depends(get_session)) -> TransactionTypeService:
    return TransactionTypeService(TransactionTypeRepository(session))

def get_item_service(session: Session = Depends(get_session)) -> ItemService:
    return ItemService(ItemRepository(session), ItemTypeRepository(session))

def get_user_service(session: Session = Depends(get_session)) -> UserService:
    return UserService(UserRepository(session))

def get_transaction_service(session: Session = Depends(get_session)) -> TransactionService:
    return TransactionService(
        TransactionRepository(session),
        TransactionTypeRepository(session),
        ItemRepository(session)
    )

def get_currency_service(session: Session = Depends(get_session)) -> CurrencyService:
    return CurrencyService(CurrencyRepository(session))