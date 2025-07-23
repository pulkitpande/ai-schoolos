"""
Service-to-Service Communication Utilities (AI SchoolOS)

HTTP client, service discovery, retry logic, and inter-service communication
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import httpx
from httpx import AsyncClient, TimeoutException, HTTPStatusError
from fastapi import HTTPException, status
import json
import os

logger = logging.getLogger(__name__)

# Service URLs (in production, use service discovery)
SERVICE_URLS = {
    "auth-service": "http://auth-service:8001",
    "student-service": "http://student-service:8002",
    "staff-service": "http://staff-service:8003",
    "fee-service": "http://fee-service:8004",
    "exam-service": "http://exam-service:8005",
    "homework-service": "http://homework-service:8006",
    "library-service": "http://library-service:8007",
    "notification-service": "http://notification-service:8008",
    "communication-service": "http://communication-service:8009",
    "analytics-service": "http://analytics-service:8010",
    "attendance-service": "http://attendance-service:8011",
    "timetable-service": "http://timetable-service:8012",
    "transport-service": "http://transport-service:8013",
    "config-service": "http://config-service:8014",
    "super-admin-service": "http://super-admin-service:8015",
}

# Service health cache
service_health_cache: Dict[str, Dict[str, Any]] = {}
cache_ttl = 30  # seconds


class ServiceCommunicationError(Exception):
    """Custom exception for service communication errors."""
    pass


class ServiceDiscoveryError(Exception):
    """Custom exception for service discovery errors."""
    pass


class ServiceClient:
    """HTTP client for inter-service communication."""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: Optional[AsyncClient] = None
    
    async def __aenter__(self):
        self._client = AsyncClient(
            timeout=self.timeout,
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()
    
    async def _make_request(
        self,
        method: str,
        service_name: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to another service."""
        if not self._client:
            raise ServiceCommunicationError("Client not initialized")
        
        service_url = SERVICE_URLS.get(service_name)
        if not service_url:
            raise ServiceDiscoveryError(f"Service {service_name} not found")
        
        url = f"{service_url}{endpoint}"
        
        # Add default headers
        if headers is None:
            headers = {}
        headers.update({
            "Content-Type": "application/json",
            "User-Agent": "ai-schoolos-service-client"
        })
        
        for attempt in range(self.max_retries):
            try:
                response = await self._client.request(
                    method=method,
                    url=url,
                    json=data,
                    headers=headers,
                    params=params
                )
                response.raise_for_status()
                return response.json()
            
            except TimeoutException:
                logger.warning(f"Timeout on attempt {attempt + 1} for {service_name}:{endpoint}")
                if attempt == self.max_retries - 1:
                    raise ServiceCommunicationError(f"Timeout after {self.max_retries} attempts")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
            
            except HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code} for {service_name}:{endpoint}")
                raise ServiceCommunicationError(f"HTTP {e.response.status_code}: {e.response.text}")
            
            except Exception as e:
                logger.error(f"Unexpected error for {service_name}:{endpoint}: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise ServiceCommunicationError(f"Request failed: {str(e)}")
                await asyncio.sleep(2 ** attempt)
    
    async def get(self, service_name: str, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make GET request to service."""
        return await self._make_request("GET", service_name, endpoint, params=params)
    
    async def post(self, service_name: str, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make POST request to service."""
        return await self._make_request("POST", service_name, endpoint, data=data)
    
    async def put(self, service_name: str, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make PUT request to service."""
        return await self._make_request("PUT", service_name, endpoint, data=data)
    
    async def delete(self, service_name: str, endpoint: str) -> Dict[str, Any]:
        """Make DELETE request to service."""
        return await self._make_request("DELETE", service_name, endpoint)


class ServiceDiscovery:
    """Service discovery and health checking."""
    
    @staticmethod
    async def check_service_health(service_name: str) -> Dict[str, Any]:
        """Check health of a specific service."""
        try:
            async with ServiceClient() as client:
                response = await client.get(service_name, "/health")
                return {
                    "service": service_name,
                    "status": "healthy",
                    "response": response,
                    "timestamp": datetime.utcnow()
                }
        except Exception as e:
            return {
                "service": service_name,
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow()
            }
    
    @staticmethod
    async def check_all_services() -> Dict[str, Dict[str, Any]]:
        """Check health of all services."""
        tasks = []
        for service_name in SERVICE_URLS.keys():
            tasks.append(ServiceDiscovery.check_service_health(service_name))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        health_status = {}
        for i, service_name in enumerate(SERVICE_URLS.keys()):
            if isinstance(results[i], Exception):
                health_status[service_name] = {
                    "service": service_name,
                    "status": "error",
                    "error": str(results[i]),
                    "timestamp": datetime.utcnow()
                }
            else:
                health_status[service_name] = results[i]
        
        return health_status
    
    @staticmethod
    def get_service_url(service_name: str) -> Optional[str]:
        """Get service URL by name."""
        return SERVICE_URLS.get(service_name)


class ServiceAuth:
    """Service authentication and authorization."""
    
    @staticmethod
    def create_service_token(service_name: str, permissions: List[str]) -> str:
        """Create service-to-service authentication token."""
        # In production, use proper JWT signing
        payload = {
            "service": service_name,
            "permissions": permissions,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        return json.dumps(payload)  # Simplified for demo
    
    @staticmethod
    def get_service_headers(service_name: str, permissions: List[str]) -> Dict[str, str]:
        """Get headers for service-to-service communication."""
        token = ServiceAuth.create_service_token(service_name, permissions)
        return {
            "Authorization": f"Bearer {token}",
            "X-Service-Name": service_name,
            "X-Service-Permissions": ",".join(permissions)
        }


class ServiceMetrics:
    """Service communication metrics and monitoring."""
    
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.response_times = []
    
    def record_request(self, service_name: str, endpoint: str, duration: float, success: bool):
        """Record service communication metrics."""
        self.request_count += 1
        if not success:
            self.error_count += 1
        
        self.response_times.append({
            "service": service_name,
            "endpoint": endpoint,
            "duration": duration,
            "success": success,
            "timestamp": datetime.utcnow()
        })
        
        # Keep only last 1000 requests
        if len(self.response_times) > 1000:
            self.response_times = self.response_times[-1000:]
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        if not self.response_times:
            return {
                "total_requests": self.request_count,
                "total_errors": self.error_count,
                "success_rate": 0.0,
                "avg_response_time": 0.0
            }
        
        success_count = sum(1 for req in self.response_times if req["success"])
        avg_response_time = sum(req["duration"] for req in self.response_times) / len(self.response_times)
        
        return {
            "total_requests": self.request_count,
            "total_errors": self.error_count,
            "success_rate": success_count / len(self.response_times),
            "avg_response_time": avg_response_time,
            "recent_requests": self.response_times[-10:]  # Last 10 requests
        }


# Global metrics instance
service_metrics = ServiceMetrics()


async def call_service(
    service_name: str,
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Convenience function to call another service."""
    start_time = datetime.utcnow()
    success = False
    
    try:
        async with ServiceClient() as client:
            if method.upper() == "GET":
                result = await client.get(service_name, endpoint, params)
            elif method.upper() == "POST":
                result = await client.post(service_name, endpoint, data or {})
            elif method.upper() == "PUT":
                result = await client.put(service_name, endpoint, data or {})
            elif method.upper() == "DELETE":
                result = await client.delete(service_name, endpoint)
            else:
                raise ServiceCommunicationError(f"Unsupported method: {method}")
            
            success = True
            return result
    
    finally:
        duration = (datetime.utcnow() - start_time).total_seconds()
        service_metrics.record_request(service_name, endpoint, duration, success)


async def get_service_health() -> Dict[str, Dict[str, Any]]:
    """Get health status of all services."""
    return await ServiceDiscovery.check_all_services()


async def get_service_metrics() -> Dict[str, Any]:
    """Get service communication metrics."""
    return service_metrics.get_metrics() 