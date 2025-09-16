"""
Attendee repository with attendee-specific database operations.
"""

from typing import List, Optional, Tuple
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attendee import Attendee
from app.repositories.base import BaseRepository
from app.schemas.attendee import AttendeeCreate
from app.schemas.base import PaginationParams


class AttendeeRepository(BaseRepository[Attendee, AttendeeCreate]):
    """
    Repository for Attendee model with attendee-specific operations.
    """
    
    def __init__(self, db: AsyncSession):
        super().__init__(Attendee, db)
    
    async def get_by_email_and_event(
        self, 
        email: str, 
        event_id: int
    ) -> Optional[Attendee]:
        """
        Get attendee by email and event ID.
        
        Args:
            email: Attendee email
            event_id: Event ID
            
        Returns:
            Optional[Attendee]: Attendee instance or None
        """
        result = await self.db.execute(
            select(Attendee).where(
                and_(
                    Attendee.email == email,
                    Attendee.event_id == event_id
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def get_attendees_by_event(
        self, 
        event_id: int, 
        pagination: Optional[PaginationParams] = None
    ) -> List[Attendee]:
        """
        Get all attendees for a specific event with optional pagination.
        
        Args:
            event_id: Event ID
            pagination: Optional pagination parameters
            
        Returns:
            List[Attendee]: List of attendees
        """
        query = select(Attendee).where(Attendee.event_id == event_id)
        print("pagination::", pagination)
        # Apply pagination if provided
        if pagination:
            query = query.offset(pagination.offset).limit(pagination.size)
            
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_attendees_by_event_with_count(
        self, 
        event_id: int, 
        pagination: PaginationParams
    ) -> Tuple[List[Attendee], int]:
        """
        Get attendees for a specific event with total count.
        
        Args:
            event_id: Event ID
            pagination: Pagination parameters
            
        Returns:
            Tuple[List[Attendee], int]: List of attendees and total count
        """
        # Get total count
        count_query = select(func.count(Attendee.id)).where(Attendee.event_id == event_id)
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0
        
        # Get paginated attendees
        attendees_query = (
            select(Attendee)
            .where(Attendee.event_id == event_id)
            .offset(pagination.offset)
            .limit(pagination.size)
        )
        attendees_result = await self.db.execute(attendees_query)
        attendees = attendees_result.scalars().all()
        
        return attendees, total

