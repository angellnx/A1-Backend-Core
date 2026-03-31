"""HTTP API endpoints for managing currencies.

Exposes CRUD operations for reference currency data as REST endpoints.
Currencies are ISO 4217 codes used by transactions and budgets.
"""
from fastapi import APIRouter, Depends, HTTPException
from core_app.services.currency_service import CurrencyService
from core_app.schemas.currency_schema import CurrencyCreate, CurrencyResponse
from core_app.dependencies import get_currency_service

router = APIRouter(prefix="/currencies", tags=["Currencies"])

@router.post("/", response_model=CurrencyResponse, status_code=201)
def create_currency(
    body: CurrencyCreate,
    service: CurrencyService = Depends(get_currency_service)
):
    """Create a new currency.
    
    Args:
        body: Request with code, name, and symbol.
        service: CurrencyService instance via dependency injection.
    
    Returns:
        CurrencyResponse: Created currency (HTTP 201).
    
    Raises:
        HTTPException: 400 if validation fails or duplicate currency exists.
    """
    try:
        return service.create_currency(code=body.code, name=body.name, symbol=body.symbol)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[CurrencyResponse])
def list_currencies(service: CurrencyService = Depends(get_currency_service)):
    """List all currencies.
    
    Args:
        service: CurrencyService instance via dependency injection.
    
    Returns:
        list[CurrencyResponse]: All reference currencies.
    """
    return service.list_currencies()

@router.get("/{code}", response_model=CurrencyResponse)
def get_currency(code: str, service: CurrencyService = Depends(get_currency_service)):
    """Retrieve a currency by ISO 4217 code.
    
    Args:
        code: ISO 4217 currency code to retrieve.
        service: CurrencyService instance via dependency injection.
    
    Returns:
        CurrencyResponse: Found currency.
    
    Raises:
        HTTPException: 404 if currency not found.
    """
    try:
        return service.get_currency(code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{code}", status_code=204)
def delete_currency(code: str, service: CurrencyService = Depends(get_currency_service)):
    """Delete a currency by code.
    
    Args:
        code: ISO 4217 currency code to delete.
        service: CurrencyService instance via dependency injection.
    
    Returns:
        None (HTTP 204 No Content).
    
    Raises:
        HTTPException: 404 if currency not found.
    """
    try:
        service.delete_currency(code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))