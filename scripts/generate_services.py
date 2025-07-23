#!/usr/bin/env python3
"""
Script to generate all microservices with basic structure.
"""

import os
import shutil
from pathlib import Path

# Service configurations
SERVICES = [
    {"name": "student-service", "port": 8002, "description": "Student profiles, enrollment, guardian management"},
    {"name": "staff-service", "port": 8003, "description": "Staff profiles, roles, permissions"},
    {"name": "fee-service", "port": 8004, "description": "Fee structure, payments, dues tracking"},
    {"name": "exam-service", "port": 8005, "description": "Exams, marks, report cards with AI feedback"},
    {"name": "attendance-service", "port": 8006, "description": "Daily attendance, reports, AI face recognition"},
    {"name": "homework-service", "port": 8007, "description": "Assignment creation, submission, AI grading"},
    {"name": "timetable-service", "port": 8008, "description": "Class schedules, room allocation"},
    {"name": "library-service", "port": 8009, "description": "Book management, borrowing, returns"},
    {"name": "transport-service", "port": 8010, "description": "Bus routes, tracking, driver management"},
    {"name": "communication-service", "port": 8011, "description": "WhatsApp bot, notifications, parent communication"},
    {"name": "analytics-service", "port": 8012, "description": "Data insights, reports, AI-powered analytics"},
    {"name": "notification-service", "port": 8013, "description": "Push notifications, email, SMS"},
    {"name": "config-service", "port": 8014, "description": "System configuration, feature flags"},
    {"name": "super-admin-service", "port": 8015, "description": "Multi-tenant management, system administration"},
]

def create_service_structure(service_name: str, port: int, description: str):
    """Create service directory structure and files."""
    
    service_path = Path(f"backend/services/{service_name}")
    service_path.mkdir(parents=True, exist_ok=True)
    
    # Create main.py
    main_content = f'''"""
AI SchoolOS {service_name.replace("-", " ").title()}

{description}
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import logging

from shared.utils.logging import setup_logging

# Setup logging
logger = setup_logging("{service_name}")

# Create FastAPI app
app = FastAPI(
    title="AI SchoolOS {service_name.replace("-", " ").title()}",
    description="{description}",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {{
        "message": "AI SchoolOS {service_name.replace("-", " ").title()}",
        "version": "1.0.0",
        "status": "running"
    }}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {{
        "status": "healthy",
        "service": "{service_name}",
        "version": "1.0.0"
    }}


# TODO: Add service-specific endpoints here


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port={port},
        reload=True,
        log_level="info"
    )
'''
    
    with open(service_path / "main.py", "w") as f:
        f.write(main_content)
    
    # Create requirements.txt
    requirements_content = f'''# Core dependencies
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0

# Shared package dependencies
-r ../../shared/requirements.txt
'''
    
    with open(service_path / "requirements.txt", "w") as f:
        f.write(requirements_content)
    
    # Create Dockerfile
    dockerfile_content = f'''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared package
COPY ../../shared ./shared

# Copy application code
COPY . .

# Expose port
EXPOSE {port}

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:{port}/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "{port}"]
'''
    
    with open(service_path / "Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    print(f"Created {service_name} service")

def main():
    """Generate all services."""
    print("Generating AI SchoolOS microservices...")
    
    for service in SERVICES:
        create_service_structure(
            service["name"],
            service["port"],
            service["description"]
        )
    
    print("All services generated successfully!")

if __name__ == "__main__":
    main() 