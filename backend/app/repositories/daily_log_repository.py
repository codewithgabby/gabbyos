from typing import Optional, List
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session, joinedload
from app.models.daily_log import DailyLog
from app.models.routine import Routine
from app.repositories.base_repository import BaseRepository


class DailyLogRepository(BaseRepository[DailyLog]):
    """Repository for DailyLog model operations"""
    
    def __init__(self, db: Session):
        super().__init__(DailyLog, db)
    
    def get_with_routine(self, log_id: UUID) -> Optional[DailyLog]:
        """Get a daily log with routine and category loaded"""
        return self.db.query(DailyLog).options(
            joinedload(DailyLog.routine)
            .joinedload(Routine.category)
        ).filter(
            DailyLog.id == log_id,
            DailyLog.is_deleted == False
        ).first()
    
    def get_by_routine_and_date(
        self,
        user_id: UUID,
        routine_id: UUID,
        log_date: date
    ) -> Optional[DailyLog]:
        """Get log for a specific routine on a specific date"""
        return self.db.query(DailyLog).filter(
            DailyLog.user_id == user_id,
            DailyLog.routine_id == routine_id,
            DailyLog.log_date == log_date,
            DailyLog.is_deleted == False
        ).first()
    
    def get_logs_by_date(
        self,
        user_id: UUID,
        log_date: date
    ) -> List[DailyLog]:
        """Get all logs for a specific date"""
        return self.db.query(DailyLog).options(
            joinedload(DailyLog.routine)
            .joinedload(Routine.category)
        ).filter(
            DailyLog.user_id == user_id,
            DailyLog.log_date == log_date,
            DailyLog.is_deleted == False
        ).order_by(DailyLog.created_at).all()
    
    def get_logs_by_routine(
        self,
        user_id: UUID,
        routine_id: UUID,
        skip: int = 0,
        limit: int = 30
    ) -> List[DailyLog]:
        """Get all logs for a specific routine"""
        return self.db.query(DailyLog).options(
            joinedload(DailyLog.routine)
            .joinedload(Routine.category)
        ).filter(
            DailyLog.user_id == user_id,
            DailyLog.routine_id == routine_id,
            DailyLog.is_deleted == False
        ).order_by(DailyLog.log_date.desc()).offset(skip).limit(limit).all()
    
    def get_all_for_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50,
        log_date: Optional[date] = None,
        routine_id: Optional[UUID] = None,
        status: Optional[str] = None
    ) -> List[DailyLog]:
        """Get all logs for a user with optional filters"""
        query = self.db.query(DailyLog).options(
            joinedload(DailyLog.routine)
            .joinedload(Routine.category)
        ).filter(
            DailyLog.user_id == user_id,
            DailyLog.is_deleted == False
        )
        
        if log_date:
            query = query.filter(DailyLog.log_date == log_date)
        
        if routine_id:
            query = query.filter(DailyLog.routine_id == routine_id)
        
        if status:
            query = query.filter(DailyLog.status == status)
        
        return query.order_by(
            DailyLog.log_date.desc(),
            DailyLog.created_at.desc()
        ).offset(skip).limit(limit).all()