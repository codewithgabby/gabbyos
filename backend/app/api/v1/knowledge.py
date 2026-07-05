from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.schemas.knowledge import (
    KnowledgeItemCreate, KnowledgeItemUpdate, KnowledgeItemResponse
)
from app.schemas.common import MessageResponse
from app.services.knowledge_service import KnowledgeService
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/knowledge", tags=["Knowledge Workspace"])


@router.post(
    "",
    response_model=KnowledgeItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a knowledge item"
)
def create_knowledge_item(
    data: KnowledgeItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add something to your Second Brain."""
    service = KnowledgeService(db)
    return service.create_item(current_user.id, data)


@router.get(
    "",
    response_model=list[KnowledgeItemResponse],
    summary="Get all knowledge items"
)
def get_knowledge_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    category_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get knowledge items with filters. Search searches title, description, and notes."""
    service = KnowledgeService(db)
    return service.get_all_items(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        category_id=category_id,
        status=status,
        search=search,
        priority=priority
    )


@router.get(
    "/{item_id}",
    response_model=KnowledgeItemResponse,
    summary="Get a knowledge item"
)
def get_knowledge_item(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single knowledge item."""
    service = KnowledgeService(db)
    return service.get_item(UUID(item_id), current_user.id)


@router.patch(
    "/{item_id}",
    response_model=KnowledgeItemResponse,
    summary="Update a knowledge item"
)
def update_knowledge_item(
    item_id: str,
    data: KnowledgeItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a knowledge item."""
    service = KnowledgeService(db)
    return service.update_item(UUID(item_id), current_user.id, data)


@router.delete(
    "/{item_id}",
    response_model=MessageResponse,
    summary="Delete a knowledge item"
)
def delete_knowledge_item(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a knowledge item."""
    service = KnowledgeService(db)
    service.delete_item(UUID(item_id), current_user.id)
    return MessageResponse(message="Knowledge item deleted successfully")


@router.patch(
    "/{item_id}/progress",
    response_model=KnowledgeItemResponse,
    summary="Update progress"
)
def update_progress(
    item_id: str,
    progress: float = Query(..., ge=0.0, le=100.0, description="Progress percentage"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update the progress percentage of a knowledge item."""
    service = KnowledgeService(db)
    return service.update_progress(UUID(item_id), current_user.id, progress)


@router.patch(
    "/{item_id}/archive",
    response_model=KnowledgeItemResponse,
    summary="Archive item"
)
def archive_item(
    item_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Archive a knowledge item."""
    service = KnowledgeService(db)
    return service.archive_item(UUID(item_id), current_user.id)