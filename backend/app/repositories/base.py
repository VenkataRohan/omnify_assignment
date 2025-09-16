"""
Base repository class with common CRUD operations.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy import select, delete, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.schemas.base import PaginationParams

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType")


class BaseRepository(Generic[ModelType, CreateSchemaType]):
    """
    Base repository class with common CRUD operations.
    
    This class provides a generic interface for database operations
    that can be extended by specific model repositories.
    """
    
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        """
        Initialize repository.
        
        Args:
            model: SQLAlchemy model class
            db: Database session
        """
        self.model = model
        self.db = db
    
    async def get(self, id: int) -> Optional[ModelType]:
        """
        Get a single record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Optional[ModelType]: Model instance or None
        """
        result = await self.db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()
    
    async def get_multi(
        self,
        pagination: Optional[PaginationParams] = None,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None
    ) -> List[ModelType]:
        """
        Get multiple records with optional filtering and pagination.
        
        Args:
            pagination: Pagination parameters
            filters: Filter conditions
            order_by: Order by field
            
        Returns:
            List[ModelType]: List of model instances
        """
        query = select(self.model)
        
        # Apply filters
        if filters:
            filter_conditions = []
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    filter_conditions.append(getattr(self.model, field) == value)
            if filter_conditions:
                query = query.where(and_(*filter_conditions))
        
        # Apply ordering
        if order_by and hasattr(self.model, order_by):
            query = query.order_by(getattr(self.model, order_by))
        
        # Apply pagination
        if pagination:
            query = query.offset(pagination.offset).limit(pagination.size)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count records with optional filtering.
        
        Args:
            filters: Filter conditions
            
        Returns:
            int: Number of records
        """
        query = select(func.count(self.model.id))
        
        # Apply filters
        if filters:
            filter_conditions = []
            for field, value in filters.items():
                if hasattr(self.model, field) and value is not None:
                    filter_conditions.append(getattr(self.model, field) == value)
            if filter_conditions:
                query = query.where(and_(*filter_conditions))
        
        result = await self.db.execute(query)
        return result.scalar() or 0
    
    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.
        
        Args:
            obj_in: Create schema instance
            
        Returns:
            ModelType: Created model instance
        """
        obj_data = obj_in.model_dump() if hasattr(obj_in, 'model_dump') else obj_in.dict()
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
    
    async def exists(self, id: int) -> bool:
        """
        Check if a record exists by ID.
        
        Args:
            id: Record ID
            
        Returns:
            bool: True if exists, False otherwise
        """
        result = await self.db.execute(
            select(func.count(self.model.id)).where(self.model.id == id)
        )
        return result.scalar() > 0
