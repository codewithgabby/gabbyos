from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.project_task import ProjectTask
from app.repositories.base_repository import BaseRepository
from datetime import datetime


class ProjectTaskRepository(BaseRepository[ProjectTask]):
    """Repository for ProjectTask model operations"""
    
    def __init__(self, db: Session):
        super().__init__(ProjectTask, db)
    
    def get_by_project(
        self,
        project_id: UUID,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[ProjectTask]:
        """Get all tasks for a project"""
        query = self.db.query(ProjectTask).filter(
            ProjectTask.project_id == project_id,
            ProjectTask.is_deleted == False
        )
        
        if status:
            query = query.filter(ProjectTask.status == status)
        
        return query.order_by(ProjectTask.created_at.asc()).offset(skip).limit(limit).all()
    
    def complete_task(self, task: ProjectTask) -> ProjectTask:
        """Mark a task as completed"""
        task.status = "completed"
        task.completed_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(task)
        return task