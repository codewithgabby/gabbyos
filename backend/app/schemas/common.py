from pydantic import BaseModel, ConfigDict, model_validator
from typing import Any
import uuid


class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    model_config = ConfigDict(from_attributes=True)


class BaseResponse(BaseSchema):
    """Base response that handles UUID to string conversion automatically"""
    id: str
    
    @model_validator(mode='before')
    @classmethod
    def convert_uuids(cls, data: Any) -> Any:
        """Convert UUID objects to strings for all fields"""
        if hasattr(data, '__dict__') or hasattr(data, '__table__'):
            # It's an ORM object
            result = {}
            for column in data.__table__.columns:
                value = getattr(data, column.name)
                if isinstance(value, uuid.UUID):
                    result[column.name] = str(value)
                else:
                    result[column.name] = value
            return result
        elif isinstance(data, dict):
            # Already a dict, convert any UUID values
            result = {}
            for key, value in data.items():
                if isinstance(value, uuid.UUID):
                    result[key] = str(value)
                else:
                    result[key] = value
            return result
        return data


class MessageResponse(BaseModel):
    """Schema for simple message responses"""
    message: str
    success: bool = True


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = 1
    page_size: int = 20