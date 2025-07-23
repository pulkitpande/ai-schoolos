"""
Helper utilities for AI SchoolOS services.
"""

import uuid
from datetime import datetime
from typing import Optional


def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


def format_datetime(dt: datetime, format_str: Optional[str] = None) -> str:
    """Format datetime object to string."""
    if format_str is None:
        format_str = "%Y-%m-%d %H:%M:%S"
    return dt.strftime(format_str)


def format_date(dt: datetime) -> str:
    """Format datetime to date string."""
    return dt.strftime("%Y-%m-%d")


def format_time(dt: datetime) -> str:
    """Format datetime to time string."""
    return dt.strftime("%H:%M:%S")


def sanitize_string(text: str) -> str:
    """Sanitize string by removing special characters."""
    import re
    return re.sub(r'[^\w\s-]', '', text)


def truncate_string(text: str, max_length: int = 100) -> str:
    """Truncate string to specified length."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..." 