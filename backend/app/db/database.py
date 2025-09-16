"""
Database configuration and session management.
"""

from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.
    
    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables() -> None:
    """Create all database tables and populate with sample data if empty."""
    # Import models to ensure they are registered with the Base metadata
    from app.models import Event, Attendee, BaseModel
    
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    
    # Check if database is empty and populate with sample data
    await create_sample_data()


async def create_sample_data() -> None:
    """Create sample data if the database is empty."""
    from datetime import datetime, timedelta
    from app.models.event import Event
    from app.models.attendee import Attendee
    from app.db.sample_names import get_random_attendees
    
    async with AsyncSessionLocal() as session:
        # Check if we already have data
        result = await session.execute(
            text("SELECT COUNT(*) FROM events")
        )
        event_count = result.scalar()
        
        if event_count > 0:
            # Database already has data, skip sample data creation
            return
        
        # Create sample events
        sample_events = [
            Event(
                name="Tech Conference 2025",
                location="San Francisco Convention Center",
                start_time=datetime.now() + timedelta(days=30),
                end_time=datetime.now() + timedelta(days=30, hours=8),
                max_capacity=50,
                current_attendees=0
            ),
            Event(
                name="Web Development Workshop",
                location="Online",
                start_time=datetime.now() + timedelta(days=15),
                end_time=datetime.now() + timedelta(days=15, hours=4),
                max_capacity=100,
                current_attendees=0
            ),
            Event(
                name="AI & Machine Learning Summit",
                location="India Tech Hub",
                start_time=datetime.now() + timedelta(days=45),
                end_time=datetime.now() + timedelta(days=47),
                max_capacity=300,
                current_attendees=0
            ),
            Event(
                name="Startup Networking Event",
                location="Austin Convention Center",
                start_time=datetime.now() + timedelta(days=20),
                end_time=datetime.now() + timedelta(days=20, hours=3),
                max_capacity=150,
                current_attendees=0
            ),
            Event(
                name="Design Thinking Masterclass",
                location="Seattle Design Center",
                start_time=datetime.now() + timedelta(days=60),
                end_time=datetime.now() + timedelta(days=60, hours=6),
                max_capacity=80,
                current_attendees=0
            )
        ]
        
        # Add events to session
        for event in sample_events:
            session.add(event)
        
        # Flush to get event IDs
        await session.flush()
        
        # Create sample attendees for each event
        sample_attendees = []
        
        
        # Tech Conference 2025 attendees (48 attendees - nearly sold out)
        tech_conf_attendees = get_random_attendees(48)
        
        for name, email in tech_conf_attendees:
            attendee = Attendee(
                name=name,
                email=email,
                event_id=sample_events[0].id,
                registered_at=datetime.now() - timedelta(days=5)
            )
            sample_attendees.append(attendee)
        
        web_workshop_attendees = get_random_attendees(100)
        
        for name, email in web_workshop_attendees:
            attendee = Attendee(
                name=name,
                email=email,
                event_id=sample_events[1].id,
                registered_at=datetime.now() - timedelta(days=3)
            )
            sample_attendees.append(attendee)
        
        # AI & ML Summit attendees (40 attendees)
        ai_summit_attendees = get_random_attendees(250)
        
        for name, email in ai_summit_attendees:
            attendee = Attendee(
                name=name,
                email=email,
                event_id=sample_events[2].id,
                registered_at=datetime.now() - timedelta(days=2)
            )
            sample_attendees.append(attendee)
        
        # Startup Networking Event attendees (31 attendees)
        startup_event_attendees = get_random_attendees(100)
        
        for name, email in startup_event_attendees:
            attendee = Attendee(
                name=name,
                email=email,
                event_id=sample_events[3].id,
                registered_at=datetime.now() - timedelta(days=1)
            )
            sample_attendees.append(attendee)
        
        design_class_attendees = get_random_attendees(50)
        for name, email in design_class_attendees:
            attendee = Attendee(
                name=name,
                email=email,
                event_id=sample_events[4].id,
                registered_at=datetime.now() - timedelta(hours=12)
            )
            sample_attendees.append(attendee)
        
        # Add all attendees to session
        for attendee in sample_attendees:
            session.add(attendee)
        
        # Update current_attendees count for each event
        sample_events[0].current_attendees = len(tech_conf_attendees)
        sample_events[1].current_attendees = len(web_workshop_attendees)
        sample_events[2].current_attendees = len(ai_summit_attendees)
        sample_events[3].current_attendees = len(startup_event_attendees)
        sample_events[4].current_attendees = len(design_class_attendees)
        
        # Commit all changes
        await session.commit()
        
        print("Sample data created successfully!")
        print(f"Created {len(sample_events)} events with a total of {len(sample_attendees)} attendees")
