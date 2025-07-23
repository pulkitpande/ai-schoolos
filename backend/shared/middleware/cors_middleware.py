"""
CORS middleware for AI SchoolOS services.
"""

from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware


class CORSMiddleware:
    """CORS middleware configuration for AI SchoolOS services."""
    
    @staticmethod
    def get_cors_middleware():
        """Get CORS middleware configuration."""
        return FastAPICORSMiddleware(
            allow_origins=["*"],  # Configure for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ) 