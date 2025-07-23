"""
SQLAlchemy models for Timetable Service (AI SchoolOS)
"""

from datetime import datetime, date, time
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


class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Subject Information
    subject_name: Mapped[str] = mapped_column(String(100), nullable=False)
    subject_code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    subject_type: Mapped[str] = mapped_column(String(50), nullable=False)  # core, elective, optional
    subject_category: Mapped[str] = mapped_column(String(50), nullable=True)  # science, arts, commerce
    
    # Academic Information
    grade_level: Mapped[str] = mapped_column(String(20), nullable=True)  # primary, secondary, higher
    class_levels: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Applicable classes
    credit_hours: Mapped[int] = mapped_column(Integer, default=0)
    
    # Scheduling Information
    weekly_hours: Mapped[int] = mapped_column(Integer, default=0)
    practical_hours: Mapped[int] = mapped_column(Integer, default=0)
    theory_hours: Mapped[int] = mapped_column(Integer, default=0)
    
    # Requirements
    room_type: Mapped[str] = mapped_column(String(50), nullable=True)  # classroom, lab, computer_lab
    equipment_required: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_compulsory: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_subjects_tenant_id", "tenant_id"),
        Index("ix_subjects_subject_code", "subject_code"),
        Index("ix_subjects_subject_type", "subject_type"),
        Index("ix_subjects_is_active", "is_active"),
    )


class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Teacher Information
    teacher_id: Mapped[str] = mapped_column(UUIDString, nullable=False)  # Reference to staff service
    teacher_name: Mapped[str] = mapped_column(String(100), nullable=False)
    teacher_code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    
    # Specialization
    specialization: Mapped[str] = mapped_column(String(100), nullable=True)
    subjects_taught: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Subject IDs
    grade_levels: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Grade levels
    
    # Availability
    max_hours_per_day: Mapped[int] = mapped_column(Integer, default=8)
    max_hours_per_week: Mapped[int] = mapped_column(Integer, default=40)
    preferred_time_slots: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    unavailable_slots: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_full_time: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_teachers_tenant_id", "tenant_id"),
        Index("ix_teachers_teacher_code", "teacher_code"),
        Index("ix_teachers_is_active", "is_active"),
    )


class Room(Base):
    __tablename__ = "rooms"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Room Information
    room_name: Mapped[str] = mapped_column(String(100), nullable=False)
    room_code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    room_type: Mapped[str] = mapped_column(String(50), nullable=False)  # classroom, lab, computer_lab, auditorium
    
    # Location
    building: Mapped[str] = mapped_column(String(100), nullable=True)
    floor: Mapped[str] = mapped_column(String(20), nullable=True)
    capacity: Mapped[int] = mapped_column(Integer, default=30)
    
    # Equipment and Facilities
    equipment: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    facilities: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Availability
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    maintenance_schedule: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_rooms_tenant_id", "tenant_id"),
        Index("ix_rooms_room_code", "room_code"),
        Index("ix_rooms_room_type", "room_type"),
        Index("ix_rooms_is_active", "is_active"),
    )


class TimeSlot(Base):
    __tablename__ = "time_slots"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Time Slot Information
    slot_name: Mapped[str] = mapped_column(String(50), nullable=False)
    slot_number: Mapped[int] = mapped_column(Integer, nullable=False)
    day_of_week: Mapped[str] = mapped_column(String(20), nullable=False)  # monday, tuesday, etc.
    
    # Time Information
    start_time: Mapped[time] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[time] = mapped_column(DateTime, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Break Information
    is_break: Mapped[bool] = mapped_column(Boolean, default=False)
    break_type: Mapped[str] = mapped_column(String(20), nullable=True)  # lunch, short_break, assembly
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_time_slots_tenant_id", "tenant_id"),
        Index("ix_time_slots_day_of_week", "day_of_week"),
        Index("ix_time_slots_slot_number", "slot_number"),
        Index("ix_time_slots_is_active", "is_active"),
    )


class TimetableSlot(Base):
    __tablename__ = "timetable_slots"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Schedule Information
    class_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    section_id: Mapped[str] = mapped_column(UUIDString, nullable=True)
    subject_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    teacher_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    room_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    time_slot_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Day and Time
    day_of_week: Mapped[str] = mapped_column(String(20), nullable=False)
    start_time: Mapped[time] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[time] = mapped_column(DateTime, nullable=False)
    
    # Academic Period
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    semester: Mapped[str] = mapped_column(String(20), nullable=True)
    week_type: Mapped[str] = mapped_column(String(20), nullable=True)  # odd, even, all
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Additional Information
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_by: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_timetable_slots_tenant_id", "tenant_id"),
        Index("ix_timetable_slots_class_id", "class_id"),
        Index("ix_timetable_slots_teacher_id", "teacher_id"),
        Index("ix_timetable_slots_room_id", "room_id"),
        Index("ix_timetable_slots_time_slot_id", "time_slot_id"),
        Index("ix_timetable_slots_day_of_week", "day_of_week"),
        Index("ix_timetable_slots_academic_year", "academic_year"),
    )


class TimetableConstraint(Base):
    __tablename__ = "timetable_constraints"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Constraint Information
    constraint_name: Mapped[str] = mapped_column(String(100), nullable=False)
    constraint_type: Mapped[str] = mapped_column(String(50), nullable=False)  # teacher, room, subject, class
    constraint_category: Mapped[str] = mapped_column(String(50), nullable=False)  # hard, soft
    
    # Target Information
    target_type: Mapped[str] = mapped_column(String(50), nullable=False)  # teacher_id, room_id, subject_id, class_id
    target_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Constraint Rules
    constraint_rules: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    priority: Mapped[int] = mapped_column(Integer, default=1)  # 1-10, higher is more important
    
    # Time Constraints
    applicable_days: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    applicable_time_slots: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_timetable_constraints_tenant_id", "tenant_id"),
        Index("ix_timetable_constraints_constraint_type", "constraint_type"),
        Index("ix_timetable_constraints_target_type", "target_type"),
        Index("ix_timetable_constraints_is_active", "is_active"),
    )


class TimetableSchedule(Base):
    __tablename__ = "timetable_schedules"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Schedule Information
    schedule_name: Mapped[str] = mapped_column(String(100), nullable=False)
    schedule_type: Mapped[str] = mapped_column(String(50), nullable=False)  # class, teacher, room
    target_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Academic Period
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    semester: Mapped[str] = mapped_column(String(20), nullable=True)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Schedule Data
    schedule_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    total_hours: Mapped[int] = mapped_column(Integer, default=0)
    total_slots: Mapped[int] = mapped_column(Integer, default=0)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    published_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Metadata
    created_by: Mapped[str] = mapped_column(UUIDString, nullable=False)
    approved_by: Mapped[str] = mapped_column(UUIDString, nullable=True)
    approval_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_timetable_schedules_tenant_id", "tenant_id"),
        Index("ix_timetable_schedules_schedule_type", "schedule_type"),
        Index("ix_timetable_schedules_target_id", "target_id"),
        Index("ix_timetable_schedules_academic_year", "academic_year"),
        Index("ix_timetable_schedules_is_active", "is_active"),
    )


class TimetableConflict(Base):
    __tablename__ = "timetable_conflicts"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Conflict Information
    conflict_type: Mapped[str] = mapped_column(String(50), nullable=False)  # teacher, room, subject
    conflict_severity: Mapped[str] = mapped_column(String(20), nullable=False)  # high, medium, low
    
    # Conflicting Slots
    slot1_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    slot2_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Conflict Details
    conflict_details: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    resolution_suggestions: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Status
    is_resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    resolved_by: Mapped[str] = mapped_column(UUIDString, nullable=True)
    resolution_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    resolution_method: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_timetable_conflicts_tenant_id", "tenant_id"),
        Index("ix_timetable_conflicts_conflict_type", "conflict_type"),
        Index("ix_timetable_conflicts_is_resolved", "is_resolved"),
    )


class TimetableTemplate(Base):
    __tablename__ = "timetable_templates"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Template Information
    template_name: Mapped[str] = mapped_column(String(100), nullable=False)
    template_description: Mapped[str] = mapped_column(Text, nullable=True)
    template_type: Mapped[str] = mapped_column(String(50), nullable=False)  # class, teacher, room
    
    # Template Data
    template_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    slot_configuration: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Usage
    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    last_used: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Metadata
    created_by: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_timetable_templates_tenant_id", "tenant_id"),
        Index("ix_timetable_templates_template_type", "template_type"),
        Index("ix_timetable_templates_is_active", "is_active"),
    ) 