from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.auth import (
    UserCreate, UserLogin, TokenResponse, TokenRefresh,
    UserResponse
)
from app.schemas.common import MessageResponse
from app.services.auth_service import AuthService
from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account."""
    auth_service = AuthService(db)
    return auth_service.register_user(user_data)


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and get access token"
)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password."""
    auth_service = AuthService(db)
    return auth_service.login_user(credentials.email, credentials.password)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token"
)
def refresh_token(refresh_data: TokenRefresh, db: Session = Depends(get_db)):
    """Get a new access token using refresh token."""
    auth_service = AuthService(db)
    return auth_service.refresh_access_token(refresh_data.refresh_token)


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Logout user"
)
def logout(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Logout by invalidating refresh token."""
    auth_service = AuthService(db)
    auth_service.logout_user(str(current_user.id))
    return MessageResponse(message="Successfully logged out")


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user"
)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user