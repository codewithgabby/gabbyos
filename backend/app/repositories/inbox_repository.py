from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.inbox_item import InboxItem
from app.repositories.base_repository import BaseRepository


class InboxRepository(BaseRepository[InboxItem]):
    """Repository for InboxItem model operations"""
    
    def __init__(self, db: Session):
        super().__init__(InboxItem, db)
    
    def get_all_for_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50,
        is_organized: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[InboxItem]:
        """Get all inbox items with filters"""
        query = self.db.query(InboxItem).filter(
            InboxItem.user_id == user_id,
            InboxItem.is_deleted == False
        )
        
        if is_organized is not None:
            query = query.filter(InboxItem.is_organized == is_organized)
        
        if search:
            query = query.filter(InboxItem.content.ilike(f"%{search}%"))
        
        return query.order_by(
            InboxItem.is_organized.asc(),
            InboxItem.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    def get_unorganized(self, user_id: UUID) -> List[InboxItem]:
        """Get only unorganized items"""
        return self.db.query(InboxItem).filter(
            InboxItem.user_id == user_id,
            InboxItem.is_deleted == False,
            InboxItem.is_organized == False
        ).order_by(InboxItem.created_at.desc()).all()
    
    def count_unorganized(self, user_id: UUID) -> int:
        """Count unorganized items"""
        return self.db.query(InboxItem).filter(
            InboxItem.user_id == user_id,
            InboxItem.is_deleted == False,
            InboxItem.is_organized == False
        ).count()
    
    def mark_organized(self, item: InboxItem, organized_to: str = None) -> InboxItem:
        """Mark an inbox item as organized"""
        item.is_organized = True
        if organized_to:
            item.organized_to = organized_to
        self.db.commit()
        self.db.refresh(item)
        return item