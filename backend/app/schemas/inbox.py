from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.common import BaseResponse, BaseSchema


class InboxItemBase(BaseSchema):
    """Base schema for inbox items"""
    content: str = Field(min_length=1, max_length=1000)
    category_hint: Optional[str] = Field(None, max_length=100)


class InboxItemCreate(InboxItemBase):
    """Schema for creating an inbox item"""
    pass


class InboxItemUpdate(BaseSchema):
    """Schema for updating an inbox item"""
    content: Optional[str] = Field(None, min_length=1, max_length=1000)
    category_hint: Optional[str] = Field(None, max_length=100)
    is_organized: Optional[bool] = None


class InboxItemResponse(BaseResponse):
    """Schema for inbox item responses"""
    user_id: str
    content: str
    category_hint: Optional[str] = None
    is_organized: bool
    organized_to: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class InboxStats(BaseModel):
    """Schema for inbox statistics"""
    total: int
    unorganized: int
    organized: int