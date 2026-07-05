from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.routine import Routine
from app.schemas.routine import RoutineCreate, RoutineUpdate
from app.repositories.routine_repository import RoutineRepository
from app.core.exceptions import NotFoundException, AlreadyExistsException


class RoutineService:
    """Service for routine operations"""
    
    def __init__(self, db: Session):
        self.routine_repo = RoutineRepository(db)
    
    def create_routine(self, user_id: UUID, data: RoutineCreate) -> Routine:
        """Create a new routine"""
        # Check for duplicate title
        existing = self.routine_repo.get_by_title(user_id, data.title)
        if existing:
            raise AlreadyExistsException(f"Routine '{data.title}'")
        
        routine_dict = data.model_dump()
        routine_dict["user_id"] = user_id
        
        # Convert category_id string to UUID if provided
        if routine_dict.get("category_id"):
            try:
                routine_dict["category_id"] = UUID(routine_dict["category_id"])
            except (ValueError, AttributeError):
                routine_dict["category_id"] = None
        
        return self.routine_repo.create(routine_dict)
    
    def get_routine(self, routine_id: UUID, user_id: UUID) -> Routine:
        """Get a single routine with category"""
        routine = self.routine_repo.get_with_category(routine_id)
        if not routine or routine.user_id != user_id:
            raise NotFoundException("Routine")
        return routine
    
    def get_all_routines(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[str] = None,
        is_active: Optional[bool] = None,
        search: Optional[str] = None
    ) -> List[Routine]:
        """Get all routines for user with filters"""
        category_uuid = UUID(category_id) if category_id else None
        
        return self.routine_repo.get_all_for_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            category_id=category_uuid,
            is_active=is_active,
            search=search
        )
    
    def update_routine(
        self,
        routine_id: UUID,
        user_id: UUID,
        data: RoutineUpdate
    ) -> Routine:
        """Update a routine"""
        routine = self.routine_repo.get_with_category(routine_id)
        if not routine or routine.user_id != user_id:
            raise NotFoundException("Routine")
        
        # If title is being changed, check for duplicates
        if data.title and data.title != routine.title:
            existing = self.routine_repo.get_by_title(user_id, data.title)
            if existing:
                raise AlreadyExistsException(f"Routine '{data.title}'")
        
        update_dict = data.model_dump(exclude_unset=True)
        
        # Convert category_id string to UUID if provided and not None
        if "category_id" in update_dict:
            if update_dict["category_id"] is not None and update_dict["category_id"] != "":
                try:
                    update_dict["category_id"] = UUID(update_dict["category_id"])
                except (ValueError, AttributeError):
                    pass  # Keep as is if conversion fails
        
        return self.routine_repo.update(routine, update_dict)
    
    def delete_routine(self, routine_id: UUID, user_id: UUID) -> None:
        """Delete a routine"""
        routine = self.routine_repo.get(routine_id)
        if not routine or routine.user_id != user_id:
            raise NotFoundException("Routine")
        self.routine_repo.soft_delete(routine.id)
    
    def toggle_routine(self, routine_id: UUID, user_id: UUID) -> Routine:
        """Toggle routine active/inactive"""
        routine = self.routine_repo.get_with_category(routine_id)
        if not routine or routine.user_id != user_id:
            raise NotFoundException("Routine")
        return self.routine_repo.toggle_active(routine)