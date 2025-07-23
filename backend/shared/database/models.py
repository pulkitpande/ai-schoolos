"""
Base database models for AI SchoolOS services.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid


class BaseModel:
    """Base model with common fields."""
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"


# Create declarative base
Base = declarative_base(cls=BaseModel) 