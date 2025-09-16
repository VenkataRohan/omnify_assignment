"""
Attendee model for the database.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.event import Event


class Attendee(BaseModel):
    """
    Attendee model representing event attendees.
    
    Attributes:
        name: Attendee name
        email: Attendee email address
        event_id: Foreign key to the event
        registered_at: Registration timestamp
        event: Relationship to the event
    """
    
    __tablename__ = "attendees"
    
    # Core fields
    name: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
        comment="Attendee name"
    )
    email: Mapped[str] = mapped_column(
        String(255), 
        nullable=False, 
        index=True,
        comment="Attendee email address"
    )
    event_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Foreign key to the event"
    )
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        comment="Registration timestamp"
    )
    
    # Relationships
    event: Mapped["Event"] = relationship(
        "Event",
        back_populates="attendees",
        lazy="selectin"
    )
    
    # Constraints
    __table_args__ = (
        UniqueConstraint(
            'email', 
            'event_id', 
            name='uix_attendee_email_event'
        ),
    )
    
    def __repr__(self) -> str:
        """String representation of the attendee."""
        return f"<Attendee(id={self.id}, name='{self.name}', email='{self.email}', event_id={self.event_id})>"
