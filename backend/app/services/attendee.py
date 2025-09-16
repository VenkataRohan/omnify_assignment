"""
Attendee service with business logic for attendee management.
"""

from typing import List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.models.attendee import Attendee
from app.repositories.attendee import AttendeeRepository
from app.repositories.event import EventRepository
from app.schemas.attendee import AttendeeCreate
from app.schemas.base import PaginationParams
from app.services.exceptions import (
    AttendeeAlreadyRegisteredError,
    EventNotFoundError,
    EventCapacityExceededError
)

logger = get_logger(__name__)


class AttendeeService:
    """
    Service class for attendee business logic.
    
    This class handles all business logic related to attendees,
    including registration, validation, and capacity management.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize attendee service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.attendee_repo = AttendeeRepository(db)
        self.event_repo = EventRepository(db)
    
    async def get_event_attendees(self, event_id: int) -> List[Attendee]:
        """
        Get attendees for a specific event.
        
        Args:
            event_id: Event ID
            
        Returns:
            List[Attendee]: List of attendees
            
        Raises:
            EventNotFoundError: If event not found
        """
        # Verify event exists
        event = await self.event_repo.get(event_id)
        if not event:
            raise EventNotFoundError(f"Event with ID {event_id} not found")
        
        return await self.attendee_repo.get_attendees_by_event(event_id)
    
    async def register_attendee(
        self,
        event_id: int,
        attendee_data: AttendeeCreate
    ) -> Attendee:
        """
        Register an attendee for an event.
        
        Args:
            event_id: Event ID
            attendee_data: Attendee registration data
            
        Returns:
            Attendee: Registered attendee
            
        Raises:
            EventNotFoundError: If event not found
            EventCapacityExceededError: If event is full
            AttendeeAlreadyRegisteredError: If attendee already registered
        """
        # Verify event exists
        event = await self.event_repo.get(event_id)
        if not event:
            raise EventNotFoundError(f"Event with ID {event_id} not found")
        
        # Check if event is full
        if event.is_full:
            logger.warning(f"Event {event_id} is at full capacity")
            raise EventCapacityExceededError(f"Event '{event.name}' is at full capacity")
        
        # Check if attendee is already registered
        existing_attendee = await self.attendee_repo.get_by_email_and_event(
            attendee_data.email, event_id
        )
        if existing_attendee:
            logger.warning(f"Attendee {attendee_data.email} already registered for event {event_id}")
            raise AttendeeAlreadyRegisteredError(
                f"Attendee with email '{attendee_data.email}' is already registered for this event"
            )
        
        # Create attendee record
        attendee_dict = attendee_data.model_dump()
        attendee_dict["event_id"] = event_id
        
        # Use a transaction to ensure consistency
        try:
            # Create attendee
            attendee = await self.attendee_repo.create(
                AttendeeCreate(**attendee_dict)
            )
            
            # Increment event attendee count
            await self.event_repo.increment_attendee_count(event_id)
            
            logger.info(f"Attendee registered: {attendee.email} for event {event_id}")
            return attendee
        
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to register attendee: {e}")
            raise

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.models.attendee import Attendee
from app.repositories.attendee import AttendeeRepository
from app.repositories.event import EventRepository
from app.schemas.attendee import AttendeeCreate
from app.schemas.base import PaginationParams
from app.services.exceptions import (
    AttendeeNotFoundError,
    AttendeeAlreadyRegisteredError,
    EventNotFoundError,
    EventCapacityExceededError
)

logger = get_logger(__name__)


class AttendeeService:
    """
    Service class for attendee business logic.
    
    This class handles all business logic related to attendees,
    including registration, validation, and capacity management.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize attendee service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.attendee_repo = AttendeeRepository(db)
        self.event_repo = EventRepository(db)
    
    async def get_attendee(self, attendee_id: int) -> Attendee:
        """
        Get attendee by ID.
        
        Args:
            attendee_id: Attendee ID
            
        Returns:
            Attendee: Attendee instance
            
        Raises:
            AttendeeNotFoundError: If attendee not found
        """
        attendee = await self.attendee_repo.get(attendee_id)
        if not attendee:
            logger.warning(f"Attendee not found: {attendee_id}")
            raise AttendeeNotFoundError(f"Attendee with ID {attendee_id} not found")
        return attendee
    
    async def get_event_attendees(
        self,
        event_id: int,
        pagination: PaginationParams
    ) -> Tuple[List[Attendee], int]:
        """
        Get attendees for a specific event with pagination.
        
        Args:
            event_id: Event ID
            pagination: Pagination parameters
            
        Returns:
            Tuple[List[Attendee], int]: List of attendees and total count
            
        Raises:
            EventNotFoundError: If event not found
        """
        # Verify event exists
        event = await self.event_repo.get(event_id)
        if not event:
            raise EventNotFoundError(f"Event with ID {event_id} not found")
        
        return await self.attendee_repo.get_attendees_by_event_with_count(event_id, pagination)
    
    async def register_attendee(
        self,
        event_id: int,
        attendee_data: AttendeeCreate
    ) -> Attendee:
        """
        Register an attendee for an event.
        
        Args:
            event_id: Event ID
            attendee_data: Attendee registration data
            
        Returns:
            Attendee: Registered attendee
            
        Raises:
            EventNotFoundError: If event not found
            EventCapacityExceededError: If event is full
            AttendeeAlreadyRegisteredError: If attendee already registered
        """
        # Verify event exists
        event = await self.event_repo.get(event_id)
        if not event:
            raise EventNotFoundError(f"Event with ID {event_id} not found")
        
        # Check if event is full
        if event.is_full:
            logger.warning(f"Event {event_id} is at full capacity")
            raise EventCapacityExceededError(f"Event '{event.name}' is at full capacity")
        
        # Check if attendee is already registered
        existing_attendee = await self.attendee_repo.get_by_email_and_event(
            attendee_data.email, event_id
        )
        if existing_attendee:
            logger.warning(f"Attendee {attendee_data.email} already registered for event {event_id}")
            raise AttendeeAlreadyRegisteredError(
                f"Attendee with email '{attendee_data.email}' is already registered for this event"
            )
        
        # Create attendee record
        attendee_dict = attendee_data.model_dump()
        attendee_dict["event_id"] = event_id
        
        # Use a transaction to ensure consistency
        try:
            # Create attendee
            attendee = await self.attendee_repo.create(
                AttendeeCreate(**attendee_dict)
            )
            # Increment event attendee count
            await self.event_repo.increment_attendee_count(event_id)
            
            logger.info(f"Attendee registered: {attendee.email} for event {event_id}")
            return attendee
        
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Failed to register attendee: {e}")
            raise
    
    async def is_attendee_registered(self, event_id: int, email: str) -> bool:
        """
        Check if an attendee is registered for an event.
        
        Args:
            event_id: Event ID
            email: Attendee email
            
        Returns:
            bool: True if registered
        """
        return await self.attendee_repo.is_registered(email, event_id)
