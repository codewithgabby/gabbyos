from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.schemas.routine import (
    RoutineCreate, RoutineUpdate, RoutineResponse, RoutineToggleResponse
)
from app.schemas.common import MessageResponse
from app.services.routine_service import RoutineService
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/routines", tags=["Routines"])


@router.post(
    "",
    response_model=RoutineResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new routine"
)
def create_routine(
    data: RoutineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new routine with category, duration, and reason."""
    service = RoutineService(db)
    return service.create_routine(current_user.id, data)


@router.get(
    "",
    response_model=list[RoutineResponse],
    summary="Get all routines"
)
def get_routines(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    category_id: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all routines with optional filters."""
    service = RoutineService(db)
    return service.get_all_routines(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        category_id=category_id,
        is_active=is_active,
        search=search
    )


@router.get(
    "/{routine_id}",
    response_model=RoutineResponse,
    summary="Get a single routine"
)
def get_routine(
    routine_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a routine by ID with category information."""
    service = RoutineService(db)
    return service.get_routine(UUID(routine_id), current_user.id)


@router.patch(
    "/{routine_id}",
    response_model=RoutineResponse,
    summary="Update a routine"
)
def update_routine(
    routine_id: str,
    data: RoutineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a routine. Only provided fields will be updated."""
    service = RoutineService(db)
    return service.update_routine(UUID(routine_id), current_user.id, data)


@router.delete(
    "/{routine_id}",
    response_model=MessageResponse,
    summary="Delete a routine"
)
def delete_routine(
    routine_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soft delete a routine."""
    service = RoutineService(db)
    service.delete_routine(UUID(routine_id), current_user.id)
    return MessageResponse(message="Routine deleted successfully")


@router.patch(
    "/{routine_id}/toggle",
    response_model=RoutineToggleResponse,
    summary="Toggle routine active/inactive"
)
def toggle_routine(
    routine_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Activate or deactivate a routine."""
    service = RoutineService(db)
    routine = service.toggle_routine(UUID(routine_id), current_user.id)
    
    status_text = "activated" if routine.is_active else "deactivated"
    return RoutineToggleResponse(
        id=str(routine.id),
        title=routine.title,
        is_active=routine.is_active,
        message=f"Routine '{routine.title}' {status_text}"
    )