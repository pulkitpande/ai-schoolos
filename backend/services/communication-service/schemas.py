"""
Pydantic schemas for Communication Service (AI SchoolOS)
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from decimal import Decimal


# Message schemas
class MessageBase(BaseModel):
    sender_id: str
    sender_type: str = Field(..., min_length=1, max_length=20)
    recipient_id: str
    recipient_type: str = Field(..., min_length=1, max_length=20)
    subject: Optional[str] = Field(None, max_length=200)
    content: str = Field(..., min_length=1)
    message_type: str = Field(..., min_length=1, max_length=50)
    priority: str = Field("normal", max_length=20)
    attachments: Optional[Dict[str, Any]] = {}
    sent_at: datetime


class MessageCreate(MessageBase):
    tenant_id: str


class MessageUpdate(BaseModel):
    subject: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    message_type: Optional[str] = Field(None, min_length=1, max_length=50)
    priority: Optional[str] = Field(None, max_length=20)
    is_read: Optional[bool] = None
    is_archived: Optional[bool] = None
    is_deleted: Optional[bool] = None
    attachments: Optional[Dict[str, Any]] = None


class MessageResponse(MessageBase):
    id: str
    tenant_id: str
    is_read: bool
    is_archived: bool
    is_deleted: bool
    read_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageListResponse(BaseModel):
    messages: List[MessageResponse]
    total: int
    page: int
    size: int


# Chat Room schemas
class ChatRoomBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    room_type: str = Field(..., min_length=1, max_length=50)
    is_private: bool = False
    is_active: bool = True
    max_participants: int = Field(100, ge=1, le=1000)
    created_by: str
    created_by_type: str = Field(..., min_length=1, max_length=20)


class ChatRoomCreate(ChatRoomBase):
    tenant_id: str


class ChatRoomUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    room_type: Optional[str] = Field(None, min_length=1, max_length=50)
    is_private: Optional[bool] = None
    is_active: Optional[bool] = None
    max_participants: Optional[int] = Field(None, ge=1, le=1000)


class ChatRoomResponse(ChatRoomBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatRoomListResponse(BaseModel):
    chat_rooms: List[ChatRoomResponse]
    total: int
    page: int
    size: int


# Chat Participant schemas
class ChatParticipantBase(BaseModel):
    room_id: str
    user_id: str
    user_type: str = Field(..., min_length=1, max_length=20)
    role: str = Field("member", max_length=20)
    is_active: bool = True
    joined_at: datetime


class ChatParticipantCreate(ChatParticipantBase):
    pass


class ChatParticipantUpdate(BaseModel):
    role: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None
    left_at: Optional[datetime] = None


class ChatParticipantResponse(ChatParticipantBase):
    id: str
    left_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatParticipantListResponse(BaseModel):
    participants: List[ChatParticipantResponse]
    total: int
    page: int
    size: int


# Chat Message schemas
class ChatMessageBase(BaseModel):
    room_id: str
    sender_id: str
    sender_type: str = Field(..., min_length=1, max_length=20)
    content: str = Field(..., min_length=1)
    message_type: str = Field("text", max_length=50)
    reply_to_id: Optional[str] = None
    attachments: Optional[Dict[str, Any]] = {}
    sent_at: datetime


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1)
    message_type: Optional[str] = Field(None, max_length=50)
    is_edited: Optional[bool] = None
    is_deleted: Optional[bool] = None
    attachments: Optional[Dict[str, Any]] = None


class ChatMessageResponse(ChatMessageBase):
    id: str
    is_edited: bool
    is_deleted: bool
    edited_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatMessageListResponse(BaseModel):
    messages: List[ChatMessageResponse]
    total: int
    page: int
    size: int


# Announcement schemas
class AnnouncementBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    announcement_type: str = Field(..., min_length=1, max_length=50)
    author_id: str
    author_type: str = Field(..., min_length=1, max_length=20)
    target_audience: Optional[Dict[str, Any]] = {}
    is_public: bool = True
    published_at: datetime
    expires_at: Optional[datetime] = None
    status: str = Field("draft", max_length=20)
    priority: str = Field("normal", max_length=20)
    attachments: Optional[Dict[str, Any]] = {}


class AnnouncementCreate(AnnouncementBase):
    tenant_id: str


class AnnouncementUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    announcement_type: Optional[str] = Field(None, min_length=1, max_length=50)
    target_audience: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None
    published_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    status: Optional[str] = Field(None, max_length=20)
    priority: Optional[str] = Field(None, max_length=20)
    attachments: Optional[Dict[str, Any]] = None


class AnnouncementResponse(AnnouncementBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnnouncementListResponse(BaseModel):
    announcements: List[AnnouncementResponse]
    total: int
    page: int
    size: int


# Broadcast schemas
class BroadcastBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    broadcast_type: str = Field(..., min_length=1, max_length=50)
    author_id: str
    author_type: str = Field(..., min_length=1, max_length=20)
    recipient_filters: Optional[Dict[str, Any]] = {}
    scheduled_at: Optional[datetime] = None
    status: str = Field("draft", max_length=20)
    priority: str = Field("normal", max_length=20)
    template_id: Optional[str] = None


class BroadcastCreate(BroadcastBase):
    tenant_id: str


class BroadcastUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    broadcast_type: Optional[str] = Field(None, min_length=1, max_length=50)
    recipient_filters: Optional[Dict[str, Any]] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[str] = Field(None, max_length=20)
    priority: Optional[str] = Field(None, max_length=20)
    template_id: Optional[str] = None


class BroadcastResponse(BroadcastBase):
    id: str
    tenant_id: str
    total_recipients: int
    sent_recipients: int
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BroadcastListResponse(BaseModel):
    broadcasts: List[BroadcastResponse]
    total: int
    page: int
    size: int


# Communication Template schemas
class CommunicationTemplateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    template_type: str = Field(..., min_length=1, max_length=50)
    subject_template: Optional[str] = Field(None, max_length=200)
    content_template: str = Field(..., min_length=1)
    html_template: Optional[str] = None
    variables: Optional[Dict[str, Any]] = {}
    default_values: Optional[Dict[str, Any]] = {}
    is_active: bool = True
    is_system: bool = False


class CommunicationTemplateCreate(CommunicationTemplateBase):
    tenant_id: str


class CommunicationTemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    template_type: Optional[str] = Field(None, min_length=1, max_length=50)
    subject_template: Optional[str] = Field(None, max_length=200)
    content_template: Optional[str] = Field(None, min_length=1)
    html_template: Optional[str] = None
    variables: Optional[Dict[str, Any]] = None
    default_values: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_system: Optional[bool] = None


class CommunicationTemplateResponse(CommunicationTemplateBase):
    id: str
    tenant_id: str
    usage_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CommunicationTemplateListResponse(BaseModel):
    templates: List[CommunicationTemplateResponse]
    total: int
    page: int
    size: int


# Communication Analytics schemas
class CommunicationAnalyticsBase(BaseModel):
    tenant_id: str
    total_messages: int = Field(0, ge=0)
    total_announcements: int = Field(0, ge=0)
    total_broadcasts: int = Field(0, ge=0)
    active_chat_rooms: int = Field(0, ge=0)
    sent_messages: int = Field(0, ge=0)
    read_messages: int = Field(0, ge=0)
    unread_messages: int = Field(0, ge=0)
    successful_broadcasts: int = Field(0, ge=0)
    failed_broadcasts: int = Field(0, ge=0)
    active_users: int = Field(0, ge=0)
    total_users: int = Field(0, ge=0)
    daily_messages: Optional[Dict[str, Any]] = {}
    weekly_messages: Optional[Dict[str, Any]] = {}


class CommunicationAnalyticsCreate(CommunicationAnalyticsBase):
    pass


class CommunicationAnalyticsUpdate(BaseModel):
    total_messages: Optional[int] = Field(None, ge=0)
    total_announcements: Optional[int] = Field(None, ge=0)
    total_broadcasts: Optional[int] = Field(None, ge=0)
    active_chat_rooms: Optional[int] = Field(None, ge=0)
    sent_messages: Optional[int] = Field(None, ge=0)
    read_messages: Optional[int] = Field(None, ge=0)
    unread_messages: Optional[int] = Field(None, ge=0)
    successful_broadcasts: Optional[int] = Field(None, ge=0)
    failed_broadcasts: Optional[int] = Field(None, ge=0)
    active_users: Optional[int] = Field(None, ge=0)
    total_users: Optional[int] = Field(None, ge=0)
    daily_messages: Optional[Dict[str, Any]] = None
    weekly_messages: Optional[Dict[str, Any]] = None


class CommunicationAnalyticsResponse(CommunicationAnalyticsBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CommunicationAnalyticsListResponse(BaseModel):
    analytics: List[CommunicationAnalyticsResponse]
    total: int
    page: int
    size: int


# Summary schemas
class CommunicationSummary(BaseModel):
    total_messages: int
    total_announcements: int
    total_broadcasts: int
    active_chat_rooms: int
    unread_messages: int
    active_users: int
    total_users: int
    message_success_rate: Decimal
    broadcast_success_rate: Decimal


class UserCommunicationSummary(BaseModel):
    user_id: str
    user_type: str
    total_messages_sent: int
    total_messages_received: int
    unread_messages: int
    active_chat_rooms: int
    last_message_at: Optional[datetime] = None
    last_activity_at: Optional[datetime] = None


class ChatRoomSummary(BaseModel):
    room_id: str
    room_name: str
    room_type: str
    total_participants: int
    total_messages: int
    last_message_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime 