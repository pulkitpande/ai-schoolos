"""
SQLAlchemy models for Attendance Service (AI SchoolOS)
"""

from datetime import datetime
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


class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Student Information
    student_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    class_id: Mapped[str] = mapped_column(UUIDString, nullable=True)
    section_id: Mapped[str] = mapped_column(UUIDString, nullable=True)
    
    # Attendance Information
    attendance_date: Mapped[date] = mapped_column(Date, nullable=False)
    attendance_status: Mapped[str] = mapped_column(String(20), nullable=False)  # present, absent, late, half_day
    attendance_type: Mapped[str] = mapped_column(String(20), nullable=False)  # manual, biometric, qr_code, face_recognition
    
    # Time Information
    check_in_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    check_out_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    late_minutes: Mapped[int] = mapped_column(Integer, default=0)
    
    # Location Information
    check_in_location: Mapped[str] = mapped_column(String(200), nullable=True)
    check_out_location: Mapped[str] = mapped_column(String(200), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    
    # Additional Data
    remarks: Mapped[str] = mapped_column(Text, nullable=True)
    verified_by: Mapped[str] = mapped_column(UUIDString, nullable=True)
    verification_method: Mapped[str] = mapped_column(String(50), nullable=True)  # teacher, admin, system
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_attendance_records_tenant_id", "tenant_id"),
        Index("ix_attendance_records_student_id", "student_id"),
        Index("ix_attendance_records_attendance_date", "attendance_date"),
        Index("ix_attendance_records_attendance_status", "attendance_status"),
        Index("ix_attendance_records_class_id", "class_id"),
    )


class BiometricData(Base):
    __tablename__ = "biometric_data"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # User Information
    user_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    user_type: Mapped[str] = mapped_column(String(20), nullable=False)  # student, teacher, staff
    
    # Biometric Information
    biometric_type: Mapped[str] = mapped_column(String(50), nullable=False)  # fingerprint, face, iris, voice
    biometric_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Encrypted biometric data
    template_hash: Mapped[str] = mapped_column(String(255), nullable=False)  # Hash of biometric template
    
    # Device Information
    device_id: Mapped[str] = mapped_column(String(100), nullable=True)
    device_type: Mapped[str] = mapped_column(String(50), nullable=True)  # scanner, camera, sensor
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_biometric_data_tenant_id", "tenant_id"),
        Index("ix_biometric_data_user_id", "user_id"),
        Index("ix_biometric_data_biometric_type", "biometric_type"),
        Index("ix_biometric_data_is_active", "is_active"),
    )


class AttendanceRule(Base):
    __tablename__ = "attendance_rules"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Rule Information
    rule_name: Mapped[str] = mapped_column(String(100), nullable=False)
    rule_type: Mapped[str] = mapped_column(String(50), nullable=False)  # class, section, individual
    target_id: Mapped[str] = mapped_column(UUIDString, nullable=False)  # class_id, section_id, student_id
    
    # Time Settings
    start_time: Mapped[str] = mapped_column(String(10), nullable=False)  # HH:MM format
    end_time: Mapped[str] = mapped_column(String(10), nullable=False)  # HH:MM format
    late_threshold: Mapped[int] = mapped_column(Integer, default=15)  # Minutes
    half_day_threshold: Mapped[int] = mapped_column(Integer, default=240)  # Minutes
    
    # Days Settings
    applicable_days: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Days of week
    holidays: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Holiday dates
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_attendance_rules_tenant_id", "tenant_id"),
        Index("ix_attendance_rules_rule_type", "rule_type"),
        Index("ix_attendance_rules_target_id", "target_id"),
        Index("ix_attendance_rules_is_active", "is_active"),
    )


class AttendanceDevice(Base):
    __tablename__ = "attendance_devices"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Device Information
    device_name: Mapped[str] = mapped_column(String(100), nullable=False)
    device_type: Mapped[str] = mapped_column(String(50), nullable=False)  # fingerprint, face, qr, card
    device_model: Mapped[str] = mapped_column(String(100), nullable=True)
    serial_number: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Location Information
    location: Mapped[str] = mapped_column(String(200), nullable=False)
    building: Mapped[str] = mapped_column(String(100), nullable=True)
    floor: Mapped[str] = mapped_column(String(20), nullable=True)
    room: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Configuration
    device_config: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)  # IPv4/IPv6
    mac_address: Mapped[str] = mapped_column(String(17), nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_online: Mapped[bool] = mapped_column(Boolean, default=False)
    last_heartbeat: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_attendance_devices_tenant_id", "tenant_id"),
        Index("ix_attendance_devices_device_type", "device_type"),
        Index("ix_attendance_devices_is_active", "is_active"),
        Index("ix_attendance_devices_location", "location"),
    )


class AttendanceException(Base):
    __tablename__ = "attendance_exceptions"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Exception Information
    student_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    exception_type: Mapped[str] = mapped_column(String(50), nullable=False)  # leave, sick, emergency, other
    exception_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    # Duration
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    is_half_day: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Approval Information
    requested_by: Mapped[str] = mapped_column(UUIDString, nullable=False)  # parent, student, teacher
    approved_by: Mapped[str] = mapped_column(UUIDString, nullable=True)
    approval_status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, approved, rejected
    approval_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Details
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    supporting_documents: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    remarks: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_attendance_exceptions_tenant_id", "tenant_id"),
        Index("ix_attendance_exceptions_student_id", "student_id"),
        Index("ix_attendance_exceptions_exception_date", "exception_date"),
        Index("ix_attendance_exceptions_approval_status", "approval_status"),
    )


class AttendanceReport(Base):
    __tablename__ = "attendance_reports"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Report Information
    report_name: Mapped[str] = mapped_column(String(200), nullable=False)
    report_type: Mapped[str] = mapped_column(String(50), nullable=False)  # daily, weekly, monthly, custom
    report_period: Mapped[str] = mapped_column(String(20), nullable=False)  # period identifier
    
    # Scope
    target_type: Mapped[str] = mapped_column(String(20), nullable=False)  # class, section, student, all
    target_id: Mapped[str] = mapped_column(UUIDString, nullable=True)
    
    # Report Data
    report_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    summary_stats: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Generation Information
    generated_by: Mapped[str] = mapped_column(UUIDString, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_attendance_reports_tenant_id", "tenant_id"),
        Index("ix_attendance_reports_report_type", "report_type"),
        Index("ix_attendance_reports_target_type", "target_type"),
        Index("ix_attendance_reports_generated_at", "generated_at"),
    )


class AttendanceAnalytics(Base):
    __tablename__ = "attendance_analytics"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Analytics Data
    total_students: Mapped[int] = mapped_column(Integer, default=0)
    present_count: Mapped[int] = mapped_column(Integer, default=0)
    absent_count: Mapped[int] = mapped_column(Integer, default=0)
    late_count: Mapped[int] = mapped_column(Integer, default=0)
    half_day_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Attendance Rate
    attendance_rate: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0)
    late_rate: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0)
    absence_rate: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0)
    
    # Time Analytics
    average_check_in_time: Mapped[str] = mapped_column(String(10), nullable=True)  # HH:MM format
    average_check_out_time: Mapped[str] = mapped_column(String(10), nullable=True)  # HH:MM format
    average_late_minutes: Mapped[int] = mapped_column(Integer, default=0)
    
    # Period Information
    analytics_date: Mapped[date] = mapped_column(Date, nullable=False)
    analytics_period: Mapped[str] = mapped_column(String(20), nullable=False)  # daily, weekly, monthly
    
    # Additional Data
    class_wise_stats: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    trend_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_attendance_analytics_tenant_id", "tenant_id"),
        Index("ix_attendance_analytics_analytics_date", "analytics_date"),
        Index("ix_attendance_analytics_analytics_period", "analytics_period"),
    ) 