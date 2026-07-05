from typing import Optional
from uuid import UUID
from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.schemas.daily_log import DailyLogCreate, DailyLogUpdate, DailyLogResponse
from app.schemas.common import MessageResponse
from app.services.daily_log_service import DailyLogService
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/logs", tags=["Daily Logs"])


@router.post(
    "",
    response_model=DailyLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a daily log"
)
def create_log(
    data: DailyLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new daily log for a routine."""
    service = DailyLogService(db)
    return service.create_log(current_user.id, data)


@router.get(
    "",
    response_model=list[DailyLogResponse],
    summary="Get all daily logs"
)
def get_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    log_date: Optional[date] = Query(None),
    routine_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get daily logs with optional filters."""
    service = DailyLogService(db)
    return service.get_all_logs(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        log_date=log_date,
        routine_id=routine_id,
        status=status
    )


@router.get(
    "/today",
    response_model=list[DailyLogResponse],
    summary="Get today's logs"
)
def get_today_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all daily logs for today."""
    service = DailyLogService(db)
    return service.get_logs_by_date(current_user.id, date.today())


@router.get(
    "/stats/today",
    summary="Get today's stats"
)
def get_today_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get completion statistics for today."""
    service = DailyLogService(db)
    return service.get_today_stats(current_user.id)


@router.get(
    "/routine/{routine_id}",
    response_model=list[DailyLogResponse],
    summary="Get logs for a routine"
)
def get_routine_logs(
    routine_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all logs for a specific routine."""
    service = DailyLogService(db)
    return service.get_logs_by_routine(
        current_user.id, UUID(routine_id), skip, limit
    )


@router.get(
    "/{log_id}",
    response_model=DailyLogResponse,
    summary="Get a daily log"
)
def get_log(
    log_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a daily log by ID."""
    service = DailyLogService(db)
    return service.get_log(UUID(log_id), current_user.id)


@router.patch(
    "/{log_id}",
    response_model=DailyLogResponse,
    summary="Update a daily log"
)
def update_log(
    log_id: str,
    data: DailyLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update status or notes of a daily log."""
    service = DailyLogService(db)
    return service.update_log(UUID(log_id), current_user.id, data)


@router.delete(
    "/{log_id}",
    response_model=MessageResponse,
    summary="Delete a daily log"
)
def delete_log(
    log_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a daily log."""
    service = DailyLogService(db)
    service.delete_log(UUID(log_id), current_user.id)
    return MessageResponse(message="Daily log deleted successfully")