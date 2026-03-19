from fastapi import APIRouter, Depends, HTTPException
from core_app.services.item_type_service import ItemTypeService
from core_app.schemas.item_type_schema import ItemTypeRequest, ItemTypeResponse
from core_app.dependencies import get_item_type_service

router = APIRouter(prefix="/item-types", tags=["Item Types"])

@router.post("/", response_model=ItemTypeResponse, status_code=201)
def create_item_type(
    body: ItemTypeRequest,
    service: ItemTypeService = Depends(get_item_type_service)
):
    try:
        return service.create_item_type(name=body.name, color=body.color)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ItemTypeResponse])
def list_item_types(service: ItemTypeService = Depends(get_item_type_service)):
    return service.list_item_types()

@router.get("/{name}", response_model=ItemTypeResponse)
def get_item_type(name: str, service: ItemTypeService = Depends(get_item_type_service)):
    try:
        return service.get_item_type(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{name}", status_code=204)
def delete_item_type(name: str, service: ItemTypeService = Depends(get_item_type_service)):
    try:
        service.delete_item_type(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    