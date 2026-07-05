from sqlalchemy import String, Integer, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, BaseModel
from app.core.constants import DayOfWeek
import uuid
from datetime import date


class WeeklyPlan(Base, BaseModel):
    """
    Weekly plans for organizing routines across days.
    Created every weekend for the upcoming week.
    """
    __tablename__ = "weekly_plans"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    week_start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    
    week_end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    
    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    
    week_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    
    notes: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )
    
    # Relationships
    user = relationship("User", back_populates="weekly_plans")
    items = relationship(
        "WeeklyPlanItem",
        back_populates="weekly_plan",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<WeeklyPlan Week {self.week_number}, {self.year}>"


class WeeklyPlanItem(Base, BaseModel):
    """
    Individual routine assignments within a weekly plan.
    Each item links a routine to a specific day.
    """
    __tablename__ = "weekly_plan_items"
    
    plan_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("weekly_plans.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    routine_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("routines.id"),
        nullable=False,
        index=True
    )
    
    day_of_week: Mapped[DayOfWeek] = mapped_column(
        SQLEnum(DayOfWeek),
        nullable=False
    )
    
    custom_time: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )
    
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0
    )
    
    # Relationships
    weekly_plan = relationship("WeeklyPlan", back_populates="items")
    routine = relationship("Routine", back_populates="weekly_plan_items")
    
    def __repr__(self):
        return f"<WeeklyPlanItem {self.day_of_week}: {self.routine_id}>"