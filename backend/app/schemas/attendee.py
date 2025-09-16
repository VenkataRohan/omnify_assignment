"""
Attendee schemas for request/response serialization.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator

from app.schemas.base import BaseSchema


class AttendeeBase(BaseSchema):
    """Base attendee schema with common fields."""
    
    name: str = Field(min_length=1, max_length=255, description="Attendee name")
    email: EmailStr = Field(description="Attendee email address")
    
    @validator("name")
    def validate_name(cls, v):
        """Validate attendee name."""
        if not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class AttendeeCreate(AttendeeBase):
    """Schema for registering a new attendee."""
    event_id: int = Field(gt=0, description="Event ID")


class AttendeeResponse(AttendeeBase):
    """Schema for attendee responses."""
    
    id: int = Field(description="Attendee ID")
    event_id: int = Field(description="Event ID")
    registered_at: datetime = Field(description="Registration timestamp")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    
    class Config:
        from_attributes = True
