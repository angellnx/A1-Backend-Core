"""HTTP API endpoints for managing categories.

Exposes CRUD operations as REST endpoints. Handles error conversion:
- ValueError from service layer → HTTPException 400 (bad request)
- ValueError for not found → HTTPException 404 (not found)
- Success returns appropriate status codes (201 for create, 204 for delete)
"""
from fastapi import APIRouter, Depends, HTTPException
from core_app.services.category_service import CategoryService
from core_app.schemas.category_schema import CategoryRequest, CategoryResponse
from core_app.dependencies import get_category_service

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    body: CategoryRequest,
    service: CategoryService = Depends(get_category_service)
):
    """Create a new category.
    
    Args:
        body: Request with name and color.
        service: CategoryService instance via dependency injection.
        
    Returns:
        CategoryResponse: Created category (HTTP 201).
        
    Raises:
        HTTPException: 400 if invalid input, 400 if duplicate name.
    """
    try:
        return service.create_category(name=body.name, color=body.color)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[CategoryResponse])
def list_categories(service: CategoryService = Depends(get_category_service)):
    """List all categories.
    
    Args:
        service: CategoryService instance via dependency injection.
        
    Returns:
        list[CategoryResponse]: All categories.
    """
    return service.list_categories()

@router.get("/{name}", response_model=CategoryResponse)
def get_category(name: str, service: CategoryService = Depends(get_category_service)):
    """Retrieve a category by name.
    
    Args:
        name: Category name to find.
        service: CategoryService instance via dependency injection.
        
    Returns:
        CategoryResponse: Found category.
        
    Raises:
        HTTPException: 404 if category not found.
    """
    try:
        return service.get_category(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{name}", status_code=204)
def delete_category(name: str, service: CategoryService = Depends(get_category_service)):
    """Delete a category by name.
    
    Args:
        name: Category name to delete.
        service: CategoryService instance via dependency injection.
        
    Returns:
        None (HTTP 204 No Content).
        
    Raises:
        HTTPException: 404 if category not found.
    """
    try:
        service.delete_category(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    