from sqlalchemy import String, Integer, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, BaseModel
from app.core.constants import Priority
import uuid


class Routine(Base, BaseModel):
    """
    Routines are the core daily disciplines in GabbyOS.
    Each routine belongs to a category and has a reason_why
    connecting it to your identity and goals.
    
    Examples:
    - AI/ML Class (Category: AI/ML, Priority: High)
    - French Learning (Category: French, Priority: Medium)
    - Exercise (Category: Health, Priority: High)
    """
    __tablename__ = "routines"
    
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
    
    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        default=30
    )
    
    reason_why: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )
    
    priority: Mapped[Priority] = mapped_column(
        SQLEnum(Priority),
        default=Priority.MEDIUM
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0
    )
    
    # Relationships
    user = relationship("User", back_populates="routines")
    category = relationship("Category", back_populates="routines")
    weekly_plan_items = relationship("WeeklyPlanItem", back_populates="routine")
    daily_logs = relationship("DailyLog", back_populates="routine", lazy="dynamic")
    streak = relationship("Streak", back_populates="routine", uselist=False)


    def __repr__(self):
        return f"<Routine {self.title}>"