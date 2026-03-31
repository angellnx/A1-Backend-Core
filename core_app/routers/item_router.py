"""HTTP API endpoints for managing items.

Exposes CRUD operations for transaction line items as REST endpoints.
Items belong to categories and are used as transaction details.
"""
from fastapi import APIRouter, Depends, HTTPException
from core_app.services.item_service import ItemService
from core_app.schemas.item_schema import ItemRequest, ItemResponse
from core_app.dependencies import get_item_service

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(
    body: ItemRequest,
    service: ItemService = Depends(get_item_service)
):
    """Create a new item.
    
    Args:
        body: Request with name and category_name.
        service: ItemService instance via dependency injection.
    
    Returns:
        ItemResponse: Created item (HTTP 201).
    
    Raises:
        HTTPException: 400 if validation fails or category not found.
    """
    try:
        item = service.create_item(name=body.name, category_name=body.category_name)
        return ItemResponse(
            id=item.id,
            name=item.name,
            category_name=item.category.name
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ItemResponse])
def list_items(service: ItemService = Depends(get_item_service)):
    """List all items.
    
    Args:
        service: ItemService instance via dependency injection.
    
    Returns:
        list[ItemResponse]: All items.
    """
    return [
        ItemResponse(id=i.id, name=i.name, category_name=i.category.name)
        for i in service.list_items()
    ]

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, service: ItemService = Depends(get_item_service)):
    """Retrieve an item by ID.
    
    Args:
        item_id: Item ID to retrieve.
        service: ItemService instance via dependency injection.
    
    Returns:
        ItemResponse: Found item.
    
    Raises:
        HTTPException: 404 if item not found.
    """
    try:
        item = service.get_item(item_id)
        return ItemResponse(id=item.id, name=item.name, category_name=item.category.name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, service: ItemService = Depends(get_item_service)):
    """Delete an item by ID.
    
    Args:
        item_id: Item ID to delete.
        service: ItemService instance via dependency injection.
    
    Returns:
        None (HTTP 204 No Content).
    
    Raises:
        HTTPException: 404 if item not found.
    """
    try:
        service.delete_item(item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    