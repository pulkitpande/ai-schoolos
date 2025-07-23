"""
Pydantic schemas for Staff Service (AI SchoolOS)
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr


# Base schemas
class StaffBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    date_of_birth: date
    gender: str = Field(..., min_length=1, max_length=20)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    employee_id: str = Field(..., min_length=1, max_length=50)
    hire_date: date
    position: str = Field(..., min_length=1, max_length=100)
    salary: Optional[float] = None
    profile_data: Optional[Dict[str, Any]] = {}
    emergency_contact: Optional[Dict[str, Any]] = {}


class StaffCreate(StaffBase):
    tenant_id: str
    user_id: str
    department_id: Optional[str] = None


class StaffUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, min_length=1, max_length=20)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    employee_id: Optional[str] = Field(None, min_length=1, max_length=50)
    hire_date: Optional[date] = None
    department_id: Optional[str] = None
    position: Optional[str] = Field(None, min_length=1, max_length=100)
    salary: Optional[float] = None
    is_active: Optional[bool] = None
    employment_status: Optional[str] = Field(None, max_length=20)
    profile_data: Optional[Dict[str, Any]] = None
    emergency_contact: Optional[Dict[str, Any]] = None


class StaffResponse(StaffBase):
    id: str
    tenant_id: str
    user_id: str
    department_id: Optional[str] = None
    is_active: bool
    employment_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StaffListResponse(BaseModel):
    staff: List[StaffResponse]
    total: int
    page: int
    size: int


# Department schemas
class DepartmentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=20)
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    tenant_id: str
    head_staff_id: Optional[str] = None


class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = None
    head_staff_id: Optional[str] = None
    is_active: Optional[bool] = None


class DepartmentResponse(DepartmentBase):
    id: str
    tenant_id: str
    head_staff_id: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DepartmentListResponse(BaseModel):
    departments: List[DepartmentResponse]
    total: int
    page: int
    size: int


# Role schemas
class RoleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = {}


class RoleCreate(RoleBase):
    tenant_id: str


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class RoleResponse(RoleBase):
    id: str
    tenant_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoleListResponse(BaseModel):
    roles: List[RoleResponse]
    total: int
    page: int
    size: int


# Staff Role schemas
class StaffRoleBase(BaseModel):
    role_id: str
    assigned_date: date
    expiry_date: Optional[date] = None


class StaffRoleCreate(StaffRoleBase):
    staff_id: str
    assigned_by: Optional[str] = None


class StaffRoleUpdate(BaseModel):
    expiry_date: Optional[date] = None
    is_active: Optional[bool] = None


class StaffRoleResponse(StaffRoleBase):
    id: str
    staff_id: str
    assigned_by: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StaffRoleListResponse(BaseModel):
    staff_roles: List[StaffRoleResponse]
    total: int
    page: int
    size: int


# Leave Request schemas
class LeaveRequestBase(BaseModel):
    leave_type: str = Field(..., min_length=1, max_length=50)
    start_date: date
    end_date: date
    days_requested: int = Field(..., ge=1)
    reason: Optional[str] = None


class LeaveRequestCreate(LeaveRequestBase):
    staff_id: str


class LeaveRequestUpdate(BaseModel):
    leave_type: Optional[str] = Field(None, min_length=1, max_length=50)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    days_requested: Optional[int] = Field(None, ge=1)
    reason: Optional[str] = None
    status: Optional[str] = Field(None, max_length=20)
    approved_by: Optional[str] = None
    approval_notes: Optional[str] = None


class LeaveRequestResponse(LeaveRequestBase):
    id: str
    staff_id: str
    status: str
    approved_by: Optional[str] = None
    approved_date: Optional[datetime] = None
    approval_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LeaveRequestListResponse(BaseModel):
    leave_requests: List[LeaveRequestResponse]
    total: int
    page: int
    size: int


# Attendance schemas
class AttendanceBase(BaseModel):
    date: date
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    status: str = Field(..., min_length=1, max_length=20)
    notes: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    staff_id: str


class AttendanceUpdate(BaseModel):
    check_in: Optional[datetime] = None
    check_out: Optional[datetime] = None
    status: Optional[str] = Field(None, min_length=1, max_length=20)
    notes: Optional[str] = None


class AttendanceResponse(AttendanceBase):
    id: str
    staff_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AttendanceListResponse(BaseModel):
    attendance_records: List[AttendanceResponse]
    total: int
    page: int
    size: int 