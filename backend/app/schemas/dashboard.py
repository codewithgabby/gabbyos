from pydantic import BaseModel
from typing import Optional
from datetime import date


class TodayRoutine(BaseModel):
    """Schema for a routine in today's dashboard"""
    id: str
    routine_id: str
    title: str
    category_name: Optional[str] = None
    category_color: Optional[str] = None
    duration_minutes: int
    priority: str
    reason_why: Optional[str] = None
    status: str = "not_started"
    log_id: Optional[str] = None
    notes: Optional[str] = None


class DashboardResponse(BaseModel):
    """Schema for the today dashboard"""
    greeting: str
    current_date: date
    day_of_week: str
    identity_statement: Optional[str] = None
    today_routines: list[TodayRoutine]
    completion_percentage: float
    completed_count: int
    total_count: int
    active_streaks_count: int
    inbox_count: int
    active_projects: int
    quote: str