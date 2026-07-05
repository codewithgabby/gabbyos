from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model operations"""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(
            User.email == email,
            User.is_deleted == False
        ).first()
    
    def get_by_refresh_token(self, user_id: str, refresh_token: str) -> Optional[User]:
        """Get user by ID and refresh token"""
        return self.db.query(User).filter(
            User.id == user_id,
            User.refresh_token == refresh_token,
            User.is_deleted == False
        ).first()
    
    def update_last_login(self, user: User) -> User:
        """Update user's last login timestamp"""
        from datetime import datetime
        user.last_login = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_refresh_token(self, user: User, token: Optional[str]) -> User:
        """Update or clear user's refresh token"""
        user.refresh_token = token
        self.db.commit()
        self.db.refresh(user)
        return user