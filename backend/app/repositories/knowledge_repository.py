from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from app.models.knowledge_item import KnowledgeItem
from app.models.category import Category
from app.repositories.base_repository import BaseRepository


class KnowledgeRepository(BaseRepository[KnowledgeItem]):
    """Repository for KnowledgeItem model operations"""
    
    def __init__(self, db: Session):
        super().__init__(KnowledgeItem, db)
    
    def get_with_category(self, item_id: UUID) -> Optional[KnowledgeItem]:
        """Get a knowledge item with category loaded"""
        return self.db.query(KnowledgeItem).options(
            joinedload(KnowledgeItem.category)
        ).filter(
            KnowledgeItem.id == item_id,
            KnowledgeItem.is_deleted == False
        ).first()
    
    def get_all_for_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50,
        category_id: Optional[UUID] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[KnowledgeItem]:
        """Get all knowledge items with filters"""
        query = self.db.query(KnowledgeItem).options(
            joinedload(KnowledgeItem.category)
        ).filter(
            KnowledgeItem.user_id == user_id,
            KnowledgeItem.is_deleted == False
        )
        
        if category_id:
            query = query.filter(KnowledgeItem.category_id == category_id)
        
        if status:
            query = query.filter(KnowledgeItem.status == status)
        
        if search:
            query = query.filter(
                KnowledgeItem.title.ilike(f"%{search}%") |
                KnowledgeItem.description.ilike(f"%{search}%") |
                KnowledgeItem.notes.ilike(f"%{search}%")
            )
        
        if priority:
            query = query.filter(KnowledgeItem.priority == priority)
        
        return query.order_by(
            KnowledgeItem.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    def archive_item(self, item: KnowledgeItem) -> KnowledgeItem:
        """Archive a knowledge item"""
        item.status = "archived"
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def count_by_status(self, user_id: UUID, status: str) -> int:
        """Count items by status"""
        return self.db.query(KnowledgeItem).filter(
            KnowledgeItem.user_id == user_id,
            KnowledgeItem.status == status,
            KnowledgeItem.is_deleted == False
        ).count()