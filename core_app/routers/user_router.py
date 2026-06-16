"""HTTP API endpoints for managing users.

Exposes CRUD operations for user accounts as REST endpoints.
User management includes authentication credential handling.
"""
from fastapi import APIRouter, Depends, HTTPException
from core_app.services.user_service import UserService
from core_app.schemas.user_schema import UserRequest, UserResponse
from core_app.dependencies import get_user_service, get_current_user
from core_app.domain.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    body: UserRequest,
    service: UserService = Depends(get_user_service)
):
    try:
        return service.create_user(
            email=body.email,
            name=body.name,
            username=body.username,
            password=body.password,
            phone=body.phone
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[UserResponse])
def list_users(
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    try:
        return service.list_users()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    try:
        return service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}", status_code=204)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    try:
        service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
