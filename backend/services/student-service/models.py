"""
SQLAlchemy models for Student Service (AI SchoolOS)
"""

from datetime import datetime
import uuid
import json
from sqlalchemy import (
    Column, String, DateTime, Boolean, ForeignKey, Table, Index, Text, Integer, Date, Float
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


class Student(Base):
    __tablename__ = "students"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    user_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Personal Information
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    blood_group: Mapped[str] = mapped_column(String(10), nullable=True)
    
    # Contact Information
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    state: Mapped[str] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Academic Information
    admission_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    admission_date: Mapped[Date] = mapped_column(Date, nullable=False)
    current_class: Mapped[str] = mapped_column(String(50), nullable=True)
    current_section: Mapped[str] = mapped_column(String(10), nullable=True)
    academic_year: Mapped[str] = mapped_column(String(20), nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    enrollment_status: Mapped[str] = mapped_column(String(20), default="enrolled")  # enrolled, withdrawn, graduated
    
    # Additional Data
    profile_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    medical_info: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_students_tenant_id", "tenant_id"),
        Index("ix_students_user_id", "user_id"),
        Index("ix_students_admission_number", "admission_number"),
        Index("ix_students_current_class", "current_class"),
    )


class Guardian(Base):
    __tablename__ = "guardians"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    # Personal Information
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    relationship: Mapped[str] = mapped_column(String(50), nullable=False)  # father, mother, guardian, etc.
    
    # Contact Information
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    state: Mapped[str] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Additional Information
    occupation: Mapped[str] = mapped_column(String(100), nullable=True)
    income: Mapped[Float] = mapped_column(Float, nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    is_emergency_contact: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_guardians_student_id", "student_id"),
        Index("ix_guardians_email", "email"),
        Index("ix_guardians_phone", "phone"),
    )


class Enrollment(Base):
    __tablename__ = "enrollments"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    # Enrollment Details
    class_name: Mapped[str] = mapped_column(String(50), nullable=False)
    section: Mapped[str] = mapped_column(String(10), nullable=False)
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    enrollment_date: Mapped[Date] = mapped_column(Date, nullable=False)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, completed, withdrawn
    completion_date: Mapped[Date] = mapped_column(Date, nullable=True)
    
    # Additional Data
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_enrollments_student_id", "student_id"),
        Index("ix_enrollments_academic_year", "academic_year"),
        Index("ix_enrollments_class_section", "class_name", "section"),
    )


class AcademicRecord(Base):
    __tablename__ = "academic_records"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    # Academic Details
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    class_name: Mapped[str] = mapped_column(String(50), nullable=False)
    section: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # Performance Data
    total_marks: Mapped[Float] = mapped_column(Float, nullable=True)
    obtained_marks: Mapped[Float] = mapped_column(Float, nullable=True)
    percentage: Mapped[Float] = mapped_column(Float, nullable=True)
    grade: Mapped[str] = mapped_column(String(10), nullable=True)
    rank: Mapped[Integer] = mapped_column(Integer, nullable=True)
    
    # Additional Data
    remarks: Mapped[str] = mapped_column(Text, nullable=True)
    achievements: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_academic_records_student_id", "student_id"),
        Index("ix_academic_records_academic_year", "academic_year"),
        Index("ix_academic_records_class_section", "class_name", "section"),
    )


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    
    # Attendance Details
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # present, absent, late, half-day
    class_name: Mapped[str] = mapped_column(String(50), nullable=False)
    section: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # Additional Information
    reason: Mapped[str] = mapped_column(String(255), nullable=True)
    remarks: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_attendance_records_student_id", "student_id"),
        Index("ix_attendance_records_date", "date"),
        Index("ix_attendance_records_status", "status"),
        Index("ix_attendance_records_student_date", "student_id", "date", unique=True),
    ) 