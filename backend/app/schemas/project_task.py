from pydantic import Field
from typing import Optional
from datetime import date, datetime
from app.schemas.common import BaseResponse, BaseSchema
from app.core.constants import TaskStatus


class ProjectTaskBase(BaseSchema):
    """Base schema for project tasks"""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[str] = Field(None, max_length=50)
    status: TaskStatus = TaskStatus.TODO
    due_date: Optional[date] = None


class ProjectTaskCreate(ProjectTaskBase):
    """Schema for creating a task"""
    pass


class ProjectTaskUpdate(BaseSchema):
    """Schema for updating a task"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[str] = Field(None, max_length=50)
    status: Optional[TaskStatus] = None
    due_date: Optional[date] = None


class ProjectTaskResponse(BaseResponse):
    """Schema for task responses"""
    project_id: str
    title: str
    description: Optional[str] = None
    priority: Optional[str] = None
    status: TaskStatus
    due_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime