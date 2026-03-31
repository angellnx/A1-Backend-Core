"""HTTP API endpoints for managing transaction types.

Exposes CRUD operations for transaction type reference data as REST endpoints.
Transaction types classify transactions as income (positive) or expense (negative).
"""
from fastapi import APIRouter, Depends, HTTPException
from core_app.services.transaction_type_service import TransactionTypeService
from core_app.schemas.transaction_type_schema import TransactionTypeRequest, TransactionTypeResponse
from core_app.dependencies import get_transaction_type_service

router = APIRouter(prefix="/transaction-types", tags=["Transaction Types"])

@router.post("/", response_model=TransactionTypeResponse, status_code=201)
def create_transaction_type(
    body: TransactionTypeRequest,
    service: TransactionTypeService = Depends(get_transaction_type_service)
):
    """Create a new transaction type.
    
    Args:
        body: Request with name and is_positive.
        service: TransactionTypeService instance via dependency injection.
    
    Returns:
        TransactionTypeResponse: Created transaction type (HTTP 201).
    
    Raises:
        HTTPException: 400 if validation fails or duplicate transaction type exists.
    """
    try:
        return service.create_transaction_type(name=body.name, is_positive=body.is_positive)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[TransactionTypeResponse])
def list_transaction_types(service: TransactionTypeService = Depends(get_transaction_type_service)):
    """List all transaction types.
    
    Args:
        service: TransactionTypeService instance via dependency injection.
    
    Returns:
        list[TransactionTypeResponse]: All transaction types.
    """
    return service.list_transaction_types()

@router.get("/{name}", response_model=TransactionTypeResponse)
def get_transaction_type(name: str, service: TransactionTypeService = Depends(get_transaction_type_service)):
    """Retrieve a transaction type by name.
    
    Args:
        name: Transaction type name to retrieve.
        service: TransactionTypeService instance via dependency injection.
    
    Returns:
        TransactionTypeResponse: Found transaction type.
    
    Raises:
        HTTPException: 404 if transaction type not found.
    """
    try:
        return service.get_transaction_type(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{name}", status_code=204)
def delete_transaction_type(name: str, service: TransactionTypeService = Depends(get_transaction_type_service)):
    """Delete a transaction type by name.
    
    Args:
        name: Transaction type name to delete.
        service: TransactionTypeService instance via dependency injection.
    
    Returns:
        None (HTTP 204 No Content).
    
    Raises:
        HTTPException: 404 if transaction type not found.
    """
    try:
        service.delete_transaction_type(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    