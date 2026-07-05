from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.category import Category
from app.repositories.base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Repository for Category model operations"""
    
    def __init__(self, db: Session):
        super().__init__(Category, db)
    
    def get_by_name(self, user_id: UUID, name: str) -> Optional[Category]:
        """Check if category with same name exists for user"""
        return self.db.query(Category).filter(
            Category.user_id == user_id,
            Category.name == name,
            Category.is_deleted == False
        ).first()
    
    def get_all_for_user(
        self, 
        user_id: UUID, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None
    ) -> List[Category]:
        """Get all categories for a user with optional search"""
        query = self.db.query(Category).filter(
            Category.user_id == user_id,
            Category.is_deleted == False
        )
        
        if search:
            query = query.filter(Category.name.ilike(f"%{search}%"))
        
        return query.order_by(Category.name).offset(skip).limit(limit).all()
    
    def count_for_user(self, user_id: UUID) -> int:
        """Count categories for a user"""
        return self.db.query(Category).filter(
            Category.user_id == user_id,
            Category.is_deleted == False
        ).count()