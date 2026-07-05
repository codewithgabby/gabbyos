from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base, BaseModel
from datetime import datetime


class User(Base, BaseModel):
    """
    User model for authentication and identity.
    Currently single-user, but architected for multi-user support.
    """
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    identity_statement: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )
    
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    refresh_token: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    # Relationships
    categories = relationship("Category", back_populates="user", lazy="dynamic")
    routines = relationship("Routine", back_populates="user", lazy="dynamic")
    weekly_plans = relationship("WeeklyPlan", back_populates="user", lazy="dynamic")
    daily_logs = relationship("DailyLog", back_populates="user", lazy="dynamic")
    reflections = relationship("Reflection", back_populates="user", lazy="dynamic")
    goals = relationship("Goal", back_populates="user", lazy="dynamic")
    knowledge_items = relationship("KnowledgeItem", back_populates="user", lazy="dynamic")
    projects = relationship("Project", back_populates="user", lazy="dynamic")
    inbox_items = relationship("InboxItem", back_populates="user", lazy="dynamic")


    def __repr__(self):
        return f"<User {self.email}>"