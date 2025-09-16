"""
Event repository with event-specific database operations.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, asc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.repositories.base import BaseRepository
from app.schemas.event import EventCreate
from app.core.logging import get_logger

logger = get_logger(__name__)

class EventRepository(BaseRepository[Event, EventCreate]):
    """
    Repository for Event model with event-specific operations.
    """
    
    def __init__(self, db: AsyncSession):
        super().__init__(Event, db)
    
    async def get_by_name(self, name: str) -> Optional[Event]:
        """
        Get event by name.
        
        Args:
            name: Event name
            
        Returns:
            Optional[Event]: Event instance or None
        """
        result = await self.db.execute(
            select(Event).where(Event.name == name)
        )
        return result.scalar_one_or_none()
    
    async def get_upcoming_events(self) -> List[Event]:
        """
        Get upcoming events (future start_time).
        
        Returns:
            List[Event]: List of upcoming events
        """
        query = select(Event).where(
            Event.start_time > datetime.utcnow()
        ).order_by(asc(Event.start_time))
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def increment_attendee_count(self, event_id: int) -> None:
        """
        Increment the attendee count for an event.
        
        Args:
            event_id: Event ID
        """
        event = await self.get(event_id)
        if event:
            event.current_attendees += 1
            await self.db.commit()
    
    async def decrement_attendee_count(self, event_id: int) -> None:
        """
        Decrement the attendee count for an event.
        
        Args:
            event_id: Event ID
        """
        event = await self.get(event_id)
        if event and event.current_attendees > 0:
            event.current_attendees -= 1
            await self.db.commit()
