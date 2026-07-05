from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.repositories.category_repository import CategoryRepository
from app.core.exceptions import NotFoundException, AlreadyExistsException


class CategoryService:
    """Service for category operations"""
    
    def __init__(self, db: Session):
        self.category_repo = CategoryRepository(db)
    
    def create_category(self, user_id: UUID, data: CategoryCreate) -> Category:
        """Create a new category"""
        # Check for duplicate name
        existing = self.category_repo.get_by_name(user_id, data.name)
        if existing:
            raise AlreadyExistsException(f"Category '{data.name}'")
        
        category_dict = data.model_dump()
        category_dict["user_id"] = user_id
        
        return self.category_repo.create(category_dict)
    
    def get_category(self, category_id: UUID, user_id: UUID) -> Category:
        """Get a single category"""
        category = self.category_repo.get(category_id)
        if not category or category.user_id != user_id:
            raise NotFoundException("Category")
        return category
    
    def get_all_categories(
        self, 
        user_id: UUID, 
        skip: int = 0, 
        limit: int = 100,
        search: str = None
    ) -> List[Category]:
        """Get all categories for user"""
        return self.category_repo.get_all_for_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            search=search
        )
    
    def update_category(
        self, 
        category_id: UUID, 
        user_id: UUID, 
        data: CategoryUpdate
    ) -> Category:
        """Update a category"""
        category = self.get_category(category_id, user_id)
        
        # If name is being changed, check for duplicates
        if data.name and data.name != category.name:
            existing = self.category_repo.get_by_name(user_id, data.name)
            if existing:
                raise AlreadyExistsException(f"Category '{data.name}'")
        
        update_dict = data.model_dump(exclude_unset=True)
        return self.category_repo.update(category, update_dict)
    
    def delete_category(self, category_id: UUID, user_id: UUID) -> None:
        """Delete a category"""
        category = self.get_category(category_id, user_id)
        self.category_repo.soft_delete(category.id)