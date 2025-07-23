"""
Logging utilities for AI SchoolOS services.
"""

import logging
import os
from typing import Optional


def setup_logging(
    service_name: str,
    log_level: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """Setup logging configuration for a service."""
    
    if log_level is None:
        log_level = os.getenv("LOG_LEVEL", "INFO")
    
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Create logger
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger


def get_logger(service_name: str) -> logging.Logger:
    """Get a logger for a specific service."""
    return logging.getLogger(service_name) 