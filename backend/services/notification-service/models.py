"""
SQLAlchemy models for Notification Service (AI SchoolOS)
"""

from datetime import datetime
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


class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Notification Information
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    notification_type: Mapped[str] = mapped_column(String(50), nullable=False)  # email, sms, push, in_app
    priority: Mapped[str] = mapped_column(String(20), default="normal")  # low, normal, high, urgent
    
    # Recipients
    recipient_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    recipient_type: Mapped[str] = mapped_column(String(20), nullable=False)  # student, teacher, parent, admin
    recipient_email: Mapped[str] = mapped_column(String(200), nullable=True)
    recipient_phone: Mapped[str] = mapped_column(String(20), nullable=True)
    
    # Content
    subject: Mapped[str] = mapped_column(String(200), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    template_id: Mapped[str] = mapped_column(UUIDString, nullable=True)
    template_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Scheduling
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, sent, delivered, failed, cancelled
    
    # Additional Settings
    channels: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Which channels to use
    meta_info: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_notifications_tenant_id", "tenant_id"),
        Index("ix_notifications_recipient_id", "recipient_id"),
        Index("ix_notifications_notification_type", "notification_type"),
        Index("ix_notifications_status", "status"),
        Index("ix_notifications_scheduled_at", "scheduled_at"),
        Index("ix_notifications_sent_at", "sent_at"),
    )


class NotificationTemplate(Base):
    __tablename__ = "notification_templates"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Template Information
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    template_type: Mapped[str] = mapped_column(String(50), nullable=False)  # email, sms, push, in_app
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # academic, administrative, emergency, marketing
    
    # Template Content
    subject_template: Mapped[str] = mapped_column(String(200), nullable=True)
    title_template: Mapped[str] = mapped_column(String(200), nullable=True)
    message_template: Mapped[str] = mapped_column(Text, nullable=False)
    html_template: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Variables
    variables: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Available template variables
    default_values: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Default values for variables
    
    # Settings
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)  # System templates cannot be deleted
    
    # Usage Statistics
    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_notification_templates_tenant_id", "tenant_id"),
        Index("ix_notification_templates_template_type", "template_type"),
        Index("ix_notification_templates_category", "category"),
        Index("ix_notification_templates_is_active", "is_active"),
    )


class NotificationChannel(Base):
    __tablename__ = "notification_channels"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Channel Information
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    channel_type: Mapped[str] = mapped_column(String(50), nullable=False)  # email, sms, push, webhook
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Configuration
    config: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Channel-specific configuration
    credentials: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # API keys, tokens, etc.
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Performance
    success_rate: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0)
    average_delivery_time: Mapped[int] = mapped_column(Integer, default=0)  # Seconds
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_notification_channels_tenant_id", "tenant_id"),
        Index("ix_notification_channels_channel_type", "channel_type"),
        Index("ix_notification_channels_is_active", "is_active"),
    )


class NotificationDelivery(Base):
    __tablename__ = "notification_deliveries"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    notification_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("notifications.id", ondelete="CASCADE"), nullable=False)
    channel_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("notification_channels.id", ondelete="CASCADE"), nullable=False)
    
    # Delivery Information
    delivery_status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, sent, delivered, failed
    delivery_attempts: Mapped[int] = mapped_column(Integer, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3)
    
    # Timing
    sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    delivered_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    failed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Response
    external_id: Mapped[str] = mapped_column(String(100), nullable=True)  # External service ID
    response_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_notification_deliveries_notification_id", "notification_id"),
        Index("ix_notification_deliveries_channel_id", "channel_id"),
        Index("ix_notification_deliveries_delivery_status", "delivery_status"),
        Index("ix_notification_deliveries_sent_at", "sent_at"),
    )


class NotificationSubscription(Base):
    __tablename__ = "notification_subscriptions"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Subscription Information
    user_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    user_type: Mapped[str] = mapped_column(String(20), nullable=False)  # student, teacher, parent, admin
    category: Mapped[str] = mapped_column(String(50), nullable=False)  # academic, administrative, emergency, marketing
    
    # Channel Preferences
    email_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    sms_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    push_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    in_app_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Contact Information
    email: Mapped[str] = mapped_column(String(200), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    push_token: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Settings
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    frequency: Mapped[str] = mapped_column(String(20), default="immediate")  # immediate, daily, weekly, never
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_notification_subscriptions_tenant_id", "tenant_id"),
        Index("ix_notification_subscriptions_user_id", "user_id"),
        Index("ix_notification_subscriptions_category", "category"),
        Index("ix_notification_subscriptions_is_active", "is_active"),
    )


class NotificationBatch(Base):
    __tablename__ = "notification_batches"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Batch Information
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    batch_type: Mapped[str] = mapped_column(String(50), nullable=False)  # bulk, scheduled, campaign
    
    # Content
    template_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("notification_templates.id", ondelete="SET NULL"), nullable=True)
    subject: Mapped[str] = mapped_column(String(200), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    template_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Recipients
    recipient_filters: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Filters for selecting recipients
    total_recipients: Mapped[int] = mapped_column(Integer, default=0)
    processed_recipients: Mapped[int] = mapped_column(Integer, default=0)
    
    # Scheduling
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, running, completed, failed, cancelled
    
    # Statistics
    success_count: Mapped[int] = mapped_column(Integer, default=0)
    failure_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_notification_batches_tenant_id", "tenant_id"),
        Index("ix_notification_batches_batch_type", "batch_type"),
        Index("ix_notification_batches_status", "status"),
        Index("ix_notification_batches_scheduled_at", "scheduled_at"),
    )


class NotificationAnalytics(Base):
    __tablename__ = "notification_analytics"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Analytics Data
    total_notifications: Mapped[int] = mapped_column(Integer, default=0)
    sent_notifications: Mapped[int] = mapped_column(Integer, default=0)
    delivered_notifications: Mapped[int] = mapped_column(Integer, default=0)
    failed_notifications: Mapped[int] = mapped_column(Integer, default=0)
    
    # Channel Statistics
    email_sent: Mapped[int] = mapped_column(Integer, default=0)
    email_delivered: Mapped[int] = mapped_column(Integer, default=0)
    sms_sent: Mapped[int] = mapped_column(Integer, default=0)
    sms_delivered: Mapped[int] = mapped_column(Integer, default=0)
    push_sent: Mapped[int] = mapped_column(Integer, default=0)
    push_delivered: Mapped[int] = mapped_column(Integer, default=0)
    
    # Performance Metrics
    average_delivery_time: Mapped[int] = mapped_column(Integer, default=0)  # Seconds
    success_rate: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0)
    
    # Category Statistics
    category_stats: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Time Analytics
    hourly_stats: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    daily_stats: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_notification_analytics_tenant_id", "tenant_id"),
        Index("ix_notification_analytics_created_at", "created_at"),
    ) 