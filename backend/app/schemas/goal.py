from pydantic import Field
from typing import Optional
from datetime import date, datetime
from app.schemas.common import BaseResponse, BaseSchema
from app.core.constants import GoalStatus


class GoalBase(BaseSchema):
    """Base schema for goals"""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category_id: Optional[str] = None
    target_value: Optional[str] = Field(None, max_length=100)
    current_progress: Optional[str] = Field(None, max_length=100)
    status: GoalStatus = GoalStatus.NOT_STARTED
    deadline: Optional[date] = None


class GoalCreate(GoalBase):
    """Schema for creating a goal"""
    pass


class GoalUpdate(BaseSchema):
    """Schema for updating a goal"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category_id: Optional[str] = None
    target_value: Optional[str] = Field(None, max_length=100)
    current_progress: Optional[str] = Field(None, max_length=100)
    status: Optional[GoalStatus] = None
    deadline: Optional[date] = None


class GoalResponse(BaseResponse):
    """Schema for goal responses"""
    user_id: str
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    title: str
    description: Optional[str] = None
    target_value: Optional[str] = None
    current_progress: Optional[str] = None
    status: GoalStatus
    deadline: Optional[date] = None
    created_at: datetime
    updated_at: datetime