"""
Attendee endpoints for the API.
"""

from typing import List, Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.attendee import AttendeeService
from app.services.exceptions import (
    AttendeeNotFoundError,
    AttendeeAlreadyRegisteredError,
    EventNotFoundError,
    EventCapacityExceededError
)
from app.schemas.attendee import (
    AttendeeBase,
    AttendeeResponse
)

from app.schemas.base import PaginationParams, SuccessResponse, PaginatedResponse

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[AttendeeResponse])
async def get_event_attendees(
    event_id: Annotated[int, Path(description="Event ID")],
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db)
) -> PaginatedResponse[AttendeeResponse]:
    """
    Get all attendees for a specific event.

    Args:
        event_id: Event ID
        pagination: Pagination parameters
        db: Database session

    Returns:
        PaginatedResponse[AttendeeResponse]: Paginated list of attendees

    Raises:
        HTTPException: If event not found
    """
    
    service = AttendeeService(db)
    
    try:
        attendees, total = await service.get_event_attendees(event_id, pagination)
        
        return PaginatedResponse.create(
            data=[AttendeeResponse.model_validate(attendee) for attendee in attendees],
            page=pagination.page,
            size=pagination.size,
            total=total,
            message="Attendees retrieved successfully"
        )
    except EventNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/", response_model=SuccessResponse[AttendeeResponse], status_code=status.HTTP_201_CREATED)
async def register_attendee(
    event_id: Annotated[int, Path(description="Event ID")],
    attendee_data: AttendeeBase,
    db: AsyncSession = Depends(get_db)
) -> SuccessResponse[AttendeeResponse]:
    """
    Register a new attendee for an event.
    
    Args:
        event_id: Event ID
        attendee_data: Attendee registration data
        db: Database session
        
    Returns:
        SuccessResponse[AttendeeResponse]: Registered attendee
        
    Raises:
        HTTPException: If validation fails, event not found, or capacity exceeded
    """
    service = AttendeeService(db)
    
    try:
        attendee = await service.register_attendee(event_id, attendee_data)
        return SuccessResponse(
            data=AttendeeResponse.model_validate(attendee),
            message="Attendee registered successfully"
        )
    except EventNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except EventCapacityExceededError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except AttendeeAlreadyRegisteredError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
