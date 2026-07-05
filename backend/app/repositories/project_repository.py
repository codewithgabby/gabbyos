from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.project_task import ProjectTask
from app.repositories.base_repository import BaseRepository
from app.core.constants import TaskStatus


class ProjectRepository(BaseRepository[Project]):
    """Repository for Project model operations"""
    
    def __init__(self, db: Session):
        super().__init__(Project, db)
    
    def get_with_tasks(self, project_id: UUID) -> Optional[Project]:
        """Get a project with its tasks loaded"""
        return self.db.query(Project).filter(
            Project.id == project_id,
            Project.is_deleted == False
        ).first()
    
    def get_all_for_user(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Project]:
        """Get all projects with filters"""
        query = self.db.query(Project).filter(
            Project.user_id == user_id,
            Project.is_deleted == False
        )
        
        if status:
            query = query.filter(Project.status == status)
        
        if search:
            query = query.filter(
                Project.title.ilike(f"%{search}%") |
                Project.description.ilike(f"%{search}%")
            )
        
        return query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    
    def archive_project(self, project: Project) -> Project:
        """Archive a project"""
        project.status = "archived"
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def get_task_counts(self, project_id: UUID) -> tuple:
        """Get total and completed task counts for a project"""
        total = self.db.query(ProjectTask).filter(
            ProjectTask.project_id == project_id,
            ProjectTask.is_deleted == False
        ).count()
        
        completed = self.db.query(ProjectTask).filter(
            ProjectTask.project_id == project_id,
            ProjectTask.status == TaskStatus.COMPLETED,
            ProjectTask.is_deleted == False
        ).count()
        
        return total, completed