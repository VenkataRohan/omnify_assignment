"""
Error handling middleware for consistent error responses.
"""

import traceback
from typing import Callable

from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.core.logging import get_logger
from app.services.exceptions import ServiceError

logger = get_logger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle exceptions and provide consistent error responses.
    
    This middleware catches all unhandled exceptions and converts them
    to appropriate HTTP responses with consistent structure.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and handle any exceptions.
        
        Args:
            request: The incoming request
            call_next: The next middleware or endpoint
            
        Returns:
            Response: The response or error response
        """
        try:
            response = await call_next(request)
            return response
        
        except HTTPException:
            # Let FastAPI handle HTTP exceptions
            raise
        
        except ServiceError as e:
            # Handle service layer exceptions
            logger.warning(f"Service error: {str(e)}", exc_info=True)
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": str(e),
                    "code": e.__class__.__name__
                }
            )
        
        except Exception as e:
            # Handle unexpected exceptions
            logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            
            # Log the full traceback in development
            if hasattr(request.app.state, "debug") and request.app.state.debug:
                logger.error(f"Traceback: {traceback.format_exc()}")
            
            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "success": False,
                    "error": "Internal server error",
                    "code": "INTERNAL_SERVER_ERROR"
                }
            )
