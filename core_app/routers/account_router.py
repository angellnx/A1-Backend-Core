"""HTTP API endpoints for managing accounts.

Exposes CRUD operations for user accounts as REST endpoints. Handles error
conversion from service layer ValueError to appropriate HTTPException codes.

Status codes:
- 201: Resource created (POST)
- 204: Deleted successfully (DELETE)
- 400: Bad request (validation failed)
- 404: Resource not found
"""
from fastapi import APIRouter, Depends, HTTPException
from core_app.services.account_service import AccountService
from core_app.schemas.account_schema import AccountRequest, AccountResponse
from core_app.dependencies import get_account_service

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/", response_model=AccountResponse, status_code=201)
def create_account(
    body: AccountRequest,
    service: AccountService = Depends(get_account_service)
):
    """Create a new account.
    
    Args:
        body: Request with name, account_type, and user_id.
        service: AccountService instance via dependency injection.
        
    Returns:
        AccountResponse: Created account with calculated balance (HTTP 201).
        
    Raises:
        HTTPException: 400 if validation fails, 400 if user not found.
    """
    try:
        account = service.create_account(
            name=body.name,
            account_type=body.account_type,
            user_id=body.user_id
        )
        return AccountResponse(
            id=account.id,
            name=account.name,
            account_type=account.account_type,
            user_id=account.user_id,
            balance=account.balance
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}", response_model=list[AccountResponse])
def list_accounts_by_user(
    user_id: int,
    service: AccountService = Depends(get_account_service)
):
    """List all accounts for a specific user.
    
    Args:
        user_id: Owner user ID.
        service: AccountService instance via dependency injection.
        
    Returns:
        list[AccountResponse]: User's accounts.
        
    Raises:
        HTTPException: 404 if user not found.
    """
    try:
        accounts = service.list_accounts_by_user(user_id)
        return [
            AccountResponse(
                id=a.id,
                name=a.name,
                account_type=a.account_type,
                user_id=a.user_id,
                balance=a.balance
            )
            for a in accounts
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(
    account_id: int,
    service: AccountService = Depends(get_account_service)
):
    """Retrieve an account by ID.
    
    Args:
        account_id: Account ID to retrieve.
        service: AccountService instance via dependency injection.
        
    Returns:
        AccountResponse: Found account with calculated balance.
        
    Raises:
        HTTPException: 404 if account not found.
    """
    try:
        account = service.get_account(account_id)
        return AccountResponse(
            id=account.id,
            name=account.name,
            account_type=account.account_type,
            user_id=account.user_id,
            balance=account.balance
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{account_id}", status_code=204)
def delete_account(
    account_id: int,
    service: AccountService = Depends(get_account_service)
):
    """Delete an account by ID.
    
    Args:
        account_id: Account ID to delete.
        service: AccountService instance via dependency injection.
        
    Returns:
        None (HTTP 204 No Content).
        
    Raises:
        HTTPException: 404 if account not found.
    """
    try:
        service.delete_account(account_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
