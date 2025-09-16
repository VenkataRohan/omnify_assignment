"""
Event model for the database.
"""

from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import DateTime, Integer, String, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.attendee import Attendee


class Event(BaseModel):
    """
    Event model representing an event in the system.
    
    Attributes:
        name: Event name
        location: Event location
        start_time: Event start date and time
        end_time: Event end date and time
        max_capacity: Maximum number of attendees
        current_attendees: Current number of registered attendees
        attendees: Relationship to attendee records
    """
    
    __tablename__ = "events"
    
    # Core fields
    name: Mapped[str] = mapped_column(
        String(255), 
        nullable=False, 
        index=True,
        comment="Event name"
    )
    location: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
        comment="Event location"
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        index=True,
        comment="Event start date and time"
    )
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        index=True,
        comment="Event end date and time"
    )
    max_capacity: Mapped[int] = mapped_column(
        Integer, 
        nullable=False,
        comment="Maximum number of attendees"
    )
    current_attendees: Mapped[int] = mapped_column(
        Integer, 
        default=0, 
        nullable=False,
        comment="Current number of registered attendees"
    )
    
    # Relationships
    attendees: Mapped[List["Attendee"]] = relationship(
        "Attendee",
        back_populates="event",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint('max_capacity > 0', name='check_max_capacity_positive'),
        CheckConstraint('current_attendees >= 0', name='check_current_attendees_non_negative'),
        CheckConstraint('current_attendees <= max_capacity', name='check_capacity_not_exceeded'),
        CheckConstraint('start_time < end_time', name='check_start_before_end'),
    )
    
    @property
    def is_full(self) -> bool:
        """Check if the event is at full capacity."""
        return self.current_attendees >= self.max_capacity
    
    @property
    def available_spots(self) -> int:
        """Get the number of available spots."""
        return max(0, self.max_capacity - self.current_attendees)
    
    @property
    def capacity_percentage(self) -> float:
        """Get the capacity utilization as a percentage."""
        if self.max_capacity == 0:
            return 0.0
        return (self.current_attendees / self.max_capacity) * 100
    
    def __repr__(self) -> str:
        """String representation of the event."""
        return f"<Event(id={self.id}, name='{self.name}', capacity={self.current_attendees}/{self.max_capacity})>"
