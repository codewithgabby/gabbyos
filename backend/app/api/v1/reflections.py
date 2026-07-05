from typing import Optional
from uuid import UUID
from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.schemas.reflection import (
    ReflectionCreate, ReflectionUpdate, ReflectionResponse
)
from app.schemas.common import MessageResponse
from app.services.reflection_service import ReflectionService
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/reflections", tags=["Reflections"])


@router.post(
    "",
    response_model=ReflectionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a reflection"
)
def create_reflection(
    data: ReflectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new daily reflection."""
    service = ReflectionService(db)
    return service.create_reflection(current_user.id, data)


@router.get(
    "",
    response_model=list[ReflectionResponse],
    summary="Get all reflections"
)
def get_reflections(
    skip: int = Query(0, ge=0),
    limit: int = Query(30, ge=1, le=100),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all reflections with optional date range."""
    service = ReflectionService(db)
    return service.get_all_reflections(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date
    )


@router.get(
    "/today",
    response_model=ReflectionResponse,
    summary="Get today's reflection"
)
def get_today_reflection(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get or create today's reflection."""
    service = ReflectionService(db)
    return service.get_or_create_today(current_user.id)


@router.get(
    "/recent",
    response_model=list[ReflectionResponse],
    summary="Get recent reflections"
)
def get_recent_reflections(
    limit: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get your most recent reflections."""
    service = ReflectionService(db)
    return service.get_recent_reflections(current_user.id, limit)


@router.get(
    "/date/{reflection_date}",
    response_model=ReflectionResponse,
    summary="Get reflection by date"
)
def get_reflection_by_date(
    reflection_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get reflection for a specific date."""
    service = ReflectionService(db)
    reflection = service.get_reflection_by_date(current_user.id, reflection_date)
    if not reflection:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("Reflection")
    return reflection


@router.get(
    "/{reflection_id}",
    response_model=ReflectionResponse,
    summary="Get a reflection"
)
def get_reflection(
    reflection_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a reflection by ID."""
    service = ReflectionService(db)
    return service.get_reflection(UUID(reflection_id), current_user.id)


@router.patch(
    "/{reflection_id}",
    response_model=ReflectionResponse,
    summary="Update a reflection"
)
def update_reflection(
    reflection_id: str,
    data: ReflectionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a reflection's content."""
    service = ReflectionService(db)
    return service.update_reflection(UUID(reflection_id), current_user.id, data)


@router.delete(
    "/{reflection_id}",
    response_model=MessageResponse,
    summary="Delete a reflection"
)
def delete_reflection(
    reflection_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a reflection."""
    service = ReflectionService(db)
    service.delete_reflection(UUID(reflection_id), current_user.id)
    return MessageResponse(message="Reflection deleted successfully")