from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.common import MessageResponse
from app.services.category_service import CategoryService
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new category"
)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new dynamic category."""
    service = CategoryService(db)
    return service.create_category(current_user.id, data)


@router.get(
    "",
    response_model=list[CategoryResponse],
    summary="Get all categories"
)
def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all categories for the current user."""
    service = CategoryService(db)
    return service.get_all_categories(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        search=search
    )


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Get a single category"
)
def get_category(
    category_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a category by ID."""
    service = CategoryService(db)
    return service.get_category(UUID(category_id), current_user.id)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    summary="Update a category"
)
def update_category(
    category_id: str,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a category. Only provided fields will be updated."""
    service = CategoryService(db)
    return service.update_category(UUID(category_id), current_user.id, data)


@router.delete(
    "/{category_id}",
    response_model=MessageResponse,
    summary="Delete a category"
)
def delete_category(
    category_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soft delete a category."""
    service = CategoryService(db)
    service.delete_category(UUID(category_id), current_user.id)
    return MessageResponse(message="Category deleted successfully")