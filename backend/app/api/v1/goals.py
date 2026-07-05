from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse
from app.schemas.common import MessageResponse
from app.services.goal_service import GoalService
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.post(
    "",
    response_model=GoalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a goal"
)
def create_goal(
    data: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new long-term goal."""
    service = GoalService(db)
    return service.create_goal(current_user.id, data)


@router.get(
    "",
    response_model=list[GoalResponse],
    summary="Get all goals"
)
def get_goals(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all goals with optional filters."""
    service = GoalService(db)
    return service.get_all_goals(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        category_id=category_id,
        status=status,
        search=search
    )


@router.get(
    "/active",
    response_model=list[GoalResponse],
    summary="Get active goals"
)
def get_active_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get only active goals (not started or in progress)."""
    service = GoalService(db)
    return service.get_active_goals(current_user.id)


@router.get(
    "/{goal_id}",
    response_model=GoalResponse,
    summary="Get a goal"
)
def get_goal(
    goal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a goal by ID."""
    service = GoalService(db)
    return service.get_goal(UUID(goal_id), current_user.id)


@router.patch(
    "/{goal_id}",
    response_model=GoalResponse,
    summary="Update a goal"
)
def update_goal(
    goal_id: str,
    data: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a goal's details or progress."""
    service = GoalService(db)
    return service.update_goal(UUID(goal_id), current_user.id, data)


@router.delete(
    "/{goal_id}",
    response_model=MessageResponse,
    summary="Delete a goal"
)
def delete_goal(
    goal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a goal."""
    service = GoalService(db)
    service.delete_goal(UUID(goal_id), current_user.id)
    return MessageResponse(message="Goal deleted successfully")