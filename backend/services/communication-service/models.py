"""
SQLAlchemy models for Communication Service (AI SchoolOS)
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


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Message Information
    sender_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    sender_type: Mapped[str] = mapped_column(String(20), nullable=False)  # student, teacher, parent, admin
    recipient_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    recipient_type: Mapped[str] = mapped_column(String(20), nullable=False)  # student, teacher, parent, admin
    
    # Message Content
    subject: Mapped[str] = mapped_column(String(200), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[str] = mapped_column(String(50), nullable=False)  # text, image, file, announcement, broadcast
    
    # Message Details
    priority: Mapped[str] = mapped_column(String(20), default="normal")  # low, normal, high, urgent
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Attachments
    attachments: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    read_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_messages_tenant_id", "tenant_id"),
        Index("ix_messages_sender_id", "sender_id"),
        Index("ix_messages_recipient_id", "recipient_id"),
        Index("ix_messages_message_type", "message_type"),
        Index("ix_messages_sent_at", "sent_at"),
        Index("ix_messages_is_read", "is_read"),
    )


class ChatRoom(Base):
    __tablename__ = "chat_rooms"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Chat Room Information
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    room_type: Mapped[str] = mapped_column(String(50), nullable=False)  # direct, group, class, department
    
    # Room Settings
    is_private: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    max_participants: Mapped[int] = mapped_column(Integer, default=100)
    
    # Room Details
    created_by: Mapped[str] = mapped_column(UUIDString, nullable=False)
    created_by_type: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_chat_rooms_tenant_id", "tenant_id"),
        Index("ix_chat_rooms_room_type", "room_type"),
        Index("ix_chat_rooms_is_active", "is_active"),
        Index("ix_chat_rooms_created_by", "created_by"),
    )


class ChatParticipant(Base):
    __tablename__ = "chat_participants"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("chat_rooms.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    user_type: Mapped[str] = mapped_column(String(20), nullable=False)  # student, teacher, parent, admin
    
    # Participant Settings
    role: Mapped[str] = mapped_column(String(20), default="member")  # admin, moderator, member
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    left_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_chat_participants_room_id", "room_id"),
        Index("ix_chat_participants_user_id", "user_id"),
        Index("ix_chat_participants_role", "role"),
        Index("ix_chat_participants_is_active", "is_active"),
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    room_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("chat_rooms.id", ondelete="CASCADE"), nullable=False)
    sender_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    sender_type: Mapped[str] = mapped_column(String(20), nullable=False)  # student, teacher, parent, admin
    
    # Message Content
    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_type: Mapped[str] = mapped_column(String(50), default="text")  # text, image, file, emoji
    
    # Message Details
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    reply_to_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("chat_messages.id", ondelete="SET NULL"), nullable=True)
    
    # Attachments
    attachments: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    edited_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_chat_messages_room_id", "room_id"),
        Index("ix_chat_messages_sender_id", "sender_id"),
        Index("ix_chat_messages_sent_at", "sent_at"),
        Index("ix_chat_messages_reply_to_id", "reply_to_id"),
    )


class MessageRead(Base):
    __tablename__ = "message_reads"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    message_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    user_type: Mapped[str] = mapped_column(String(20), nullable=False)  # student, teacher, parent, admin
    
    # Read Information
    read_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_message_reads_message_id", "message_id"),
        Index("ix_message_reads_user_id", "user_id"),
        Index("ix_message_reads_read_at", "read_at"),
    )


class Announcement(Base):
    __tablename__ = "announcements"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Announcement Information
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    announcement_type: Mapped[str] = mapped_column(String(50), nullable=False)  # general, academic, administrative, emergency
    
    # Author Information
    author_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    author_type: Mapped[str] = mapped_column(String(20), nullable=False)  # teacher, admin
    
    # Target Audience
    target_audience: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Specific groups/classes
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Scheduling
    published_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, published, archived
    
    # Additional Settings
    priority: Mapped[str] = mapped_column(String(20), default="normal")  # low, normal, high, urgent
    attachments: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_announcements_tenant_id", "tenant_id"),
        Index("ix_announcements_announcement_type", "announcement_type"),
        Index("ix_announcements_author_id", "author_id"),
        Index("ix_announcements_status", "status"),
        Index("ix_announcements_published_at", "published_at"),
    )


class Broadcast(Base):
    __tablename__ = "broadcasts"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Broadcast Information
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    broadcast_type: Mapped[str] = mapped_column(String(50), nullable=False)  # email, sms, push, in_app
    
    # Author Information
    author_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    author_type: Mapped[str] = mapped_column(String(20), nullable=False)  # teacher, admin
    
    # Target Audience
    recipient_filters: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Filters for selecting recipients
    total_recipients: Mapped[int] = mapped_column(Integer, default=0)
    sent_recipients: Mapped[int] = mapped_column(Integer, default=0)
    
    # Scheduling
    scheduled_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, scheduled, sent, failed
    
    # Additional Settings
    priority: Mapped[str] = mapped_column(String(20), default="normal")  # low, normal, high, urgent
    template_id: Mapped[str] = mapped_column(UUIDString, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_broadcasts_tenant_id", "tenant_id"),
        Index("ix_broadcasts_broadcast_type", "broadcast_type"),
        Index("ix_broadcasts_author_id", "author_id"),
        Index("ix_broadcasts_status", "status"),
        Index("ix_broadcasts_scheduled_at", "scheduled_at"),
    )


class CommunicationTemplate(Base):
    __tablename__ = "communication_templates"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Template Information
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    template_type: Mapped[str] = mapped_column(String(50), nullable=False)  # email, sms, announcement, broadcast
    
    # Template Content
    subject_template: Mapped[str] = mapped_column(String(200), nullable=True)
    content_template: Mapped[str] = mapped_column(Text, nullable=False)
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
        Index("ix_communication_templates_tenant_id", "tenant_id"),
        Index("ix_communication_templates_template_type", "template_type"),
        Index("ix_communication_templates_is_active", "is_active"),
    )


class CommunicationAnalytics(Base):
    __tablename__ = "communication_analytics"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Analytics Data
    total_messages: Mapped[int] = mapped_column(Integer, default=0)
    total_announcements: Mapped[int] = mapped_column(Integer, default=0)
    total_broadcasts: Mapped[int] = mapped_column(Integer, default=0)
    active_chat_rooms: Mapped[int] = mapped_column(Integer, default=0)
    
    # Message Statistics
    sent_messages: Mapped[int] = mapped_column(Integer, default=0)
    read_messages: Mapped[int] = mapped_column(Integer, default=0)
    unread_messages: Mapped[int] = mapped_column(Integer, default=0)
    
    # Broadcast Statistics
    successful_broadcasts: Mapped[int] = mapped_column(Integer, default=0)
    failed_broadcasts: Mapped[int] = mapped_column(Integer, default=0)
    
    # User Statistics
    active_users: Mapped[int] = mapped_column(Integer, default=0)
    total_users: Mapped[int] = mapped_column(Integer, default=0)
    
    # Time Analytics
    daily_messages: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    weekly_messages: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_communication_analytics_tenant_id", "tenant_id"),
        Index("ix_communication_analytics_created_at", "created_at"),
    ) 