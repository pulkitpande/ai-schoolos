"""
Pydantic schemas for Auth Service (AI SchoolOS)
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, validator
import uuid


# Base schemas
class BaseResponse(BaseModel):
    success: bool = True
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[str] = None


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    tenant_id: uuid.UUID
    role_id: Optional[uuid.UUID] = None
    profile_data: Optional[dict] = {}


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    role_id: Optional[uuid.UUID] = None
    profile_data: Optional[dict] = None


class UserResponse(UserBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    role_id: Optional[uuid.UUID]
    profile_data: dict
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Authentication schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LogoutRequest(BaseModel):
    refresh_token: str


class LogoutResponse(BaseResponse):
    message: str = "Successfully logged out"


# Registration schemas
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    tenant_id: uuid.UUID
    role_id: Optional[uuid.UUID] = None
    profile_data: Optional[dict] = {}

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class RegisterResponse(BaseModel):
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# Password reset schemas
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseResponse):
    message: str = "Password reset email sent successfully"


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, max_length=128)

    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class ResetPasswordResponse(BaseResponse):
    message: str = "Password reset successfully"


# Permission schemas
class PermissionBase(BaseModel):
    name: str
    resource: str
    action: str


class PermissionCreate(PermissionBase):
    pass


class PermissionResponse(PermissionBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Role schemas
class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    tenant_id: uuid.UUID
    permission_ids: Optional[List[uuid.UUID]] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    permission_ids: Optional[List[uuid.UUID]] = None


class RoleResponse(RoleBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    permissions: List[PermissionResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Tenant schemas
class TenantBase(BaseModel):
    name: str
    domain: str


class TenantCreate(TenantBase):
    config: Optional[dict] = {}
    subscription_tier: str = "basic"


class TenantUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    config: Optional[dict] = None
    subscription_tier: Optional[str] = None
    is_active: Optional[bool] = None


class TenantResponse(TenantBase):
    id: uuid.UUID
    config: dict
    subscription_tier: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Current user schemas
class CurrentUserResponse(BaseModel):
    user: UserResponse
    permissions: List[str]
    role: Optional[RoleResponse] = None
    tenant: TenantResponse


# Health check schema
class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow) 