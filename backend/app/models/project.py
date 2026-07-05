from sqlalchemy import String, Float, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, BaseModel
from app.core.constants import ProjectStatus
import uuid
from datetime import date


class Project(Base, BaseModel):
    """
    Projects you're building and managing.
    Examples: GabbyOS, Saleszy, AI Resume Analyzer, Portfolio Website
    """
    __tablename__ = "projects"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    description: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True
    )
    
    priority: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )
    
    status: Mapped[ProjectStatus] = mapped_column(
        SQLEnum(ProjectStatus),
        default=ProjectStatus.PLANNED
    )
    
    progress_percentage: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )
    
    current_phase: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    
    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )
    
    target_completion_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )
    
    notes: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        default=list
    )
    
    tags: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
        default=list
    )
    
    # Relationships
    user = relationship("User", back_populates="projects")
    tasks = relationship("ProjectTask", back_populates="project", lazy="dynamic", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project {self.title}>"