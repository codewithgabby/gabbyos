from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.weekly_plan import WeeklyPlan, WeeklyPlanItem
from app.schemas.weekly_plan import (
    WeeklyPlanCreate,
    WeeklyPlanUpdate,
    AddPlanItemRequest
)
from app.repositories.weekly_plan_repository import (
    WeeklyPlanRepository,
    WeeklyPlanItemRepository
)
from app.core.exceptions import NotFoundException, AlreadyExistsException


class WeeklyPlannerService:
    """Service for weekly planner operations"""
    
    def __init__(self, db: Session):
        self.plan_repo = WeeklyPlanRepository(db)
        self.item_repo = WeeklyPlanItemRepository(db)
    
    def create_plan(self, user_id: UUID, data: WeeklyPlanCreate) -> WeeklyPlan:
        """Create a new weekly plan with items"""
        # Check if plan already exists for this week
        existing = self.plan_repo.get_by_week(
            user_id, data.year, data.week_number
        )
        if existing:
            raise AlreadyExistsException(
                f"Weekly plan for Week {data.week_number}, {data.year}"
            )
        
        # Create the plan
        plan_dict = {
            "user_id": user_id,
            "week_start_date": data.week_start_date,
            "week_end_date": data.week_end_date,
            "year": data.year,
            "week_number": data.week_number,
            "notes": data.notes
        }
        
        plan = self.plan_repo.create(plan_dict)
        
        # Add items if provided
        for item_data in data.items:
            self._add_item(plan.id, item_data.routine_id, item_data)
        
        return self.plan_repo.get_with_items(plan.id)
    
    def get_plan(self, plan_id: UUID, user_id: UUID) -> WeeklyPlan:
        """Get a weekly plan with all items"""
        plan = self.plan_repo.get_with_items(plan_id)
        if not plan or plan.user_id != user_id:
            raise NotFoundException("Weekly plan")
        return plan
    
    def get_plan_by_week(
        self, user_id: UUID, year: int, week_number: int
    ) -> Optional[WeeklyPlan]:
        """Get a plan for a specific week"""
        return self.plan_repo.get_by_week(user_id, year, week_number)
    
    def get_all_plans(
        self, user_id: UUID, skip: int = 0, limit: int = 50
    ) -> List[WeeklyPlan]:
        """Get all weekly plans for user"""
        return self.plan_repo.get_all_for_user(user_id, skip, limit)
    
    def update_plan(
        self, plan_id: UUID, user_id: UUID, data: WeeklyPlanUpdate
    ) -> WeeklyPlan:
        """Update a weekly plan"""
        plan = self.plan_repo.get(plan_id)
        if not plan or plan.user_id != user_id:
            raise NotFoundException("Weekly plan")
        
        update_dict = data.model_dump(exclude_unset=True)
        return self.plan_repo.update(plan, update_dict)
    
    def delete_plan(self, plan_id: UUID, user_id: UUID) -> None:
        """Delete a weekly plan and all its items"""
        plan = self.plan_repo.get(plan_id)
        if not plan or plan.user_id != user_id:
            raise NotFoundException("Weekly plan")
        self.plan_repo.soft_delete(plan.id)
    
    def add_item(
        self, plan_id: UUID, user_id: UUID, data: AddPlanItemRequest
    ) -> WeeklyPlanItem:
        """Add a routine to a specific day in the plan"""
        plan = self.plan_repo.get(plan_id)
        if not plan or plan.user_id != user_id:
            raise NotFoundException("Weekly plan")
        
        # Check for duplicate
        existing = self.item_repo.get_by_plan_and_routine(
            plan_id, UUID(data.routine_id), data.day_of_week.value
        )
        if existing:
            raise AlreadyExistsException(
                "Routine already assigned to this day"
            )
        
        return self._add_item(plan_id, data.routine_id, data)
    
    def remove_item(
        self, plan_id: UUID, item_id: UUID, user_id: UUID
    ) -> None:
        """Remove an item from a plan"""
        plan = self.plan_repo.get(plan_id)
        if not plan or plan.user_id != user_id:
            raise NotFoundException("Weekly plan")
        
        item = self.item_repo.get(item_id)
        if not item or item.plan_id != plan_id:
            raise NotFoundException("Plan item")
        
        self.item_repo.soft_delete(item.id)
    
    def _add_item(
        self, plan_id: UUID, routine_id: str, data
    ) -> WeeklyPlanItem:
        """Internal method to add an item"""
        # Get day_of_week value whether it's an enum or string
        if hasattr(data, 'day_of_week'):
            day = data.day_of_week
            if hasattr(day, 'value'):
                day = day.value
        else:
            day = data
        
        item_dict = {
            "plan_id": plan_id,
            "routine_id": UUID(routine_id) if isinstance(routine_id, str) else routine_id,
            "day_of_week": day,
            "custom_time": getattr(data, 'custom_time', None),
            "sort_order": getattr(data, 'sort_order', 0)
        }
        return self.item_repo.create(item_dict)