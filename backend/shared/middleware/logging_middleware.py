"""
Logging middleware for AI SchoolOS services.
"""

import time
import logging
from fastapi import Request, Response
from typing import Callable

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    """Logging middleware for FastAPI applications."""
    
    def __init__(self, app_name: str):
        self.app_name = app_name
    
    async def __call__(self, request: Request, call_next: Callable) -> Response:
        """Log request and response information."""
        
        # Start time
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            logger.info(
                f"Response: {response.status_code} "
                f"took {duration:.3f}s"
            )
            
            return response
            
        except Exception as e:
            # Calculate duration
            duration = time.time() - start_time
            
            # Log error
            logger.error(
                f"Error: {str(e)} "
                f"took {duration:.3f}s"
            )
            raise 