from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from app.models.weekly_plan import WeeklyPlan, WeeklyPlanItem
from app.models.routine import Routine
from app.models.category import Category
from app.repositories.base_repository import BaseRepository


class WeeklyPlanRepository(BaseRepository[WeeklyPlan]):
    """Repository for WeeklyPlan model operations"""
    
    def __init__(self, db: Session):
        super().__init__(WeeklyPlan, db)
    
    def get_with_items(self, plan_id: UUID) -> Optional[WeeklyPlan]:
        """Get a weekly plan with all items and routines loaded"""
        return self.db.query(WeeklyPlan).options(
            joinedload(WeeklyPlan.items)
            .joinedload(WeeklyPlanItem.routine)
            .joinedload(Routine.category)
        ).filter(
            WeeklyPlan.id == plan_id,
            WeeklyPlan.is_deleted == False
        ).first()
    
    def get_by_week(
        self, 
        user_id: UUID, 
        year: int, 
        week_number: int
    ) -> Optional[WeeklyPlan]:
        """Get a plan for a specific week"""
        return self.db.query(WeeklyPlan).options(
            joinedload(WeeklyPlan.items)
            .joinedload(WeeklyPlanItem.routine)
        ).filter(
            WeeklyPlan.user_id == user_id,
            WeeklyPlan.year == year,
            WeeklyPlan.week_number == week_number,
            WeeklyPlan.is_deleted == False
        ).first()
    
    def get_all_for_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50
    ) -> List[WeeklyPlan]:
        """Get all weekly plans for a user"""
        return self.db.query(WeeklyPlan).options(
            joinedload(WeeklyPlan.items)
            .joinedload(WeeklyPlanItem.routine)
        ).filter(
            WeeklyPlan.user_id == user_id,
            WeeklyPlan.is_deleted == False
        ).order_by(
            WeeklyPlan.year.desc(),
            WeeklyPlan.week_number.desc()
        ).offset(skip).limit(limit).all()
    
    def get_items_by_day(
        self,
        plan_id: UUID,
        day_of_week: str
    ) -> List[WeeklyPlanItem]:
        """Get all items for a specific day in a plan"""
        return self.db.query(WeeklyPlanItem).options(
            joinedload(WeeklyPlanItem.routine)
            .joinedload(Routine.category)
        ).filter(
            WeeklyPlanItem.plan_id == plan_id,
            WeeklyPlanItem.day_of_week == day_of_week,
            WeeklyPlanItem.is_deleted == False
        ).order_by(WeeklyPlanItem.sort_order).all()


class WeeklyPlanItemRepository(BaseRepository[WeeklyPlanItem]):
    """Repository for WeeklyPlanItem model operations"""
    
    def __init__(self, db: Session):
        super().__init__(WeeklyPlanItem, db)
    
    def get_by_plan_and_routine(
        self,
        plan_id: UUID,
        routine_id: UUID,
        day_of_week: str
    ) -> Optional[WeeklyPlanItem]:
        """Check if routine already assigned to a day in this plan"""
        return self.db.query(WeeklyPlanItem).filter(
            WeeklyPlanItem.plan_id == plan_id,
            WeeklyPlanItem.routine_id == routine_id,
            WeeklyPlanItem.day_of_week == day_of_week,
            WeeklyPlanItem.is_deleted == False
        ).first()