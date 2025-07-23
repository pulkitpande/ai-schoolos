"""
SQLAlchemy models for Config Service (AI SchoolOS)
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
    category: Mapped[str] = mapped_column(String(50), default="general")
    version: Mapped[str] = mapped_column(String(20), default="1.0")
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_system_configs_config_key", "config_key"),
        Index("ix_system_configs_config_type", "config_type"),
        Index("ix_system_configs_category", "category"),
    )


class FeatureFlag(Base):
    __tablename__ = "feature_flags"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Feature Flag Information
    flag_name: Mapped[str] = mapped_column(String(100), nullable=False)
    flag_key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Flag Settings
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    rollout_percentage: Mapped[int] = mapped_column(Integer, default=0)
    
    # Targeting
    target_tenants: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    target_users: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    conditions: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Validity
    expiry_date: Mapped[date] = mapped_column(Date, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_feature_flags_flag_key", "flag_key"),
        Index("ix_feature_flags_is_enabled", "is_enabled"),
        Index("ix_feature_flags_expiry_date", "expiry_date"),
    )


class EnvironmentConfig(Base):
    __tablename__ = "environment_configs"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Environment Information
    environment_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    environment_type: Mapped[str] = mapped_column(String(50), nullable=False)  # dev, staging, prod
    
    # Configuration Data
    config_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    variables: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    secrets: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Metadata
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_environment_configs_environment_name", "environment_name"),
        Index("ix_environment_configs_environment_type", "environment_type"),
    )


class ServiceConfig(Base):
    __tablename__ = "service_configs"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Service Information
    service_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    service_type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Configuration Data
    config_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    endpoints: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    health_check_url: Mapped[str] = mapped_column(String(200), nullable=True)
    
    # Connection Settings
    timeout: Mapped[int] = mapped_column(Integer, default=30)
    retry_config: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    circuit_breaker_config: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_service_configs_service_name", "service_name"),
        Index("ix_service_configs_service_type", "service_type"),
    )


class ConfigTemplate(Base):
    __tablename__ = "config_templates"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Template Information
    template_name: Mapped[str] = mapped_column(String(100), nullable=False)
    template_type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Template Data
    template_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    variables: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Metadata
    description: Mapped[str] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(20), default="1.0")
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_config_templates_template_name", "template_name"),
        Index("ix_config_templates_template_type", "template_type"),
        Index("ix_config_templates_version", "version"),
    )


class ConfigOverride(Base):
    __tablename__ = "config_overrides"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Override Information
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    config_key: Mapped[str] = mapped_column(String(100), nullable=False)
    config_value: Mapped[str] = mapped_column(Text, nullable=False)
    override_type: Mapped[str] = mapped_column(String(50), nullable=False)  # tenant, user, global
    
    # Priority and Conditions
    priority: Mapped[int] = mapped_column(Integer, default=1)
    conditions: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Metadata
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_config_overrides_tenant_id", "tenant_id"),
        Index("ix_config_overrides_config_key", "config_key"),
        Index("ix_config_overrides_override_type", "override_type"),
        Index("ix_config_overrides_priority", "priority"),
    ) 