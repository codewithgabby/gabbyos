from typing import Generic, TypeVar, Type, Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base repository with common CRUD operations.
    All repositories inherit from this.
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db
    
    def get(self, id: UUID) -> Optional[ModelType]:
        """Get a single record by ID"""
        return self.db.query(self.model).filter(
            self.model.id == id,
            self.model.is_deleted == False
        ).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Get all active records with pagination"""
        return self.db.query(self.model).filter(
            self.model.is_deleted == False
        ).offset(skip).limit(limit).all()
    
    def create(self, obj_in: dict) -> ModelType:
        """Create a new record"""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def update(self, db_obj: ModelType, obj_in: dict) -> ModelType:
        """Update an existing record"""
        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
    
    def soft_delete(self, id: UUID) -> None:
        """Soft delete a record"""
        db_obj = self.get(id)
        if db_obj:
            db_obj.is_deleted = True
            from datetime import datetime
            db_obj.deleted_at = datetime.utcnow()
            self.db.commit()
    
    def count(self) -> int:
        """Count all active records"""
        return self.db.query(self.model).filter(
            self.model.is_deleted == False
        ).count()