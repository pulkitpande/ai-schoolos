"""
Notifications router for Notification Service (AI SchoolOS)
"""

import logging
from typing import List, Optional
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from decimal import Decimal

from database import get_db
from models import Notification, NotificationTemplate, NotificationChannel, NotificationDelivery, NotificationSubscription, NotificationBatch, NotificationAnalytics
from schemas import (
    NotificationCreate, NotificationUpdate, NotificationResponse, NotificationListResponse,
    NotificationTemplateCreate, NotificationTemplateUpdate, NotificationTemplateResponse, NotificationTemplateListResponse,
    NotificationChannelCreate, NotificationChannelUpdate, NotificationChannelResponse, NotificationChannelListResponse,
    NotificationDeliveryCreate, NotificationDeliveryUpdate, NotificationDeliveryResponse, NotificationDeliveryListResponse,
    NotificationSubscriptionCreate, NotificationSubscriptionUpdate, NotificationSubscriptionResponse, NotificationSubscriptionListResponse,
    NotificationBatchCreate, NotificationBatchUpdate, NotificationBatchResponse, NotificationBatchListResponse,
    NotificationAnalyticsCreate, NotificationAnalyticsUpdate, NotificationAnalyticsResponse, NotificationAnalyticsListResponse,
    NotificationSummary, UserNotificationSummary
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notifications", tags=["notifications"])


# Notification CRUD Operations
@router.post("/", response_model=NotificationResponse)
async def create_notification(
    notification_data: NotificationCreate,
    db: Session = Depends(get_db)
):
    """Create a new notification."""
    try:
        # Create new notification
        notification = Notification(**notification_data.dict())
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        logger.info(f"New notification created: {notification.title}")
        return notification
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating notification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/", response_model=NotificationListResponse)
async def get_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    recipient_id: Optional[str] = None,
    recipient_type: Optional[str] = None,
    notification_type: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of notifications with filtering and pagination."""
    try:
        query = db.query(Notification)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Notification.tenant_id == tenant_id)
        
        if recipient_id:
            query = query.filter(Notification.recipient_id == recipient_id)
        
        if recipient_type:
            query = query.filter(Notification.recipient_type == recipient_type)
        
        if notification_type:
            query = query.filter(Notification.notification_type == notification_type)
        
        if status:
            query = query.filter(Notification.status == status)
        
        if priority:
            query = query.filter(Notification.priority == priority)
        
        # Search functionality
        if search:
            search_filter = or_(
                Notification.title.ilike(f"%{search}%"),
                Notification.message.ilike(f"%{search}%"),
                Notification.subject.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        notifications = query.offset(skip).limit(limit).all()
        
        return NotificationListResponse(
            notifications=notifications,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting notifications: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific notification by ID."""
    try:
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        
        return notification
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting notification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/{notification_id}", response_model=NotificationResponse)
async def update_notification(
    notification_id: str,
    notification_data: NotificationUpdate,
    db: Session = Depends(get_db)
):
    """Update a notification."""
    try:
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        
        # Update fields
        update_data = notification_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(notification, field, value)
        
        notification.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(notification)
        
        logger.info(f"Notification updated: {notification.title}")
        return notification
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating notification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: str,
    db: Session = Depends(get_db)
):
    """Delete a notification (soft delete)."""
    try:
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        
        if not notification:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification not found"
            )
        
        # Soft delete
        notification.status = "cancelled"
        notification.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Notification deleted: {notification.title}")
        return {"message": "Notification deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting notification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Notification Template Operations
@router.post("/templates", response_model=NotificationTemplateResponse)
async def create_template(
    template_data: NotificationTemplateCreate,
    db: Session = Depends(get_db)
):
    """Create a new notification template."""
    try:
        # Create new template
        template = NotificationTemplate(**template_data.dict())
        db.add(template)
        db.commit()
        db.refresh(template)
        
        logger.info(f"New notification template created: {template.name}")
        return template
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating template: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/templates", response_model=NotificationTemplateListResponse)
async def get_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    template_type: Optional[str] = None,
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_system: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get notification templates with filtering and pagination."""
    try:
        query = db.query(NotificationTemplate)
        
        # Apply filters
        if tenant_id:
            query = query.filter(NotificationTemplate.tenant_id == tenant_id)
        
        if template_type:
            query = query.filter(NotificationTemplate.template_type == template_type)
        
        if category:
            query = query.filter(NotificationTemplate.category == category)
        
        if is_active is not None:
            query = query.filter(NotificationTemplate.is_active == is_active)
        
        if is_system is not None:
            query = query.filter(NotificationTemplate.is_system == is_system)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        templates = query.offset(skip).limit(limit).all()
        
        return NotificationTemplateListResponse(
            templates=templates,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting templates: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/templates/{template_id}", response_model=NotificationTemplateResponse)
async def get_template(
    template_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific notification template by ID."""
    try:
        template = db.query(NotificationTemplate).filter(NotificationTemplate.id == template_id).first()
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification template not found"
            )
        
        return template
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting template: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/templates/{template_id}", response_model=NotificationTemplateResponse)
async def update_template(
    template_id: str,
    template_data: NotificationTemplateUpdate,
    db: Session = Depends(get_db)
):
    """Update a notification template."""
    try:
        template = db.query(NotificationTemplate).filter(NotificationTemplate.id == template_id).first()
        
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification template not found"
            )
        
        # Update fields
        update_data = template_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(template, field, value)
        
        template.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(template)
        
        logger.info(f"Notification template updated: {template.name}")
        return template
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating template: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Notification Channel Operations
@router.post("/channels", response_model=NotificationChannelResponse)
async def create_channel(
    channel_data: NotificationChannelCreate,
    db: Session = Depends(get_db)
):
    """Create a new notification channel."""
    try:
        # Create new channel
        channel = NotificationChannel(**channel_data.dict())
        db.add(channel)
        db.commit()
        db.refresh(channel)
        
        logger.info(f"New notification channel created: {channel.name}")
        return channel
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating channel: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/channels", response_model=NotificationChannelListResponse)
async def get_channels(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    channel_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_default: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get notification channels with filtering and pagination."""
    try:
        query = db.query(NotificationChannel)
        
        # Apply filters
        if tenant_id:
            query = query.filter(NotificationChannel.tenant_id == tenant_id)
        
        if channel_type:
            query = query.filter(NotificationChannel.channel_type == channel_type)
        
        if is_active is not None:
            query = query.filter(NotificationChannel.is_active == is_active)
        
        if is_default is not None:
            query = query.filter(NotificationChannel.is_default == is_default)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        channels = query.offset(skip).limit(limit).all()
        
        return NotificationChannelListResponse(
            channels=channels,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting channels: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Notification Subscription Operations
@router.post("/subscriptions", response_model=NotificationSubscriptionResponse)
async def create_subscription(
    subscription_data: NotificationSubscriptionCreate,
    db: Session = Depends(get_db)
):
    """Create a new notification subscription."""
    try:
        # Check if subscription already exists
        existing_subscription = db.query(NotificationSubscription).filter(
            and_(
                NotificationSubscription.user_id == subscription_data.user_id,
                NotificationSubscription.category == subscription_data.category,
                NotificationSubscription.tenant_id == subscription_data.tenant_id
            )
        ).first()
        
        if existing_subscription:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subscription already exists for this user and category"
            )
        
        # Create new subscription
        subscription = NotificationSubscription(**subscription_data.dict())
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        
        logger.info(f"New notification subscription created for user {subscription_data.user_id}")
        return subscription
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating subscription: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/subscriptions", response_model=NotificationSubscriptionListResponse)
async def get_subscriptions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    user_id: Optional[str] = None,
    user_type: Optional[str] = None,
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get notification subscriptions with filtering and pagination."""
    try:
        query = db.query(NotificationSubscription)
        
        # Apply filters
        if tenant_id:
            query = query.filter(NotificationSubscription.tenant_id == tenant_id)
        
        if user_id:
            query = query.filter(NotificationSubscription.user_id == user_id)
        
        if user_type:
            query = query.filter(NotificationSubscription.user_type == user_type)
        
        if category:
            query = query.filter(NotificationSubscription.category == category)
        
        if is_active is not None:
            query = query.filter(NotificationSubscription.is_active == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        subscriptions = query.offset(skip).limit(limit).all()
        
        return NotificationSubscriptionListResponse(
            subscriptions=subscriptions,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting subscriptions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Notification Batch Operations
@router.post("/batches", response_model=NotificationBatchResponse)
async def create_batch(
    batch_data: NotificationBatchCreate,
    db: Session = Depends(get_db)
):
    """Create a new notification batch."""
    try:
        # Create new batch
        batch = NotificationBatch(**batch_data.dict())
        db.add(batch)
        db.commit()
        db.refresh(batch)
        
        logger.info(f"New notification batch created: {batch.name}")
        return batch
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating batch: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/batches", response_model=NotificationBatchListResponse)
async def get_batches(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    batch_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get notification batches with filtering and pagination."""
    try:
        query = db.query(NotificationBatch)
        
        # Apply filters
        if tenant_id:
            query = query.filter(NotificationBatch.tenant_id == tenant_id)
        
        if batch_type:
            query = query.filter(NotificationBatch.batch_type == batch_type)
        
        if status:
            query = query.filter(NotificationBatch.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        batches = query.offset(skip).limit(limit).all()
        
        return NotificationBatchListResponse(
            batches=batches,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting batches: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Notification Analytics Operations
@router.post("/analytics", response_model=NotificationAnalyticsResponse)
async def create_analytics(
    analytics_data: NotificationAnalyticsCreate,
    db: Session = Depends(get_db)
):
    """Create new notification analytics."""
    try:
        # Create new analytics
        analytics = NotificationAnalytics(**analytics_data.dict())
        db.add(analytics)
        db.commit()
        db.refresh(analytics)
        
        logger.info(f"New notification analytics created for tenant {analytics_data.tenant_id}")
        return analytics
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating analytics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/analytics", response_model=NotificationAnalyticsListResponse)
async def get_analytics(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get notification analytics with filtering and pagination."""
    try:
        query = db.query(NotificationAnalytics)
        
        # Apply filters
        if tenant_id:
            query = query.filter(NotificationAnalytics.tenant_id == tenant_id)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        analytics = query.offset(skip).limit(limit).all()
        
        return NotificationAnalyticsListResponse(
            analytics=analytics,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Summary Endpoints
@router.get("/summary", response_model=NotificationSummary)
async def get_notification_summary(
    tenant_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get notification summary statistics."""
    try:
        # Build base queries
        notifications_query = db.query(Notification)
        channels_query = db.query(NotificationChannel)
        templates_query = db.query(NotificationTemplate)
        
        # Apply filters
        if tenant_id:
            notifications_query = notifications_query.filter(Notification.tenant_id == tenant_id)
            channels_query = channels_query.filter(NotificationChannel.tenant_id == tenant_id)
            templates_query = templates_query.filter(NotificationTemplate.tenant_id == tenant_id)
        
        # Get notification statistics
        total_notifications = notifications_query.count()
        pending_notifications = notifications_query.filter(Notification.status == "pending").count()
        sent_notifications = notifications_query.filter(Notification.status == "sent").count()
        delivered_notifications = notifications_query.filter(Notification.status == "delivered").count()
        failed_notifications = notifications_query.filter(Notification.status == "failed").count()
        
        # Get channel and template statistics
        active_channels = channels_query.filter(NotificationChannel.is_active == True).count()
        active_templates = templates_query.filter(NotificationTemplate.is_active == True).count()
        
        # Calculate averages
        success_rate = (delivered_notifications / max(total_notifications, 1)) * 100 if total_notifications > 0 else Decimal('0.00')
        avg_delivery_time = notifications_query.with_entities(func.avg(func.extract('epoch', Notification.sent_at) - func.extract('epoch', Notification.created_at))).scalar() or 0
        
        return NotificationSummary(
            total_notifications=total_notifications,
            pending_notifications=pending_notifications,
            sent_notifications=sent_notifications,
            delivered_notifications=delivered_notifications,
            failed_notifications=failed_notifications,
            success_rate=Decimal(str(success_rate)),
            average_delivery_time=int(avg_delivery_time),
            active_channels=active_channels,
            active_templates=active_templates
        )
        
    except Exception as e:
        logger.error(f"Error getting notification summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/users/{user_id}/summary", response_model=UserNotificationSummary)
async def get_user_notification_summary(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get notification summary for a specific user."""
    try:
        # Get notification statistics for user
        notifications_query = db.query(Notification).filter(Notification.recipient_id == user_id)
        
        total_notifications = notifications_query.count()
        unread_notifications = notifications_query.filter(Notification.status == "pending").count()
        
        # Get channel-specific statistics
        email_notifications = notifications_query.filter(Notification.notification_type == "email").count()
        sms_notifications = notifications_query.filter(Notification.notification_type == "sms").count()
        push_notifications = notifications_query.filter(Notification.notification_type == "push").count()
        in_app_notifications = notifications_query.filter(Notification.notification_type == "in_app").count()
        
        # Get last notification time
        last_notification = notifications_query.order_by(Notification.created_at.desc()).first()
        last_notification_at = last_notification.created_at if last_notification else None
        
        # Get user type from first notification
        user_type = notifications_query.with_entities(Notification.recipient_type).first()
        user_type = user_type[0] if user_type else "unknown"
        
        return UserNotificationSummary(
            user_id=user_id,
            user_type=user_type,
            total_notifications=total_notifications,
            unread_notifications=unread_notifications,
            email_notifications=email_notifications,
            sms_notifications=sms_notifications,
            push_notifications=push_notifications,
            in_app_notifications=in_app_notifications,
            last_notification_at=last_notification_at
        )
        
    except Exception as e:
        logger.error(f"Error getting user notification summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 