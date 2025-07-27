"""
Communications router for Communication Service (AI SchoolOS)
"""

import logging
from typing import List, Optional
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from decimal import Decimal

from database import get_db
from models import Message, ChatRoom, ChatParticipant, ChatMessage, MessageRead, Announcement, Broadcast, CommunicationTemplate, CommunicationAnalytics
from schemas import (
    MessageCreate, MessageUpdate, MessageResponse, MessageListResponse,
    ChatRoomCreate, ChatRoomUpdate, ChatRoomResponse, ChatRoomListResponse,
    ChatParticipantCreate, ChatParticipantUpdate, ChatParticipantResponse, ChatParticipantListResponse,
    ChatMessageCreate, ChatMessageUpdate, ChatMessageResponse, ChatMessageListResponse,
    AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse, AnnouncementListResponse,
    BroadcastCreate, BroadcastUpdate, BroadcastResponse, BroadcastListResponse,
    CommunicationTemplateCreate, CommunicationTemplateUpdate, CommunicationTemplateResponse, CommunicationTemplateListResponse,
    CommunicationAnalyticsCreate, CommunicationAnalyticsUpdate, CommunicationAnalyticsResponse, CommunicationAnalyticsListResponse,
    CommunicationSummary, UserCommunicationSummary, ChatRoomSummary
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/communications", tags=["communications"])


@router.get("/")
async def root():
    return {"message": "Communication Service is running"}


# Message CRUD Operations
@router.post("/messages", response_model=MessageResponse)
async def create_message(
    message_data: MessageCreate,
    db: Session = Depends(get_db)
):
    """Create a new message."""
    try:
        # Create new message
        message = Message(**message_data.dict())
        db.add(message)
        db.commit()
        db.refresh(message)
        
        logger.info(f"New message created from {message.sender_id} to {message.recipient_id}")
        return message
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/messages", response_model=MessageListResponse)
async def get_messages(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    sender_id: Optional[str] = None,
    recipient_id: Optional[str] = None,
    message_type: Optional[str] = None,
    is_read: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of messages with filtering and pagination."""
    try:
        query = db.query(Message)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Message.tenant_id == tenant_id)
        
        if sender_id:
            query = query.filter(Message.sender_id == sender_id)
        
        if recipient_id:
            query = query.filter(Message.recipient_id == recipient_id)
        
        if message_type:
            query = query.filter(Message.message_type == message_type)
        
        if is_read is not None:
            query = query.filter(Message.is_read == is_read)
        
        # Search functionality
        if search:
            search_filter = or_(
                Message.subject.ilike(f"%{search}%"),
                Message.content.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        messages = query.offset(skip).limit(limit).all()
        
        return MessageListResponse(
            messages=messages,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting messages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific message by ID."""
    try:
        message = db.query(Message).filter(Message.id == message_id).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        return message
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/messages/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: str,
    message_data: MessageUpdate,
    db: Session = Depends(get_db)
):
    """Update a message."""
    try:
        message = db.query(Message).filter(Message.id == message_id).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        # Update fields
        update_data = message_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(message, field, value)
        
        message.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(message)
        
        logger.info(f"Message updated: {message.id}")
        return message
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/messages/{message_id}")
async def delete_message(
    message_id: str,
    db: Session = Depends(get_db)
):
    """Delete a message (soft delete)."""
    try:
        message = db.query(Message).filter(Message.id == message_id).first()
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Message not found"
            )
        
        # Soft delete
        message.is_deleted = True
        message.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Message deleted: {message.id}")
        return {"message": "Message deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Chat Room Operations
@router.post("/chat-rooms", response_model=ChatRoomResponse)
async def create_chat_room(
    room_data: ChatRoomCreate,
    db: Session = Depends(get_db)
):
    """Create a new chat room."""
    try:
        # Create new chat room
        room = ChatRoom(**room_data.dict())
        db.add(room)
        db.commit()
        db.refresh(room)
        
        logger.info(f"New chat room created: {room.name}")
        return room
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating chat room: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/chat-rooms", response_model=ChatRoomListResponse)
async def get_chat_rooms(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    room_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    created_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get chat rooms with filtering and pagination."""
    try:
        query = db.query(ChatRoom)
        
        # Apply filters
        if tenant_id:
            query = query.filter(ChatRoom.tenant_id == tenant_id)
        
        if room_type:
            query = query.filter(ChatRoom.room_type == room_type)
        
        if is_active is not None:
            query = query.filter(ChatRoom.is_active == is_active)
        
        if created_by:
            query = query.filter(ChatRoom.created_by == created_by)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        chat_rooms = query.offset(skip).limit(limit).all()
        
        return ChatRoomListResponse(
            chat_rooms=chat_rooms,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting chat rooms: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/chat-rooms/{room_id}", response_model=ChatRoomResponse)
async def get_chat_room(
    room_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific chat room by ID."""
    try:
        room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat room not found"
            )
        
        return room
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting chat room: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Chat Participant Operations
@router.post("/chat-rooms/{room_id}/participants", response_model=ChatParticipantResponse)
async def add_participant(
    room_id: str,
    participant_data: ChatParticipantCreate,
    db: Session = Depends(get_db)
):
    """Add a participant to a chat room."""
    try:
        # Check if room exists
        room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat room not found"
            )
        
        # Check if participant already exists
        existing_participant = db.query(ChatParticipant).filter(
            and_(
                ChatParticipant.room_id == room_id,
                ChatParticipant.user_id == participant_data.user_id
            )
        ).first()
        
        if existing_participant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Participant already exists in this room"
            )
        
        # Create new participant
        participant = ChatParticipant(**participant_data.dict())
        db.add(participant)
        db.commit()
        db.refresh(participant)
        
        logger.info(f"Participant added to chat room: {participant.user_id}")
        return participant
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding participant: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/chat-rooms/{room_id}/participants", response_model=ChatParticipantListResponse)
async def get_participants(
    room_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get participants of a chat room."""
    try:
        query = db.query(ChatParticipant).filter(ChatParticipant.room_id == room_id)
        
        if is_active is not None:
            query = query.filter(ChatParticipant.is_active == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        participants = query.offset(skip).limit(limit).all()
        
        return ChatParticipantListResponse(
            participants=participants,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting participants: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Chat Message Operations
@router.post("/chat-rooms/{room_id}/messages", response_model=ChatMessageResponse)
async def create_chat_message(
    room_id: str,
    message_data: ChatMessageCreate,
    db: Session = Depends(get_db)
):
    """Create a new chat message."""
    try:
        # Check if room exists
        room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat room not found"
            )
        
        # Create new chat message
        message = ChatMessage(**message_data.dict())
        db.add(message)
        db.commit()
        db.refresh(message)
        
        logger.info(f"New chat message created in room {room_id}")
        return message
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating chat message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/chat-rooms/{room_id}/messages", response_model=ChatMessageListResponse)
async def get_chat_messages(
    room_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sender_id: Optional[str] = None,
    message_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get messages from a chat room."""
    try:
        query = db.query(ChatMessage).filter(ChatMessage.room_id == room_id)
        
        if sender_id:
            query = query.filter(ChatMessage.sender_id == sender_id)
        
        if message_type:
            query = query.filter(ChatMessage.message_type == message_type)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and order by sent_at
        messages = query.order_by(ChatMessage.sent_at.desc()).offset(skip).limit(limit).all()
        
        return ChatMessageListResponse(
            messages=messages,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting chat messages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Announcement Operations
@router.post("/announcements", response_model=AnnouncementResponse)
async def create_announcement(
    announcement_data: AnnouncementCreate,
    db: Session = Depends(get_db)
):
    """Create a new announcement."""
    try:
        # Create new announcement
        announcement = Announcement(**announcement_data.dict())
        db.add(announcement)
        db.commit()
        db.refresh(announcement)
        
        logger.info(f"New announcement created: {announcement.title}")
        return announcement
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating announcement: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/announcements", response_model=AnnouncementListResponse)
async def get_announcements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    announcement_type: Optional[str] = None,
    author_id: Optional[str] = None,
    status: Optional[str] = None,
    is_public: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get announcements with filtering and pagination."""
    try:
        query = db.query(Announcement)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Announcement.tenant_id == tenant_id)
        
        if announcement_type:
            query = query.filter(Announcement.announcement_type == announcement_type)
        
        if author_id:
            query = query.filter(Announcement.author_id == author_id)
        
        if status:
            query = query.filter(Announcement.status == status)
        
        if is_public is not None:
            query = query.filter(Announcement.is_public == is_public)
        
        # Search functionality
        if search:
            search_filter = or_(
                Announcement.title.ilike(f"%{search}%"),
                Announcement.content.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and order by published_at
        announcements = query.order_by(Announcement.published_at.desc()).offset(skip).limit(limit).all()
        
        return AnnouncementListResponse(
            announcements=announcements,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting announcements: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Broadcast Operations
@router.post("/broadcasts", response_model=BroadcastResponse)
async def create_broadcast(
    broadcast_data: BroadcastCreate,
    db: Session = Depends(get_db)
):
    """Create a new broadcast."""
    try:
        # Create new broadcast
        broadcast = Broadcast(**broadcast_data.dict())
        db.add(broadcast)
        db.commit()
        db.refresh(broadcast)
        
        logger.info(f"New broadcast created: {broadcast.title}")
        return broadcast
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating broadcast: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/broadcasts", response_model=BroadcastListResponse)
async def get_broadcasts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    broadcast_type: Optional[str] = None,
    author_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get broadcasts with filtering and pagination."""
    try:
        query = db.query(Broadcast)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Broadcast.tenant_id == tenant_id)
        
        if broadcast_type:
            query = query.filter(Broadcast.broadcast_type == broadcast_type)
        
        if author_id:
            query = query.filter(Broadcast.author_id == author_id)
        
        if status:
            query = query.filter(Broadcast.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and order by created_at
        broadcasts = query.order_by(Broadcast.created_at.desc()).offset(skip).limit(limit).all()
        
        return BroadcastListResponse(
            broadcasts=broadcasts,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting broadcasts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Communication Template Operations
@router.post("/templates", response_model=CommunicationTemplateResponse)
async def create_template(
    template_data: CommunicationTemplateCreate,
    db: Session = Depends(get_db)
):
    """Create a new communication template."""
    try:
        # Create new template
        template = CommunicationTemplate(**template_data.dict())
        db.add(template)
        db.commit()
        db.refresh(template)
        
        logger.info(f"New communication template created: {template.name}")
        return template
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating template: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/templates", response_model=CommunicationTemplateListResponse)
async def get_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    template_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_system: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get communication templates with filtering and pagination."""
    try:
        query = db.query(CommunicationTemplate)
        
        # Apply filters
        if tenant_id:
            query = query.filter(CommunicationTemplate.tenant_id == tenant_id)
        
        if template_type:
            query = query.filter(CommunicationTemplate.template_type == template_type)
        
        if is_active is not None:
            query = query.filter(CommunicationTemplate.is_active == is_active)
        
        if is_system is not None:
            query = query.filter(CommunicationTemplate.is_system == is_system)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        templates = query.offset(skip).limit(limit).all()
        
        return CommunicationTemplateListResponse(
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


# Summary Endpoints
@router.get("/summary", response_model=CommunicationSummary)
async def get_communication_summary(
    tenant_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get communication summary statistics."""
    try:
        # Build base queries
        messages_query = db.query(Message)
        announcements_query = db.query(Announcement)
        broadcasts_query = db.query(Broadcast)
        chat_rooms_query = db.query(ChatRoom)
        
        # Apply filters
        if tenant_id:
            messages_query = messages_query.filter(Message.tenant_id == tenant_id)
            announcements_query = announcements_query.filter(Announcement.tenant_id == tenant_id)
            broadcasts_query = broadcasts_query.filter(Broadcast.tenant_id == tenant_id)
            chat_rooms_query = chat_rooms_query.filter(ChatRoom.tenant_id == tenant_id)
        
        # Get statistics
        total_messages = messages_query.count()
        total_announcements = announcements_query.count()
        total_broadcasts = broadcasts_query.count()
        active_chat_rooms = chat_rooms_query.filter(ChatRoom.is_active == True).count()
        unread_messages = messages_query.filter(Message.is_read == False).count()
        
        # Calculate success rates
        message_success_rate = Decimal('100.0') if total_messages > 0 else Decimal('0.0')
        broadcast_success_rate = Decimal('100.0') if total_broadcasts > 0 else Decimal('0.0')
        
        # Get user statistics (simplified)
        active_users = messages_query.with_entities(Message.sender_id).distinct().count()
        total_users = active_users  # Simplified for now
        
        return CommunicationSummary(
            total_messages=total_messages,
            total_announcements=total_announcements,
            total_broadcasts=total_broadcasts,
            active_chat_rooms=active_chat_rooms,
            unread_messages=unread_messages,
            active_users=active_users,
            total_users=total_users,
            message_success_rate=message_success_rate,
            broadcast_success_rate=broadcast_success_rate
        )
        
    except Exception as e:
        logger.error(f"Error getting communication summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/users/{user_id}/summary", response_model=UserCommunicationSummary)
async def get_user_communication_summary(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get communication summary for a specific user."""
    try:
        # Get message statistics for user
        messages_sent = db.query(Message).filter(Message.sender_id == user_id).count()
        messages_received = db.query(Message).filter(Message.recipient_id == user_id).count()
        unread_messages = db.query(Message).filter(
            and_(
                Message.recipient_id == user_id,
                Message.is_read == False
            )
        ).count()
        
        # Get chat room statistics
        active_chat_rooms = db.query(ChatParticipant).filter(
            and_(
                ChatParticipant.user_id == user_id,
                ChatParticipant.is_active == True
            )
        ).count()
        
        # Get last activity times
        last_message = db.query(Message).filter(
            or_(
                Message.sender_id == user_id,
                Message.recipient_id == user_id
            )
        ).order_by(Message.sent_at.desc()).first()
        
        last_message_at = last_message.sent_at if last_message else None
        last_activity_at = last_message_at  # Simplified for now
        
        # Get user type from first message
        user_message = db.query(Message).filter(
            or_(
                Message.sender_id == user_id,
                Message.recipient_id == user_id
            )
        ).first()
        user_type = user_message.sender_type if user_message and user_message.sender_id == user_id else "unknown"
        
        return UserCommunicationSummary(
            user_id=user_id,
            user_type=user_type,
            total_messages_sent=messages_sent,
            total_messages_received=messages_received,
            unread_messages=unread_messages,
            active_chat_rooms=active_chat_rooms,
            last_message_at=last_message_at,
            last_activity_at=last_activity_at
        )
        
    except Exception as e:
        logger.error(f"Error getting user communication summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 