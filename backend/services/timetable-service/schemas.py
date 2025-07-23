"""
Pydantic schemas for Timetable Service (AI SchoolOS)
"""

from datetime import datetime, date, time
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum


# Enums
class SubjectType(str, Enum):
    CORE = "core"
    ELECTIVE = "elective"
    OPTIONAL = "optional"


class SubjectCategory(str, Enum):
    SCIENCE = "science"
    ARTS = "arts"
    COMMERCE = "commerce"
    MATHEMATICS = "mathematics"
    LANGUAGES = "languages"
    SOCIAL_STUDIES = "social_studies"
    PHYSICAL_EDUCATION = "physical_education"


class RoomType(str, Enum):
    CLASSROOM = "classroom"
    LAB = "lab"
    COMPUTER_LAB = "computer_lab"
    AUDITORIUM = "auditorium"
    LIBRARY = "library"
    GYMNASIUM = "gymnasium"


class ConstraintType(str, Enum):
    TEACHER = "teacher"
    ROOM = "room"
    SUBJECT = "subject"
    CLASS = "class"


class ConstraintCategory(str, Enum):
    HARD = "hard"
    SOFT = "soft"


class ConflictType(str, Enum):
    TEACHER = "teacher"
    ROOM = "room"
    SUBJECT = "subject"


class ConflictSeverity(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ScheduleType(str, Enum):
    CLASS = "class"
    TEACHER = "teacher"
    ROOM = "room"


class TemplateType(str, Enum):
    CLASS = "class"
    TEACHER = "teacher"
    ROOM = "room"


# Base Models
class BaseTimetableModel(BaseModel):
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            time: lambda v: v.isoformat(),
        }


# Subject Schemas
class SubjectBase(BaseTimetableModel):
    subject_name: str = Field(..., description="Subject name")
    subject_code: str = Field(..., description="Subject code")
    subject_type: SubjectType = Field(..., description="Subject type")
    subject_category: Optional[SubjectCategory] = Field(None, description="Subject category")
    grade_level: Optional[str] = Field(None, description="Grade level")
    class_levels: Dict[str, Any] = Field(default_factory=dict, description="Applicable classes")
    credit_hours: int = Field(0, description="Credit hours")
    weekly_hours: int = Field(0, description="Weekly hours")
    practical_hours: int = Field(0, description="Practical hours")
    theory_hours: int = Field(0, description="Theory hours")
    room_type: Optional[RoomType] = Field(None, description="Required room type")
    equipment_required: Dict[str, Any] = Field(default_factory=dict, description="Required equipment")
    is_active: bool = Field(True, description="Is active")
    is_compulsory: bool = Field(True, description="Is compulsory")


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseTimetableModel):
    subject_name: Optional[str] = None
    subject_code: Optional[str] = None
    subject_type: Optional[SubjectType] = None
    subject_category: Optional[SubjectCategory] = None
    grade_level: Optional[str] = None
    class_levels: Optional[Dict[str, Any]] = None
    credit_hours: Optional[int] = None
    weekly_hours: Optional[int] = None
    practical_hours: Optional[int] = None
    theory_hours: Optional[int] = None
    room_type: Optional[RoomType] = None
    equipment_required: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_compulsory: Optional[bool] = None


class SubjectResponse(SubjectBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


# Teacher Schemas
class TeacherBase(BaseTimetableModel):
    teacher_id: str = Field(..., description="Teacher ID")
    teacher_name: str = Field(..., description="Teacher name")
    teacher_code: str = Field(..., description="Teacher code")
    specialization: Optional[str] = Field(None, description="Specialization")
    subjects_taught: Dict[str, Any] = Field(default_factory=dict, description="Subjects taught")
    grade_levels: Dict[str, Any] = Field(default_factory=dict, description="Grade levels")
    max_hours_per_day: int = Field(8, description="Max hours per day")
    max_hours_per_week: int = Field(40, description="Max hours per week")
    preferred_time_slots: Dict[str, Any] = Field(default_factory=dict, description="Preferred time slots")
    unavailable_slots: Dict[str, Any] = Field(default_factory=dict, description="Unavailable slots")
    is_active: bool = Field(True, description="Is active")
    is_full_time: bool = Field(True, description="Is full time")


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseTimetableModel):
    teacher_name: Optional[str] = None
    teacher_code: Optional[str] = None
    specialization: Optional[str] = None
    subjects_taught: Optional[Dict[str, Any]] = None
    grade_levels: Optional[Dict[str, Any]] = None
    max_hours_per_day: Optional[int] = None
    max_hours_per_week: Optional[int] = None
    preferred_time_slots: Optional[Dict[str, Any]] = None
    unavailable_slots: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_full_time: Optional[bool] = None


class TeacherResponse(TeacherBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


# Room Schemas
class RoomBase(BaseTimetableModel):
    room_name: str = Field(..., description="Room name")
    room_code: str = Field(..., description="Room code")
    room_type: RoomType = Field(..., description="Room type")
    building: Optional[str] = Field(None, description="Building")
    floor: Optional[str] = Field(None, description="Floor")
    capacity: int = Field(30, description="Capacity")
    equipment: Dict[str, Any] = Field(default_factory=dict, description="Equipment")
    facilities: Dict[str, Any] = Field(default_factory=dict, description="Facilities")
    is_available: bool = Field(True, description="Is available")
    maintenance_schedule: Dict[str, Any] = Field(default_factory=dict, description="Maintenance schedule")
    is_active: bool = Field(True, description="Is active")


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseTimetableModel):
    room_name: Optional[str] = None
    room_code: Optional[str] = None
    room_type: Optional[RoomType] = None
    building: Optional[str] = None
    floor: Optional[str] = None
    capacity: Optional[int] = None
    equipment: Optional[Dict[str, Any]] = None
    facilities: Optional[Dict[str, Any]] = None
    is_available: Optional[bool] = None
    maintenance_schedule: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class RoomResponse(RoomBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


# Time Slot Schemas
class TimeSlotBase(BaseTimetableModel):
    slot_name: str = Field(..., description="Slot name")
    slot_number: int = Field(..., description="Slot number")
    day_of_week: str = Field(..., description="Day of week")
    start_time: time = Field(..., description="Start time")
    end_time: time = Field(..., description="End time")
    duration_minutes: int = Field(..., description="Duration in minutes")
    is_break: bool = Field(False, description="Is break")
    break_type: Optional[str] = Field(None, description="Break type")
    is_active: bool = Field(True, description="Is active")


class TimeSlotCreate(TimeSlotBase):
    pass


class TimeSlotUpdate(BaseTimetableModel):
    slot_name: Optional[str] = None
    slot_number: Optional[int] = None
    day_of_week: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    duration_minutes: Optional[int] = None
    is_break: Optional[bool] = None
    break_type: Optional[str] = None
    is_active: Optional[bool] = None


class TimeSlotResponse(TimeSlotBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


# Timetable Slot Schemas
class TimetableSlotBase(BaseTimetableModel):
    class_id: str = Field(..., description="Class ID")
    section_id: Optional[str] = Field(None, description="Section ID")
    subject_id: str = Field(..., description="Subject ID")
    teacher_id: str = Field(..., description="Teacher ID")
    room_id: str = Field(..., description="Room ID")
    time_slot_id: str = Field(..., description="Time slot ID")
    day_of_week: str = Field(..., description="Day of week")
    start_time: time = Field(..., description="Start time")
    end_time: time = Field(..., description="End time")
    academic_year: str = Field(..., description="Academic year")
    semester: Optional[str] = Field(None, description="Semester")
    week_type: Optional[str] = Field(None, description="Week type")
    is_active: bool = Field(True, description="Is active")
    is_recurring: bool = Field(True, description="Is recurring")
    notes: Optional[str] = Field(None, description="Notes")
    created_by: str = Field(..., description="Created by")


class TimetableSlotCreate(TimetableSlotBase):
    pass


class TimetableSlotUpdate(BaseTimetableModel):
    subject_id: Optional[str] = None
    teacher_id: Optional[str] = None
    room_id: Optional[str] = None
    time_slot_id: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    semester: Optional[str] = None
    week_type: Optional[str] = None
    is_active: Optional[bool] = None
    is_recurring: Optional[bool] = None
    notes: Optional[str] = None


class TimetableSlotResponse(TimetableSlotBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


# Timetable Constraint Schemas
class TimetableConstraintBase(BaseTimetableModel):
    constraint_name: str = Field(..., description="Constraint name")
    constraint_type: ConstraintType = Field(..., description="Constraint type")
    constraint_category: ConstraintCategory = Field(..., description="Constraint category")
    target_type: str = Field(..., description="Target type")
    target_id: str = Field(..., description="Target ID")
    constraint_rules: Dict[str, Any] = Field(default_factory=dict, description="Constraint rules")
    priority: int = Field(1, ge=1, le=10, description="Priority (1-10)")
    applicable_days: Dict[str, Any] = Field(default_factory=dict, description="Applicable days")
    applicable_time_slots: Dict[str, Any] = Field(default_factory=dict, description="Applicable time slots")
    is_active: bool = Field(True, description="Is active")


class TimetableConstraintCreate(TimetableConstraintBase):
    pass


class TimetableConstraintUpdate(BaseTimetableModel):
    constraint_name: Optional[str] = None
    constraint_type: Optional[ConstraintType] = None
    constraint_category: Optional[ConstraintCategory] = None
    target_type: Optional[str] = None
    target_id: Optional[str] = None
    constraint_rules: Optional[Dict[str, Any]] = None
    priority: Optional[int] = None
    applicable_days: Optional[Dict[str, Any]] = None
    applicable_time_slots: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class TimetableConstraintResponse(TimetableConstraintBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


# Timetable Schedule Schemas
class TimetableScheduleBase(BaseTimetableModel):
    schedule_name: str = Field(..., description="Schedule name")
    schedule_type: ScheduleType = Field(..., description="Schedule type")
    target_id: str = Field(..., description="Target ID")
    academic_year: str = Field(..., description="Academic year")
    semester: Optional[str] = Field(None, description="Semester")
    start_date: date = Field(..., description="Start date")
    end_date: date = Field(..., description="End date")
    schedule_data: Dict[str, Any] = Field(default_factory=dict, description="Schedule data")
    total_hours: int = Field(0, description="Total hours")
    total_slots: int = Field(0, description="Total slots")
    is_active: bool = Field(True, description="Is active")
    is_published: bool = Field(False, description="Is published")
    published_at: Optional[datetime] = Field(None, description="Published at")
    created_by: str = Field(..., description="Created by")
    approved_by: Optional[str] = Field(None, description="Approved by")
    approval_date: Optional[datetime] = Field(None, description="Approval date")


class TimetableScheduleCreate(TimetableScheduleBase):
    pass


class TimetableScheduleUpdate(BaseTimetableModel):
    schedule_name: Optional[str] = None
    schedule_type: Optional[ScheduleType] = None
    target_id: Optional[str] = None
    academic_year: Optional[str] = None
    semester: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    schedule_data: Optional[Dict[str, Any]] = None
    total_hours: Optional[int] = None
    total_slots: Optional[int] = None
    is_active: Optional[bool] = None
    is_published: Optional[bool] = None
    published_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    approval_date: Optional[datetime] = None


class TimetableScheduleResponse(TimetableScheduleBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


# Timetable Conflict Schemas
class TimetableConflictBase(BaseTimetableModel):
    conflict_type: ConflictType = Field(..., description="Conflict type")
    conflict_severity: ConflictSeverity = Field(..., description="Conflict severity")
    slot1_id: str = Field(..., description="First slot ID")
    slot2_id: str = Field(..., description="Second slot ID")
    conflict_details: Dict[str, Any] = Field(default_factory=dict, description="Conflict details")
    resolution_suggestions: Dict[str, Any] = Field(default_factory=dict, description="Resolution suggestions")
    is_resolved: bool = Field(False, description="Is resolved")
    resolved_by: Optional[str] = Field(None, description="Resolved by")
    resolution_date: Optional[datetime] = Field(None, description="Resolution date")
    resolution_method: Optional[str] = Field(None, description="Resolution method")


class TimetableConflictCreate(TimetableConflictBase):
    pass


class TimetableConflictUpdate(BaseTimetableModel):
    conflict_type: Optional[ConflictType] = None
    conflict_severity: Optional[ConflictSeverity] = None
    slot1_id: Optional[str] = None
    slot2_id: Optional[str] = None
    conflict_details: Optional[Dict[str, Any]] = None
    resolution_suggestions: Optional[Dict[str, Any]] = None
    is_resolved: Optional[bool] = None
    resolved_by: Optional[str] = None
    resolution_date: Optional[datetime] = None
    resolution_method: Optional[str] = None


class TimetableConflictResponse(TimetableConflictBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


# Timetable Template Schemas
class TimetableTemplateBase(BaseTimetableModel):
    template_name: str = Field(..., description="Template name")
    template_description: Optional[str] = Field(None, description="Template description")
    template_type: TemplateType = Field(..., description="Template type")
    template_data: Dict[str, Any] = Field(default_factory=dict, description="Template data")
    slot_configuration: Dict[str, Any] = Field(default_factory=dict, description="Slot configuration")
    usage_count: int = Field(0, description="Usage count")
    last_used: Optional[datetime] = Field(None, description="Last used")
    is_active: bool = Field(True, description="Is active")
    is_default: bool = Field(False, description="Is default")
    created_by: str = Field(..., description="Created by")


class TimetableTemplateCreate(TimetableTemplateBase):
    pass


class TimetableTemplateUpdate(BaseTimetableModel):
    template_name: Optional[str] = None
    template_description: Optional[str] = None
    template_type: Optional[TemplateType] = None
    template_data: Optional[Dict[str, Any]] = None
    slot_configuration: Optional[Dict[str, Any]] = None
    usage_count: Optional[int] = None
    last_used: Optional[datetime] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None


class TimetableTemplateResponse(TimetableTemplateBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


# Search and Filter Schemas
class TimetableSearchParams(BaseTimetableModel):
    class_id: Optional[str] = None
    section_id: Optional[str] = None
    subject_id: Optional[str] = None
    teacher_id: Optional[str] = None
    room_id: Optional[str] = None
    day_of_week: Optional[str] = None
    academic_year: Optional[str] = None
    semester: Optional[str] = None
    is_active: Optional[bool] = None
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)


class TimetableStats(BaseTimetableModel):
    total_slots: int
    total_hours: int
    total_subjects: int
    total_teachers: int
    total_rooms: int
    conflicts_count: int
    utilization_rate: float


# Bulk Operations
class BulkTimetableSlotCreate(BaseTimetableModel):
    slots: List[TimetableSlotCreate] = Field(..., description="Timetable slots")


class BulkTimetableSlotResponse(BaseTimetableModel):
    created: int
    failed: int
    errors: List[Dict[str, Any]]


# Response Models
class SuccessResponse(BaseTimetableModel):
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseTimetableModel):
    success: bool = False
    error: str
    details: Optional[str] = None


# Health Check
class HealthCheck(BaseTimetableModel):
    status: str
    service: str
    version: str
    timestamp: datetime 