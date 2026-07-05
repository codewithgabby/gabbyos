from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, BaseModel
import uuid


class Category(Base, BaseModel):
    """
    Dynamic categories for organizing everything in GabbyOS.
    Examples: AI/ML, French, Public Speaking, Health, Family, etc.
    """
    __tablename__ = "categories"
    
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    
    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )
    
    color: Mapped[str | None] = mapped_column(
        String(7),
        nullable=True,
        default="#000000"
    )
    
    icon: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )
    
    # Relationships
    user = relationship("User", back_populates="categories")
    routines = relationship("Routine", back_populates="category", lazy="dynamic")
    knowledge_items = relationship("KnowledgeItem", back_populates="category", lazy="dynamic")
    goals = relationship("Goal", back_populates="category", lazy="dynamic")
    
    
    
    def __repr__(self):
        return f"<Category {self.name}>"