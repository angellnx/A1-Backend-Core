"""HTTP API endpoints for authentication.

Handles user registration and login, returning JWT access tokens.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core_app.database.session import get_session
from core_app.repositories.user_repository import UserRepository
from core_app.services.user_service import UserService
from core_app.core.security import create_access_token
from core_app.schemas.user_schema import UserRequest, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(
    body: UserRequest,
    session: Session = Depends(get_session)
):
    """Register a new user.

    Args:
        body: Request with email, name, username, password, and optional phone.
        session: Database session via dependency injection.

    Returns:
        UserResponse: Created user (HTTP 201).

    Raises:
        HTTPException: 400 if validation fails or username/email already exists.
    """
    service = UserService(UserRepository(session))
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


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """Authenticate a user and return a JWT access token.

    Args:
        form_data: OAuth2 form with username and password fields.
        session: Database session via dependency injection.

    Returns:
        dict: Access token and token type.

    Raises:
        HTTPException: 401 if credentials are invalid.
    """
    repo = UserRepository(session)
    user = repo.get_by_username(form_data.username)

    if not user or not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}