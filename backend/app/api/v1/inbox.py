from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.schemas.inbox import (
    InboxItemCreate, InboxItemUpdate, InboxItemResponse
)
from app.schemas.common import MessageResponse
from app.services.inbox_service import InboxService
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/inbox", tags=["Inbox"])


@router.post(
    "",
    response_model=InboxItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Quick capture an idea"
)
def create_inbox_item(
    data: InboxItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Quickly save an idea, thought, or thing to explore later."""
    service = InboxService(db)
    return service.create_item(current_user.id, data)


@router.get(
    "",
    response_model=list[InboxItemResponse],
    summary="Get all inbox items"
)
def get_inbox_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    is_organized: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get inbox items with filters."""
    service = InboxService(db)
    return service.get_all_items(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        is_organized=is_organized,
        search=search
    )


@router.get(
    "/unorganized",
    response_model=list[InboxItemResponse],
    summary="Get unorganized items"
)
def get_unorganized(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get items that still need to be organized."""
    service = InboxService(db)
    return service.get_unorganized(current_user.id)


@router.get(
    "/stats",
    summary="Get inbox stats"
)
def get_inbox_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get inbox count and organization stats."""
    service = InboxService(db)
    return service.get_stats(current_user.id)


@router.get(
    "/{item_id}",
    response_model=InboxItemResponse,
    summary="Get an inbox item"
)
def get_inbox_item(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single inbox item."""
    service = InboxService(db)
    return service.get_item(UUID(item_id), current_user.id)


@router.patch(
    "/{item_id}",
    response_model=InboxItemResponse,
    summary="Update an inbox item"
)
def update_inbox_item(
    item_id: str,
    data: InboxItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an inbox item."""
    service = InboxService(db)
    return service.update_item(UUID(item_id), current_user.id, data)


@router.patch(
    "/{item_id}/organize",
    response_model=InboxItemResponse,
    summary="Mark item as organized"
)
def organize_item(
    item_id: str,
    organized_to: Optional[str] = Query(None, description="Where it was moved to (knowledge/project/routine)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark an inbox item as organized."""
    service = InboxService(db)
    return service.mark_organized(UUID(item_id), current_user.id, organized_to)


@router.delete(
    "/{item_id}",
    response_model=MessageResponse,
    summary="Delete an inbox item"
)
def delete_inbox_item(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an inbox item."""
    service = InboxService(db)
    service.delete_item(UUID(item_id), current_user.id)
    return MessageResponse(message="Inbox item deleted successfully")