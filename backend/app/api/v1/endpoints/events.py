"""
Event endpoints for the API.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.event import EventService
from app.services.exceptions import (
    EventAlreadyExistsError,
    EventValidationError
)
from app.schemas.event import (
    EventCreate,
    EventResponse
)
from app.schemas.base import SuccessResponse

router = APIRouter()


@router.get("/", response_model=SuccessResponse[List[EventResponse]])
async def get_events(
    db: AsyncSession = Depends(get_db)
) -> SuccessResponse[List[EventResponse]]:
    """
    Get all upcoming events.
    
    Args:
        db: Database session
        
    Returns:
        SuccessResponse[List[EventResponse]]: List of events
    """
    service = EventService(db)
    
    try:
        events = await service.get_upcoming_events()
        
        # Convert events to response format
        event_responses = []
        for event in events:
            event_dict = {
                "id": event.id,
                "name": event.name,
                "location": event.location,
                "start_time": event.start_time,
                "end_time": event.end_time,
                "max_capacity": event.max_capacity,
                "current_attendees": event.current_attendees,
                "created_at": event.created_at,
                "updated_at": event.updated_at,
                "is_full": event.is_full,
                "available_spots": event.available_spots,
                "capacity_percentage": event.capacity_percentage
            }
            event_responses.append(EventResponse(**event_dict))
        
        return SuccessResponse(
            data=event_responses,
            message="Events retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/", response_model=SuccessResponse[EventResponse], status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreate,
    db: AsyncSession = Depends(get_db)
) -> SuccessResponse[EventResponse]:
    """
    Create a new event.
    
    Args:
        event_data: Event creation data
        db: Database session
        
    Returns:
        SuccessResponse[EventResponse]: Created event
        
    Raises:
        HTTPException: If validation fails or event already exists
    """
    service = EventService(db)
    
    try:
        event = await service.create_event(event_data)
        return SuccessResponse(
            data=EventResponse.model_validate(event),
            message="Event created successfully"
        )
    except EventAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except EventValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
