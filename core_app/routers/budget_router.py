"""HTTP API endpoints for managing budgets.
Exposes CRUD operations for spending budgets as REST endpoints.
Budgets define spending limits per user, category, currency, month/year.
"""
from fastapi import APIRouter, Depends, HTTPException
from core_app.services.budget_service import BudgetService
from core_app.schemas.budget_schema import BudgetRequest, BudgetResponse
from core_app.dependencies import get_budget_service, get_current_user
from core_app.domain.models.user import User

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.post("/", response_model=BudgetResponse, status_code=201)
def create_budget(
    body: BudgetRequest,
    service: BudgetService = Depends(get_budget_service),
    current_user: User = Depends(get_current_user)
):
    try:
        budget = service.create_budget(
            amount=body.amount,
            month=body.month,
            year=body.year,
            user_id=current_user.id,
            category_name=body.category_name,
            currency_code=body.currency_code
        )
        return BudgetResponse(
            id=budget.id,
            amount=budget.amount,
            month=budget.month,
            year=budget.year,
            user_id=budget.user_id,
            category_name=budget.category.name,
            currency_code=budget.currency_code
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=list[BudgetResponse])
def list_my_budgets(
    service: BudgetService = Depends(get_budget_service),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 20
):
    """List all budgets for the authenticated user.

    Args:
        service: BudgetService instance via dependency injection.
        current_user: Authenticated user from JWT token.
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.

    Returns:
        list[BudgetResponse]: Paginated budgets belonging to the user.
    """
    try:
        budgets = service.list_budgets_by_user(current_user.id, skip=skip, limit=limit)
        return [
            BudgetResponse(
                id=b.id,
                amount=b.amount,
                month=b.month,
                year=b.year,
                user_id=b.user_id,
                category_name=b.category.name,
                currency_code=b.currency_code
            )
            for b in budgets
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{budget_id}", response_model=BudgetResponse)
def get_budget(
    budget_id: int,
    service: BudgetService = Depends(get_budget_service),
    current_user: User = Depends(get_current_user)
):
    try:
        budget = service.get_budget(budget_id, current_user_id=current_user.id)
        return BudgetResponse(
            id=budget.id,
            amount=budget.amount,
            month=budget.month,
            year=budget.year,
            user_id=budget.user_id,
            category_name=budget.category.name,
            currency_code=budget.currency_code
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{budget_id}", status_code=204)
def delete_budget(
    budget_id: int,
    service: BudgetService = Depends(get_budget_service),
    current_user: User = Depends(get_current_user)
):
    try:
        service.delete_budget(budget_id, current_user_id=current_user.id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
