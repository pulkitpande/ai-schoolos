"""
SQLAlchemy models for Super Admin Service (AI SchoolOS)
"""

from datetime import datetime, date
import uuid
import json
from sqlalchemy import (
    Column, String, DateTime, Boolean, ForeignKey, Table, Index, Text, Integer, Date, Float, Numeric
)
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base
from sqlalchemy.types import TypeDecorator, Text

Base = declarative_base()

class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string."""
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class UUIDString(TypeDecorator):
    """Custom UUID type that works with both PostgreSQL and SQLite."""
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return str(value)  # Keep as string to avoid UUID object issues
        return value


class Tenant(Base):
    __tablename__ = "tenants"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Tenant Information
    tenant_name: Mapped[str] = mapped_column(String(200), nullable=False)
    tenant_code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    domain: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Contact Information
    contact_person: Mapped[str] = mapped_column(String(100), nullable=False)
    contact_email: Mapped[str] = mapped_column(String(100), nullable=False)
    contact_phone: Mapped[str] = mapped_column(String(20), nullable=True)
    
    # Address Information
    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=True)
    
    # Configuration
    timezone: Mapped[str] = mapped_column(String(50), default="UTC")
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    language: Mapped[str] = mapped_column(String(10), default="en")
    
    # Limits
    max_users: Mapped[int] = mapped_column(Integer, default=100)
    max_students: Mapped[int] = mapped_column(Integer, default=1000)
    
    # Subscription Information
    subscription_plan: Mapped[str] = mapped_column(String(50), default="basic")
    subscription_status: Mapped[str] = mapped_column(String(20), default="active")
    trial_end_date: Mapped[date] = mapped_column(Date, nullable=True)
    
    # Settings
    settings: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_tenants_tenant_code", "tenant_code"),
        Index("ix_tenants_domain", "domain"),
        Index("ix_tenants_subscription_status", "subscription_status"),
        Index("ix_tenants_is_active", "is_active"),
    )


class SystemConfig(Base):
    __tablename__ = "system_configs"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Configuration Information
    config_key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    config_value: Mapped[str] = mapped_column(Text, nullable=False)
    config_type: Mapped[str] = mapped_column(String(50), nullable=False)  # string, number, boolean, json
    
    # Metadata
    description: Mapped[str] = mapped_column(Text, nullable=True)
    is_encrypted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_sensitive: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_system_configs_config_key", "config_key"),
        Index("ix_system_configs_config_type", "config_type"),
    )


class AdminUser(Base):
    __tablename__ = "admin_users"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # User Information
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Authentication
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Role and Permissions
    role: Mapped[str] = mapped_column(String(50), nullable=False)  # super_admin, admin, operator
    permissions: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    is_super_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Activity
    last_login: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_admin_users_username", "username"),
        Index("ix_admin_users_email", "email"),
        Index("ix_admin_users_role", "role"),
        Index("ix_admin_users_is_active", "is_active"),
    )


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # User Information
    user_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Action Information
    action: Mapped[str] = mapped_column(String(100), nullable=False)  # create, update, delete, login, etc.
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False)  # tenant, user, config, etc.
    resource_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Changes
    old_values: Mapped[dict] = mapped_column(JSONEncodedDict, nullable=True)
    new_values: Mapped[dict] = mapped_column(JSONEncodedDict, nullable=True)
    
    # Request Information
    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_audit_logs_user_id", "user_id"),
        Index("ix_audit_logs_action", "action"),
        Index("ix_audit_logs_resource_type", "resource_type"),
        Index("ix_audit_logs_timestamp", "timestamp"),
    )


class SystemBackup(Base):
    __tablename__ = "system_backups"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Backup Information
    backup_name: Mapped[str] = mapped_column(String(200), nullable=False)
    backup_type: Mapped[str] = mapped_column(String(50), nullable=False)  # full, incremental, differential
    
    # File Information
    backup_size: Mapped[int] = mapped_column(Integer, nullable=False)  # in bytes
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    
    # Compression and Encryption
    compression_type: Mapped[str] = mapped_column(String(50), nullable=True)  # gzip, bzip2, etc.
    encryption_type: Mapped[str] = mapped_column(String(50), nullable=True)  # AES, etc.
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="completed")  # in_progress, completed, failed
    
    # Metadata
    backup_notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_system_backups_backup_type", "backup_type"),
        Index("ix_system_backups_status", "status"),
        Index("ix_system_backups_created_at", "created_at"),
    )


class SystemMaintenance(Base):
    __tablename__ = "system_maintenance"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Maintenance Information
    maintenance_type: Mapped[str] = mapped_column(String(50), nullable=False)  # scheduled, emergency, routine
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Scheduling
    scheduled_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    scheduled_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    actual_start: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    actual_end: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Affected Services
    affected_services: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    maintenance_window: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Priority and Assignment
    priority: Mapped[str] = mapped_column(String(20), nullable=False)  # low, medium, high, critical
    assigned_to: Mapped[str] = mapped_column(UUIDString, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="scheduled")  # scheduled, in_progress, completed, cancelled
    
    # Notes
    maintenance_notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_system_maintenance_maintenance_type", "maintenance_type"),
        Index("ix_system_maintenance_status", "status"),
        Index("ix_system_maintenance_priority", "priority"),
        Index("ix_system_maintenance_scheduled_start", "scheduled_start"),
    )


class License(Base):
    __tablename__ = "licenses"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # License Information
    license_key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    license_type: Mapped[str] = mapped_column(String(50), nullable=False)  # basic, premium, enterprise
    
    # Tenant Association
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Features and Limits
    features: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    max_users: Mapped[int] = mapped_column(Integer, default=100)
    max_students: Mapped[int] = mapped_column(Integer, default=1000)
    
    # Validity
    valid_from: Mapped[date] = mapped_column(Date, nullable=False)
    valid_until: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Notes
    license_notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_licenses_license_key", "license_key"),
        Index("ix_licenses_tenant_id", "tenant_id"),
        Index("ix_licenses_license_type", "license_type"),
        Index("ix_licenses_is_active", "is_active"),
        Index("ix_licenses_valid_until", "valid_until"),
    )


class Subscription(Base):
    __tablename__ = "subscriptions"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Tenant Association
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Plan Information
    plan_name: Mapped[str] = mapped_column(String(100), nullable=False)
    plan_type: Mapped[str] = mapped_column(String(50), nullable=False)  # basic, premium, enterprise
    
    # Billing Information
    billing_cycle: Mapped[str] = mapped_column(String(20), nullable=False)  # monthly, quarterly, yearly
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    
    # Dates
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    trial_end_date: Mapped[date] = mapped_column(Date, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, suspended, cancelled, expired
    
    # Payment
    payment_method: Mapped[str] = mapped_column(String(50), nullable=True)
    auto_renew: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Notes
    subscription_notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_subscriptions_tenant_id", "tenant_id"),
        Index("ix_subscriptions_plan_type", "plan_type"),
        Index("ix_subscriptions_status", "status"),
        Index("ix_subscriptions_end_date", "end_date"),
    ) 