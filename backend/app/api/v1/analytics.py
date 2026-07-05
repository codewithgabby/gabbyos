from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.analytics_service import AnalyticsService
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "",
    summary="Get full analytics dashboard"
)
def get_analytics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get complete analytics including:
    - Daily, weekly, monthly completion rates
    - Hours spent by category
    - Most and least completed routines
    - Current streaks
    - Projects and knowledge summaries
    - Recent activity
    - Inbox count
    """
    service = AnalyticsService(db)
    return service.get_full_analytics(current_user.id)


@router.get(
    "/completion",
    summary="Get completion rates"
)
def get_completion_rates(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get daily, weekly, and monthly completion percentages."""
    from datetime import date
    service = AnalyticsService(db)
    return service._get_completion_rates(current_user.id, date.today())


@router.get(
    "/hours",
    summary="Get hours by category"
)
def get_hours_by_category(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get hours spent per category this week."""
    from datetime import date
    service = AnalyticsService(db)
    return service._get_hours_by_category(current_user.id, date.today())


@router.get(
    "/routines/top",
    summary="Get top routines"
)
def get_top_routines(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get most completed routines."""
    service = AnalyticsService(db)
    return service._get_top_routines(current_user.id)


@router.get(
    "/routines/bottom",
    summary="Get least completed routines"
)
def get_bottom_routines(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get least completed routines."""
    service = AnalyticsService(db)
    return service._get_bottom_routines(current_user.id)


@router.get(
    "/overview",
    summary="Get system overview"
)
def get_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get overall system stats."""
    from datetime import date
    service = AnalyticsService(db)
    return service._get_overview(current_user.id, date.today())