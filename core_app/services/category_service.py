"""Business logic service for managing Categories.

Coordinates category operations by validating inputs, delegating to
the repository for persistence, and enforcing business rules.
"""
from core_app.domain.models.category import Category
from core_app.repositories.category_repository import CategoryRepository

class CategoryService:
    """Orchestrates category business logic and repository coordination.
    
    Responsibilities:
    - Validate category inputs (name and color required)
    - Prevent duplicate category names
    - Coordinate between routers and repository layer
    """
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def create_category(self, name: str, color: str) -> Category:
        """Create a new category with validation.
        
        Args:
            name: Category name (required).
            color: Hex color code (required).
            
        Returns:
            Category: The created domain model.
            
        Raises:
            ValueError: If name or color missing, or category already exists.
        """
        if not name:
            raise ValueError("Name is required.")
        if not color:
            raise ValueError("Color is required.")
        
        existing = self.repository.find_by_name(name)
        if existing:
            raise ValueError(f"Category '{name}' already exists.")
        
        category = Category(name=name, color=color)
        return self.repository.create(category)
    
    def get_category(self, name: str) -> Category:
        """Retrieve a category by name.
        
        Args:
            name: Category name to find.
            
        Returns:
            Category: The found domain model.
            
        Raises:
            ValueError: If category not found.
        """
        category = self.repository.find_by_name(name)
        if not category:
            raise ValueError(f"Category '{name}' not found.")
        return category
    
    def list_categories(self) -> list[Category]:
        """Retrieve all categories.
        
        Returns:
            list[Category]: All available categories.
        """
        return self.repository.find_all()
    
    def delete_category(self, name: str) -> None:
        """Delete a category by name.
        
        Args:
            name: Category name to delete.
            
        Raises:
            ValueError: If category not found.
        """
        category = self.repository.find_by_name(name)
        if not category:
            raise ValueError(f"Category '{name}' not found.")
        self.repository.delete(name)
        