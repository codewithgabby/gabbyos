from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, BaseModel
import uuid


class InboxItem(Base, BaseModel):
    """
    Quick capture inbox for ideas, thoughts, and things to organize later.
    Examples: "Learn Redis", "Read Atomic Habits again", "Build AI recommendation engine"
    """
    __tablename__ = "inbox_items"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    content: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )
    
    category_hint: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    
    is_organized: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    
    organized_to: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )
    
    # Relationships
    user = relationship("User", back_populates="inbox_items")
    
    def __repr__(self):
        return f"<InboxItem {self.content[:50]}>"