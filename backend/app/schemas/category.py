from pydantic import Field
from typing import Optional
from datetime import datetime
from app.schemas.common import BaseResponse, BaseSchema


class CategoryBase(BaseSchema):
    """Base schema for categories"""
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    color: Optional[str] = Field(None, max_length=7)
    icon: Optional[str] = Field(None, max_length=50)


class CategoryCreate(CategoryBase):
    """Schema for creating a category"""
    pass


class CategoryUpdate(BaseSchema):
    """Schema for updating a category - all fields optional"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    color: Optional[str] = Field(None, max_length=7)
    icon: Optional[str] = Field(None, max_length=50)


class CategoryResponse(BaseResponse):
    """Schema for category responses"""
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    created_at: datetime
    updated_at: datetime