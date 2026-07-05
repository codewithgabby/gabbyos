from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate
from app.repositories.goal_repository import GoalRepository
from app.core.constants import GoalStatus
from app.core.exceptions import NotFoundException


class GoalService:
    """Service for goal operations"""
    
    def __init__(self, db: Session):
        self.goal_repo = GoalRepository(db)
    
    def create_goal(self, user_id: UUID, data: GoalCreate) -> Goal:
        """Create a new goal"""
        goal_dict = data.model_dump()
        goal_dict["user_id"] = user_id
        
        if goal_dict.get("category_id"):
            goal_dict["category_id"] = UUID(goal_dict["category_id"])
        
        goal = self.goal_repo.create(goal_dict)
        return self.goal_repo.get_with_category(goal.id)
    
    def get_goal(self, goal_id: UUID, user_id: UUID) -> Goal:
        """Get a single goal"""
        goal = self.goal_repo.get_with_category(goal_id)
        if not goal or goal.user_id != user_id:
            raise NotFoundException("Goal")
        return goal
    
    def get_all_goals(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50,
        category_id: Optional[str] = None,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Goal]:
        """Get all goals with filters"""
        category_uuid = UUID(category_id) if category_id else None
        return self.goal_repo.get_all_for_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            category_id=category_uuid,
            status=status,
            search=search
        )
    
    def get_active_goals(self, user_id: UUID) -> List[Goal]:
        """Get active goals only"""
        return self.goal_repo.get_active(user_id)
    
    def update_goal(
        self, goal_id: UUID, user_id: UUID, data: GoalUpdate
    ) -> Goal:
        """Update a goal"""
        goal = self.goal_repo.get(goal_id)
        if not goal or goal.user_id != user_id:
            raise NotFoundException("Goal")
        
        update_dict = data.model_dump(exclude_unset=True)
        
        if "category_id" in update_dict and update_dict["category_id"]:
            update_dict["category_id"] = UUID(update_dict["category_id"])
        
        goal = self.goal_repo.update(goal, update_dict)
        return self.goal_repo.get_with_category(goal.id)
    
    def delete_goal(self, goal_id: UUID, user_id: UUID) -> None:
        """Delete a goal"""
        goal = self.goal_repo.get(goal_id)
        if not goal or goal.user_id != user_id:
            raise NotFoundException("Goal")
        self.goal_repo.soft_delete(goal.id)