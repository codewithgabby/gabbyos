
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.weekly_plan import WeeklyPlan, WeeklyPlanItem
from app.models.daily_log import DailyLog
from app.models.routine import Routine
from app.core.constants import LogStatus
from app.schemas.dashboard import TodayRoutine
import calendar
from datetime import date, datetime, timedelta, timezone


class DashboardService:
    """Service for the Today Dashboard"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_today_dashboard(self, user_id: UUID) -> dict:
        """Build the complete today dashboard"""
        # Use Nigeria timezone (UTC+1)
        nigeria_tz = timezone(timedelta(hours=1))
        today = datetime.now(nigeria_tz).date()
        day_name = calendar.day_name[today.weekday()]
        
        # Get user
        from app.models.user import User
        user = self.db.query(User).filter(
            User.id == user_id,
            User.is_deleted == False
        ).first()
        
        # Get today's routines from weekly plan
        today_routines = self._get_today_routines(user_id, today)
        
        # Calculate completion
        completed = [r for r in today_routines if r["status"] == "completed"]
        total = len(today_routines)
        percentage = (len(completed) / total * 100) if total > 0 else 0
        
        # Get greeting based on time
        hour = datetime.now(nigeria_tz).hour
        if hour < 12:
            greeting = "Good Morning"
        elif hour < 17:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"
        
        # Get streak count
        streaks_count = self._get_active_streaks_count(user_id)
        
        # Get inbox count (placeholder - will use real count when built)
        inbox_count = 0
        
        # Get active projects count (placeholder)
        active_projects = 0
        
        # Daily quote
        quotes = [
            "The only way to do great work is to love what you do. — Steve Jobs",
            "Small daily improvements over time lead to stunning results. — Robin Sharma",
            "Your future is created by what you do today, not tomorrow. — Robert Kiyosaki",
            "Discipline is the bridge between goals and accomplishment. — Jim Rohn",
            "The secret of your future is hidden in your daily routine. — Mike Murdock",
            "You do not rise to the level of your goals. You fall to the level of your systems. — James Clear",
            "We are what we repeatedly do. Excellence, then, is not an act, but a habit. — Aristotle",
        ]
        import random
        quote = random.choice(quotes)
        
        return {
            "greeting": f"{greeting}, {user.full_name}",
            "current_date": today,
            "day_of_week": day_name,
            "identity_statement": user.identity_statement or "I am becoming the best version of myself.",
            "today_routines": today_routines,
            "completion_percentage": round(percentage, 1),
            "completed_count": len(completed),
            "total_count": total,
            "active_streaks_count": streaks_count,
            "inbox_count": inbox_count,
            "active_projects": active_projects,
            "quote": quote
        }
    
    def _get_today_routines(self, user_id: UUID, today: date) -> list:
        """Get routines scheduled for today from the weekly plan"""
        day_name = calendar.day_name[today.weekday()].lower()
        
        # Find current week's plan
        year = today.isocalendar()[0]
        week_number = today.isocalendar()[1]
        
        plan = self.db.query(WeeklyPlan).filter(
            WeeklyPlan.user_id == user_id,
            WeeklyPlan.year == year,
            WeeklyPlan.week_number == week_number,
            WeeklyPlan.is_deleted == False
        ).first()
        
        if not plan:
            return []
        
        # Get items for today
        items = self.db.query(WeeklyPlanItem).filter(
            WeeklyPlanItem.plan_id == plan.id,
            WeeklyPlanItem.day_of_week == day_name,
            WeeklyPlanItem.is_deleted == False
        ).order_by(WeeklyPlanItem.sort_order).all()
        
        today_routines = []
        
        for item in items:
            routine = self.db.query(Routine).filter(
                Routine.id == item.routine_id,
                Routine.is_deleted == False
            ).first()
            
            if not routine:
                continue
            
            # Get or create daily log
            daily_log = self.db.query(DailyLog).filter(
                DailyLog.user_id == user_id,
                DailyLog.routine_id == routine.id,
                DailyLog.log_date == today,
                DailyLog.is_deleted == False
            ).first()
            
            if not daily_log:
                daily_log = DailyLog(
                    user_id=user_id,
                    routine_id=routine.id,
                    log_date=today,
                    status=LogStatus.NOT_STARTED
                )
                self.db.add(daily_log)
                self.db.commit()
                self.db.refresh(daily_log)
            
            category = routine.category
            
            today_routines.append({
                "id": str(daily_log.id),
                "routine_id": str(routine.id),
                "title": routine.title,
                "category_name": category.name if category else None,
                "category_color": category.color if category else None,
                "duration_minutes": routine.duration_minutes,
                "priority": routine.priority.value if hasattr(routine.priority, 'value') else routine.priority,
                "reason_why": routine.reason_why,
                "status": daily_log.status.value if hasattr(daily_log.status, 'value') else daily_log.status,
                "log_id": str(daily_log.id),
                "notes": daily_log.notes
            })
        
        return today_routines
    
    def _get_active_streaks_count(self, user_id: UUID) -> int:
        """Get count of active streaks (simplified - will be proper when Streaks module is built)"""
        return 0