from typing import Optional
from datetime import date, datetime
from app.schemas.common import BaseResponse


class StreakResponse(BaseResponse):
    """Schema for streak responses"""
    routine_id: str
    routine_title: Optional[str] = None
    category_name: Optional[str] = None
    current_streak: int
    longest_streak: int
    last_activity_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime


class AllStreaksResponse(BaseResponse):
    """Schema for all streaks overview"""
    streaks: list[StreakResponse]
    total_active_streaks: int
    average_streak: float
    best_streak_routine: Optional[StreakResponse] = None