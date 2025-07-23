"""
Staff router for Staff Service (AI SchoolOS)
"""

import logging
from typing import List, Optional
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from database import get_db
from models import Staff, Department, Role, StaffRole, LeaveRequest, Attendance
from schemas import (
    StaffCreate, StaffUpdate, StaffResponse, StaffListResponse,
    DepartmentCreate, DepartmentUpdate, DepartmentResponse, DepartmentListResponse,
    RoleCreate, RoleUpdate, RoleResponse, RoleListResponse,
    StaffRoleCreate, StaffRoleUpdate, StaffRoleResponse, StaffRoleListResponse,
    LeaveRequestCreate, LeaveRequestUpdate, LeaveRequestResponse, LeaveRequestListResponse,
    AttendanceCreate, AttendanceUpdate, AttendanceResponse, AttendanceListResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/staff", tags=["staff"])


# Staff CRUD Operations
@router.post("/", response_model=StaffResponse)
async def create_staff(
    staff_data: StaffCreate,
    db: Session = Depends(get_db)
):
    """Create a new staff member."""
    try:
        # Check if employee ID already exists
        existing_staff = db.query(Staff).filter(
            Staff.employee_id == staff_data.employee_id,
            Staff.tenant_id == staff_data.tenant_id
        ).first()
        
        if existing_staff:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Staff with this employee ID already exists"
            )
        
        # Create new staff member
        staff = Staff(**staff_data.dict())
        db.add(staff)
        db.commit()
        db.refresh(staff)
        
        logger.info(f"New staff member created: {staff.employee_id}")
        return staff
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating staff member: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/", response_model=StaffListResponse)
async def get_staff(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    department_id: Optional[str] = None,
    position: Optional[str] = None,
    employment_status: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of staff members with filtering and pagination."""
    try:
        query = db.query(Staff)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Staff.tenant_id == tenant_id)
        
        if department_id:
            query = query.filter(Staff.department_id == department_id)
        
        if position:
            query = query.filter(Staff.position == position)
        
        if employment_status:
            query = query.filter(Staff.employment_status == employment_status)
        
        if is_active is not None:
            query = query.filter(Staff.is_active == is_active)
        
        # Search functionality
        if search:
            search_filter = or_(
                Staff.first_name.ilike(f"%{search}%"),
                Staff.last_name.ilike(f"%{search}%"),
                Staff.employee_id.ilike(f"%{search}%"),
                Staff.email.ilike(f"%{search}%"),
                Staff.phone.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        staff_members = query.offset(skip).limit(limit).all()
        
        return StaffListResponse(
            staff=staff_members,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting staff members: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{staff_id}", response_model=StaffResponse)
async def get_staff_member(
    staff_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific staff member by ID."""
    try:
        staff = db.query(Staff).filter(Staff.id == staff_id).first()
        
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found"
            )
        
        return staff
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting staff member: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/{staff_id}", response_model=StaffResponse)
async def update_staff_member(
    staff_id: str,
    staff_data: StaffUpdate,
    db: Session = Depends(get_db)
):
    """Update a staff member."""
    try:
        staff = db.query(Staff).filter(Staff.id == staff_id).first()
        
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found"
            )
        
        # Update fields
        update_data = staff_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(staff, field, value)
        
        staff.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(staff)
        
        logger.info(f"Staff member updated: {staff.employee_id}")
        return staff
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating staff member: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{staff_id}")
async def delete_staff_member(
    staff_id: str,
    db: Session = Depends(get_db)
):
    """Delete a staff member (soft delete)."""
    try:
        staff = db.query(Staff).filter(Staff.id == staff_id).first()
        
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found"
            )
        
        # Soft delete
        staff.is_active = False
        staff.employment_status = "terminated"
        staff.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Staff member deleted: {staff.employee_id}")
        return {"message": "Staff member deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting staff member: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Department CRUD Operations
@router.post("/departments", response_model=DepartmentResponse)
async def create_department(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db)
):
    """Create a new department."""
    try:
        # Check if department code already exists
        existing_dept = db.query(Department).filter(
            Department.code == department_data.code,
            Department.tenant_id == department_data.tenant_id
        ).first()
        
        if existing_dept:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department with this code already exists"
            )
        
        # Create new department
        department = Department(**department_data.dict())
        db.add(department)
        db.commit()
        db.refresh(department)
        
        logger.info(f"New department created: {department.code}")
        return department
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating department: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/departments", response_model=DepartmentListResponse)
async def get_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of departments with filtering and pagination."""
    try:
        query = db.query(Department)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Department.tenant_id == tenant_id)
        
        if is_active is not None:
            query = query.filter(Department.is_active == is_active)
        
        # Search functionality
        if search:
            search_filter = or_(
                Department.name.ilike(f"%{search}%"),
                Department.code.ilike(f"%{search}%"),
                Department.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        departments = query.offset(skip).limit(limit).all()
        
        return DepartmentListResponse(
            departments=departments,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting departments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Role CRUD Operations
@router.post("/roles", response_model=RoleResponse)
async def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db)
):
    """Create a new role."""
    try:
        # Check if role code already exists
        existing_role = db.query(Role).filter(
            Role.code == role_data.code,
            Role.tenant_id == role_data.tenant_id
        ).first()
        
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role with this code already exists"
            )
        
        # Create new role
        role = Role(**role_data.dict())
        db.add(role)
        db.commit()
        db.refresh(role)
        
        logger.info(f"New role created: {role.code}")
        return role
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating role: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/roles", response_model=RoleListResponse)
async def get_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of roles with filtering and pagination."""
    try:
        query = db.query(Role)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Role.tenant_id == tenant_id)
        
        if is_active is not None:
            query = query.filter(Role.is_active == is_active)
        
        # Search functionality
        if search:
            search_filter = or_(
                Role.name.ilike(f"%{search}%"),
                Role.code.ilike(f"%{search}%"),
                Role.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        roles = query.offset(skip).limit(limit).all()
        
        return RoleListResponse(
            roles=roles,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting roles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Staff Role Assignment
@router.post("/{staff_id}/roles", response_model=StaffRoleResponse)
async def assign_role_to_staff(
    staff_id: str,
    role_assignment: StaffRoleCreate,
    db: Session = Depends(get_db)
):
    """Assign a role to a staff member."""
    try:
        # Check if staff member exists
        staff = db.query(Staff).filter(Staff.id == staff_id).first()
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found"
            )
        
        # Check if role exists
        role = db.query(Role).filter(Role.id == role_assignment.role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        # Check if role is already assigned
        existing_assignment = db.query(StaffRole).filter(
            StaffRole.staff_id == staff_id,
            StaffRole.role_id == role_assignment.role_id,
            StaffRole.is_active == True
        ).first()
        
        if existing_assignment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role is already assigned to this staff member"
            )
        
        # Create role assignment
        staff_role = StaffRole(
            staff_id=staff_id,
            role_id=role_assignment.role_id,
            assigned_date=role_assignment.assigned_date,
            expiry_date=role_assignment.expiry_date,
            assigned_by=role_assignment.assigned_by
        )
        db.add(staff_role)
        db.commit()
        db.refresh(staff_role)
        
        logger.info(f"Role {role.code} assigned to staff {staff.employee_id}")
        return staff_role
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning role to staff: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{staff_id}/roles", response_model=StaffRoleListResponse)
async def get_staff_roles(
    staff_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get roles assigned to a staff member."""
    try:
        # Check if staff member exists
        staff = db.query(Staff).filter(Staff.id == staff_id).first()
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found"
            )
        
        query = db.query(StaffRole).filter(StaffRole.staff_id == staff_id)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        staff_roles = query.offset(skip).limit(limit).all()
        
        return StaffRoleListResponse(
            staff_roles=staff_roles,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting staff roles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Leave Request Operations
@router.post("/{staff_id}/leave-requests", response_model=LeaveRequestResponse)
async def create_leave_request(
    staff_id: str,
    leave_data: LeaveRequestCreate,
    db: Session = Depends(get_db)
):
    """Create a leave request for a staff member."""
    try:
        # Check if staff member exists
        staff = db.query(Staff).filter(Staff.id == staff_id).first()
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found"
            )
        
        # Create leave request
        leave_request = LeaveRequest(
            staff_id=staff_id,
            leave_type=leave_data.leave_type,
            start_date=leave_data.start_date,
            end_date=leave_data.end_date,
            days_requested=leave_data.days_requested,
            reason=leave_data.reason
        )
        db.add(leave_request)
        db.commit()
        db.refresh(leave_request)
        
        logger.info(f"Leave request created for staff {staff.employee_id}")
        return leave_request
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating leave request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{staff_id}/leave-requests", response_model=LeaveRequestListResponse)
async def get_staff_leave_requests(
    staff_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get leave requests for a staff member."""
    try:
        # Check if staff member exists
        staff = db.query(Staff).filter(Staff.id == staff_id).first()
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found"
            )
        
        query = db.query(LeaveRequest).filter(LeaveRequest.staff_id == staff_id)
        
        # Apply status filter
        if status_filter:
            query = query.filter(LeaveRequest.status == status_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        leave_requests = query.offset(skip).limit(limit).all()
        
        return LeaveRequestListResponse(
            leave_requests=leave_requests,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting leave requests: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Attendance Operations
@router.post("/{staff_id}/attendance", response_model=AttendanceResponse)
async def create_attendance_record(
    staff_id: str,
    attendance_data: AttendanceCreate,
    db: Session = Depends(get_db)
):
    """Create an attendance record for a staff member."""
    try:
        # Check if staff member exists
        staff = db.query(Staff).filter(Staff.id == staff_id).first()
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found"
            )
        
        # Check if attendance record already exists for this date
        existing_record = db.query(Attendance).filter(
            Attendance.staff_id == staff_id,
            Attendance.date == attendance_data.date
        ).first()
        
        if existing_record:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendance record already exists for this date"
            )
        
        # Create attendance record
        attendance = Attendance(
            staff_id=staff_id,
            date=attendance_data.date,
            check_in=attendance_data.check_in,
            check_out=attendance_data.check_out,
            status=attendance_data.status,
            notes=attendance_data.notes
        )
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        
        logger.info(f"Attendance record created for staff {staff.employee_id}")
        return attendance
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating attendance record: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{staff_id}/attendance", response_model=AttendanceListResponse)
async def get_staff_attendance(
    staff_id: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get attendance records for a staff member."""
    try:
        # Check if staff member exists
        staff = db.query(Staff).filter(Staff.id == staff_id).first()
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found"
            )
        
        query = db.query(Attendance).filter(Attendance.staff_id == staff_id)
        
        # Apply date filters
        if start_date:
            query = query.filter(Attendance.date >= start_date)
        
        if end_date:
            query = query.filter(Attendance.date <= end_date)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        attendance_records = query.offset(skip).limit(limit).all()
        
        return AttendanceListResponse(
            attendance_records=attendance_records,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting attendance records: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 