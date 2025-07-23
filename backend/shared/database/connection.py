"""
Database connection utilities for AI SchoolOS services.
"""

import os
from typing import Optional
from sqlalchemy import create_engine as sa_create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool


def get_database_url() -> str:
    """Get database URL from environment variables."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")
    return database_url


def create_engine(database_url: Optional[str] = None) -> Engine:
    """Create SQLAlchemy engine with connection pooling."""
    if database_url is None:
        database_url = get_database_url()
    
    # Configure connection pooling
    engine = sa_create_engine(
        database_url,
        pool_size=20,
        max_overflow=30,
        pool_pre_ping=True,
        pool_recycle=3600,
        echo=os.getenv("SQL_ECHO", "false").lower() == "true"
    )
    
    return engine


def get_session(engine: Optional[Engine] = None) -> Session:
    """Get database session."""
    if engine is None:
        engine = create_engine()
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal() 