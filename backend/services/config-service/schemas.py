"""
Pydantic schemas for Config Service (AI SchoolOS)
"""

from datetime import datetime, date
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from sqlalchemy.orm import Query


# Base schemas
class SystemConfigBase(BaseModel):
    config_key: str = Field(..., description="Configuration key")
    config_value: str = Field(..., description="Configuration value")
    config_type: str = Field(..., description="Configuration type (string, number, boolean, json)")
    description: Optional[str] = Field(None, description="Description")
    is_encrypted: bool = Field(False, description="Is encrypted")
    is_sensitive: bool = Field(False, description="Is sensitive")
    category: str = Field("general", description="Configuration category")
    version: str = Field("1.0", description="Configuration version")


class SystemConfigCreate(SystemConfigBase):
    pass


class SystemConfigUpdate(BaseModel):
    config_key: Optional[str] = None
    config_value: Optional[str] = None
    config_type: Optional[str] = None
    description: Optional[str] = None
    is_encrypted: Optional[bool] = None
    is_sensitive: Optional[bool] = None
    category: Optional[str] = None
    version: Optional[str] = None


class SystemConfigResponse(SystemConfigBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Feature Flag schemas
class FeatureFlagBase(BaseModel):
    flag_name: str = Field(..., description="Feature flag name")
    flag_key: str = Field(..., description="Feature flag key")
    description: Optional[str] = Field(None, description="Description")
    is_enabled: bool = Field(False, description="Is enabled")
    rollout_percentage: int = Field(0, ge=0, le=100, description="Rollout percentage")
    target_tenants: List[str] = Field(default_factory=list, description="Target tenants")
    target_users: List[str] = Field(default_factory=list, description="Target users")
    conditions: Dict[str, Any] = Field(default_factory=dict, description="Conditions")
    expiry_date: Optional[date] = Field(None, description="Expiry date")


class FeatureFlagCreate(FeatureFlagBase):
    pass


class FeatureFlagUpdate(BaseModel):
    flag_name: Optional[str] = None
    flag_key: Optional[str] = None
    description: Optional[str] = None
    is_enabled: Optional[bool] = None
    rollout_percentage: Optional[int] = None
    target_tenants: Optional[List[str]] = None
    target_users: Optional[List[str]] = None
    conditions: Optional[Dict[str, Any]] = None
    expiry_date: Optional[date] = None


class FeatureFlagResponse(FeatureFlagBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Environment Configuration schemas
class EnvironmentConfigBase(BaseModel):
    environment_name: str = Field(..., description="Environment name")
    environment_type: str = Field(..., description="Environment type (dev, staging, prod)")
    config_data: Dict[str, Any] = Field(default_factory=dict, description="Configuration data")
    variables: Dict[str, Any] = Field(default_factory=dict, description="Environment variables")
    secrets: Dict[str, Any] = Field(default_factory=dict, description="Secrets")
    description: Optional[str] = Field(None, description="Description")


class EnvironmentConfigCreate(EnvironmentConfigBase):
    pass


class EnvironmentConfigUpdate(BaseModel):
    environment_name: Optional[str] = None
    environment_type: Optional[str] = None
    config_data: Optional[Dict[str, Any]] = None
    variables: Optional[Dict[str, Any]] = None
    secrets: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class EnvironmentConfigResponse(EnvironmentConfigBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Service Configuration schemas
class ServiceConfigBase(BaseModel):
    service_name: str = Field(..., description="Service name")
    service_type: str = Field(..., description="Service type")
    config_data: Dict[str, Any] = Field(default_factory=dict, description="Configuration data")
    endpoints: Dict[str, str] = Field(default_factory=dict, description="Service endpoints")
    health_check_url: Optional[str] = Field(None, description="Health check URL")
    timeout: int = Field(30, description="Timeout in seconds")
    retry_config: Dict[str, Any] = Field(default_factory=dict, description="Retry configuration")
    circuit_breaker_config: Dict[str, Any] = Field(default_factory=dict, description="Circuit breaker configuration")


class ServiceConfigCreate(ServiceConfigBase):
    pass


class ServiceConfigUpdate(BaseModel):
    service_name: Optional[str] = None
    service_type: Optional[str] = None
    config_data: Optional[Dict[str, Any]] = None
    endpoints: Optional[Dict[str, str]] = None
    health_check_url: Optional[str] = None
    timeout: Optional[int] = None
    retry_config: Optional[Dict[str, Any]] = None
    circuit_breaker_config: Optional[Dict[str, Any]] = None


class ServiceConfigResponse(ServiceConfigBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Configuration Template schemas
class ConfigTemplateBase(BaseModel):
    template_name: str = Field(..., description="Template name")
    template_type: str = Field(..., description="Template type")
    template_data: Dict[str, Any] = Field(default_factory=dict, description="Template data")
    variables: List[str] = Field(default_factory=list, description="Template variables")
    description: Optional[str] = Field(None, description="Description")
    version: str = Field("1.0", description="Template version")


class ConfigTemplateCreate(ConfigTemplateBase):
    pass


class ConfigTemplateUpdate(BaseModel):
    template_name: Optional[str] = None
    template_type: Optional[str] = None
    template_data: Optional[Dict[str, Any]] = None
    variables: Optional[List[str]] = None
    description: Optional[str] = None
    version: Optional[str] = None


class ConfigTemplateResponse(ConfigTemplateBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Configuration Override schemas
class ConfigOverrideBase(BaseModel):
    tenant_id: str = Field(..., description="Tenant ID")
    config_key: str = Field(..., description="Configuration key")
    config_value: str = Field(..., description="Configuration value")
    override_type: str = Field(..., description="Override type")
    priority: int = Field(1, ge=1, le=10, description="Priority")
    conditions: Dict[str, Any] = Field(default_factory=dict, description="Override conditions")
    description: Optional[str] = Field(None, description="Description")


class ConfigOverrideCreate(ConfigOverrideBase):
    pass


class ConfigOverrideUpdate(BaseModel):
    tenant_id: Optional[str] = None
    config_key: Optional[str] = None
    config_value: Optional[str] = None
    override_type: Optional[str] = None
    priority: Optional[int] = None
    conditions: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class ConfigOverrideResponse(ConfigOverrideBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Health check response
class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str 