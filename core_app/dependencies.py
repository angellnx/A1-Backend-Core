"""Dependency injection factories for the Service Layer.

This module provides factory functions used by FastAPI to instantiate
services with their required repository dependencies. It acts as the
composition root of the application, wiring together repositories and services
while keeping the rest of the system decoupled from infrastructure concerns.
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from core_app.database.session import get_session
from core_app.repositories.category_repository import CategoryRepository
from core_app.repositories.transaction_type_repository import TransactionTypeRepository
from core_app.repositories.item_repository import ItemRepository
from core_app.repositories.user_repository import UserRepository
from core_app.repositories.transaction_repository import TransactionRepository
from core_app.repositories.account_repository import AccountRepository
from core_app.repositories.budget_repository import BudgetRepository
from core_app.repositories.currency_repository import CurrencyRepository

from core_app.services.category_service import CategoryService
from core_app.services.transaction_type_service import TransactionTypeService
from core_app.services.item_service import ItemService
from core_app.services.user_service import UserService
from core_app.services.transaction_service import TransactionService
from core_app.services.currency_service import CurrencyService
from core_app.services.account_service import AccountService
from core_app.services.budget_service import BudgetService


def get_category_service(session: Session = Depends(get_session)) -> CategoryService:
    """Provide CategoryService with required dependencies.

    Args:
        session: Database session provided by FastAPI dependency injection.

    Returns:
        CategoryService instance.
    """
    return CategoryService(CategoryRepository(session))


def get_transaction_type_service(session: Session = Depends(get_session)) -> TransactionTypeService:
    """Provide TransactionTypeService with required dependencies.

    Args:
        session: Database session provided by FastAPI dependency injection.

    Returns:
        TransactionTypeService instance.
    """
    return TransactionTypeService(TransactionTypeRepository(session))


def get_item_service(session: Session = Depends(get_session)) -> ItemService:
    """Provide ItemService with required dependencies.

    Args:
        session: Database session provided by FastAPI dependency injection.

    Returns:
        ItemService instance.
    """
    return ItemService(ItemRepository(session), CategoryRepository(session))


def get_user_service(session: Session = Depends(get_session)) -> UserService:
    """Provide UserService with required dependencies.

    Args:
        session: Database session provided by FastAPI dependency injection.

    Returns:
        UserService instance.
    """
    return UserService(UserRepository(session))


def get_transaction_service(session: Session = Depends(get_session)) -> TransactionService:
    """Provide TransactionService with required dependencies.

    Args:
        session: Database session provided by FastAPI dependency injection.

    Returns:
        TransactionService instance.
    """
    return TransactionService(
        TransactionRepository(session),
        TransactionTypeRepository(session),
        ItemRepository(session),
        CurrencyRepository(session)
    )


def get_currency_service(session: Session = Depends(get_session)) -> CurrencyService:
    """Provide CurrencyService with required dependencies.

    Args:
        session: Database session provided by FastAPI dependency injection.

    Returns:
        CurrencyService instance.
    """
    return CurrencyService(CurrencyRepository(session))


def get_account_service(session: Session = Depends(get_session)) -> AccountService:
    """Provide AccountService with required dependencies.

    Args:
        session: Database session provided by FastAPI dependency injection.

    Returns:
        AccountService instance.
    """
    return AccountService(AccountRepository(session), UserRepository(session))


def get_budget_service(session: Session = Depends(get_session)) -> BudgetService:
    """Provide BudgetService with required dependencies.

    Args:
        session: Database session provided by FastAPI dependency injection.

    Returns:
        BudgetService instance.
    """
    return BudgetService(
        BudgetRepository(session),
        UserRepository(session),
        CategoryRepository(session),
        CurrencyRepository(session)
    )