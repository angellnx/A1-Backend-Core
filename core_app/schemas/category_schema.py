"""Pydantic models defining the API contract for category operations.

Separates request and response schemas to allow different input/output
structures and prevents exposing sensitive data.
"""
from pydantic import BaseModel


class CategoryRequest(BaseModel):
    """Validates category creation/update request from client."""
    name: str
    color: str


class CategoryResponse(BaseModel):
    """Serializes category data in API response to client."""
    name: str
    color: str