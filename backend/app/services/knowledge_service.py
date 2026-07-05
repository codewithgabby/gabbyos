from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.knowledge_item import KnowledgeItem
from app.schemas.knowledge import KnowledgeItemCreate, KnowledgeItemUpdate
from app.repositories.knowledge_repository import KnowledgeRepository
from app.core.constants import KnowledgeStatus
from app.core.exceptions import NotFoundException


class KnowledgeService:
    """Service for knowledge workspace operations"""
    
    def __init__(self, db: Session):
        self.knowledge_repo = KnowledgeRepository(db)
    
    def create_item(self, user_id: UUID, data: KnowledgeItemCreate) -> KnowledgeItem:
        """Create a new knowledge item"""
        item_dict = data.model_dump()
        item_dict["user_id"] = user_id
        
        if item_dict.get("category_id"):
            item_dict["category_id"] = UUID(item_dict["category_id"])
        
        item = self.knowledge_repo.create(item_dict)
        return self.knowledge_repo.get_with_category(item.id)
    
    def get_item(self, item_id: UUID, user_id: UUID) -> KnowledgeItem:
        """Get a single knowledge item"""
        item = self.knowledge_repo.get_with_category(item_id)
        if not item or item.user_id != user_id:
            raise NotFoundException("Knowledge item")
        return item
    
    def get_all_items(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50,
        category_id: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None,
        priority: Optional[str] = None
    ) -> List[KnowledgeItem]:
        """Get all knowledge items with filters"""
        category_uuid = UUID(category_id) if category_id else None
        return self.knowledge_repo.get_all_for_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            category_id=category_uuid,
            status=status,
            search=search,
            priority=priority
        )
    
    def update_item(
        self, item_id: UUID, user_id: UUID, data: KnowledgeItemUpdate
    ) -> KnowledgeItem:
        """Update a knowledge item"""
        item = self.knowledge_repo.get(item_id)
        if not item or item.user_id != user_id:
            raise NotFoundException("Knowledge item")
        
        update_dict = data.model_dump(exclude_unset=True)
        
        if "category_id" in update_dict and update_dict["category_id"]:
            update_dict["category_id"] = UUID(update_dict["category_id"])
        
        item = self.knowledge_repo.update(item, update_dict)
        return self.knowledge_repo.get_with_category(item.id)
    
    def delete_item(self, item_id: UUID, user_id: UUID) -> None:
        """Delete a knowledge item"""
        item = self.knowledge_repo.get(item_id)
        if not item or item.user_id != user_id:
            raise NotFoundException("Knowledge item")
        self.knowledge_repo.soft_delete(item.id)
    
    def update_progress(
        self, item_id: UUID, user_id: UUID, progress: float
    ) -> KnowledgeItem:
        """Update progress percentage"""
        item = self.knowledge_repo.get(item_id)
        if not item or item.user_id != user_id:
            raise NotFoundException("Knowledge item")
        
        item = self.knowledge_repo.update(item, {"progress_percentage": progress})
        return self.knowledge_repo.get_with_category(item.id)
    
    def archive_item(self, item_id: UUID, user_id: UUID) -> KnowledgeItem:
        """Archive a knowledge item"""
        item = self.knowledge_repo.get(item_id)
        if not item or item.user_id != user_id:
            raise NotFoundException("Knowledge item")
        return self.knowledge_repo.archive_item(item)