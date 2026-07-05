from sqlalchemy import String, Float, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, BaseModel
from app.core.constants import GoalStatus
import uuid
from datetime import date


class Goal(Base, BaseModel):
    """
    Long-term goals that give purpose to daily routines.
    Examples: Make ₦5M, Finish Python Fundamentals, Reach A1 French
    """
    __tablename__ = "goals"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
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
    
    target_value: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    
    current_progress: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    
    status: Mapped[GoalStatus] = mapped_column(
        SQLEnum(GoalStatus),
        default=GoalStatus.NOT_STARTED
    )
    
    deadline: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )
    
    # Relationships
    user = relationship("User", back_populates="goals")
    category = relationship("Category", back_populates="goals")
    
    def __repr__(self):
        return f"<Goal {self.title}>"