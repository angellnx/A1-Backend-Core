"""HTTP API endpoints for managing transactions.

Exposes CRUD operations for financial transactions as REST endpoints.
Transactions record income and expense movements affecting account balances.
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from core_app.services.transaction_service import TransactionService
from core_app.schemas.transaction_schema import TransactionRequest, TransactionResponse
from core_app.dependencies import get_transaction_service, get_current_user
from core_app.domain.models.user import User

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(
    body: TransactionRequest,
    service: TransactionService = Depends(get_transaction_service),
    current_user: User = Depends(get_current_user),
):
    try:
        transaction = service.create_transaction(
            user_id=current_user.id,
            item_id=body.item_id,
            account_id=body.account_id,
            transaction_type_name=body.transaction_type_name,
            currency_code=body.currency_code,
            value=body.value,
            date=body.date,
            notes=body.notes,
        )
        return TransactionResponse(
            id=transaction.id,
            date=transaction.date,
            value=transaction.value,
            transaction_type_name=transaction.transaction_type.name,
            account_id=transaction.account_id,
            item_id=transaction.item_id,
            currency_code=transaction.currency_code,
            notes=transaction.notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[TransactionResponse])
def list_transactions(
    service: TransactionService = Depends(get_transaction_service),
    current_user: User = Depends(get_current_user),
    transaction_type_name: str | None = None,
    currency_code: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    skip: int = 0,
    limit: int = 20,
):
    """List transactions for the authenticated user with optional filters.

    Args:
        service: TransactionService instance via dependency injection.
        current_user: Authenticated user from JWT token.
        transaction_type_name: Optional filter by transaction type name.
        currency_code: Optional filter by currency code.
        date_from: Optional start date filter (ISO 8601).
        date_to: Optional end date filter (ISO 8601).
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return (max 100).

    Returns:
        list[TransactionResponse]: Filtered and paginated user transactions.
    """
    try:
        return [
            TransactionResponse(
                id=t.id,
                date=t.date,
                value=t.value,
                transaction_type_name=t.transaction_type.name,
                account_id=t.account_id,
                item_id=t.item_id,
                currency_code=t.currency_code,
                notes=t.notes,
            )
            for t in service.list_transactions_by_user(
                user_id=current_user.id,
                transaction_type_name=transaction_type_name,
                currency_code=currency_code,
                date_from=date_from,
                date_to=date_to,
                skip=skip,
                limit=limit,
            )
        ]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    service: TransactionService = Depends(get_transaction_service),
    current_user: User = Depends(get_current_user),
):
    try:
        t = service.get_transaction(transaction_id)
        return TransactionResponse(
            id=t.id,
            date=t.date,
            value=t.value,
            transaction_type_name=t.transaction_type.name,
            account_id=t.account_id,
            item_id=t.item_id,
            currency_code=t.currency_code,
            notes=t.notes,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(
    transaction_id: int,
    service: TransactionService = Depends(get_transaction_service),
    current_user: User = Depends(get_current_user),
):
    try:
        service.delete_transaction(transaction_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
