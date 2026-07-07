from typing import List, Optional
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session
from app.models.reflection import Reflection
from app.schemas.reflection import ReflectionCreate, ReflectionUpdate
from app.repositories.reflection_repository import ReflectionRepository
from app.core.exceptions import NotFoundException, AlreadyExistsException


class ReflectionService:
    """Service for reflection operations"""
    
    def __init__(self, db: Session):
        self.reflection_repo = ReflectionRepository(db)
    
    def create_reflection(self, user_id: UUID, data: ReflectionCreate) -> Reflection:
        """Create a new reflection"""
        existing = self.reflection_repo.get_by_date(user_id, data.reflection_date)
        if existing:
            raise AlreadyExistsException(
                f"Reflection for {data.reflection_date}"
            )
        
        reflection_dict = data.model_dump()
        reflection_dict["user_id"] = user_id
        
        return self.reflection_repo.create(reflection_dict)
    
    def get_reflection(self, reflection_id: UUID, user_id: UUID) -> Reflection:
        """Get a single reflection"""
        reflection = self.reflection_repo.get(reflection_id)
        if not reflection or reflection.user_id != user_id:
            raise NotFoundException("Reflection")
        return reflection
    
    def get_reflection_by_date(self, user_id: UUID, reflection_date: date) -> Optional[Reflection]:
        """Get reflection for a specific date"""
        return self.reflection_repo.get_by_date(user_id, reflection_date)
    
    def get_all_reflections(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 30,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Reflection]:
        """Get all reflections with filters"""
        return self.reflection_repo.get_all_for_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            start_date=start_date,
            end_date=end_date
        )
    
    def get_recent_reflections(self, user_id: UUID, limit: int = 7) -> List[Reflection]:
        """Get recent reflections"""
        return self.reflection_repo.get_recent(user_id, limit)
    
    def update_reflection(
        self, reflection_id: UUID, user_id: UUID, data: ReflectionUpdate
    ) -> Reflection:
        """Update a reflection"""
        reflection = self.reflection_repo.get(reflection_id)
        if not reflection or reflection.user_id != user_id:
            raise NotFoundException("Reflection")
        
        update_dict = data.model_dump(exclude_unset=True)
        return self.reflection_repo.update(reflection, update_dict)
    
    def delete_reflection(self, reflection_id: UUID, user_id: UUID) -> None:
        """Delete a reflection"""
        reflection = self.reflection_repo.get(reflection_id)
        if not reflection or reflection.user_id != user_id:
            raise NotFoundException("Reflection")
        self.reflection_repo.soft_delete(reflection.id)
    
    def get_or_create_today(self, user_id: UUID) -> Reflection:
        """Get today's reflection or create empty one"""
        today = date.today()
        
        # First check for active reflection
        reflection = self.reflection_repo.get_by_date(user_id, today)
        if reflection:
            return reflection
        
        # Check if a soft-deleted one exists
        try:
            existing = self.reflection_repo.db.query(Reflection).filter(
                Reflection.user_id == user_id,
                Reflection.reflection_date == today
            ).first()
            
            if existing:
                # Restore it
                existing.is_deleted = False
                existing.deleted_at = None
                existing.wins = None
                existing.challenges = None
                existing.gratitude = None
                existing.tomorrow_focus = None
                existing.mood_rating = None
                self.reflection_repo.db.commit()
                self.reflection_repo.db.refresh(existing)
                return existing
        except:
            pass
        
        # Create new one
        try:
            reflection_dict = {
                "user_id": user_id,
                "reflection_date": today
            }
            reflection = self.reflection_repo.create(reflection_dict)
            return reflection
        except Exception as e:
            # If duplicate, try fetching one more time
            self.reflection_repo.db.rollback()
            reflection = self.reflection_repo.get_by_date(user_id, today)
            if reflection:
                return reflection
            raise e