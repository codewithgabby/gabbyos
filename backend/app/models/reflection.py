from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, BaseModel
import uuid
from datetime import date


class Reflection(Base, BaseModel):
    """
    Daily reflections for intentional living.
    Captures wins, challenges, gratitude, and tomorrow's focus.
    """
    __tablename__ = "reflections"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    reflection_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        unique=True
    )
    
    wins: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True
    )
    
    challenges: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True
    )
    
    gratitude: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True
    )
    
    tomorrow_focus: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True
    )
    
    mood_rating: Mapped[int | None] = mapped_column(
        nullable=True
    )
    
    # Relationships
    user = relationship("User", back_populates="reflections")
    
    def __repr__(self):
        return f"<Reflection {self.reflection_date}>"