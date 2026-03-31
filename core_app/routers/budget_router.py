"""HTTP API endpoints for managing budgets.

Exposes CRUD operations for spending budgets as REST endpoints.
Budgets define spending limits per user, category, currency, month/year.
"""
from fastapi import APIRouter, Depends, HTTPException
from core_app.services.budget_service import BudgetService
from core_app.schemas.budget_schema import BudgetRequest, BudgetResponse
from core_app.dependencies import get_budget_service

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.post("/", response_model=BudgetResponse, status_code=201)
def create_budget(
    body: BudgetRequest,
    service: BudgetService = Depends(get_budget_service)
):
    """Create a new budget.
    
    Args:
        body: Request with amount, month, year, user_id, category_name, currency_code.
        service: BudgetService instance via dependency injection.
    
    Returns:
        BudgetResponse: Created budget (HTTP 201).
    
    Raises:
        HTTPException: 400 if validation fails or duplicate budget exists.
    """
    try:
        budget = service.create_budget(
            amount=body.amount,
            month=body.month,
            year=body.year,
            user_id=body.user_id,
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


@router.get("/user/{user_id}", response_model=list[BudgetResponse])
def list_budgets_by_user(
    user_id: int,
    service: BudgetService = Depends(get_budget_service)
):
    """List all budgets for a specific user.
    
    Args:
        user_id: Owner user ID.
        service: BudgetService instance via dependency injection.
    
    Returns:
        list[BudgetResponse]: User's budgets.
    
    Raises:
        HTTPException: 404 if user not found.
    """
    try:
        budgets = service.list_budgets_by_user(user_id)
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
    service: BudgetService = Depends(get_budget_service)
):
    """Retrieve a budget by ID.
    
    Args:
        budget_id: Budget ID to retrieve.
        service: BudgetService instance via dependency injection.
    
    Returns:
        BudgetResponse: Found budget.
    
    Raises:
        HTTPException: 404 if budget not found.
    """
    try:
        budget = service.get_budget(budget_id)
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
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{budget_id}", status_code=204)
def delete_budget(
    budget_id: int,
    service: BudgetService = Depends(get_budget_service)
):
    """Delete a budget by ID.
    
    Args:
        budget_id: Budget ID to delete.
        service: BudgetService instance via dependency injection.
    
    Returns:
        None (HTTP 204 No Content).
    
    Raises:
        HTTPException: 404 if budget not found.
    """
    try:
        service.delete_budget(budget_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
