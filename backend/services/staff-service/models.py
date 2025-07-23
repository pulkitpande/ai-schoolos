"""
SQLAlchemy models for Staff Service (AI SchoolOS)
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


class Staff(Base):
    __tablename__ = "staff"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    user_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Personal Information
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Contact Information
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    address: Mapped[str] = mapped_column(Text, nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    state: Mapped[str] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Employment Information
    employee_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hire_date: Mapped[Date] = mapped_column(Date, nullable=False)
    department_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("departments.id"), nullable=True)
    position: Mapped[str] = mapped_column(String(100), nullable=False)
    salary: Mapped[Float] = mapped_column(Float, nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    employment_status: Mapped[str] = mapped_column(String(20), default="active")  # active, terminated, retired
    
    # Additional Data
    profile_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    emergency_contact: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_staff_tenant_id", "tenant_id"),
        Index("ix_staff_user_id", "user_id"),
        Index("ix_staff_employee_id", "employee_id"),
        Index("ix_staff_department_id", "department_id"),
        Index("ix_staff_email", "email"),
    )


class Department(Base):
    __tablename__ = "departments"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Department Information
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Management
    head_staff_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("staff.id"), nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_departments_tenant_id", "tenant_id"),
        Index("ix_departments_code", "code"),
        Index("ix_departments_head_staff_id", "head_staff_id"),
    )


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Role Information
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Permissions
    permissions: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_roles_tenant_id", "tenant_id"),
        Index("ix_roles_code", "code"),
    )


class StaffRole(Base):
    __tablename__ = "staff_roles"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    staff_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    role_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    
    # Assignment Details
    assigned_by: Mapped[str] = mapped_column(UUIDString, nullable=True)
    assigned_date: Mapped[Date] = mapped_column(Date, nullable=False)
    expiry_date: Mapped[Date] = mapped_column(Date, nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_staff_roles_staff_id", "staff_id"),
        Index("ix_staff_roles_role_id", "role_id"),
        Index("ix_staff_roles_staff_role", "staff_id", "role_id", unique=True),
    )


class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    staff_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    
    # Leave Details
    leave_type: Mapped[str] = mapped_column(String(50), nullable=False)  # sick, vacation, personal, etc.
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    days_requested: Mapped[Integer] = mapped_column(Integer, nullable=False)
    
    # Request Details
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, approved, rejected
    
    # Approval
    approved_by: Mapped[str] = mapped_column(UUIDString, nullable=True)
    approved_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    approval_notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_leave_requests_staff_id", "staff_id"),
        Index("ix_leave_requests_status", "status"),
        Index("ix_leave_requests_dates", "start_date", "end_date"),
    )


class Attendance(Base):
    __tablename__ = "staff_attendance"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    staff_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("staff.id", ondelete="CASCADE"), nullable=False)
    
    # Attendance Details
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    check_in: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    check_out: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False)  # present, absent, late, half-day
    
    # Additional Information
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_staff_attendance_staff_id", "staff_id"),
        Index("ix_staff_attendance_date", "date"),
        Index("ix_staff_attendance_status", "status"),
        Index("ix_staff_attendance_staff_date", "staff_id", "date", unique=True),
    ) 