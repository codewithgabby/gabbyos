from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "/today",
    response_model=DashboardResponse,
    summary="Get today's dashboard"
)
def get_today_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get everything you need for today:
    - Greeting
    - Date and day
    - Identity statement
    - Today's planned routines with status
    - Completion percentage
    - Active streaks
    - Daily quote
    """
    service = DashboardService(db)
    return service.get_today_dashboard(current_user.id)