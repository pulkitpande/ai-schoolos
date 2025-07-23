"""
Pydantic schemas for Attendance Service (AI SchoolOS)
"""

from datetime import datetime, date, time
from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum


# Enums
class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    HALF_DAY = "half_day"
    LEAVE = "leave"


class AttendanceType(str, Enum):
    MANUAL = "manual"
    BIOMETRIC = "biometric"
    QR_CODE = "qr_code"
    FACE_RECOGNITION = "face_recognition"
    CARD = "card"


class BiometricType(str, Enum):
    FINGERPRINT = "fingerprint"
    FACE = "face"
    IRIS = "iris"
    VOICE = "voice"


class DeviceType(str, Enum):
    FINGERPRINT = "fingerprint"
    FACE = "face"
    QR = "qr"
    CARD = "card"


class ExceptionType(str, Enum):
    LEAVE = "leave"
    SICK = "sick"
    EMERGENCY = "emergency"
    OTHER = "other"


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class ReportType(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    CUSTOM = "custom"


# Base Models
class BaseAttendanceModel(BaseModel):
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
        }


# Attendance Record Schemas
class AttendanceRecordBase(BaseAttendanceModel):
    student_id: str = Field(..., description="Student ID")
    class_id: Optional[str] = Field(None, description="Class ID")
    section_id: Optional[str] = Field(None, description="Section ID")
    attendance_date: date = Field(..., description="Attendance date")
    attendance_status: AttendanceStatus = Field(..., description="Attendance status")
    attendance_type: AttendanceType = Field(..., description="Attendance type")
    check_in_time: Optional[datetime] = Field(None, description="Check-in time")
    check_out_time: Optional[datetime] = Field(None, description="Check-out time")
    late_minutes: Optional[int] = Field(0, description="Late minutes")
    check_in_location: Optional[str] = Field(None, description="Check-in location")
    check_out_location: Optional[str] = Field(None, description="Check-out location")
    latitude: Optional[float] = Field(None, description="Latitude")
    longitude: Optional[float] = Field(None, description="Longitude")
    remarks: Optional[str] = Field(None, description="Remarks")
    verified_by: Optional[str] = Field(None, description="Verified by")
    verification_method: Optional[str] = Field(None, description="Verification method")


class AttendanceRecordCreate(AttendanceRecordBase):
    pass


class AttendanceRecordUpdate(BaseAttendanceModel):
    attendance_status: Optional[AttendanceStatus] = None
    check_in_time: Optional[datetime] = None
    check_out_time: Optional[datetime] = None
    late_minutes: Optional[int] = None
    check_in_location: Optional[str] = None
    check_out_location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    remarks: Optional[str] = None
    verified_by: Optional[str] = None
    verification_method: Optional[str] = None


class AttendanceRecordResponse(AttendanceRecordBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


class AttendanceRecordList(BaseAttendanceModel):
    records: List[AttendanceRecordResponse]
    total: int
    page: int
    size: int


# Biometric Data Schemas
class BiometricDataBase(BaseAttendanceModel):
    user_id: str = Field(..., description="User ID")
    user_type: str = Field(..., description="User type (student, teacher, staff)")
    biometric_type: BiometricType = Field(..., description="Biometric type")
    biometric_data: Dict[str, Any] = Field(default_factory=dict, description="Biometric data")
    template_hash: str = Field(..., description="Template hash")
    device_id: Optional[str] = Field(None, description="Device ID")
    device_type: Optional[str] = Field(None, description="Device type")
    is_active: bool = Field(True, description="Is active")
    is_verified: bool = Field(False, description="Is verified")


class BiometricDataCreate(BiometricDataBase):
    pass


class BiometricDataUpdate(BaseAttendanceModel):
    biometric_data: Optional[Dict[str, Any]] = None
    template_hash: Optional[str] = None
    device_id: Optional[str] = None
    device_type: Optional[str] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class BiometricDataResponse(BiometricDataBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


# Attendance Rule Schemas
class AttendanceRuleBase(BaseAttendanceModel):
    rule_name: str = Field(..., description="Rule name")
    rule_type: str = Field(..., description="Rule type (class, section, individual)")
    target_id: str = Field(..., description="Target ID")
    start_time: str = Field(..., description="Start time (HH:MM)")
    end_time: str = Field(..., description="End time (HH:MM)")
    late_threshold: int = Field(15, description="Late threshold in minutes")
    half_day_threshold: int = Field(240, description="Half day threshold in minutes")
    applicable_days: Dict[str, bool] = Field(default_factory=dict, description="Applicable days")
    holidays: Dict[str, str] = Field(default_factory=dict, description="Holidays")
    is_active: bool = Field(True, description="Is active")
    is_default: bool = Field(False, description="Is default")


class AttendanceRuleCreate(AttendanceRuleBase):
    pass


class AttendanceRuleUpdate(BaseAttendanceModel):
    rule_name: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    late_threshold: Optional[int] = None
    half_day_threshold: Optional[int] = None
    applicable_days: Optional[Dict[str, bool]] = None
    holidays: Optional[Dict[str, str]] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None


class AttendanceRuleResponse(AttendanceRuleBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


# Attendance Device Schemas
class AttendanceDeviceBase(BaseAttendanceModel):
    device_name: str = Field(..., description="Device name")
    device_type: DeviceType = Field(..., description="Device type")
    device_model: Optional[str] = Field(None, description="Device model")
    serial_number: Optional[str] = Field(None, description="Serial number")
    location: str = Field(..., description="Location")
    building: Optional[str] = Field(None, description="Building")
    floor: Optional[str] = Field(None, description="Floor")
    room: Optional[str] = Field(None, description="Room")
    device_config: Dict[str, Any] = Field(default_factory=dict, description="Device configuration")
    ip_address: Optional[str] = Field(None, description="IP address")
    mac_address: Optional[str] = Field(None, description="MAC address")
    is_active: bool = Field(True, description="Is active")
    is_online: bool = Field(False, description="Is online")
    last_heartbeat: Optional[datetime] = Field(None, description="Last heartbeat")


class AttendanceDeviceCreate(AttendanceDeviceBase):
    pass


class AttendanceDeviceUpdate(BaseAttendanceModel):
    device_name: Optional[str] = None
    device_model: Optional[str] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    building: Optional[str] = None
    floor: Optional[str] = None
    room: Optional[str] = None
    device_config: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    is_active: Optional[bool] = None
    is_online: Optional[bool] = None
    last_heartbeat: Optional[datetime] = None


class AttendanceDeviceResponse(AttendanceDeviceBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


# Attendance Exception Schemas
class AttendanceExceptionBase(BaseAttendanceModel):
    student_id: str = Field(..., description="Student ID")
    exception_type: ExceptionType = Field(..., description="Exception type")
    exception_date: date = Field(..., description="Exception date")
    start_date: date = Field(..., description="Start date")
    end_date: date = Field(..., description="End date")
    is_half_day: bool = Field(False, description="Is half day")
    requested_by: str = Field(..., description="Requested by")
    approved_by: Optional[str] = Field(None, description="Approved by")
    approval_status: ApprovalStatus = Field(ApprovalStatus.PENDING, description="Approval status")
    approval_date: Optional[datetime] = Field(None, description="Approval date")
    reason: str = Field(..., description="Reason")
    supporting_documents: Dict[str, str] = Field(default_factory=dict, description="Supporting documents")
    remarks: Optional[str] = Field(None, description="Remarks")


class AttendanceExceptionCreate(AttendanceExceptionBase):
    pass


class AttendanceExceptionUpdate(BaseAttendanceModel):
    exception_type: Optional[ExceptionType] = None
    exception_date: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_half_day: Optional[bool] = None
    approved_by: Optional[str] = None
    approval_status: Optional[ApprovalStatus] = None
    approval_date: Optional[datetime] = None
    reason: Optional[str] = None
    supporting_documents: Optional[Dict[str, str]] = None
    remarks: Optional[str] = None


class AttendanceExceptionResponse(AttendanceExceptionBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


# Attendance Report Schemas
class AttendanceReportBase(BaseAttendanceModel):
    report_name: str = Field(..., description="Report name")
    report_type: ReportType = Field(..., description="Report type")
    report_period: str = Field(..., description="Report period")
    target_type: str = Field(..., description="Target type")
    target_id: Optional[str] = Field(None, description="Target ID")
    report_data: Dict[str, Any] = Field(default_factory=dict, description="Report data")
    summary_stats: Dict[str, Any] = Field(default_factory=dict, description="Summary statistics")
    generated_by: str = Field(..., description="Generated by")
    generated_at: datetime = Field(..., description="Generated at")
    file_path: Optional[str] = Field(None, description="File path")


class AttendanceReportCreate(AttendanceReportBase):
    pass


class AttendanceReportResponse(AttendanceReportBase):
    id: str
    tenant_id: str
    created_at: datetime


# Attendance Analytics Schemas
class AttendanceAnalyticsBase(BaseAttendanceModel):
    total_students: int = Field(0, description="Total students")
    present_count: int = Field(0, description="Present count")
    absent_count: int = Field(0, description="Absent count")
    late_count: int = Field(0, description="Late count")
    half_day_count: int = Field(0, description="Half day count")
    attendance_rate: float = Field(0.0, description="Attendance rate")
    late_rate: float = Field(0.0, description="Late rate")
    absence_rate: float = Field(0.0, description="Absence rate")
    average_check_in_time: Optional[str] = Field(None, description="Average check-in time")
    average_check_out_time: Optional[str] = Field(None, description="Average check-out time")
    average_late_minutes: int = Field(0, description="Average late minutes")
    analytics_date: date = Field(..., description="Analytics date")
    analytics_period: str = Field(..., description="Analytics period")
    class_wise_stats: Dict[str, Any] = Field(default_factory=dict, description="Class-wise statistics")
    trend_data: Dict[str, Any] = Field(default_factory=dict, description="Trend data")


class AttendanceAnalyticsCreate(AttendanceAnalyticsBase):
    pass


class AttendanceAnalyticsUpdate(BaseAttendanceModel):
    total_students: Optional[int] = None
    present_count: Optional[int] = None
    absent_count: Optional[int] = None
    late_count: Optional[int] = None
    half_day_count: Optional[int] = None
    attendance_rate: Optional[float] = None
    late_rate: Optional[float] = None
    absence_rate: Optional[float] = None
    average_check_in_time: Optional[str] = None
    average_check_out_time: Optional[str] = None
    average_late_minutes: Optional[int] = None
    class_wise_stats: Optional[Dict[str, Any]] = None
    trend_data: Optional[Dict[str, Any]] = None


class AttendanceAnalyticsResponse(AttendanceAnalyticsBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime


# Bulk Operations
class BulkAttendanceCreate(BaseAttendanceModel):
    records: List[AttendanceRecordCreate] = Field(..., description="Attendance records")


class BulkAttendanceResponse(BaseAttendanceModel):
    created: int
    failed: int
    errors: List[Dict[str, Any]]


# Search and Filter Schemas
class AttendanceSearchParams(BaseAttendanceModel):
    student_id: Optional[str] = None
    class_id: Optional[str] = None
    section_id: Optional[str] = None
    attendance_date: Optional[date] = None
    attendance_status: Optional[AttendanceStatus] = None
    attendance_type: Optional[AttendanceType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)


class AttendanceStats(BaseAttendanceModel):
    total_records: int
    present_count: int
    absent_count: int
    late_count: int
    half_day_count: int
    attendance_rate: float
    date_range: Dict[str, date]


# Response Models
class SuccessResponse(BaseAttendanceModel):
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseAttendanceModel):
    success: bool = False
    error: str
    details: Optional[str] = None


# Health Check
class HealthCheck(BaseAttendanceModel):
    status: str
    service: str
    version: str
    timestamp: datetime 