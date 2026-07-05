from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.streak import StreakResponse
from app.services.streak_service import StreakService
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/streaks", tags=["Streaks"])


@router.get(
    "",
    response_model=list[StreakResponse],
    summary="Get all streaks"
)
def get_streaks(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all streaks for your routines, sorted by streak length."""
    service = StreakService(db)
    return service.get_all_streaks(current_user.id, skip, limit)


@router.get(
    "/top",
    response_model=list[StreakResponse],
    summary="Get top streaks"
)
def get_top_streaks(
    limit: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get your top performing streaks."""
    service = StreakService(db)
    return service.get_top_streaks(current_user.id, limit)


@router.get(
    "/overview",
    summary="Get streaks overview"
)
def get_streaks_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get streaks overview with stats."""
    service = StreakService(db)
    return service.get_streaks_overview(current_user.id)


@router.get(
    "/routine/{routine_id}",
    response_model=StreakResponse,
    summary="Get streak for a routine"
)
def get_routine_streak(
    routine_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get streak for a specific routine."""
    service = StreakService(db)
    return service.get_streak(UUID(routine_id), current_user.id)


@router.post(
    "/recalculate",
    summary="Recalculate all streaks"
)
def recalculate_streaks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Force recalculation of all streaks."""
    service = StreakService(db)
    service.recalculate_all_streaks(current_user.id)
    return {"message": "All streaks recalculated", "success": True}