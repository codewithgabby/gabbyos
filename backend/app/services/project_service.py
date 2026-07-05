from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.project import Project
from app.models.project_task import ProjectTask
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.schemas.project_task import ProjectTaskCreate, ProjectTaskUpdate
from app.repositories.project_repository import ProjectRepository
from app.repositories.project_task_repository import ProjectTaskRepository
from app.core.constants import TaskStatus
from app.core.exceptions import NotFoundException
from datetime import datetime


class ProjectService:
    """Service for project operations"""
    
    def __init__(self, db: Session):
        self.project_repo = ProjectRepository(db)
        self.task_repo = ProjectTaskRepository(db)
    
    # Project methods
    def create_project(self, user_id: UUID, data: ProjectCreate) -> Project:
        """Create a new project"""
        project_dict = data.model_dump()
        project_dict["user_id"] = user_id
        return self.project_repo.create(project_dict)
    
    def get_project(self, project_id: UUID, user_id: UUID) -> Project:
        """Get a project"""
        project = self.project_repo.get_with_tasks(project_id)
        if not project or project.user_id != user_id:
            raise NotFoundException("Project")
        return project
    
    def get_all_projects(
        self,
        user_id: UUID,
        skip: int = 0,
        limit: int = 50,
        status: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Project]:
        """Get all projects"""
        return self.project_repo.get_all_for_user(
            user_id=user_id, skip=skip, limit=limit,
            status=status, search=search
        )
    
    def update_project(
        self, project_id: UUID, user_id: UUID, data: ProjectUpdate
    ) -> Project:
        """Update a project"""
        project = self.project_repo.get(project_id)
        if not project or project.user_id != user_id:
            raise NotFoundException("Project")
        
        update_dict = data.model_dump(exclude_unset=True)
        return self.project_repo.update(project, update_dict)
    
    def delete_project(self, project_id: UUID, user_id: UUID) -> None:
        """Delete a project and its tasks"""
        project = self.project_repo.get(project_id)
        if not project or project.user_id != user_id:
            raise NotFoundException("Project")
        self.project_repo.soft_delete(project.id)
    
    def update_progress(
        self, project_id: UUID, user_id: UUID, progress: float
    ) -> Project:
        """Update project progress"""
        project = self.project_repo.get(project_id)
        if not project or project.user_id != user_id:
            raise NotFoundException("Project")
        return self.project_repo.update(project, {"progress_percentage": progress})
    
    def update_phase(
        self, project_id: UUID, user_id: UUID, phase: str
    ) -> Project:
        """Update current phase"""
        project = self.project_repo.get(project_id)
        if not project or project.user_id != user_id:
            raise NotFoundException("Project")
        return self.project_repo.update(project, {"current_phase": phase})
    
    def add_note(
        self, project_id: UUID, user_id: UUID, note: str
    ) -> Project:
        """Add a note to project"""
        project = self.project_repo.get(project_id)
        if not project or project.user_id != user_id:
            raise NotFoundException("Project")
        
        notes = project.notes or []
        notes.append(note)
        return self.project_repo.update(project, {"notes": notes})
    
    def archive_project(self, project_id: UUID, user_id: UUID) -> Project:
        """Archive a project"""
        project = self.project_repo.get(project_id)
        if not project or project.user_id != user_id:
            raise NotFoundException("Project")
        return self.project_repo.archive_project(project)
    
    # Task methods
    def create_task(
        self, project_id: UUID, user_id: UUID, data: ProjectTaskCreate
    ) -> ProjectTask:
        """Create a task within a project"""
        project = self.project_repo.get(project_id)
        if not project or project.user_id != user_id:
            raise NotFoundException("Project")
        
        task_dict = data.model_dump()
        task_dict["project_id"] = project_id
        return self.task_repo.create(task_dict)
    
    def get_tasks(
        self,
        project_id: UUID,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[ProjectTask]:
        """Get tasks for a project"""
        project = self.project_repo.get(project_id)
        if not project or project.user_id != user_id:
            raise NotFoundException("Project")
        return self.task_repo.get_by_project(project_id, skip, limit, status)
    
    def update_task(
        self, task_id: UUID, project_id: UUID, user_id: UUID, data: ProjectTaskUpdate
    ) -> ProjectTask:
        """Update a task"""
        project = self.project_repo.get(project_id)
        if not project or project.user_id != user_id:
            raise NotFoundException("Project")
        
        task = self.task_repo.get(task_id)
        if not task or task.project_id != project_id:
            raise NotFoundException("Task")
        
        update_dict = data.model_dump(exclude_unset=True)
        
        if update_dict.get("status") == TaskStatus.COMPLETED and task.status != TaskStatus.COMPLETED:
            update_dict["completed_at"] = datetime.utcnow()
        
        return self.task_repo.update(task, update_dict)
    
    def complete_task(
        self, task_id: UUID, project_id: UUID, user_id: UUID
    ) -> ProjectTask:
        """Mark a task as completed"""
        project = self.project_repo.get(project_id)
        if not project or project.user_id != user_id:
            raise NotFoundException("Project")
        
        task = self.task_repo.get(task_id)
        if not task or task.project_id != project_id:
            raise NotFoundException("Task")
        
        return self.task_repo.complete_task(task)
    
    def delete_task(
        self, task_id: UUID, project_id: UUID, user_id: UUID
    ) -> None:
        """Delete a task"""
        project = self.project_repo.get(project_id)
        if not project or project.user_id != user_id:
            raise NotFoundException("Project")
        
        task = self.task_repo.get(task_id)
        if not task or task.project_id != project_id:
            raise NotFoundException("Task")
        
        self.task_repo.soft_delete(task.id)