from typing import List, Optional
from uuid import UUID
from datetime import date, datetime
from sqlalchemy.orm import Session
from app.models.daily_log import DailyLog
from app.schemas.daily_log import DailyLogCreate, DailyLogUpdate
from app.repositories.daily_log_repository import DailyLogRepository
from app.core.constants import LogStatus
from app.core.exceptions import NotFoundException, AlreadyExistsException


class DailyLogService:
    """Service for daily log operations"""
    
    def __init__(self, db: Session):
        self.log_repo = DailyLogRepository(db)
    
    def create_log(self, user_id: UUID, data: DailyLogCreate) -> DailyLog:
        """Create a new daily log entry"""
        # Check if log already exists for this routine on this date
        existing = self.log_repo.get_by_routine_and_date(
            user_id, UUID(data.routine_id), data.log_date
        )
        if existing:
            raise AlreadyExistsException(
                "Log already exists for this routine on this date"
            )
        
        log_dict = {
            "user_id": user_id,
            "routine_id": UUID(data.routine_id),
            "log_date": data.log_date,
            "status": data.status,
            "notes": data.notes
        }
        
        # Set completed_at if status is completed
        if data.status == LogStatus.COMPLETED:
            log_dict["completed_at"] = datetime.utcnow()
        
        log = self.log_repo.create(log_dict)
        return self.log_repo.get_with_routine(log.id)
    
    def get_log(self, log_id: UUID, user_id: UUID) -> DailyLog:
        """Get a single daily log"""
        log = self.log_repo.get_with_routine(log_id)
        if not log or log.user_id != user_id:
            raise NotFoundException("Daily log")
        return log
    
    def get_logs_by_date(self, user_id: UUID, log_date: date) -> List[DailyLog]:
        """Get all logs for a specific date"""
        return self.log_repo.get_logs_by_date(user_id, log_date)
    
    def get_logs_by_routine(
        self, user_id: UUID, routine_id: UUID, skip: int = 0, limit: int = 30
    ) -> List[DailyLog]:
        """Get all logs for a specific routine"""
        return self.log_repo.get_logs_by_routine(user_id, routine_id, skip, limit)
    
    def get_all_logs(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50,
        log_date: Optional[date] = None,
        routine_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[DailyLog]:
        """Get all logs with filters"""
        routine_uuid = UUID(routine_id) if routine_id else None
        return self.log_repo.get_all_for_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            log_date=log_date,
            routine_id=routine_uuid,
            status=status
        )
    
    def update_log(
        self, log_id: UUID, user_id: UUID, data: DailyLogUpdate
    ) -> DailyLog:
        """Update a daily log"""
        log = self.log_repo.get_with_routine(log_id)
        if not log or log.user_id != user_id:
            raise NotFoundException("Daily log")
        
        update_dict = data.model_dump(exclude_unset=True)
        
        # Set completed_at when status changes to completed
        if update_dict.get("status") == LogStatus.COMPLETED and log.status != LogStatus.COMPLETED:
            update_dict["completed_at"] = datetime.utcnow()
        
        # Clear completed_at if status changes from completed
        if update_dict.get("status") and update_dict["status"] != LogStatus.COMPLETED:
            update_dict["completed_at"] = None
        
        updated_log = self.log_repo.update(log, update_dict)
        
        # Auto-calculate streak when status changes
        if "status" in update_dict:
            from app.services.streak_service import StreakService
            streak_service = StreakService(self.log_repo.db)
            streak_service.calculate_streak(user_id, log.routine_id)
        
        return updated_log
    
    def delete_log(self, log_id: UUID, user_id: UUID) -> None:
        """Delete a daily log"""
        log = self.log_repo.get(log_id)
        if not log or log.user_id != user_id:
            raise NotFoundException("Daily log")
        self.log_repo.soft_delete(log.id)
    
    def get_today_stats(self, user_id: UUID) -> dict:
        """Get today's completion statistics"""
        today = date.today()
        logs = self.log_repo.get_logs_by_date(user_id, today)
        
        total = len(logs)
        completed = sum(1 for log in logs if log.status == LogStatus.COMPLETED)
        in_progress = sum(1 for log in logs if log.status == LogStatus.IN_PROGRESS)
        not_started = sum(1 for log in logs if log.status == LogStatus.NOT_STARTED)
        skipped = sum(1 for log in logs if log.status == LogStatus.SKIPPED)
        
        return {
            "date": today,
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "not_started": not_started,
            "skipped": skipped,
            "completion_percentage": round((completed / total * 100), 1) if total > 0 else 0
        }