from sqlalchemy import String, Integer, Float, Date, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, BaseModel
from app.core.constants import KnowledgeStatus
import uuid
from datetime import date


class KnowledgeItem(Base, BaseModel):
    """
    Second Brain - capture everything you want to learn, remember, explore, or build.
    Examples: NumPy, Pandas, French Grammar, System Design, Book recommendations
    """
    __tablename__ = "knowledge_items"
    
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
        String(500),
        nullable=False
    )
    
    description: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True
    )
    
    tags: Mapped[list | None] = mapped_column(
        JSONB,
        nullable=True,
        default=list
    )
    
    priority: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )
    
    status: Mapped[KnowledgeStatus] = mapped_column(
        SQLEnum(KnowledgeStatus),
        default=KnowledgeStatus.INBOX
    )
    
    progress_percentage: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )
    
    source_link: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )
    
    notes: Mapped[str | None] = mapped_column(
        String(5000),
        nullable=True
    )
    
    target_completion_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )
    
    # Relationships
    user = relationship("User", back_populates="knowledge_items")
    category = relationship("Category", back_populates="knowledge_items")
    
    def __repr__(self):
        return f"<KnowledgeItem {self.title}>"