"""
Pydantic schemas for Super Admin Service (AI SchoolOS)
"""

from datetime import datetime, date
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from sqlalchemy.orm import Query


# Base schemas
class TenantBase(BaseModel):
    tenant_name: str = Field(..., description="Tenant name")
    tenant_code: str = Field(..., description="Tenant code")
    domain: Optional[str] = Field(None, description="Domain")
    contact_person: str = Field(..., description="Contact person")
    contact_email: str = Field(..., description="Contact email")
    contact_phone: Optional[str] = Field(None, description="Contact phone")
    address: str = Field(..., description="Address")
    city: str = Field(..., description="City")
    state: str = Field(..., description="State")
    country: str = Field(..., description="Country")
    postal_code: Optional[str] = Field(None, description="Postal code")
    timezone: str = Field("UTC", description="Timezone")
    currency: str = Field("USD", description="Currency")
    language: str = Field("en", description="Language")
    max_users: int = Field(100, description="Maximum users")
    max_students: int = Field(1000, description="Maximum students")
    subscription_plan: str = Field("basic", description="Subscription plan")
    subscription_status: str = Field("active", description="Subscription status")
    trial_end_date: Optional[date] = Field(None, description="Trial end date")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Tenant settings")


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    tenant_name: Optional[str] = None
    tenant_code: Optional[str] = None
    domain: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    timezone: Optional[str] = None
    currency: Optional[str] = None
    language: Optional[str] = None
    max_users: Optional[int] = None
    max_students: Optional[int] = None
    subscription_plan: Optional[str] = None
    subscription_status: Optional[str] = None
    trial_end_date: Optional[date] = None
    settings: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class TenantResponse(TenantBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# System Configuration schemas
class SystemConfigBase(BaseModel):
    config_key: str = Field(..., description="Configuration key")
    config_value: str = Field(..., description="Configuration value")
    config_type: str = Field(..., description="Configuration type")
    description: Optional[str] = Field(None, description="Description")
    is_encrypted: bool = Field(False, description="Is encrypted")
    is_sensitive: bool = Field(False, description="Is sensitive")


class SystemConfigCreate(SystemConfigBase):
    pass


class SystemConfigUpdate(BaseModel):
    config_key: Optional[str] = None
    config_value: Optional[str] = None
    config_type: Optional[str] = None
    description: Optional[str] = None
    is_encrypted: Optional[bool] = None
    is_sensitive: Optional[bool] = None


class SystemConfigResponse(SystemConfigBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Admin User schemas
class AdminUserBase(BaseModel):
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email")
    full_name: str = Field(..., description="Full name")
    role: str = Field(..., description="Role")
    permissions: Dict[str, Any] = Field(default_factory=dict, description="Permissions")
    is_super_admin: bool = Field(False, description="Is super admin")
    last_login: Optional[datetime] = Field(None, description="Last login")
    password_hash: str = Field(..., description="Password hash")


class AdminUserCreate(AdminUserBase):
    pass


class AdminUserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = None
    is_super_admin: Optional[bool] = None
    last_login: Optional[datetime] = None
    password_hash: Optional[str] = None
    is_active: Optional[bool] = None


class AdminUserResponse(AdminUserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Audit Log schemas
class AuditLogBase(BaseModel):
    user_id: str = Field(..., description="User ID")
    action: str = Field(..., description="Action performed")
    resource_type: str = Field(..., description="Resource type")
    resource_id: str = Field(..., description="Resource ID")
    old_values: Optional[Dict[str, Any]] = Field(None, description="Old values")
    new_values: Optional[Dict[str, Any]] = Field(None, description="New values")
    ip_address: Optional[str] = Field(None, description="IP address")
    user_agent: Optional[str] = Field(None, description="User agent")
    timestamp: datetime = Field(..., description="Timestamp")


class AuditLogResponse(AuditLogBase):
    id: str

    class Config:
        from_attributes = True


# System Backup schemas
class SystemBackupBase(BaseModel):
    backup_name: str = Field(..., description="Backup name")
    backup_type: str = Field(..., description="Backup type")
    backup_size: int = Field(..., description="Backup size in bytes")
    file_path: str = Field(..., description="File path")
    checksum: str = Field(..., description="Checksum")
    compression_type: Optional[str] = Field(None, description="Compression type")
    encryption_type: Optional[str] = Field(None, description="Encryption type")
    backup_notes: Optional[str] = Field(None, description="Backup notes")


class SystemBackupCreate(SystemBackupBase):
    pass


class SystemBackupResponse(SystemBackupBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# System Maintenance schemas
class SystemMaintenanceBase(BaseModel):
    maintenance_type: str = Field(..., description="Maintenance type")
    title: str = Field(..., description="Title")
    description: str = Field(..., description="Description")
    scheduled_start: datetime = Field(..., description="Scheduled start")
    scheduled_end: datetime = Field(..., description="Scheduled end")
    affected_services: List[str] = Field(default_factory=list, description="Affected services")
    maintenance_window: str = Field(..., description="Maintenance window")
    priority: str = Field(..., description="Priority")
    assigned_to: Optional[str] = Field(None, description="Assigned to")
    maintenance_notes: Optional[str] = Field(None, description="Maintenance notes")


class SystemMaintenanceCreate(SystemMaintenanceBase):
    pass


class SystemMaintenanceUpdate(BaseModel):
    maintenance_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    affected_services: Optional[List[str]] = None
    maintenance_window: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    maintenance_notes: Optional[str] = None
    status: Optional[str] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None


class SystemMaintenanceResponse(SystemMaintenanceBase):
    id: str
    status: str
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# License schemas
class LicenseBase(BaseModel):
    license_key: str = Field(..., description="License key")
    license_type: str = Field(..., description="License type")
    tenant_id: str = Field(..., description="Tenant ID")
    features: List[str] = Field(default_factory=list, description="Features")
    max_users: int = Field(100, description="Maximum users")
    max_students: int = Field(1000, description="Maximum students")
    valid_from: date = Field(..., description="Valid from date")
    valid_until: date = Field(..., description="Valid until date")
    is_active: bool = Field(True, description="Is active")
    license_notes: Optional[str] = Field(None, description="License notes")


class LicenseCreate(LicenseBase):
    pass


class LicenseUpdate(BaseModel):
    license_key: Optional[str] = None
    license_type: Optional[str] = None
    tenant_id: Optional[str] = None
    features: Optional[List[str]] = None
    max_users: Optional[int] = None
    max_students: Optional[int] = None
    valid_from: Optional[date] = None
    valid_until: Optional[date] = None
    is_active: Optional[bool] = None
    license_notes: Optional[str] = None


class LicenseResponse(LicenseBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Subscription schemas
class SubscriptionBase(BaseModel):
    tenant_id: str = Field(..., description="Tenant ID")
    plan_name: str = Field(..., description="Plan name")
    plan_type: str = Field(..., description="Plan type")
    billing_cycle: str = Field(..., description="Billing cycle")
    amount: float = Field(..., description="Amount")
    currency: str = Field("USD", description="Currency")
    start_date: date = Field(..., description="Start date")
    end_date: date = Field(..., description="End date")
    trial_end_date: Optional[date] = Field(None, description="Trial end date")
    status: str = Field("active", description="Status")
    payment_method: Optional[str] = Field(None, description="Payment method")
    auto_renew: bool = Field(True, description="Auto renew")
    subscription_notes: Optional[str] = Field(None, description="Subscription notes")


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    tenant_id: Optional[str] = None
    plan_name: Optional[str] = None
    plan_type: Optional[str] = None
    billing_cycle: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    trial_end_date: Optional[date] = None
    status: Optional[str] = None
    payment_method: Optional[str] = None
    auto_renew: Optional[bool] = None
    subscription_notes: Optional[str] = None


class SubscriptionResponse(SubscriptionBase):
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