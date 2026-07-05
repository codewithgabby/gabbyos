from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from app.models.goal import Goal
from app.models.category import Category
from app.repositories.base_repository import BaseRepository
from app.core.constants import GoalStatus


class GoalRepository(BaseRepository[Goal]):
    """Repository for Goal model operations"""
    
    def __init__(self, db: Session):
        super().__init__(Goal, db)
    
    def get_with_category(self, goal_id: UUID) -> Optional[Goal]:
        """Get a goal with category loaded"""
        return self.db.query(Goal).options(
            joinedload(Goal.category)
        ).filter(
            Goal.id == goal_id,
            Goal.is_deleted == False
        ).first()
    
    def get_all_for_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50,
        category_id: Optional[UUID] = None,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Goal]:
        """Get all goals with filters"""
        query = self.db.query(Goal).options(
            joinedload(Goal.category)
        ).filter(
            Goal.user_id == user_id,
            Goal.is_deleted == False
        )
        
        if category_id:
            query = query.filter(Goal.category_id == category_id)
        
        if status:
            query = query.filter(Goal.status == status)
        
        if search:
            query = query.filter(Goal.title.ilike(f"%{search}%"))
        
        return query.order_by(Goal.deadline.asc().nullslast(), Goal.created_at.desc()).offset(skip).limit(limit).all()
    
    

    def get_active(self, user_id: UUID) -> List[Goal]:
        """Get active goals (not completed or abandoned)"""
        return self.db.query(Goal).options(
            joinedload(Goal.category)
        ).filter(
            Goal.user_id == user_id,
            Goal.is_deleted == False,
            Goal.status.in_([GoalStatus.NOT_STARTED, GoalStatus.IN_PROGRESS])
        ).order_by(Goal.deadline.asc().nullslast()).all()