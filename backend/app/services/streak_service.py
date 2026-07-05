from typing import List
from uuid import UUID
from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models.streak import Streak
from app.models.daily_log import DailyLog
from app.repositories.streak_repository import StreakRepository
from app.core.constants import LogStatus


class StreakService:
    """Service for streak calculations and operations"""
    
    def __init__(self, db: Session):
        self.streak_repo = StreakRepository(db)
        self.db = db
    
    def calculate_streak(self, user_id: UUID, routine_id: UUID) -> Streak:
        """
        Calculate the current streak for a routine.
        Counts consecutive days with completed logs.
        """
        today = date.today()
        streak = self.streak_repo.get_or_create(user_id, routine_id)
        
        # Get completed logs for this routine, ordered by date descending
        logs = self.db.query(DailyLog).filter(
            DailyLog.user_id == user_id,
            DailyLog.routine_id == routine_id,
            DailyLog.status == LogStatus.COMPLETED,
            DailyLog.is_deleted == False
        ).order_by(DailyLog.log_date.desc()).limit(365).all()
        
        if not logs:
            # No completed logs, reset streak
            return self.streak_repo.reset_streak(streak)
        
        # Check if most recent log is from today or yesterday
        most_recent = logs[0].log_date
        
        if most_recent < today - timedelta(days=1):
            # Last completion was more than 1 day ago, streak broken
            return self.streak_repo.reset_streak(streak)
        
        # Count consecutive days
        current_streak = 1
        expected_date = most_recent - timedelta(days=1)
        
        for log in logs[1:]:
            if log.log_date == expected_date:
                current_streak += 1
                expected_date -= timedelta(days=1)
            else:
                break
        
        return self.streak_repo.update_streak(streak, current_streak)
    
    def recalculate_all_streaks(self, user_id: UUID) -> None:
        """Recalculate streaks for all user's routines"""
        from app.models.routine import Routine
        
        routines = self.db.query(Routine).filter(
            Routine.user_id == user_id,
            Routine.is_deleted == False
        ).all()
        
        for routine in routines:
            self.calculate_streak(user_id, routine.id)
    
    def get_streak(self, routine_id: UUID, user_id: UUID) -> Streak:
        """Get streak for a routine, calculating if needed"""
        streak = self.streak_repo.get_by_routine(routine_id)
        if not streak:
            streak = self.calculate_streak(user_id, routine_id)
        return streak
    
    def get_all_streaks(
        self, user_id: UUID, skip: int = 0, limit: int = 50
    ) -> List[Streak]:
        """Get all streaks for user"""
        # Recalculate all before returning
        self.recalculate_all_streaks(user_id)
        return self.streak_repo.get_all_for_user(user_id, skip, limit)
    
    def get_top_streaks(
        self, user_id: UUID, limit: int = 5
    ) -> List[Streak]:
        """Get top performing streaks"""
        return self.streak_repo.get_top_streaks(user_id, limit)
    
    def get_streaks_overview(self, user_id: UUID) -> dict:
        """Get overview of all streaks"""
        streaks = self.get_all_streaks(user_id)
        
        if not streaks:
            return {
                "total_active_streaks": 0,
                "average_streak": 0,
                "best_streak_routine": None,
                "streaks": []
            }
        
        active = [s for s in streaks if s.current_streak > 0]
        avg = sum(s.current_streak for s in streaks) / len(streaks) if streaks else 0
        
        best = max(streaks, key=lambda s: s.current_streak) if streaks else None
        
        return {
            "total_active_streaks": len(active),
            "average_streak": round(avg, 1),
            "best_streak_routine": best,
            "streaks": streaks
        }