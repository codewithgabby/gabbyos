from pydantic import Field
from typing import Optional
from datetime import date, datetime
from app.schemas.common import BaseResponse, BaseSchema
from app.core.constants import LogStatus


class DailyLogBase(BaseSchema):
    """Base schema for daily logs"""
    routine_id: str
    log_date: date
    status: LogStatus = LogStatus.NOT_STARTED
    notes: Optional[str] = Field(None, max_length=2000)


class DailyLogCreate(DailyLogBase):
    """Schema for creating a daily log"""
    pass


class DailyLogUpdate(BaseSchema):
    """Schema for updating a daily log"""
    status: Optional[LogStatus] = None
    notes: Optional[str] = Field(None, max_length=2000)


class DailyLogResponse(BaseResponse):
    """Schema for daily log responses"""
    user_id: str
    routine_id: str
    routine_title: Optional[str] = None
    category_name: Optional[str] = None
    log_date: date
    status: LogStatus
    notes: Optional[str] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime