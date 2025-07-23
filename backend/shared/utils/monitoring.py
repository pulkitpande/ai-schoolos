"""
Monitoring and Observability Utilities (AI SchoolOS)

Prometheus metrics, structured logging, health checks, and observability
"""

import logging
import time
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
from fastapi import Request, Response
from prometheus_client import Counter, Histogram, Gauge, Summary, generate_latest
import psutil
import json

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code', 'service']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint', 'service']
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active connections',
    ['service']
)

DATABASE_CONNECTIONS = Gauge(
    'database_connections',
    'Number of database connections',
    ['service', 'database']
)

SERVICE_HEALTH = Gauge(
    'service_health',
    'Service health status (1=healthy, 0=unhealthy)',
    ['service', 'endpoint']
)

MEMORY_USAGE = Gauge(
    'memory_usage_bytes',
    'Memory usage in bytes',
    ['service']
)

CPU_USAGE = Gauge(
    'cpu_usage_percent',
    'CPU usage percentage',
    ['service']
)

# Custom metrics
SERVICE_CALLS = Counter(
    'service_calls_total',
    'Total service-to-service calls',
    ['from_service', 'to_service', 'endpoint', 'status']
)

SERVICE_CALL_DURATION = Histogram(
    'service_call_duration_seconds',
    'Service-to-service call duration',
    ['from_service', 'to_service', 'endpoint']
)

ERROR_COUNT = Counter(
    'errors_total',
    'Total errors',
    ['service', 'error_type', 'endpoint']
)


class MonitoringMiddleware:
    """Middleware for request monitoring and metrics collection."""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
    
    async def __call__(self, request: Request, call_next):
        """Monitor request and collect metrics."""
        start_time = time.time()
        
        # Record request start
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=0,
            service=self.service_name
        ).inc()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Record successful request
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status_code=response.status_code,
                service=self.service_name
            ).inc()
            
            # Record request duration
            duration = time.time() - start_time
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.url.path,
                service=self.service_name
            ).observe(duration)
            
            return response
        
        except Exception as e:
            # Record error
            ERROR_COUNT.labels(
                service=self.service_name,
                error_type=type(e).__name__,
                endpoint=request.url.path
            ).inc()
            
            # Record failed request
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status_code=500,
                service=self.service_name
            ).inc()
            
            raise


class SystemMetrics:
    """System metrics collection."""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
    
    def collect_system_metrics(self):
        """Collect system metrics."""
        # Memory usage
        memory = psutil.virtual_memory()
        MEMORY_USAGE.labels(service=self.service_name).set(memory.used)
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        CPU_USAGE.labels(service=self.service_name).set(cpu_percent)
        
        # Active connections (simplified)
        try:
            connections = len(psutil.net_connections())
            ACTIVE_CONNECTIONS.labels(service=self.service_name).set(connections)
        except:
            pass
    
    async def start_metrics_collection(self, interval: int = 30):
        """Start periodic metrics collection."""
        while True:
            try:
                self.collect_system_metrics()
                await asyncio.sleep(interval)
            except Exception as e:
                logging.error(f"Error collecting system metrics: {e}")
                await asyncio.sleep(interval)


class HealthChecker:
    """Health check utilities."""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.health_status = {
            "status": "healthy",
            "service": service_name,
            "timestamp": datetime.utcnow(),
            "checks": {}
        }
    
    async def check_database_health(self, db_session) -> Dict[str, Any]:
        """Check database health."""
        try:
            # Simple database health check
            await db_session.execute("SELECT 1")
            return {"status": "healthy", "message": "Database connection OK"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Database error: {str(e)}"}
    
    async def check_external_services(self, service_urls: Dict[str, str]) -> Dict[str, Any]:
        """Check external services health."""
        import httpx
        
        results = {}
        async with httpx.AsyncClient(timeout=5.0) as client:
            for service_name, url in service_urls.items():
                try:
                    response = await client.get(f"{url}/health")
                    if response.status_code == 200:
                        results[service_name] = {"status": "healthy", "response_time": response.elapsed.total_seconds()}
                    else:
                        results[service_name] = {"status": "unhealthy", "error": f"HTTP {response.status_code}"}
                except Exception as e:
                    results[service_name] = {"status": "unhealthy", "error": str(e)}
        
        return results
    
    async def run_health_checks(self, db_session=None, service_urls=None) -> Dict[str, Any]:
        """Run all health checks."""
        checks = {}
        
        # System health
        checks["system"] = {
            "status": "healthy",
            "memory_usage": psutil.virtual_memory().percent,
            "cpu_usage": psutil.cpu_percent(),
            "disk_usage": psutil.disk_usage('/').percent
        }
        
        # Database health
        if db_session:
            checks["database"] = await self.check_database_health(db_session)
        
        # External services health
        if service_urls:
            checks["external_services"] = await self.check_external_services(service_urls)
        
        # Determine overall health
        overall_status = "healthy"
        for check_name, check_result in checks.items():
            if check_result.get("status") == "unhealthy":
                overall_status = "unhealthy"
                break
        
        self.health_status.update({
            "status": overall_status,
            "timestamp": datetime.utcnow(),
            "checks": checks
        })
        
        return self.health_status


class StructuredLogger:
    """Structured logging utilities."""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
    
    def log_request(self, request: Request, response: Response, duration: float):
        """Log request details."""
        log_data = {
            "event": "http_request",
            "service": self.service_name,
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "duration_ms": duration * 1000,
            "user_agent": request.headers.get("user-agent"),
            "client_ip": request.client.host if request.client else None,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if response.status_code >= 400:
            self.logger.error(json.dumps(log_data))
        else:
            self.logger.info(json.dumps(log_data))
    
    def log_service_call(self, from_service: str, to_service: str, endpoint: str, duration: float, success: bool):
        """Log service-to-service call."""
        log_data = {
            "event": "service_call",
            "from_service": from_service,
            "to_service": to_service,
            "endpoint": endpoint,
            "duration_ms": duration * 1000,
            "success": success,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if not success:
            self.logger.error(json.dumps(log_data))
        else:
            self.logger.info(json.dumps(log_data))
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log error with context."""
        log_data = {
            "event": "error",
            "service": self.service_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if context:
            log_data.update(context)
        
        self.logger.error(json.dumps(log_data))


class MetricsExporter:
    """Prometheus metrics exporter."""
    
    @staticmethod
    def get_metrics() -> str:
        """Get Prometheus metrics."""
        return generate_latest()
    
    @staticmethod
    def get_metrics_dict() -> Dict[str, Any]:
        """Get metrics as dictionary."""
        # This is a simplified version - in production, use prometheus_client's registry
        return {
            "request_count": REQUEST_COUNT._value.sum(),
            "request_duration": REQUEST_DURATION._sum.sum(),
            "active_connections": ACTIVE_CONNECTIONS._value.sum(),
            "memory_usage": MEMORY_USAGE._value.sum(),
            "cpu_usage": CPU_USAGE._value.sum(),
            "error_count": ERROR_COUNT._value.sum()
        }


@asynccontextmanager
async def monitor_request(service_name: str, endpoint: str):
    """Context manager for request monitoring."""
    start_time = time.time()
    try:
        yield
    finally:
        duration = time.time() - start_time
        REQUEST_DURATION.labels(
            method="UNKNOWN",
            endpoint=endpoint,
            service=service_name
        ).observe(duration)


@asynccontextmanager
async def monitor_service_call(from_service: str, to_service: str, endpoint: str):
    """Context manager for service call monitoring."""
    start_time = time.time()
    success = False
    try:
        yield
        success = True
    finally:
        duration = time.time() - start_time
        SERVICE_CALLS.labels(
            from_service=from_service,
            to_service=to_service,
            endpoint=endpoint,
            status="success" if success else "error"
        ).inc()
        
        SERVICE_CALL_DURATION.labels(
            from_service=from_service,
            to_service=to_service,
            endpoint=endpoint
        ).observe(duration)


def setup_monitoring(app, service_name: str):
    """Setup monitoring for FastAPI app."""
    # Add monitoring middleware
    app.add_middleware(MonitoringMiddleware, service_name=service_name)
    
    # Add metrics endpoint
    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint."""
        return Response(
            content=MetricsExporter.get_metrics(),
            media_type="text/plain"
        )
    
    # Add health check endpoint
    health_checker = HealthChecker(service_name)
    
    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return await health_checker.run_health_checks()
    
    return health_checker


def setup_logging(service_name: str, log_level: str = "INFO"):
    """Setup structured logging."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create structured logger
    structured_logger = StructuredLogger(service_name)
    
    return structured_logger 