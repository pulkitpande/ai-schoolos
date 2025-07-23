"""
Pydantic schemas for Notification Service (AI SchoolOS)
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from decimal import Decimal


# Notification schemas
class NotificationBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1)
    notification_type: str = Field(..., min_length=1, max_length=50)
    priority: str = Field("normal", max_length=20)
    recipient_id: str
    recipient_type: str = Field(..., min_length=1, max_length=20)
    recipient_email: Optional[str] = Field(None, max_length=200)
    recipient_phone: Optional[str] = Field(None, max_length=20)
    subject: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None
    template_id: Optional[str] = None
    template_data: Optional[Dict[str, Any]] = {}
    scheduled_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    channels: Optional[Dict[str, Any]] = {}
    metadata: Optional[Dict[str, Any]] = {}


class NotificationCreate(NotificationBase):
    tenant_id: str


class NotificationUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    message: Optional[str] = Field(None, min_length=1)
    notification_type: Optional[str] = Field(None, min_length=1, max_length=50)
    priority: Optional[str] = Field(None, max_length=20)
    recipient_email: Optional[str] = Field(None, max_length=200)
    recipient_phone: Optional[str] = Field(None, max_length=20)
    subject: Optional[str] = Field(None, max_length=200)
    content: Optional[str] = None
    template_id: Optional[str] = None
    template_data: Optional[Dict[str, Any]] = None
    scheduled_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    status: Optional[str] = Field(None, max_length=20)
    channels: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class NotificationResponse(NotificationBase):
    id: str
    tenant_id: str
    sent_at: Optional[datetime] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    notifications: List[NotificationResponse]
    total: int
    page: int
    size: int


# Notification Template schemas
class NotificationTemplateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    template_type: str = Field(..., min_length=1, max_length=50)
    category: str = Field(..., min_length=1, max_length=50)
    subject_template: Optional[str] = Field(None, max_length=200)
    title_template: Optional[str] = Field(None, max_length=200)
    message_template: str = Field(..., min_length=1)
    html_template: Optional[str] = None
    variables: Optional[Dict[str, Any]] = {}
    default_values: Optional[Dict[str, Any]] = {}
    is_active: bool = True
    is_system: bool = False


class NotificationTemplateCreate(NotificationTemplateBase):
    tenant_id: str


class NotificationTemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    template_type: Optional[str] = Field(None, min_length=1, max_length=50)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    subject_template: Optional[str] = Field(None, max_length=200)
    title_template: Optional[str] = Field(None, max_length=200)
    message_template: Optional[str] = Field(None, min_length=1)
    html_template: Optional[str] = None
    variables: Optional[Dict[str, Any]] = None
    default_values: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_system: Optional[bool] = None


class NotificationTemplateResponse(NotificationTemplateBase):
    id: str
    tenant_id: str
    usage_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationTemplateListResponse(BaseModel):
    templates: List[NotificationTemplateResponse]
    total: int
    page: int
    size: int


# Notification Channel schemas
class NotificationChannelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    channel_type: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = {}
    credentials: Optional[Dict[str, Any]] = {}
    is_active: bool = True
    is_default: bool = False


class NotificationChannelCreate(NotificationChannelBase):
    tenant_id: str


class NotificationChannelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    channel_type: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    credentials: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    success_rate: Optional[Decimal] = Field(None, ge=0, le=100)
    average_delivery_time: Optional[int] = Field(None, ge=0)


class NotificationChannelResponse(NotificationChannelBase):
    id: str
    tenant_id: str
    success_rate: Decimal
    average_delivery_time: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationChannelListResponse(BaseModel):
    channels: List[NotificationChannelResponse]
    total: int
    page: int
    size: int


# Notification Delivery schemas
class NotificationDeliveryBase(BaseModel):
    notification_id: str
    channel_id: str
    delivery_status: str = Field("pending", max_length=20)
    delivery_attempts: int = Field(0, ge=0)
    max_attempts: int = Field(3, ge=1)
    external_id: Optional[str] = Field(None, max_length=100)
    response_data: Optional[Dict[str, Any]] = {}
    error_message: Optional[str] = None


class NotificationDeliveryCreate(NotificationDeliveryBase):
    pass


class NotificationDeliveryUpdate(BaseModel):
    delivery_status: Optional[str] = Field(None, max_length=20)
    delivery_attempts: Optional[int] = Field(None, ge=0)
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    external_id: Optional[str] = Field(None, max_length=100)
    response_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None


class NotificationDeliveryResponse(NotificationDeliveryBase):
    id: str
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationDeliveryListResponse(BaseModel):
    deliveries: List[NotificationDeliveryResponse]
    total: int
    page: int
    size: int


# Notification Subscription schemas
class NotificationSubscriptionBase(BaseModel):
    user_id: str
    user_type: str = Field(..., min_length=1, max_length=20)
    category: str = Field(..., min_length=1, max_length=50)
    email_enabled: bool = True
    sms_enabled: bool = False
    push_enabled: bool = True
    in_app_enabled: bool = True
    email: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    push_token: Optional[str] = Field(None, max_length=500)
    is_active: bool = True
    frequency: str = Field("immediate", max_length=20)


class NotificationSubscriptionCreate(NotificationSubscriptionBase):
    tenant_id: str


class NotificationSubscriptionUpdate(BaseModel):
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    email_enabled: Optional[bool] = None
    sms_enabled: Optional[bool] = None
    push_enabled: Optional[bool] = None
    in_app_enabled: Optional[bool] = None
    email: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    push_token: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None
    frequency: Optional[str] = Field(None, max_length=20)


class NotificationSubscriptionResponse(NotificationSubscriptionBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationSubscriptionListResponse(BaseModel):
    subscriptions: List[NotificationSubscriptionResponse]
    total: int
    page: int
    size: int


# Notification Batch schemas
class NotificationBatchBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    batch_type: str = Field(..., min_length=1, max_length=50)
    template_id: Optional[str] = None
    subject: Optional[str] = Field(None, max_length=200)
    message: str = Field(..., min_length=1)
    template_data: Optional[Dict[str, Any]] = {}
    recipient_filters: Optional[Dict[str, Any]] = {}
    scheduled_at: Optional[datetime] = None


class NotificationBatchCreate(NotificationBatchBase):
    tenant_id: str


class NotificationBatchUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    batch_type: Optional[str] = Field(None, min_length=1, max_length=50)
    template_id: Optional[str] = None
    subject: Optional[str] = Field(None, max_length=200)
    message: Optional[str] = Field(None, min_length=1)
    template_data: Optional[Dict[str, Any]] = None
    recipient_filters: Optional[Dict[str, Any]] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[str] = Field(None, max_length=20)


class NotificationBatchResponse(NotificationBatchBase):
    id: str
    tenant_id: str
    total_recipients: int
    processed_recipients: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: str
    success_count: int
    failure_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationBatchListResponse(BaseModel):
    batches: List[NotificationBatchResponse]
    total: int
    page: int
    size: int


# Notification Analytics schemas
class NotificationAnalyticsBase(BaseModel):
    tenant_id: str
    total_notifications: int = Field(0, ge=0)
    sent_notifications: int = Field(0, ge=0)
    delivered_notifications: int = Field(0, ge=0)
    failed_notifications: int = Field(0, ge=0)
    email_sent: int = Field(0, ge=0)
    email_delivered: int = Field(0, ge=0)
    sms_sent: int = Field(0, ge=0)
    sms_delivered: int = Field(0, ge=0)
    push_sent: int = Field(0, ge=0)
    push_delivered: int = Field(0, ge=0)
    average_delivery_time: int = Field(0, ge=0)
    success_rate: Decimal = Field(0.0, ge=0, le=100)
    category_stats: Optional[Dict[str, Any]] = {}
    hourly_stats: Optional[Dict[str, Any]] = {}
    daily_stats: Optional[Dict[str, Any]] = {}


class NotificationAnalyticsCreate(NotificationAnalyticsBase):
    pass


class NotificationAnalyticsUpdate(BaseModel):
    total_notifications: Optional[int] = Field(None, ge=0)
    sent_notifications: Optional[int] = Field(None, ge=0)
    delivered_notifications: Optional[int] = Field(None, ge=0)
    failed_notifications: Optional[int] = Field(None, ge=0)
    email_sent: Optional[int] = Field(None, ge=0)
    email_delivered: Optional[int] = Field(None, ge=0)
    sms_sent: Optional[int] = Field(None, ge=0)
    sms_delivered: Optional[int] = Field(None, ge=0)
    push_sent: Optional[int] = Field(None, ge=0)
    push_delivered: Optional[int] = Field(None, ge=0)
    average_delivery_time: Optional[int] = Field(None, ge=0)
    success_rate: Optional[Decimal] = Field(None, ge=0, le=100)
    category_stats: Optional[Dict[str, Any]] = None
    hourly_stats: Optional[Dict[str, Any]] = None
    daily_stats: Optional[Dict[str, Any]] = None


class NotificationAnalyticsResponse(NotificationAnalyticsBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotificationAnalyticsListResponse(BaseModel):
    analytics: List[NotificationAnalyticsResponse]
    total: int
    page: int
    size: int


# Summary schemas
class NotificationSummary(BaseModel):
    total_notifications: int
    pending_notifications: int
    sent_notifications: int
    delivered_notifications: int
    failed_notifications: int
    success_rate: Decimal
    average_delivery_time: int
    active_channels: int
    active_templates: int


class UserNotificationSummary(BaseModel):
    user_id: str
    user_type: str
    total_notifications: int
    unread_notifications: int
    email_notifications: int
    sms_notifications: int
    push_notifications: int
    in_app_notifications: int
    last_notification_at: Optional[datetime] = None 