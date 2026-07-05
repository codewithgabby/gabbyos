from pydantic import Field
from typing import Optional
from datetime import date, datetime
from app.schemas.common import BaseResponse, BaseSchema


class ReflectionBase(BaseSchema):
    """Base schema for reflections"""
    reflection_date: date
    wins: Optional[str] = Field(None, max_length=2000)
    challenges: Optional[str] = Field(None, max_length=2000)
    gratitude: Optional[str] = Field(None, max_length=2000)
    tomorrow_focus: Optional[str] = Field(None, max_length=2000)
    mood_rating: Optional[int] = Field(None, ge=1, le=10)


class ReflectionCreate(ReflectionBase):
    """Schema for creating a reflection"""
    pass


class ReflectionUpdate(BaseSchema):
    """Schema for updating a reflection"""
    wins: Optional[str] = Field(None, max_length=2000)
    challenges: Optional[str] = Field(None, max_length=2000)
    gratitude: Optional[str] = Field(None, max_length=2000)
    tomorrow_focus: Optional[str] = Field(None, max_length=2000)
    mood_rating: Optional[int] = Field(None, ge=1, le=10)


class ReflectionResponse(BaseResponse):
    """Schema for reflection responses"""
    user_id: str
    reflection_date: date
    wins: Optional[str] = None
    challenges: Optional[str] = None
    gratitude: Optional[str] = None
    tomorrow_focus: Optional[str] = None
    mood_rating: Optional[int] = None
    created_at: datetime
    updated_at: datetime