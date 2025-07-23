"""
Pydantic schemas for Student Service (AI SchoolOS)
"""

from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, validator
from enum import Enum


# Enums
class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class EnrollmentStatus(str, Enum):
    ENROLLED = "enrolled"
    WITHDRAWN = "withdrawn"
    GRADUATED = "graduated"


class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    HALF_DAY = "half-day"


class GuardianRelationship(str, Enum):
    FATHER = "father"
    MOTHER = "mother"
    GUARDIAN = "guardian"
    GRANDFATHER = "grandfather"
    GRANDMOTHER = "grandmother"
    UNCLE = "uncle"
    AUNT = "aunt"
    OTHER = "other"


# Base Models
class StudentBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    gender: Gender
    blood_group: Optional[str] = Field(None, max_length=10)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    admission_number: str = Field(..., min_length=1, max_length=50)
    admission_date: date
    current_class: Optional[str] = Field(None, max_length=50)
    current_section: Optional[str] = Field(None, max_length=10)
    academic_year: Optional[str] = Field(None, max_length=20)
    enrollment_status: EnrollmentStatus = EnrollmentStatus.ENROLLED
    profile_data: Dict[str, Any] = Field(default_factory=dict)
    medical_info: Dict[str, Any] = Field(default_factory=dict)


class StudentCreate(StudentBase):
    tenant_id: str
    user_id: str


class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    blood_group: Optional[str] = Field(None, max_length=10)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    current_class: Optional[str] = Field(None, max_length=50)
    current_section: Optional[str] = Field(None, max_length=10)
    academic_year: Optional[str] = Field(None, max_length=20)
    enrollment_status: Optional[EnrollmentStatus] = None
    profile_data: Optional[Dict[str, Any]] = None
    medical_info: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class StudentResponse(StudentBase):
    id: str
    tenant_id: str
    user_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GuardianBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    relationship: GuardianRelationship
    email: Optional[EmailStr] = None
    phone: str = Field(..., min_length=1, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    occupation: Optional[str] = Field(None, max_length=100)
    income: Optional[float] = Field(None, ge=0)
    is_primary: bool = False
    is_emergency_contact: bool = False


class GuardianCreate(GuardianBase):
    student_id: str


class GuardianUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    relationship: Optional[GuardianRelationship] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=1, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    occupation: Optional[str] = Field(None, max_length=100)
    income: Optional[float] = Field(None, ge=0)
    is_primary: Optional[bool] = None
    is_emergency_contact: Optional[bool] = None
    is_active: Optional[bool] = None


class GuardianResponse(GuardianBase):
    id: str
    student_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EnrollmentBase(BaseModel):
    class_name: str = Field(..., min_length=1, max_length=50)
    section: str = Field(..., min_length=1, max_length=10)
    academic_year: str = Field(..., min_length=1, max_length=20)
    enrollment_date: date
    status: str = Field(default="active", max_length=20)
    completion_date: Optional[date] = None
    notes: Optional[str] = None


class EnrollmentCreate(EnrollmentBase):
    student_id: str


class EnrollmentUpdate(BaseModel):
    class_name: Optional[str] = Field(None, min_length=1, max_length=50)
    section: Optional[str] = Field(None, min_length=1, max_length=10)
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    enrollment_date: Optional[date] = None
    status: Optional[str] = Field(None, max_length=20)
    completion_date: Optional[date] = None
    notes: Optional[str] = None


class EnrollmentResponse(EnrollmentBase):
    id: str
    student_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AcademicRecordBase(BaseModel):
    academic_year: str = Field(..., min_length=1, max_length=20)
    class_name: str = Field(..., min_length=1, max_length=50)
    section: str = Field(..., min_length=1, max_length=10)
    total_marks: Optional[float] = Field(None, ge=0)
    obtained_marks: Optional[float] = Field(None, ge=0)
    percentage: Optional[float] = Field(None, ge=0, le=100)
    grade: Optional[str] = Field(None, max_length=10)
    rank: Optional[int] = Field(None, ge=1)
    remarks: Optional[str] = None
    achievements: Dict[str, Any] = Field(default_factory=dict)


class AcademicRecordCreate(AcademicRecordBase):
    student_id: str


class AcademicRecordUpdate(BaseModel):
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    class_name: Optional[str] = Field(None, min_length=1, max_length=50)
    section: Optional[str] = Field(None, min_length=1, max_length=10)
    total_marks: Optional[float] = Field(None, ge=0)
    obtained_marks: Optional[float] = Field(None, ge=0)
    percentage: Optional[float] = Field(None, ge=0, le=100)
    grade: Optional[str] = Field(None, max_length=10)
    rank: Optional[int] = Field(None, ge=1)
    remarks: Optional[str] = None
    achievements: Optional[Dict[str, Any]] = None


class AcademicRecordResponse(AcademicRecordBase):
    id: str
    student_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AttendanceRecordBase(BaseModel):
    date: date
    status: AttendanceStatus
    class_name: str = Field(..., min_length=1, max_length=50)
    section: str = Field(..., min_length=1, max_length=10)
    reason: Optional[str] = Field(None, max_length=255)
    remarks: Optional[str] = None


class AttendanceRecordCreate(AttendanceRecordBase):
    student_id: str


class AttendanceRecordUpdate(BaseModel):
    date: Optional[date] = None
    status: Optional[AttendanceStatus] = None
    class_name: Optional[str] = Field(None, min_length=1, max_length=50)
    section: Optional[str] = Field(None, min_length=1, max_length=10)
    reason: Optional[str] = Field(None, max_length=255)
    remarks: Optional[str] = None


class AttendanceRecordResponse(AttendanceRecordBase):
    id: str
    student_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Response Models with Relationships
class StudentWithGuardians(StudentResponse):
    guardians: List[GuardianResponse] = []


class StudentWithEnrollments(StudentResponse):
    enrollments: List[EnrollmentResponse] = []


class StudentWithAcademicRecords(StudentResponse):
    academic_records: List[AcademicRecordResponse] = []


class StudentWithAttendance(StudentResponse):
    attendance_records: List[AttendanceRecordResponse] = []


class StudentComplete(StudentResponse):
    guardians: List[GuardianResponse] = []
    enrollments: List[EnrollmentResponse] = []
    academic_records: List[AcademicRecordResponse] = []
    attendance_records: List[AttendanceRecordResponse] = []


# List Response Models
class StudentListResponse(BaseModel):
    students: List[StudentResponse]
    total: int
    page: int
    size: int


class GuardianListResponse(BaseModel):
    guardians: List[GuardianResponse]
    total: int
    page: int
    size: int


class EnrollmentListResponse(BaseModel):
    enrollments: List[EnrollmentResponse]
    total: int
    page: int
    size: int


class AcademicRecordListResponse(BaseModel):
    academic_records: List[AcademicRecordResponse]
    total: int
    page: int
    size: int


class AttendanceRecordListResponse(BaseModel):
    attendance_records: List[AttendanceRecordResponse]
    total: int
    page: int
    size: int


# Health Response
class HealthResponse(BaseModel):
    status: str
    service: str
    version: str 