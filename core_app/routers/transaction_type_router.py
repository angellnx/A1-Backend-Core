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
    try:
        return service.create_transaction_type(name=body.name, is_positive=body.is_positive)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[TransactionTypeResponse])
def list_transaction_types(service: TransactionTypeService = Depends(get_transaction_type_service)):
    return service.list_transaction_types()

@router.get("/{name}", response_model=TransactionTypeResponse)
def get_transaction_type(name: str, service: TransactionTypeService = Depends(get_transaction_type_service)):
    try:
        return service.get_transaction_type(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{name}", status_code=204)
def delete_transaction_type(name: str, service: TransactionTypeService = Depends(get_transaction_type_service)):
    try:
        service.delete_transaction_type(name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    