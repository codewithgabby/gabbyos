from typing import Optional, List
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session
from app.models.reflection import Reflection
from app.repositories.base_repository import BaseRepository


class ReflectionRepository(BaseRepository[Reflection]):
    """Repository for Reflection model operations"""
    
    def __init__(self, db: Session):
        super().__init__(Reflection, db)
    
    def get_by_date(self, user_id: UUID, reflection_date: date) -> Optional[Reflection]:
        """Get reflection for a specific date"""
        return self.db.query(Reflection).filter(
            Reflection.user_id == user_id,
            Reflection.reflection_date == reflection_date,
            Reflection.is_deleted == False
        ).first()
    
    def get_all_for_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 30,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Reflection]:
        """Get all reflections for a user with date range filter"""
        query = self.db.query(Reflection).filter(
            Reflection.user_id == user_id,
            Reflection.is_deleted == False
        )
        
        if start_date:
            query = query.filter(Reflection.reflection_date >= start_date)
        
        if end_date:
            query = query.filter(Reflection.reflection_date <= end_date)
        
        return query.order_by(
            Reflection.reflection_date.desc()
        ).offset(skip).limit(limit).all()
    
    def get_recent(self, user_id: UUID, limit: int = 7) -> List[Reflection]:
        """Get most recent reflections"""
        return self.db.query(Reflection).filter(
            Reflection.user_id == user_id,
            Reflection.is_deleted == False
        ).order_by(
            Reflection.reflection_date.desc()
        ).limit(limit).all()