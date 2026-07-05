from pydantic import Field
from typing import Optional
from datetime import date, datetime
from app.schemas.common import BaseResponse, BaseSchema
from app.core.constants import ProjectStatus


class ProjectBase(BaseSchema):
    """Base schema for projects"""
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Optional[str] = Field(None, max_length=50)
    status: ProjectStatus = ProjectStatus.PLANNED
    progress_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    current_phase: Optional[str] = Field(None, max_length=255)
    start_date: Optional[date] = None
    target_completion_date: Optional[date] = None
    notes: Optional[list[str]] = Field(default_factory=list)
    tags: Optional[list[str]] = Field(default_factory=list)


class ProjectCreate(ProjectBase):
    """Schema for creating a project"""
    pass


class ProjectUpdate(BaseSchema):
    """Schema for updating a project"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    priority: Optional[str] = Field(None, max_length=50)
    status: Optional[ProjectStatus] = None
    progress_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    current_phase: Optional[str] = Field(None, max_length=255)
    start_date: Optional[date] = None
    target_completion_date: Optional[date] = None
    notes: Optional[list[str]] = None
    tags: Optional[list[str]] = None


class ProjectResponse(BaseResponse):
    """Schema for project responses"""
    user_id: str
    title: str
    description: Optional[str] = None
    priority: Optional[str] = None
    status: ProjectStatus
    progress_percentage: float
    current_phase: Optional[str] = None
    start_date: Optional[date] = None
    target_completion_date: Optional[date] = None
    notes: Optional[list[str]] = None
    tags: Optional[list[str]] = None
    created_at: datetime
    updated_at: datetime