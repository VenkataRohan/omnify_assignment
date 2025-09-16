"""
Base schema classes and common response models.
"""

from typing import Any, Dict, Generic, List, TypeVar, Union
from pydantic import BaseModel, Field

DataType = TypeVar("DataType")


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        use_enum_values = True


class PaginationParams(BaseModel):
    """Pagination parameters for list endpoints."""
    
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=10, ge=1, le=100, description="Page size")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries."""
        return (self.page - 1) * self.size


class PaginatedResponse(BaseSchema, Generic[DataType]):
    """Generic paginated response model."""
    
    success: bool = Field(default=True, description="Success indicator")
    data: List[DataType] = Field(description="List of items")
    meta: "PaginationMeta" = Field(description="Pagination metadata")
    message: Union[str, None] = Field(default=None, description="Success message")
    
    @classmethod
    def create(
        cls,
        data: List[DataType],
        page: int,
        size: int,
        total: int,
        message: Union[str, None] = None
    ) -> "PaginatedResponse[DataType]":
        """Create a paginated response."""
        meta = PaginationMeta.create(page=page, size=size, total=total)
        return cls(
            data=data,
            meta=meta,
            message=message
        )


class PaginationMeta(BaseSchema):
    """Pagination metadata."""
    
    page: int = Field(description="Current page number")
    size: int = Field(description="Page size")
    total: int = Field(description="Total number of items")
    pages: int = Field(description="Total number of pages")
    has_next: bool = Field(description="Whether there is a next page")
    has_previous: bool = Field(description="Whether there is a previous page")
    
    @classmethod
    def create(
        cls,
        page: int,
        size: int,
        total: int
    ) -> "PaginationMeta":
        """Create pagination metadata."""
        pages = (total + size - 1) // size if total > 0 else 0  # Ceiling division
        has_next = page < pages
        has_previous = page > 1
        
        return cls(
            page=page,
            size=size,
            total=total,
            pages=pages,
            has_next=has_next,
            has_previous=has_previous
        )


class SuccessResponse(BaseSchema, Generic[DataType]):
    """Generic success response model."""
    
    success: bool = Field(default=True, description="Success indicator")
    data: Union[DataType, None] = Field(default=None, description="Response data")
    message: Union[str, None] = Field(default=None, description="Success message")


class ErrorResponse(BaseSchema):
    """Error response model."""
    
    success: bool = Field(default=False, description="Success indicator")
    error: str = Field(description="Error message")
    details: Union[Dict[str, Any], None] = Field(default=None, description="Error details")
    code: Union[str, None] = Field(default=None, description="Error code")


class HealthCheck(BaseSchema):
    """Health check response model."""
    
    status: str = Field(description="Service status")
    version: str = Field(description="API version")
    timestamp: str = Field(description="Check timestamp")
    database: str = Field(description="Database status")
    dependencies: Dict[str, str] = Field(description="Dependencies status")
