from sqlalchemy import String, Date, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, BaseModel
from app.core.constants import TaskStatus
import uuid
from datetime import date, datetime


class ProjectTask(Base, BaseModel):
    """
    Tasks within a project.
    Example: GabbyOS → Design Database Schema, Implement Authentication, Create Category APIs
    """
    __tablename__ = "project_tasks"
    
    project_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )
    
    priority: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )
    
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus),
        default=TaskStatus.TODO
    )
    
    due_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )
    
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    
    def __repr__(self):
        return f"<ProjectTask {self.title}>"