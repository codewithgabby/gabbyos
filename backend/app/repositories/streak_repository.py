from typing import Optional, List
from uuid import UUID
from datetime import date, timedelta
from sqlalchemy.orm import Session, joinedload
from app.models.streak import Streak
from app.models.routine import Routine
from app.repositories.base_repository import BaseRepository


class StreakRepository(BaseRepository[Streak]):
    """Repository for Streak model operations"""
    
    def __init__(self, db: Session):
        super().__init__(Streak, db)
    
    def get_by_routine(self, routine_id: UUID) -> Optional[Streak]:
        """Get streak for a specific routine"""
        return self.db.query(Streak).filter(
            Streak.routine_id == routine_id,
            Streak.is_deleted == False
        ).first()
    
    def get_all_for_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50
    ) -> List[Streak]:
        """Get all streaks for a user"""
        return self.db.query(Streak).options(
            joinedload(Streak.routine)
            .joinedload(Routine.category)
        ).filter(
            Streak.user_id == user_id,
            Streak.is_deleted == False
        ).order_by(
            Streak.current_streak.desc()
        ).offset(skip).limit(limit).all()
    
    def get_top_streaks(
        self,
        user_id: UUID,
        limit: int = 5
    ) -> List[Streak]:
        """Get top streaks by current streak count"""
        return self.db.query(Streak).options(
            joinedload(Streak.routine)
            .joinedload(Routine.category)
        ).filter(
            Streak.user_id == user_id,
            Streak.is_deleted == False,
            Streak.current_streak > 0
        ).order_by(
            Streak.current_streak.desc()
        ).limit(limit).all()
    
    def get_or_create(self, user_id: UUID, routine_id: UUID) -> Streak:
        """Get existing streak or create new one"""
        streak = self.get_by_routine(routine_id)
        if not streak:
            streak = self.create({
                "user_id": user_id,
                "routine_id": routine_id,
                "current_streak": 0,
                "longest_streak": 0
            })
        return streak
    
    def update_streak(self, streak: Streak, new_streak: int) -> Streak:
        """Update streak counts"""
        streak.current_streak = new_streak
        if new_streak > streak.longest_streak:
            streak.longest_streak = new_streak
        streak.last_activity_date = date.today()
        self.db.commit()
        self.db.refresh(streak)
        return streak
    
    def reset_streak(self, streak: Streak) -> Streak:
        """Reset current streak to 0"""
        streak.current_streak = 0
        self.db.commit()
        self.db.refresh(streak)
        return streak