"""Pydantic models defining the API contract for user operations.

User request schema accepts password for registration/updates.
User response schema intentionally excludes password for security.
"""
from pydantic import BaseModel, EmailStr

class UserRequest(BaseModel):
    """Validates user creation/update request from client.
    
    Password is accepted here but never stored or returned in responses.
    """
    email: EmailStr
    name: str
    username: str
    password: str
    phone: str | None = None

class UserResponse(BaseModel):
    """Serializes user data in API response to client.
    
    Password is intentionally excluded for security.
    """
    id: int
    email: str
    name: str
    username: str
    phone: str | None = None