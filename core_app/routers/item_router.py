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
    try:
        item = service.create_item(name=body.name, item_type_name=body.item_type_name)
        return ItemResponse(
            id=item.id,
            name=item.name,
            item_type_name=item.item_type.name
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ItemResponse])
def list_items(service: ItemService = Depends(get_item_service)):
    return [
        ItemResponse(id=i.id, name=i.name, item_type_name=i.item_type.name)
        for i in service.list_items()
    ]

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, service: ItemService = Depends(get_item_service)):
    try:
        item = service.get_item(item_id)
        return ItemResponse(id=item.id, name=item.name, item_type_name=item.item_type.name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, service: ItemService = Depends(get_item_service)):
    try:
        service.delete_item(item_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    