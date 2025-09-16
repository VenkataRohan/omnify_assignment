"""
Event service with business logic for event management.
"""

from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.models.event import Event
from app.repositories.event import EventRepository
from app.schemas.event import EventCreate
from app.services.exceptions import (
    EventNotFoundError,
    EventAlreadyExistsError,
    EventValidationError
)

logger = get_logger(__name__)


class EventService:
    """
    Service class for event business logic.
    
    This class handles all business logic related to events,
    including validation, capacity management, and data consistency.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize event service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.event_repo = EventRepository(db)
    
    async def get_upcoming_events(self) -> List[Event]:
        """
        Get upcoming events.
        
        Returns:
            List[Event]: List of upcoming events
        """
        return await self.event_repo.get_upcoming_events()
    
    async def create_event(self, event_data: EventCreate) -> Event:
        """
        Create a new event.
        
        Args:
            event_data: Event creation data
            
        Returns:
            Event: Created event
            
        Raises:
            EventAlreadyExistsError: If event with same name exists
            EventValidationError: If validation fails
        """
        # Check if event with same name already exists
        existing_event = await self.event_repo.get_by_name(event_data.name)
        if existing_event:
            logger.warning(f"Event already exists: {event_data.name}")
            raise EventAlreadyExistsError(f"Event with name '{event_data.name}' already exists")
        
        # Create event
        event = await self.event_repo.create(event_data)
        logger.info(f"Event created: {event.id} - {event.name}")
        return event
