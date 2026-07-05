from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.inbox_item import InboxItem
from app.schemas.inbox import InboxItemCreate, InboxItemUpdate
from app.repositories.inbox_repository import InboxRepository
from app.core.exceptions import NotFoundException


class InboxService:
    """Service for inbox operations"""
    
    def __init__(self, db: Session):
        self.inbox_repo = InboxRepository(db)
    
    def create_item(self, user_id: UUID, data: InboxItemCreate) -> InboxItem:
        """Quick capture an idea"""
        item_dict = data.model_dump()
        item_dict["user_id"] = user_id
        return self.inbox_repo.create(item_dict)
    
    def get_item(self, item_id: UUID, user_id: UUID) -> InboxItem:
        """Get a single inbox item"""
        item = self.inbox_repo.get(item_id)
        if not item or item.user_id != user_id:
            raise NotFoundException("Inbox item")
        return item
    
    def get_all_items(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50,
        is_organized: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[InboxItem]:
        """Get all inbox items with filters"""
        return self.inbox_repo.get_all_for_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            is_organized=is_organized,
            search=search
        )
    
    def get_unorganized(self, user_id: UUID) -> List[InboxItem]:
        """Get items that need organizing"""
        return self.inbox_repo.get_unorganized(user_id)
    
    def update_item(
        self, item_id: UUID, user_id: UUID, data: InboxItemUpdate
    ) -> InboxItem:
        """Update an inbox item"""
        item = self.inbox_repo.get(item_id)
        if not item or item.user_id != user_id:
            raise NotFoundException("Inbox item")
        
        update_dict = data.model_dump(exclude_unset=True)
        return self.inbox_repo.update(item, update_dict)
    
    def delete_item(self, item_id: UUID, user_id: UUID) -> None:
        """Delete an inbox item"""
        item = self.inbox_repo.get(item_id)
        if not item or item.user_id != user_id:
            raise NotFoundException("Inbox item")
        self.inbox_repo.soft_delete(item.id)
    
    def mark_organized(
        self, item_id: UUID, user_id: UUID, organized_to: str = None
    ) -> InboxItem:
        """Mark item as organized"""
        item = self.inbox_repo.get(item_id)
        if not item or item.user_id != user_id:
            raise NotFoundException("Inbox item")
        return self.inbox_repo.mark_organized(item, organized_to)
    
    def get_stats(self, user_id: UUID) -> dict:
        """Get inbox statistics"""
        all_items = self.inbox_repo.get_all_for_user(user_id)
        unorganized = self.inbox_repo.count_unorganized(user_id)
        
        return {
            "total": len(all_items),
            "unorganized": unorganized,
            "organized": len(all_items) - unorganized
        }