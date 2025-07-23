"""
AI SchoolOS API Gateway

Main entry point for the API Gateway service.
"""

import os
import httpx
import asyncio
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging

from shared.utils.logging import setup_logging

# Setup logging
logger = setup_logging("api-gateway")

# Create FastAPI app
app = FastAPI(
    title="AI SchoolOS API Gateway",
    description="API Gateway for AI SchoolOS microservices",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure for production
)

# Remove the print statement:
# print('Registered routes:')
# for route in app.routes:
#     print(f'{route.path} -> {route.methods}')

# Service Registry
SERVICES = {
    "auth": {
        "url": os.getenv("AUTH_SERVICE_URL", "http://auth-service:8001"),
        "health": "/health"
    },
    "students": {
        "url": os.getenv("STUDENT_SERVICE_URL", "http://ai-schoolos-student-service:8002"),
        "health": "/health"
    },
    "staff": {
        "url": os.getenv("STAFF_SERVICE_URL", "http://staff-service:8003"),
        "health": "/health"
    },
    "fees": {
        "url": os.getenv("FEE_SERVICE_URL", "http://fee-service:8004"),
        "health": "/health"
    },
    "exams": {
        "url": os.getenv("EXAM_SERVICE_URL", "http://exam-service:8005"),
        "health": "/health"
    },
    "attendance": {
        "url": os.getenv("ATTENDANCE_SERVICE_URL", "http://attendance-service:8006"),
        "health": "/health"
    },
    "homework": {
        "url": os.getenv("HOMEWORK_SERVICE_URL", "http://homework-service:8007"),
        "health": "/health"
    },
    "timetable": {
        "url": os.getenv("TIMETABLE_SERVICE_URL", "http://timetable-service:8008"),
        "health": "/health"
    },
    "library": {
        "url": os.getenv("LIBRARY_SERVICE_URL", "http://library-service:8009"),
        "health": "/health"
    },
    "transport": {
        "url": os.getenv("TRANSPORT_SERVICE_URL", "http://transport-service:8010"),
        "health": "/health"
    },
    "communication": {
        "url": os.getenv("COMMUNICATION_SERVICE_URL", "http://communication-service:8011"),
        "health": "/health"
    },
    "analytics": {
        "url": os.getenv("ANALYTICS_SERVICE_URL", "http://analytics-service:8012"),
        "health": "/health"
    },
    "notifications": {
        "url": os.getenv("NOTIFICATION_SERVICE_URL", "http://notification-service:8013"),
        "health": "/health"
    },
    "config": {
        "url": os.getenv("CONFIG_SERVICE_URL", "http://config-service:8014"),
        "health": "/health"
    },
    "super-admin": {
        "url": os.getenv("SUPER_ADMIN_SERVICE_URL", "http://super-admin-service:8015"),
        "health": "/health"
    },
    "ai": {
        "url": os.getenv("AI_SERVICE_URL", "http://ai-service:8016"),
        "health": "/health"
    },
    "ai-analytics": {
        "url": os.getenv("AI_ANALYTICS_SERVICE_URL", "http://ai-analytics-service:8017"),
        "health": "/health"
    }
}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "AI SchoolOS API Gateway",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "api-gateway",
        "version": "1.0.0"
    }


@app.get("/services/health")
async def services_health_check():
    """Check health of all services."""
    health_status = {}
    
    async with httpx.AsyncClient() as client:
        for service_name, service_config in SERVICES.items():
            try:
                response = await client.get(
                    f"{service_config['url']}{service_config['health']}",
                    timeout=5.0
                )
                health_status[service_name] = {
                    "status": "healthy" if response.status_code == 200 else "unhealthy",
                    "status_code": response.status_code
                }
            except Exception as e:
                logger.error(f"Health check failed for {service_name}: {str(e)}")
                health_status[service_name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
    
    return health_status


@app.api_route("/api/v1/{service_name}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_api_request_root(service_name: str, request: Request):
    """Proxy API v1 root requests to appropriate microservices, stripping /api/v1/ prefix."""
    if service_name not in SERVICES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service '{service_name}' not found"
        )
    service_config = SERVICES[service_name]
    # Forward to the service root (strip /api/v1)
    target_url = f"{service_config['url']}/"
    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params,
                timeout=30.0
            )
            return JSONResponse(
                content=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as e:
            logger.error(f"Request to {service_name} failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Service '{service_name}' is unavailable"
            )

@app.api_route("/api/v1/{service_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_api_request(service_name: str, path: str, request: Request):
    """Proxy API v1 requests to appropriate microservices, stripping /api/v1/ prefix."""
    if service_name not in SERVICES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service '{service_name}' not found"
        )
    service_config = SERVICES[service_name]
    # Forward to /{path} (strip /api/v1/{service_name})
    target_url = f"{service_config['url']}/{path}"
    body = None
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                params=request.query_params,
                timeout=30.0
            )
            return JSONResponse(
                content=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except httpx.RequestError as e:
            logger.error(f"Request to {service_name} failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Service '{service_name}' is unavailable"
            )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 