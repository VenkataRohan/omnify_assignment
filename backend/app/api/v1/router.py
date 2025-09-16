"""
Main API router for version 1.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import events, attendees
from app.core.config import settings

api_router = APIRouter(prefix=f"/{settings.API_VERSION}")

# Include endpoint routers
api_router.include_router(
    events.router,
    prefix="/events",
    tags=["events"]
)

api_router.include_router(
    attendees.router,
    prefix="/events/{event_id}/attendees",
    tags=["attendees"]
)
