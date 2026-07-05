from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status, Body
from sqlalchemy.orm import Session
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.schemas.project_task import ProjectTaskCreate, ProjectTaskUpdate, ProjectTaskResponse
from app.schemas.common import MessageResponse
from app.services.project_service import ProjectService
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])


# ─── PROJECT ENDPOINTS ───

@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a project"
)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new project."""
    service = ProjectService(db)
    return service.create_project(current_user.id, data)


@router.get(
    "",
    response_model=list[ProjectResponse],
    summary="Get all projects"
)
def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all projects with optional filters."""
    service = ProjectService(db)
    return service.get_all_projects(
        user_id=current_user.id, skip=skip, limit=limit,
        status=status, search=search
    )


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get a project"
)
def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a project by ID."""
    service = ProjectService(db)
    return service.get_project(UUID(project_id), current_user.id)


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update a project"
)
def update_project(
    project_id: str,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a project."""
    service = ProjectService(db)
    return service.update_project(UUID(project_id), current_user.id, data)


@router.delete(
    "/{project_id}",
    response_model=MessageResponse,
    summary="Delete a project"
)
def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a project and all its tasks."""
    service = ProjectService(db)
    service.delete_project(UUID(project_id), current_user.id)
    return MessageResponse(message="Project deleted successfully")


@router.patch(
    "/{project_id}/progress",
    response_model=ProjectResponse,
    summary="Update progress"
)
def update_progress(
    project_id: str,
    progress: float = Query(..., ge=0.0, le=100.0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update project progress percentage."""
    service = ProjectService(db)
    return service.update_progress(UUID(project_id), current_user.id, progress)


@router.patch(
    "/{project_id}/phase",
    response_model=ProjectResponse,
    summary="Update current phase"
)
def update_phase(
    project_id: str,
    phase: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update the current phase of a project."""
    service = ProjectService(db)
    return service.update_phase(UUID(project_id), current_user.id, phase)


@router.post(
    "/{project_id}/notes",
    response_model=ProjectResponse,
    summary="Add a note"
)
def add_note(
    project_id: str,
    note: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add a note to a project."""
    service = ProjectService(db)
    return service.add_note(UUID(project_id), current_user.id, note)


@router.patch(
    "/{project_id}/archive",
    response_model=ProjectResponse,
    summary="Archive project"
)
def archive_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Archive a project."""
    service = ProjectService(db)
    return service.archive_project(UUID(project_id), current_user.id)


# ─── TASK ENDPOINTS ───

@router.post(
    "/{project_id}/tasks",
    response_model=ProjectTaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task"
)
def create_task(
    project_id: str,
    data: ProjectTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a task within a project."""
    service = ProjectService(db)
    return service.create_task(UUID(project_id), current_user.id, data)


@router.get(
    "/{project_id}/tasks",
    response_model=list[ProjectTaskResponse],
    summary="Get project tasks"
)
def get_tasks(
    project_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all tasks for a project."""
    service = ProjectService(db)
    return service.get_tasks(UUID(project_id), current_user.id, skip, limit, status)


@router.patch(
    "/{project_id}/tasks/{task_id}",
    response_model=ProjectTaskResponse,
    summary="Update a task"
)
def update_task(
    project_id: str,
    task_id: str,
    data: ProjectTaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a task."""
    service = ProjectService(db)
    return service.update_task(UUID(task_id), UUID(project_id), current_user.id, data)


@router.patch(
    "/{project_id}/tasks/{task_id}/complete",
    response_model=ProjectTaskResponse,
    summary="Complete a task"
)
def complete_task(
    project_id: str,
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark a task as completed."""
    service = ProjectService(db)
    return service.complete_task(UUID(task_id), UUID(project_id), current_user.id)


@router.delete(
    "/{project_id}/tasks/{task_id}",
    response_model=MessageResponse,
    summary="Delete a task"
)
def delete_task(
    project_id: str,
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a task."""
    service = ProjectService(db)
    service.delete_task(UUID(task_id), UUID(project_id), current_user.id)
    return MessageResponse(message="Task deleted successfully")