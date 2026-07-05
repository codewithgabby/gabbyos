from sqlalchemy import String, Date, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, BaseModel
from app.core.constants import LogStatus
import uuid
from datetime import date, datetime


class DailyLog(Base, BaseModel):
    """
    Daily logs track the completion status of each routine.
    One log per routine per day.
    """
    __tablename__ = "daily_logs"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    routine_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("routines.id"),
        nullable=False,
        index=True
    )
    
    log_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True
    )
    
    status: Mapped[LogStatus] = mapped_column(
        SQLEnum(LogStatus),
        default=LogStatus.NOT_STARTED
    )
    
    notes: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True
    )
    
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    # Relationships
    user = relationship("User", back_populates="daily_logs")
    routine = relationship("Routine", back_populates="daily_logs")
    
    def __repr__(self):
        return f"<DailyLog {self.log_date}: {self.routine_id}>"