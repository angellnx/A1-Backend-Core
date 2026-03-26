from fastapi import APIRouter, Depends, HTTPException
from core_app.services.currency_service import CurrencyService
from core_app.schemas.currency_schema import CurrencyCreate, CurrencyResponse
from core_app.dependencies import get_currency_service

router = APIRouter(prefix="/currencies", tags=["Currencies"])

@router.post("/", response_model=CurrencyResponse, status_code=201)
def create_currency(
    body: CurrencyCreate,
    service: CurrencyService = Depends(get_currency_service)
):
    try:
        return service.create_currency(code=body.code, name=body.name, symbol=body.symbol)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[CurrencyResponse])
def list_currencies(service: CurrencyService = Depends(get_currency_service)):
    return service.list_currencies()

@router.get("/{code}", response_model=CurrencyResponse)
def get_currency(code: str, service: CurrencyService = Depends(get_currency_service)):
    try:
        return service.get_currency(code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{code}", status_code=204)
def delete_currency(code: str, service: CurrencyService = Depends(get_currency_service)):
    try:
        service.delete_currency(code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))