from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.db.session import SessionLocal
from app.core.security import decode_token
from app.core.exceptions import CredentialsException
from app.models.user import User
from app.config import settings


# Security scheme for Swagger UI
security_scheme = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.
    Session is automatically closed after request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency that extracts and validates the current user from JWT token.
    Use this to protect endpoints that require authentication.
    
    Usage:
        @router.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"message": f"Hello {current_user.full_name}"}
    """
    token = credentials.credentials
    
    # Decode token
    payload = decode_token(token)
    
    if payload is None:
        raise CredentialsException()
    
    # Verify it's an access token
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type. Access token required.",
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise CredentialsException()
    
    # Get user from database
    user = db.query(User).filter(
        User.id == user_id,
        User.is_deleted == False
    ).first()
    
    if user is None:
        raise CredentialsException()
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been deactivated.",
        )
    
    return user