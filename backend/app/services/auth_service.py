from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserCreate
from app.repositories.user_repository import UserRepository
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.core.exceptions import (
    CredentialsException,
    InactiveUserException,
    AlreadyExistsException
)


class AuthService:
    """Authentication service using repository pattern"""
    
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
    
    def register_user(self, user_data: UserCreate) -> User:
        """Register a new user"""
        # Check if user already exists
        existing_user = self.user_repo.get_by_email(user_data.email)
        
        if existing_user:
            raise AlreadyExistsException("User with this email")
        
        # Create new user
        user_dict = {
            "email": user_data.email,
            "password_hash": get_password_hash(user_data.password),
            "full_name": user_data.full_name,
            "is_active": True
        }
        
        return self.user_repo.create(user_dict)
    
    def login_user(self, email: str, password: str) -> dict:
        """Authenticate user and return tokens"""
        user = self.user_repo.get_by_email(email)
        
        if not user:
            raise CredentialsException()
        
        if not verify_password(password, user.password_hash):
            raise CredentialsException()
        
        if not user.is_active:
            raise InactiveUserException()
        
        # Create tokens
        token_data = {
            "sub": str(user.id),
            "email": user.email
        }
        
        access_token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)
        
        # Update user
        self.user_repo.update_last_login(user)
        self.user_repo.update_refresh_token(user, refresh_token)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 1800,
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name
            }
        }
    
    def refresh_access_token(self, refresh_token: str) -> dict:
        """Generate new access token from refresh token"""
        payload = decode_token(refresh_token)
        
        if not payload or payload.get("type") != "refresh":
            raise CredentialsException()
        
        user_id = payload.get("sub")
        user = self.user_repo.get_by_refresh_token(user_id, refresh_token)
        
        if not user:
            raise CredentialsException()
        
        token_data = {
            "sub": str(user.id),
            "email": user.email
        }
        
        new_access_token = create_access_token(data=token_data)
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": 1800
        }
    
    def logout_user(self, user_id: str) -> None:
        """Logout user by clearing refresh token"""
        user = self.user_repo.get(user_id)
        if user:
            self.user_repo.update_refresh_token(user, None)
    
    def get_current_user(self, user_id: str) -> User:
        """Get current user by ID"""
        user = self.user_repo.get(user_id)
        if not user:
            raise CredentialsException()
        return user