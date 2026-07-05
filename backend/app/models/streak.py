from sqlalchemy import Integer, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, BaseModel
import uuid
from datetime import date


class Streak(Base, BaseModel):
    """
    Tracks consistency streaks for each routine.
    Auto-calculated when daily logs are completed.
    """
    __tablename__ = "streaks"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    routine_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("routines.id"),
        nullable=False,
        unique=True
    )
    
    current_streak: Mapped[int] = mapped_column(
        Integer,
        default=0
    )
    
    longest_streak: Mapped[int] = mapped_column(
        Integer,
        default=0
    )
    
    last_activity_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )
    
    # Relationships
    user = relationship("User", viewonly=True)
    routine = relationship("Routine", back_populates="streak")
    
    def __repr__(self):
        return f"<Streak {self.routine_id}: {self.current_streak} days>"