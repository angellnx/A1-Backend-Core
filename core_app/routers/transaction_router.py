from fastapi import APIRouter, Depends, HTTPException
from core_app.services.transaction_service import TransactionService
from core_app.schemas.transaction_schema import TransactionRequest, TransactionResponse
from core_app.dependencies import get_transaction_service

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(
    body: TransactionRequest,
    service: TransactionService = Depends(get_transaction_service)
):
    try:
        transaction = service.create_transaction(
            user_id=body.user_id,
            item_id=body.item_id,
            transaction_type_name=body.transaction_type_name,
            value=body.value,
            date=body.date,
            notes=body.notes
        )
        return TransactionResponse(
            id=transaction.id,
            date=transaction.date,
            value=transaction.value,
            transaction_type_name=transaction.transaction_type.name,
            user_id=transaction.user_id,
            item_id=transaction.item_id,
            notes=transaction.notes
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[TransactionResponse])
def list_transactions(service: TransactionService = Depends(get_transaction_service)):
    return [
        TransactionResponse(
            id=t.id,
            date=t.date,
            value=t.value,
            transaction_type_name=t.transaction_type.name,
            user_id=t.user_id,
            item_id=t.item_id,
            notes=t.notes
        )
        for t in service.list_transactions()
    ]

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, service: TransactionService = Depends(get_transaction_service)):
    try:
        t = service.get_transaction(transaction_id)
        return TransactionResponse(
            id=t.id,
            date=t.date,
            value=t.value,
            transaction_type_name=t.transaction_type.name,
            user_id=t.user_id,
            item_id=t.item_id,
            notes=t.notes
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(transaction_id: int, service: TransactionService = Depends(get_transaction_service)):
    try:
        service.delete_transaction(transaction_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    