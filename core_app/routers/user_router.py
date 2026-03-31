"""HTTP API endpoints for managing users.

Exposes CRUD operations for user accounts as REST endpoints.
User management includes authentication credential handling.
"""
from fastapi import APIRouter, Depends, HTTPException
from core_app.services.user_service import UserService
from core_app.schemas.user_schema import UserRequest, UserResponse
from core_app.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    body: UserRequest,
    service: UserService = Depends(get_user_service)
):
    """Create a new user.
    
    Args:
        body: Request with email, name, username, password, and optional phone.
        service: UserService instance via dependency injection.
    
    Returns:
        UserResponse: Created user (HTTP 201).
    
    Raises:
        HTTPException: 400 if validation fails.
    """
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
def list_users(service: UserService = Depends(get_user_service)):
    """List all users.
    
    Args:
        service: UserService instance via dependency injection.
    
    Returns:
        list[UserResponse]: All users.
    """
    return service.list_users()

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    """Retrieve a user by ID.
    
    Args:
        user_id: User ID to retrieve.
        service: UserService instance via dependency injection.
    
    Returns:
        UserResponse: Found user.
    
    Raises:
        HTTPException: 404 if user not found.
    """
    try:
        return service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    """Delete a user by ID.
    
    Args:
        user_id: User ID to delete.
        service: UserService instance via dependency injection.
    
    Returns:
        None (HTTP 204 No Content).
    
    Raises:
        HTTPException: 404 if user not found.
    """
    try:
        service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    