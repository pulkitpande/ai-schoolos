"""
Timetable Service Router (AI SchoolOS)

Comprehensive timetable management endpoints including:
- Subjects, Teachers, Rooms (CRUD)
- Time slots and timetable slots
- Constraints and conflicts
- Schedules and templates
"""

from datetime import datetime, date, time
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from slowapi import Limiter
from slowapi.util import get_remote_address

from database import get_db
from models import (
    Subject, Teacher, Room, TimeSlot, TimetableSlot, TimetableConstraint,
    TimetableSchedule, TimetableConflict, TimetableTemplate
)
from schemas import (
    # Subjects
    SubjectCreate, SubjectUpdate, SubjectResponse,
    # Teachers
    TeacherCreate, TeacherUpdate, TeacherResponse,
    # Rooms
    RoomCreate, RoomUpdate, RoomResponse,
    # Time Slots
    TimeSlotCreate, TimeSlotUpdate, TimeSlotResponse,
    # Timetable Slots
    TimetableSlotCreate, TimetableSlotUpdate, TimetableSlotResponse,
    # Constraints
    TimetableConstraintCreate, TimetableConstraintUpdate, TimetableConstraintResponse,
    # Schedules
    TimetableScheduleCreate, TimetableScheduleUpdate, TimetableScheduleResponse,
    # Conflicts
    TimetableConflictCreate, TimetableConflictUpdate, TimetableConflictResponse,
    # Templates
    TimetableTemplateCreate, TimetableTemplateUpdate, TimetableTemplateResponse,
    # Bulk Operations
    BulkTimetableSlotCreate, BulkTimetableSlotResponse,
    # Search and Stats
    TimetableSearchParams, TimetableStats,
    # Response Models
    SuccessResponse, ErrorResponse
)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/api/v1/timetable", tags=["timetable"])


# ============================================================================
# SUBJECTS
# ============================================================================

@router.post("/subjects", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("50/minute")
async def create_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new subject."""
    try:
        db_subject = Subject(
            tenant_id=tenant_id,
            **subject.dict()
        )
        db.add(db_subject)
        db.commit()
        db.refresh(db_subject)
        return db_subject
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create subject: {str(e)}"
        )


@router.get("/subjects/{subject_id}", response_model=SubjectResponse)
@limiter.limit("200/minute")
async def get_subject(
    subject_id: str = Path(..., description="Subject ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific subject."""
    subject = db.query(Subject).filter(
        and_(
            Subject.id == subject_id,
            Subject.tenant_id == tenant_id
        )
    ).first()
    
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    return subject


@router.get("/subjects", response_model=List[SubjectResponse])
@limiter.limit("200/minute")
async def list_subjects(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    subject_type: Optional[str] = Query(None, description="Subject type"),
    subject_category: Optional[str] = Query(None, description="Subject category"),
    is_active: Optional[bool] = Query(None, description="Is active")
):
    """List subjects with filtering."""
    query = db.query(Subject).filter(
        Subject.tenant_id == tenant_id
    )
    
    if subject_type:
        query = query.filter(Subject.subject_type == subject_type)
    if subject_category:
        query = query.filter(Subject.subject_category == subject_category)
    if is_active is not None:
        query = query.filter(Subject.is_active == is_active)
    
    return query.all()


@router.put("/subjects/{subject_id}", response_model=SubjectResponse)
@limiter.limit("50/minute")
async def update_subject(
    subject_update: SubjectUpdate,
    subject_id: str = Path(..., description="Subject ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update a subject."""
    subject = db.query(Subject).filter(
        and_(
            Subject.id == subject_id,
            Subject.tenant_id == tenant_id
        )
    ).first()
    
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    try:
        update_data = subject_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(subject, field, value)
        
        subject.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(subject)
        return subject
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update subject: {str(e)}"
        )


@router.delete("/subjects/{subject_id}", response_model=SuccessResponse)
@limiter.limit("30/minute")
async def delete_subject(
    subject_id: str = Path(..., description="Subject ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete a subject."""
    subject = db.query(Subject).filter(
        and_(
            Subject.id == subject_id,
            Subject.tenant_id == tenant_id
        )
    ).first()
    
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    try:
        db.delete(subject)
        db.commit()
        return SuccessResponse(message="Subject deleted successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete subject: {str(e)}"
        )


# ============================================================================
# TEACHERS
# ============================================================================

@router.post("/teachers", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("50/minute")
async def create_teacher(
    teacher: TeacherCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new teacher."""
    try:
        db_teacher = Teacher(
            tenant_id=tenant_id,
            **teacher.dict()
        )
        db.add(db_teacher)
        db.commit()
        db.refresh(db_teacher)
        return db_teacher
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create teacher: {str(e)}"
        )


@router.get("/teachers/{teacher_id}", response_model=TeacherResponse)
@limiter.limit("200/minute")
async def get_teacher(
    teacher_id: str = Path(..., description="Teacher ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific teacher."""
    teacher = db.query(Teacher).filter(
        and_(
            Teacher.id == teacher_id,
            Teacher.tenant_id == tenant_id
        )
    ).first()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    return teacher


@router.get("/teachers", response_model=List[TeacherResponse])
@limiter.limit("200/minute")
async def list_teachers(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    is_active: Optional[bool] = Query(None, description="Is active"),
    is_full_time: Optional[bool] = Query(None, description="Is full time")
):
    """List teachers with filtering."""
    query = db.query(Teacher).filter(
        Teacher.tenant_id == tenant_id
    )
    
    if is_active is not None:
        query = query.filter(Teacher.is_active == is_active)
    if is_full_time is not None:
        query = query.filter(Teacher.is_full_time == is_full_time)
    
    return query.all()


@router.put("/teachers/{teacher_id}", response_model=TeacherResponse)
@limiter.limit("50/minute")
async def update_teacher(
    teacher_update: TeacherUpdate,
    teacher_id: str = Path(..., description="Teacher ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update a teacher."""
    teacher = db.query(Teacher).filter(
        and_(
            Teacher.id == teacher_id,
            Teacher.tenant_id == tenant_id
        )
    ).first()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    try:
        update_data = teacher_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(teacher, field, value)
        
        teacher.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(teacher)
        return teacher
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update teacher: {str(e)}"
        )


@router.delete("/teachers/{teacher_id}", response_model=SuccessResponse)
@limiter.limit("30/minute")
async def delete_teacher(
    teacher_id: str = Path(..., description="Teacher ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete a teacher."""
    teacher = db.query(Teacher).filter(
        and_(
            Teacher.id == teacher_id,
            Teacher.tenant_id == tenant_id
        )
    ).first()
    
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    try:
        db.delete(teacher)
        db.commit()
        return SuccessResponse(message="Teacher deleted successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete teacher: {str(e)}"
        )


# ============================================================================
# ROOMS
# ============================================================================

@router.post("/rooms", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("50/minute")
async def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new room."""
    try:
        db_room = Room(
            tenant_id=tenant_id,
            **room.dict()
        )
        db.add(db_room)
        db.commit()
        db.refresh(db_room)
        return db_room
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create room: {str(e)}"
        )


@router.get("/rooms/{room_id}", response_model=RoomResponse)
@limiter.limit("200/minute")
async def get_room(
    room_id: str = Path(..., description="Room ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific room."""
    room = db.query(Room).filter(
        and_(
            Room.id == room_id,
            Room.tenant_id == tenant_id
        )
    ).first()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    return room


@router.get("/rooms", response_model=List[RoomResponse])
@limiter.limit("200/minute")
async def list_rooms(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    room_type: Optional[str] = Query(None, description="Room type"),
    is_active: Optional[bool] = Query(None, description="Is active"),
    is_available: Optional[bool] = Query(None, description="Is available")
):
    """List rooms with filtering."""
    query = db.query(Room).filter(
        Room.tenant_id == tenant_id
    )
    
    if room_type:
        query = query.filter(Room.room_type == room_type)
    if is_active is not None:
        query = query.filter(Room.is_active == is_active)
    if is_available is not None:
        query = query.filter(Room.is_available == is_available)
    
    return query.all()


@router.put("/rooms/{room_id}", response_model=RoomResponse)
@limiter.limit("50/minute")
async def update_room(
    room_update: RoomUpdate,
    room_id: str = Path(..., description="Room ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update a room."""
    room = db.query(Room).filter(
        and_(
            Room.id == room_id,
            Room.tenant_id == tenant_id
        )
    ).first()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    try:
        update_data = room_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(room, field, value)
        
        room.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(room)
        return room
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update room: {str(e)}"
        )


@router.delete("/rooms/{room_id}", response_model=SuccessResponse)
@limiter.limit("30/minute")
async def delete_room(
    room_id: str = Path(..., description="Room ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete a room."""
    room = db.query(Room).filter(
        and_(
            Room.id == room_id,
            Room.tenant_id == tenant_id
        )
    ).first()
    
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    try:
        db.delete(room)
        db.commit()
        return SuccessResponse(message="Room deleted successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete room: {str(e)}"
        )


# ============================================================================
# TIME SLOTS
# ============================================================================

@router.post("/time-slots", response_model=TimeSlotResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("50/minute")
async def create_time_slot(
    time_slot: TimeSlotCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new time slot."""
    try:
        db_time_slot = TimeSlot(
            tenant_id=tenant_id,
            **time_slot.dict()
        )
        db.add(db_time_slot)
        db.commit()
        db.refresh(db_time_slot)
        return db_time_slot
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create time slot: {str(e)}"
        )


@router.get("/time-slots/{time_slot_id}", response_model=TimeSlotResponse)
@limiter.limit("200/minute")
async def get_time_slot(
    time_slot_id: str = Path(..., description="Time slot ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific time slot."""
    time_slot = db.query(TimeSlot).filter(
        and_(
            TimeSlot.id == time_slot_id,
            TimeSlot.tenant_id == tenant_id
        )
    ).first()
    
    if not time_slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Time slot not found"
        )
    
    return time_slot


@router.get("/time-slots", response_model=List[TimeSlotResponse])
@limiter.limit("200/minute")
async def list_time_slots(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    day_of_week: Optional[str] = Query(None, description="Day of week"),
    is_break: Optional[bool] = Query(None, description="Is break"),
    is_active: Optional[bool] = Query(None, description="Is active")
):
    """List time slots with filtering."""
    query = db.query(TimeSlot).filter(
        TimeSlot.tenant_id == tenant_id
    )
    
    if day_of_week:
        query = query.filter(TimeSlot.day_of_week == day_of_week)
    if is_break is not None:
        query = query.filter(TimeSlot.is_break == is_break)
    if is_active is not None:
        query = query.filter(TimeSlot.is_active == is_active)
    
    return query.order_by(TimeSlot.slot_number).all()


@router.put("/time-slots/{time_slot_id}", response_model=TimeSlotResponse)
@limiter.limit("50/minute")
async def update_time_slot(
    time_slot_update: TimeSlotUpdate,
    time_slot_id: str = Path(..., description="Time slot ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update a time slot."""
    time_slot = db.query(TimeSlot).filter(
        and_(
            TimeSlot.id == time_slot_id,
            TimeSlot.tenant_id == tenant_id
        )
    ).first()
    
    if not time_slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Time slot not found"
        )
    
    try:
        update_data = time_slot_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(time_slot, field, value)
        
        time_slot.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(time_slot)
        return time_slot
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update time slot: {str(e)}"
        )


@router.delete("/time-slots/{time_slot_id}", response_model=SuccessResponse)
@limiter.limit("30/minute")
async def delete_time_slot(
    time_slot_id: str = Path(..., description="Time slot ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete a time slot."""
    time_slot = db.query(TimeSlot).filter(
        and_(
            TimeSlot.id == time_slot_id,
            TimeSlot.tenant_id == tenant_id
        )
    ).first()
    
    if not time_slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Time slot not found"
        )
    
    try:
        db.delete(time_slot)
        db.commit()
        return SuccessResponse(message="Time slot deleted successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete time slot: {str(e)}"
        )


# ============================================================================
# TIMETABLE SLOTS
# ============================================================================

@router.post("/slots", response_model=TimetableSlotResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("100/minute")
async def create_timetable_slot(
    slot: TimetableSlotCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new timetable slot."""
    try:
        db_slot = TimetableSlot(
            tenant_id=tenant_id,
            **slot.dict()
        )
        db.add(db_slot)
        db.commit()
        db.refresh(db_slot)
        return db_slot
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create timetable slot: {str(e)}"
        )


@router.get("/slots/{slot_id}", response_model=TimetableSlotResponse)
@limiter.limit("200/minute")
async def get_timetable_slot(
    slot_id: str = Path(..., description="Timetable slot ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific timetable slot."""
    slot = db.query(TimetableSlot).filter(
        and_(
            TimetableSlot.id == slot_id,
            TimetableSlot.tenant_id == tenant_id
        )
    ).first()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable slot not found"
        )
    
    return slot


@router.get("/slots", response_model=List[TimetableSlotResponse])
@limiter.limit("200/minute")
async def list_timetable_slots(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    class_id: Optional[str] = Query(None, description="Class ID"),
    section_id: Optional[str] = Query(None, description="Section ID"),
    subject_id: Optional[str] = Query(None, description="Subject ID"),
    teacher_id: Optional[str] = Query(None, description="Teacher ID"),
    room_id: Optional[str] = Query(None, description="Room ID"),
    day_of_week: Optional[str] = Query(None, description="Day of week"),
    academic_year: Optional[str] = Query(None, description="Academic year"),
    semester: Optional[str] = Query(None, description="Semester"),
    is_active: Optional[bool] = Query(None, description="Is active")
):
    """List timetable slots with filtering."""
    query = db.query(TimetableSlot).filter(
        TimetableSlot.tenant_id == tenant_id
    )
    
    if class_id:
        query = query.filter(TimetableSlot.class_id == class_id)
    if section_id:
        query = query.filter(TimetableSlot.section_id == section_id)
    if subject_id:
        query = query.filter(TimetableSlot.subject_id == subject_id)
    if teacher_id:
        query = query.filter(TimetableSlot.teacher_id == teacher_id)
    if room_id:
        query = query.filter(TimetableSlot.room_id == room_id)
    if day_of_week:
        query = query.filter(TimetableSlot.day_of_week == day_of_week)
    if academic_year:
        query = query.filter(TimetableSlot.academic_year == academic_year)
    if semester:
        query = query.filter(TimetableSlot.semester == semester)
    if is_active is not None:
        query = query.filter(TimetableSlot.is_active == is_active)
    
    return query.order_by(TimetableSlot.day_of_week, TimetableSlot.start_time).all()


@router.put("/slots/{slot_id}", response_model=TimetableSlotResponse)
@limiter.limit("100/minute")
async def update_timetable_slot(
    slot_update: TimetableSlotUpdate,
    slot_id: str = Path(..., description="Timetable slot ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update a timetable slot."""
    slot = db.query(TimetableSlot).filter(
        and_(
            TimetableSlot.id == slot_id,
            TimetableSlot.tenant_id == tenant_id
        )
    ).first()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable slot not found"
        )
    
    try:
        update_data = slot_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(slot, field, value)
        
        slot.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(slot)
        return slot
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update timetable slot: {str(e)}"
        )


@router.delete("/slots/{slot_id}", response_model=SuccessResponse)
@limiter.limit("50/minute")
async def delete_timetable_slot(
    slot_id: str = Path(..., description="Timetable slot ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete a timetable slot."""
    slot = db.query(TimetableSlot).filter(
        and_(
            TimetableSlot.id == slot_id,
            TimetableSlot.tenant_id == tenant_id
        )
    ).first()
    
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable slot not found"
        )
    
    try:
        db.delete(slot)
        db.commit()
        return SuccessResponse(message="Timetable slot deleted successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete timetable slot: {str(e)}"
        )


# ============================================================================
# STATISTICS
# ============================================================================

@router.get("/stats", response_model=TimetableStats)
@limiter.limit("100/minute")
async def get_timetable_stats(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    academic_year: Optional[str] = Query(None, description="Academic year")
):
    """Get timetable statistics."""
    # Count total slots
    slots_query = db.query(TimetableSlot).filter(
        TimetableSlot.tenant_id == tenant_id
    )
    if academic_year:
        slots_query = slots_query.filter(TimetableSlot.academic_year == academic_year)
    
    total_slots = slots_query.count()
    
    # Count total hours
    total_hours = db.query(func.sum(TimetableSlot.end_time - TimetableSlot.start_time)).filter(
        TimetableSlot.tenant_id == tenant_id
    ).scalar() or 0
    
    # Count subjects, teachers, rooms
    total_subjects = db.query(Subject).filter(Subject.tenant_id == tenant_id).count()
    total_teachers = db.query(Teacher).filter(Teacher.tenant_id == tenant_id).count()
    total_rooms = db.query(Room).filter(Room.tenant_id == tenant_id).count()
    
    # Count conflicts
    conflicts_count = db.query(TimetableConflict).filter(
        and_(
            TimetableConflict.tenant_id == tenant_id,
            TimetableConflict.is_resolved == False
        )
    ).count()
    
    # Calculate utilization rate
    utilization_rate = (total_slots / (total_rooms * 40)) * 100 if total_rooms > 0 else 0
    
    return TimetableStats(
        total_slots=total_slots,
        total_hours=total_hours,
        total_subjects=total_subjects,
        total_teachers=total_teachers,
        total_rooms=total_rooms,
        conflicts_count=conflicts_count,
        utilization_rate=utilization_rate
    ) 