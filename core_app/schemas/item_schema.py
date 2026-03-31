"""Pydantic models defining the API contract for item operations.

Items are transaction line items that belong to categories and provide
granularity beyond category-level spending organization.
"""
from pydantic import BaseModel


class ItemRequest(BaseModel):
    """Validates item creation request from client."""
    name: str
    category_name: str


class ItemResponse(BaseModel):
    """Serializes item data in API response to client."""
    id: int
    name: str
    category_name: str