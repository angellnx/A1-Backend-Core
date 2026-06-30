"""HTTP API endpoints for managing accounts.
Exposes CRUD operations for user accounts as REST endpoints. Handles error
conversion from service layer ValueError to appropriate HTTPException codes.
Status codes:
- 201: Resource created (POST)
- 204: Deleted successfully (DELETE)
- 400: Bad request (validation failed)
- 403: Forbidden (access to another user's resource)
- 404: Resource not found
"""
from fastapi import APIRouter, Depends, HTTPException
from core_app.services.account_service import AccountService
from core_app.schemas.account_schema import AccountRequest, AccountResponse
from core_app.dependencies import get_account_service, get_current_user
from core_app.domain.models.user import User

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("/", response_model=AccountResponse, status_code=201)
def create_account(
    body: AccountRequest,
    service: AccountService = Depends(get_account_service),
    current_user: User = Depends(get_current_user)
):
    try:
        account = service.create_account(
            name=body.name,
            account_type=body.account_type,
            user_id=current_user.id
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


@router.get("/me", response_model=list[AccountResponse])
def list_my_accounts(
    service: AccountService = Depends(get_account_service),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20
):
    """List all accounts for the authenticated user.

    Args:
        service: AccountService instance via dependency injection.
        current_user: Authenticated user from JWT token.
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.

    Returns:
        list[AccountResponse]: Paginated accounts belonging to the user.
    """
    try:
        accounts = service.list_accounts_by_user(current_user.id, skip=skip, limit=limit)
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
    service: AccountService = Depends(get_account_service),
    current_user: User = Depends(get_current_user)
):
    try:
        account = service.get_account(account_id, current_user_id=current_user.id)
        return AccountResponse(
            id=account.id,
            name=account.name,
            account_type=account.account_type,
            user_id=account.user_id,
            balance=account.balance
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{account_id}", status_code=204)
def delete_account(
    account_id: int,
    service: AccountService = Depends(get_account_service),
    current_user: User = Depends(get_current_user)
):
    try:
        service.delete_account(account_id, current_user_id=current_user.id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    