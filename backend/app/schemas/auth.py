from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=100,
        description="Password must be at least 8 characters"
    )
    full_name: str = Field(
        min_length=2,
        max_length=255,
        description="Your full name"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "gabby@example.com",
                "password": "strongpassword123",
                "full_name": "Gabby"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "gabby@example.com",
                "password": "strongpassword123"
            }
        }


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    
    
class TokenRefresh(BaseModel):
    """Schema for refreshing access token"""
    refresh_token: str


from app.schemas.common import BaseResponse

class UserResponse(BaseResponse):
    """Schema for user data in responses"""
    email: str
    full_name: str
    identity_statement: Optional[str] = None
    is_active: bool
    created_at: datetime

