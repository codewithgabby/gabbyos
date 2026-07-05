from pydantic import Field
from typing import Optional
from datetime import datetime
from app.schemas.common import BaseResponse, BaseSchema
from app.core.constants import Priority


class RoutineBase(BaseSchema):
    """Base schema for routines"""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category_id: Optional[str] = None
    duration_minutes: int = Field(default=30, ge=1, le=1440)
    reason_why: Optional[str] = Field(None, max_length=500)
    priority: Priority = Priority.MEDIUM
    is_active: bool = True


class RoutineCreate(RoutineBase):
    """Schema for creating a routine"""
    pass


class RoutineUpdate(BaseSchema):
    """Schema for updating a routine - all fields optional"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    category_id: Optional[str] = None
    duration_minutes: Optional[int] = Field(None, ge=1, le=1440)
    reason_why: Optional[str] = Field(None, max_length=500)
    priority: Optional[Priority] = None
    is_active: Optional[bool] = None


class RoutineResponse(BaseResponse):
    """Schema for routine responses"""
    user_id: str
    category_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    duration_minutes: int
    reason_why: Optional[str] = None
    priority: Priority
    is_active: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime
    
    # Optional: include category name for display
    category_name: Optional[str] = None


class RoutineToggleResponse(BaseResponse):
    """Schema for toggle activate/deactivate response"""
    title: str
    is_active: bool
    message: str