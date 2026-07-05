from pydantic import Field
from typing import Optional
from datetime import date, datetime
from app.schemas.common import BaseResponse, BaseSchema
from app.core.constants import KnowledgeStatus


class KnowledgeItemBase(BaseSchema):
    """Base schema for knowledge items"""
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=2000)
    category_id: Optional[str] = None
    tags: Optional[list[str]] = Field(default_factory=list)
    priority: Optional[str] = Field(None, max_length=50)
    status: KnowledgeStatus = KnowledgeStatus.INBOX
    progress_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    source_link: Optional[str] = Field(None, max_length=1000)
    notes: Optional[str] = Field(None, max_length=5000)
    target_completion_date: Optional[date] = None


class KnowledgeItemCreate(KnowledgeItemBase):
    """Schema for creating a knowledge item"""
    pass


class KnowledgeItemUpdate(BaseSchema):
    """Schema for updating a knowledge item"""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = Field(None, max_length=2000)
    category_id: Optional[str] = None
    tags: Optional[list[str]] = None
    priority: Optional[str] = Field(None, max_length=50)
    status: Optional[KnowledgeStatus] = None
    progress_percentage: Optional[float] = Field(None, ge=0.0, le=100.0)
    source_link: Optional[str] = Field(None, max_length=1000)
    notes: Optional[str] = Field(None, max_length=5000)
    target_completion_date: Optional[date] = None


class KnowledgeItemResponse(BaseResponse):
    """Schema for knowledge item responses"""
    user_id: str
    category_id: Optional[str] = None
    category_name: Optional[str] = None
    title: str
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    priority: Optional[str] = None
    status: KnowledgeStatus
    progress_percentage: float
    source_link: Optional[str] = None
    notes: Optional[str] = None
    target_completion_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime