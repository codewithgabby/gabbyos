from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from app.models.routine import Routine
from app.repositories.base_repository import BaseRepository


class RoutineRepository(BaseRepository[Routine]):
    """Repository for Routine model operations"""
    
    def __init__(self, db: Session):
        super().__init__(Routine, db)
    
    def get_with_category(self, routine_id: UUID) -> Optional[Routine]:
        """Get a routine with its category loaded"""
        return self.db.query(Routine).options(
            joinedload(Routine.category)
        ).filter(
            Routine.id == routine_id,
            Routine.is_deleted == False
        ).first()
    
    def get_all_for_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[UUID] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[Routine]:
        """Get all routines for a user with optional filters"""
        query = self.db.query(Routine).options(
            joinedload(Routine.category)
        ).filter(
            Routine.user_id == user_id,
            Routine.is_deleted == False
        )
        
        if category_id:
            query = query.filter(Routine.category_id == category_id)
        
        if is_active is not None:
            query = query.filter(Routine.is_active == is_active)
        
        if search:
            query = query.filter(
                Routine.title.ilike(f"%{search}%")
            )
        
        return query.order_by(
            Routine.sort_order,
            Routine.created_at
        ).offset(skip).limit(limit).all()
    
    def get_by_title(self, user_id: UUID, title: str) -> Optional[Routine]:
        """Check if routine with same title exists for user"""
        return self.db.query(Routine).filter(
            Routine.user_id == user_id,
            Routine.title == title,
            Routine.is_deleted == False
        ).first()
    
    def toggle_active(self, routine: Routine) -> Routine:
        """Toggle routine active status"""
        routine.is_active = not routine.is_active
        self.db.commit()
        self.db.refresh(routine)
        return routine
    
    def count_for_user(
        self,
        user_id: UUID,
        category_id: Optional[UUID] = None
    ) -> int:
        """Count routines for a user"""
        query = self.db.query(Routine).filter(
            Routine.user_id == user_id,
            Routine.is_deleted == False
        )
        
        if category_id:
            query = query.filter(Routine.category_id == category_id)
        
        return query.count()