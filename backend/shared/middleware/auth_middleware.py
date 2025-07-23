"""
Authentication Middleware (AI SchoolOS)

JWT authentication, role-based access control, service-to-service auth
"""

import logging
from typing import Optional, Dict, Any, List
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
import json

from ..auth.jwt import verify_token, decode_token
from ..auth.permissions import check_permissions, get_user_permissions

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer(auto_error=False)

# JWT settings
SECRET_KEY = "your-secret-key-here"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Service-to-service authentication
SERVICE_SECRET_KEY = "service-secret-key-here"  # In production, use environment variable


class AuthMiddleware:
    """Authentication middleware for API endpoints."""
    
    def __init__(self, required_permissions: Optional[List[str]] = None):
        self.required_permissions = required_permissions or []
    
    async def __call__(self, request: Request) -> Dict[str, Any]:
        """Authenticate request and return user context."""
        # Check for service-to-service authentication
        service_auth = self._check_service_auth(request)
        if service_auth:
            return service_auth
        
        # Check for regular JWT authentication
        user_auth = await self._check_user_auth(request)
        if user_auth:
            return user_auth
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    def _check_service_auth(self, request: Request) -> Optional[Dict[str, Any]]:
        """Check for service-to-service authentication."""
        service_token = request.headers.get("X-Service-Token")
        service_name = request.headers.get("X-Service-Name")
        
        if service_token and service_name:
            try:
                # Verify service token
                payload = jwt.decode(service_token, SERVICE_SECRET_KEY, algorithms=["HS256"])
                
                # Check if token is for the correct service
                if payload.get("service") != service_name:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid service token"
                    )
                
                # Check token expiration
                exp = payload.get("exp")
                if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Service token expired"
                    )
                
                return {
                    "type": "service",
                    "service_name": service_name,
                    "permissions": payload.get("permissions", []),
                    "authenticated": True
                }
            
            except JWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid service token"
                )
        
        return None
    
    async def _check_user_auth(self, request: Request) -> Optional[Dict[str, Any]]:
        """Check for user JWT authentication."""
        credentials: Optional[HTTPAuthorizationCredentials] = await security(request)
        
        if not credentials:
            return None
        
        try:
            # Verify JWT token
            payload = verify_token(credentials.credentials)
            
            # Get user permissions
            user_id = payload.get("sub")
            permissions = await get_user_permissions(user_id)
            
            # Check required permissions
            if self.required_permissions:
                if not check_permissions(permissions, self.required_permissions):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Insufficient permissions"
                    )
            
            return {
                "type": "user",
                "user_id": user_id,
                "email": payload.get("email"),
                "roles": payload.get("roles", []),
                "permissions": permissions,
                "tenant_id": payload.get("tenant_id"),
                "authenticated": True
            }
        
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )


class ServiceAuthMiddleware:
    """Middleware for service-to-service authentication."""
    
    def __init__(self, required_permissions: Optional[List[str]] = None):
        self.required_permissions = required_permissions or []
    
    async def __call__(self, request: Request) -> Dict[str, Any]:
        """Authenticate service request."""
        service_token = request.headers.get("X-Service-Token")
        service_name = request.headers.get("X-Service-Name")
        
        if not service_token or not service_name:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Service authentication required"
            )
        
        try:
            # Verify service token
            payload = jwt.decode(service_token, SERVICE_SECRET_KEY, algorithms=["HS256"])
            
            # Check if token is for the correct service
            if payload.get("service") != service_name:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid service token"
                )
            
            # Check token expiration
            exp = payload.get("exp")
            if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Service token expired"
                )
            
            # Check required permissions
            service_permissions = payload.get("permissions", [])
            if self.required_permissions:
                if not check_permissions(service_permissions, self.required_permissions):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Insufficient service permissions"
                    )
            
            return {
                "type": "service",
                "service_name": service_name,
                "permissions": service_permissions,
                "authenticated": True
            }
        
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid service token"
            )


class TenantMiddleware:
    """Middleware for tenant isolation."""
    
    async def __call__(self, request: Request) -> str:
        """Extract and validate tenant ID."""
        # Check for tenant ID in headers
        tenant_id = request.headers.get("X-Tenant-ID")
        
        if not tenant_id:
            # Try to get from query parameters
            tenant_id = request.query_params.get("tenant_id")
        
        if not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tenant ID required"
            )
        
        return tenant_id


# Dependency functions for FastAPI
async def get_current_user(request: Request) -> Dict[str, Any]:
    """Get current authenticated user."""
    auth_middleware = AuthMiddleware()
    return await auth_middleware(request)


async def get_current_service(request: Request) -> Dict[str, Any]:
    """Get current authenticated service."""
    service_middleware = ServiceAuthMiddleware()
    return await service_middleware(request)


async def get_tenant_id(request: Request) -> str:
    """Get tenant ID from request."""
    tenant_middleware = TenantMiddleware()
    return await tenant_middleware(request)


def require_permissions(permissions: List[str]):
    """Decorator to require specific permissions."""
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            auth_middleware = AuthMiddleware(required_permissions=permissions)
            await auth_middleware(request)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_service_permissions(permissions: List[str]):
    """Decorator to require specific service permissions."""
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            service_middleware = ServiceAuthMiddleware(required_permissions=permissions)
            await service_middleware(request)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


# Utility functions
def create_service_token(service_name: str, permissions: List[str], expires_in: int = 3600) -> str:
    """Create a service-to-service authentication token."""
    payload = {
        "service": service_name,
        "permissions": permissions,
        "exp": datetime.utcnow() + timedelta(seconds=expires_in),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SERVICE_SECRET_KEY, algorithm=ALGORITHM)


def verify_service_token(token: str) -> Dict[str, Any]:
    """Verify a service-to-service authentication token."""
    try:
        payload = jwt.decode(token, SERVICE_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid service token"
        )


def get_service_headers(service_name: str, permissions: List[str]) -> Dict[str, str]:
    """Get headers for service-to-service communication."""
    token = create_service_token(service_name, permissions)
    return {
        "X-Service-Token": token,
        "X-Service-Name": service_name,
        "Content-Type": "application/json"
    } 