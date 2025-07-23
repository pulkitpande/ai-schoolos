"""
AI Service - FastAPI Application (AI SchoolOS)
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

from .database import init_db, get_db
from .routers import ai

# Service configuration
SERVICE_NAME = "ai-service"
SERVICE_VERSION = "1.0.0"
SERVICE_PORT = int(os.getenv("AI_SERVICE_PORT", 8016))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print(f"Starting {SERVICE_NAME} v{SERVICE_VERSION}...")
    init_db()
    print(f"{SERVICE_NAME} started successfully!")
    
    yield
    
    # Shutdown
    print(f"Shutting down {SERVICE_NAME}...")


# Create FastAPI app
app = FastAPI(
    title=f"{SERVICE_NAME.title()} API",
    description=f"AI Service for {SERVICE_NAME} - AI SchoolOS",
    version=SERVICE_VERSION,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Include routers
app.include_router(ai.router, prefix="/api/v1")


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "port": SERVICE_PORT
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {SERVICE_NAME.title()} API",
        "version": SERVICE_VERSION,
        "docs": "/docs",
        "health": "/health"
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return {"error": "Resource not found", "detail": str(exc)}


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors."""
    return {"error": "Internal server error", "detail": str(exc)}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=SERVICE_PORT,
        reload=True,
        log_level="info"
    ) 