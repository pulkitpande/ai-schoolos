"""
Student router for Student Service (AI SchoolOS)
"""

import logging
from typing import List, Optional
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from database import get_db
from models import Student, Guardian, Enrollment, AcademicRecord, AttendanceRecord
from schemas import (
    StudentCreate, StudentUpdate, StudentResponse, StudentListResponse,
    StudentWithGuardians, StudentWithEnrollments, StudentWithAcademicRecords,
    StudentWithAttendance, StudentComplete,
    GuardianCreate, GuardianUpdate, GuardianResponse, GuardianListResponse,
    EnrollmentCreate, EnrollmentUpdate, EnrollmentResponse, EnrollmentListResponse,
    AcademicRecordCreate, AcademicRecordUpdate, AcademicRecordResponse, AcademicRecordListResponse,
    AttendanceRecordCreate, AttendanceRecordUpdate, AttendanceRecordResponse, AttendanceRecordListResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/students", tags=["students"])


# Student CRUD Operations
@router.post("/", response_model=StudentResponse)
async def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    """Create a new student."""
    try:
        # Check if admission number already exists
        existing_student = db.query(Student).filter(
            Student.admission_number == student_data.admission_number,
            Student.tenant_id == student_data.tenant_id
        ).first()
        
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student with this admission number already exists"
            )
        
        # Create new student
        student = Student(**student_data.dict())
        db.add(student)
        db.commit()
        db.refresh(student)
        
        logger.info(f"New student created: {student.admission_number}")
        return student
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating student: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/", response_model=StudentListResponse)
async def get_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    class_name: Optional[str] = None,
    section: Optional[str] = None,
    academic_year: Optional[str] = None,
    enrollment_status: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of students with filtering and pagination."""
    try:
        query = db.query(Student)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Student.tenant_id == tenant_id)
        
        if class_name:
            query = query.filter(Student.current_class == class_name)
        
        if section:
            query = query.filter(Student.current_section == section)
        
        if academic_year:
            query = query.filter(Student.academic_year == academic_year)
        
        if enrollment_status:
            query = query.filter(Student.enrollment_status == enrollment_status)
        
        if is_active is not None:
            query = query.filter(Student.is_active == is_active)
        
        # Search functionality
        if search:
            search_filter = or_(
                Student.first_name.ilike(f"%{search}%"),
                Student.last_name.ilike(f"%{search}%"),
                Student.admission_number.ilike(f"%{search}%"),
                Student.phone.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        students = query.offset(skip).limit(limit).all()
        
        return StudentListResponse(
            students=students,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting students: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific student by ID."""
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        return student
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting student: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: str,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    """Update a student."""
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        # Update fields
        update_data = student_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(student, field, value)
        
        student.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(student)
        
        logger.info(f"Student updated: {student.admission_number}")
        return student
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating student: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{student_id}")
async def delete_student(
    student_id: str,
    db: Session = Depends(get_db)
):
    """Delete a student (soft delete by setting is_active to False)."""
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        # Soft delete
        student.is_active = False
        student.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Student deleted: {student.admission_number}")
        return {"message": "Student deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting student: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Student with Relationships
@router.get("/{student_id}/complete", response_model=StudentComplete)
async def get_student_complete(
    student_id: str,
    db: Session = Depends(get_db)
):
    """Get a student with all related data."""
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        return student
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting student complete: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Guardian Operations
@router.post("/{student_id}/guardians", response_model=GuardianResponse)
async def create_guardian(
    student_id: str,
    guardian_data: GuardianCreate,
    db: Session = Depends(get_db)
):
    """Create a guardian for a student."""
    try:
        # Check if student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        # Create guardian
        guardian = Guardian(**guardian_data.dict())
        db.add(guardian)
        db.commit()
        db.refresh(guardian)
        
        logger.info(f"Guardian created for student: {student.admission_number}")
        return guardian
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating guardian: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{student_id}/guardians", response_model=GuardianListResponse)
async def get_student_guardians(
    student_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get guardians for a student."""
    try:
        # Check if student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        query = db.query(Guardian).filter(Guardian.student_id == student_id)
        total = query.count()
        guardians = query.offset(skip).limit(limit).all()
        
        return GuardianListResponse(
            guardians=guardians,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting guardians: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Enrollment Operations
@router.post("/{student_id}/enrollments", response_model=EnrollmentResponse)
async def create_enrollment(
    student_id: str,
    enrollment_data: EnrollmentCreate,
    db: Session = Depends(get_db)
):
    """Create an enrollment for a student."""
    try:
        # Check if student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        # Create enrollment
        enrollment = Enrollment(**enrollment_data.dict())
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        
        logger.info(f"Enrollment created for student: {student.admission_number}")
        return enrollment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating enrollment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{student_id}/enrollments", response_model=EnrollmentListResponse)
async def get_student_enrollments(
    student_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get enrollments for a student."""
    try:
        # Check if student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        query = db.query(Enrollment).filter(Enrollment.student_id == student_id)
        total = query.count()
        enrollments = query.offset(skip).limit(limit).all()
        
        return EnrollmentListResponse(
            enrollments=enrollments,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting enrollments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Academic Record Operations
@router.post("/{student_id}/academic-records", response_model=AcademicRecordResponse)
async def create_academic_record(
    student_id: str,
    academic_data: AcademicRecordCreate,
    db: Session = Depends(get_db)
):
    """Create an academic record for a student."""
    try:
        # Check if student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        # Create academic record
        academic_record = AcademicRecord(**academic_data.dict())
        db.add(academic_record)
        db.commit()
        db.refresh(academic_record)
        
        logger.info(f"Academic record created for student: {student.admission_number}")
        return academic_record
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating academic record: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{student_id}/academic-records", response_model=AcademicRecordListResponse)
async def get_student_academic_records(
    student_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get academic records for a student."""
    try:
        # Check if student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        query = db.query(AcademicRecord).filter(AcademicRecord.student_id == student_id)
        total = query.count()
        academic_records = query.offset(skip).limit(limit).all()
        
        return AcademicRecordListResponse(
            academic_records=academic_records,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting academic records: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Attendance Operations
@router.post("/{student_id}/attendance", response_model=AttendanceRecordResponse)
async def create_attendance_record(
    student_id: str,
    attendance_data: AttendanceRecordCreate,
    db: Session = Depends(get_db)
):
    """Create an attendance record for a student."""
    try:
        # Check if student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        # Check if attendance record already exists for the date
        existing_attendance = db.query(AttendanceRecord).filter(
            AttendanceRecord.student_id == student_id,
            AttendanceRecord.date == attendance_data.date
        ).first()
        
        if existing_attendance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Attendance record already exists for this date"
            )
        
        # Create attendance record
        attendance_record = AttendanceRecord(**attendance_data.dict())
        db.add(attendance_record)
        db.commit()
        db.refresh(attendance_record)
        
        logger.info(f"Attendance record created for student: {student.admission_number}")
        return attendance_record
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating attendance record: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{student_id}/attendance", response_model=AttendanceRecordListResponse)
async def get_student_attendance(
    student_id: str,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get attendance records for a student."""
    try:
        # Check if student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        query = db.query(AttendanceRecord).filter(AttendanceRecord.student_id == student_id)
        
        # Apply date filters
        if start_date:
            query = query.filter(AttendanceRecord.date >= start_date)
        
        if end_date:
            query = query.filter(AttendanceRecord.date <= end_date)
        
        total = query.count()
        attendance_records = query.offset(skip).limit(limit).all()
        
        return AttendanceRecordListResponse(
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