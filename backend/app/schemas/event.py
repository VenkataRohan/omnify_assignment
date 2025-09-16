"""
Event schemas for request/response serialization.
"""

from datetime import datetime, timezone
from typing import List, Optional, Any
from pydantic import BaseModel, Field, validator

from app.schemas.base import BaseSchema


class EventBase(BaseSchema):
    """Base event schema with common fields."""
    
    name: str = Field(min_length=1, max_length=255, description="Event name")
    location: str = Field(min_length=1, max_length=255, description="Event location")
    start_time: datetime = Field(description="Event start date and time")
    end_time: datetime = Field(description="Event end date and time")
    max_capacity: int = Field(gt=0, description="Maximum number of attendees")

    @validator("end_time")
    def validate_end_after_start(cls, v, values):
        """Ensure end time is after start time."""
        if "start_time" in values and v <= values["start_time"]:
            raise ValueError("End time must be after start time")
        return v


class EventCreate(EventBase):
    """Schema for creating a new event."""
    
    @validator("start_time")
    def validate_future_start_time(cls, v):
        """Ensure event start time is in the future."""
        if v <= datetime.now(timezone.utc):
            raise ValueError("Event start time must be in the future")
        return v


class EventResponse(EventBase):
    """Schema for event responses."""
    
    id: int = Field(description="Event ID")
    current_attendees: int = Field(ge=0, description="Current number of attendees")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    
    # Computed fields
    is_full: bool = Field(description="Whether the event is at full capacity")
    available_spots: int = Field(ge=0, description="Number of available spots")
    capacity_percentage: float = Field(ge=0, le=100, description="Capacity utilization percentage")
    
    class Config:
        from_attributes = True


class EventWithAttendees(EventResponse):
    """Schema for event with attendees included."""
    
    attendees: List[Any] = Field(default=[], description="List of attendees")
