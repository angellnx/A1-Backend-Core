"""HTTP API endpoints for managing transactions.

Exposes CRUD operations for financial transactions as REST endpoints.
Transactions record income and expense movements affecting account balances.
"""
from fastapi import APIRouter, Depends, HTTPException
from core_app.services.transaction_service import TransactionService
from core_app.schemas.transaction_schema import TransactionRequest, TransactionResponse
from core_app.dependencies import get_transaction_service

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(
    body: TransactionRequest,
    service: TransactionService = Depends(get_transaction_service)
):
    """Create a new transaction.
    
    Args:
        body: Request with user_id, item_id, transaction_type_name, currency_code, value, date, notes.
        service: TransactionService instance via dependency injection.
    
    Returns:
        TransactionResponse: Created transaction (HTTP 201).
    
    Raises:
        HTTPException: 400 if validation fails or dependencies not found.
    """
    try:
        transaction = service.create_transaction(
            user_id=body.user_id,
            item_id=body.item_id,
            account_id=body.account_id,
            transaction_type_name=body.transaction_type_name,
            currency_code=body.currency_code,
            value=body.value,
            date=body.date,
            notes=body.notes
        )
        return TransactionResponse(
            id=transaction.id,
            date=transaction.date,
            value=transaction.value,
            transaction_type_name=transaction.transaction_type.name,
            user_id=transaction.user_id,
            item_id=transaction.item_id,
            currency_code=transaction.currency_code,
            notes=transaction.notes
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[TransactionResponse])
def list_transactions(service: TransactionService = Depends(get_transaction_service)):
    """List all transactions.
    
    Args:
        service: TransactionService instance via dependency injection.
    
    Returns:
        list[TransactionResponse]: All transactions.
    """
    return [
        TransactionResponse(
            id=t.id,
            date=t.date,
            value=t.value,
            transaction_type_name=t.transaction_type.name,
            user_id=t.user_id,
            item_id=t.item_id,
            currency_code=t.currency_code,
            notes=t.notes
        )
        for t in service.list_transactions()
    ]


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    service: TransactionService = Depends(get_transaction_service)
):
    """Retrieve a transaction by ID.
    
    Args:
        transaction_id: Transaction ID to retrieve.
        service: TransactionService instance via dependency injection.
    
    Returns:
        TransactionResponse: Found transaction.
    
    Raises:
        HTTPException: 404 if transaction not found.
    """
    try:
        t = service.get_transaction(transaction_id)
        return TransactionResponse(
            id=t.id,
            date=t.date,
            value=t.value,
            transaction_type_name=t.transaction_type.name,
            user_id=t.user_id,
            item_id=t.item_id,
            currency_code=t.currency_code,
            notes=t.notes
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(
    transaction_id: int,
    service: TransactionService = Depends(get_transaction_service)
):
    """Delete a transaction by ID.
    
    Args:
        transaction_id: Transaction ID to delete.
        service: TransactionService instance via dependency injection.
    
    Returns:
        None (HTTP 204 No Content).
    
    Raises:
        HTTPException: 404 if transaction not found.
    """
    try:
        service.delete_transaction(transaction_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))