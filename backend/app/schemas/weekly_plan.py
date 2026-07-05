from pydantic import Field, model_validator
from typing import Optional
from datetime import date, datetime
from app.schemas.common import BaseResponse, BaseSchema
from app.core.constants import DayOfWeek


class PlanItemBase(BaseSchema):
    """Base schema for plan items"""
    routine_id: str
    day_of_week: DayOfWeek
    custom_time: Optional[str] = Field(None, max_length=10)
    sort_order: int = 0


class PlanItemCreate(PlanItemBase):
    """Schema for creating a plan item"""
    pass


class PlanItemResponse(BaseResponse):
    """Schema for plan item responses"""
    plan_id: str
    routine_id: str
    routine_title: Optional[str] = None
    routine_duration: Optional[int] = None
    category_name: Optional[str] = None
    day_of_week: DayOfWeek
    custom_time: Optional[str] = None
    sort_order: int
    created_at: datetime


class WeeklyPlanBase(BaseSchema):
    """Base schema for weekly plans"""
    week_start_date: date
    week_end_date: date
    year: int
    week_number: int
    notes: Optional[str] = Field(None, max_length=1000)


class WeeklyPlanCreate(WeeklyPlanBase):
    """Schema for creating a weekly plan"""
    items: list[PlanItemCreate] = []


class WeeklyPlanUpdate(BaseSchema):
    """Schema for updating a weekly plan"""
    notes: Optional[str] = Field(None, max_length=1000)


class WeeklyPlanResponse(BaseResponse):
    """Schema for weekly plan responses"""
    user_id: str
    week_start_date: date
    week_end_date: date
    year: int
    week_number: int
    notes: Optional[str] = None
    items: list[PlanItemResponse] = []
    created_at: datetime
    updated_at: datetime


class AddPlanItemRequest(BaseSchema):
    """Schema for adding an item to existing plan"""
    routine_id: str
    day_of_week: DayOfWeek
    custom_time: Optional[str] = Field(None, max_length=10)
    sort_order: int = 0