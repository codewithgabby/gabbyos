from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.schemas.weekly_plan import (
    WeeklyPlanCreate, WeeklyPlanUpdate, WeeklyPlanResponse,
    AddPlanItemRequest, PlanItemResponse
)
from app.schemas.common import MessageResponse
from app.services.weekly_planner_service import WeeklyPlannerService
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/planner", tags=["Weekly Planner"])


@router.post(
    "",
    response_model=WeeklyPlanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a weekly plan"
)
def create_plan(
    data: WeeklyPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new weekly plan with routines assigned to days."""
    service = WeeklyPlannerService(db)
    return service.create_plan(current_user.id, data)


@router.get(
    "",
    response_model=list[WeeklyPlanResponse],
    summary="Get all weekly plans"
)
def get_plans(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    year: Optional[int] = Query(None),
    week_number: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all weekly plans. Optionally filter by year and week."""
    service = WeeklyPlannerService(db)
    
    if year and week_number:
        plan = service.get_plan_by_week(current_user.id, year, week_number)
        return [plan] if plan else []
    
    return service.get_all_plans(current_user.id, skip, limit)


@router.get(
    "/{plan_id}",
    response_model=WeeklyPlanResponse,
    summary="Get a weekly plan"
)
def get_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a weekly plan by ID with all items."""
    service = WeeklyPlannerService(db)
    return service.get_plan(UUID(plan_id), current_user.id)


@router.patch(
    "/{plan_id}",
    response_model=WeeklyPlanResponse,
    summary="Update a weekly plan"
)
def update_plan(
    plan_id: str,
    data: WeeklyPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a weekly plan's notes."""
    service = WeeklyPlannerService(db)
    return service.update_plan(UUID(plan_id), current_user.id, data)


@router.delete(
    "/{plan_id}",
    response_model=MessageResponse,
    summary="Delete a weekly plan"
)
def delete_plan(
    plan_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a weekly plan and all its items."""
    service = WeeklyPlannerService(db)
    service.delete_plan(UUID(plan_id), current_user.id)
    return MessageResponse(message="Weekly plan deleted successfully")


@router.post(
    "/{plan_id}/items",
    response_model=PlanItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add routine to a day"
)
def add_plan_item(
    plan_id: str,
    data: AddPlanItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a routine to a specific day in the weekly plan."""
    service = WeeklyPlannerService(db)
    return service.add_item(UUID(plan_id), current_user.id, data)


@router.delete(
    "/{plan_id}/items/{item_id}",
    response_model=MessageResponse,
    summary="Remove routine from plan"
)
def remove_plan_item(
    plan_id: str,
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove a routine from the weekly plan."""
    service = WeeklyPlannerService(db)
    service.remove_item(UUID(plan_id), UUID(item_id), current_user.id)
    return MessageResponse(message="Item removed from plan")