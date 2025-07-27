"""
Attendance Service Router (AI SchoolOS)

Comprehensive attendance management endpoints including:
- Attendance records (CRUD)
- Biometric data management
- Attendance devices
- Attendance rules
- Attendance exceptions
- Reports and analytics
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Request
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc, asc
from slowapi import Limiter
from slowapi.util import get_remote_address

from models import (
    AttendanceRecord, BiometricData, AttendanceRule, AttendanceDevice,
    AttendanceException, AttendanceReport, AttendanceAnalytics
)
from database import get_db
from schemas import (
    # Attendance Records
    AttendanceRecordCreate, AttendanceRecordUpdate, AttendanceRecordResponse,
    AttendanceRecordList, AttendanceSearchParams, AttendanceStats,
    # Biometric Data
    BiometricDataCreate, BiometricDataUpdate, BiometricDataResponse,
    # Attendance Rules
    AttendanceRuleCreate, AttendanceRuleUpdate, AttendanceRuleResponse,
    # Attendance Devices
    AttendanceDeviceCreate, AttendanceDeviceUpdate, AttendanceDeviceResponse,
    # Attendance Exceptions
    AttendanceExceptionCreate, AttendanceExceptionUpdate, AttendanceExceptionResponse,
    # Reports and Analytics
    AttendanceReportCreate, AttendanceReportResponse,
    AttendanceAnalyticsCreate, AttendanceAnalyticsUpdate, AttendanceAnalyticsResponse,
    # Bulk Operations
    BulkAttendanceCreate, BulkAttendanceResponse,
    # Response Models
    SuccessResponse, ErrorResponse
)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/api/v1/attendance", tags=["attendance"])


@router.get("/")
async def root():
    return {"message": "Attendance Service is running"}


# ============================================================================
# ATTENDANCE RECORDS
# ============================================================================

@router.post("/records", response_model=AttendanceRecordResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("100/minute")
async def create_attendance_record(request: Request, record: AttendanceRecordCreate, db: Session = Depends(get_db), tenant_id: str = Query(..., description="Tenant ID")):
    """Create a new attendance record."""
    try:
        db_record = AttendanceRecord(
            tenant_id=tenant_id,
            **record.dict()
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create attendance record: {str(e)}"
        )


@router.get("/records/{record_id}", response_model=AttendanceRecordResponse)
@limiter.limit("200/minute")
async def get_attendance_record(
    record_id: str = Path(..., description="Attendance record ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific attendance record."""
    record = db.query(AttendanceRecord).filter(
        and_(
            AttendanceRecord.id == record_id,
            AttendanceRecord.tenant_id == tenant_id
        )
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    
    return record


@router.get("/records", response_model=AttendanceRecordList)
@limiter.limit("200/minute")
async def list_attendance_records(request: Request, db: Session = Depends(get_db), tenant_id: str = Query(..., description="Tenant ID"), student_id: Optional[str] = Query(None, description="Student ID"), class_id: Optional[str] = Query(None, description="Class ID"), section_id: Optional[str] = Query(None, description="Section ID"), attendance_date: Optional[date] = Query(None, description="Attendance date"), attendance_status: Optional[str] = Query(None, description="Attendance status"), attendance_type: Optional[str] = Query(None, description="Attendance type"), start_date: Optional[date] = Query(None, description="Start date"), end_date: Optional[date] = Query(None, description="End date"), page: int = Query(1, ge=1, description="Page number"), size: int = Query(10, ge=1, le=100, description="Page size")):
    """List attendance records with filtering and pagination."""
    query = db.query(AttendanceRecord).filter(
        AttendanceRecord.tenant_id == tenant_id
    )
    
    # Apply filters
    if student_id:
        query = query.filter(AttendanceRecord.student_id == student_id)
    if class_id:
        query = query.filter(AttendanceRecord.class_id == class_id)
    if section_id:
        query = query.filter(AttendanceRecord.section_id == section_id)
    if attendance_date:
        query = query.filter(AttendanceRecord.attendance_date == attendance_date)
    if attendance_status:
        query = query.filter(AttendanceRecord.attendance_status == attendance_status)
    if attendance_type:
        query = query.filter(AttendanceRecord.attendance_type == attendance_type)
    if start_date and end_date:
        query = query.filter(
            and_(
                AttendanceRecord.attendance_date >= start_date,
                AttendanceRecord.attendance_date <= end_date
            )
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    records = query.offset((page - 1) * size).limit(size).all()
    
    return AttendanceRecordList(
        records=records,
        total=total,
        page=page,
        size=size
    )


@router.put("/records/{record_id}", response_model=AttendanceRecordResponse)
@limiter.limit("100/minute")
async def update_attendance_record(
    record_update: AttendanceRecordUpdate,
    record_id: str = Path(..., description="Attendance record ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update an attendance record."""
    record = db.query(AttendanceRecord).filter(
        and_(
            AttendanceRecord.id == record_id,
            AttendanceRecord.tenant_id == tenant_id
        )
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    
    try:
        update_data = record_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(record, field, value)
        
        record.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(record)
        return record
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update attendance record: {str(e)}"
        )


@router.delete("/records/{record_id}", response_model=SuccessResponse)
@limiter.limit("50/minute")
async def delete_attendance_record(
    record_id: str = Path(..., description="Attendance record ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete an attendance record."""
    record = db.query(AttendanceRecord).filter(
        and_(
            AttendanceRecord.id == record_id,
            AttendanceRecord.tenant_id == tenant_id
        )
    ).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    
    try:
        db.delete(record)
        db.commit()
        return SuccessResponse(message="Attendance record deleted successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete attendance record: {str(e)}"
        )


@router.post("/records/bulk", response_model=BulkAttendanceResponse)
@limiter.limit("50/minute")
async def create_bulk_attendance_records(request: Request, bulk_data: BulkAttendanceCreate, db: Session = Depends(get_db), tenant_id: str = Query(..., description="Tenant ID")):
    """Create multiple attendance records in bulk."""
    created = 0
    failed = 0
    errors = []
    
    for record_data in bulk_data.records:
        try:
            db_record = AttendanceRecord(
                tenant_id=tenant_id,
                **record_data.dict()
            )
            db.add(db_record)
            created += 1
        except Exception as e:
            failed += 1
            errors.append({
                "record": record_data.dict(),
                "error": str(e)
            })
    
    try:
        db.commit()
        return BulkAttendanceResponse(
            created=created,
            failed=failed,
            errors=errors
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create bulk attendance records: {str(e)}"
        )


@router.get("/records/stats", response_model=AttendanceStats)
@limiter.limit("100/minute")
async def get_attendance_stats(request: Request, db: Session = Depends(get_db), tenant_id: str = Query(..., description="Tenant ID"), start_date: Optional[date] = Query(None, description="Start date"), end_date: Optional[date] = Query(None, description="End date"), student_id: Optional[str] = Query(None, description="Student ID"), class_id: Optional[str] = Query(None, description="Class ID")):
    """Get attendance statistics."""
    query = db.query(AttendanceRecord).filter(
        AttendanceRecord.tenant_id == tenant_id
    )
    
    if start_date and end_date:
        query = query.filter(
            and_(
                AttendanceRecord.attendance_date >= start_date,
                AttendanceRecord.attendance_date <= end_date
            )
        )
    if student_id:
        query = query.filter(AttendanceRecord.student_id == student_id)
    if class_id:
        query = query.filter(AttendanceRecord.class_id == class_id)
    
    total_records = query.count()
    present_count = query.filter(AttendanceRecord.attendance_status == "present").count()
    absent_count = query.filter(AttendanceRecord.attendance_status == "absent").count()
    late_count = query.filter(AttendanceRecord.attendance_status == "late").count()
    half_day_count = query.filter(AttendanceRecord.attendance_status == "half_day").count()
    
    attendance_rate = (present_count / total_records * 100) if total_records > 0 else 0
    
    return AttendanceStats(
        total_records=total_records,
        present_count=present_count,
        absent_count=absent_count,
        late_count=late_count,
        half_day_count=half_day_count,
        attendance_rate=attendance_rate,
        date_range={"start_date": start_date, "end_date": end_date} if start_date and end_date else {}
    )


# ============================================================================
# BIOMETRIC DATA
# ============================================================================

@router.post("/biometric", response_model=BiometricDataResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("50/minute")
async def create_biometric_data(
    biometric_data: BiometricDataCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create biometric data for a user."""
    try:
        db_biometric = BiometricData(
            tenant_id=tenant_id,
            **biometric_data.dict()
        )
        db.add(db_biometric)
        db.commit()
        db.refresh(db_biometric)
        return db_biometric
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create biometric data: {str(e)}"
        )


@router.get("/biometric/{biometric_id}", response_model=BiometricDataResponse)
@limiter.limit("200/minute")
async def get_biometric_data(
    biometric_id: str = Path(..., description="Biometric data ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get specific biometric data."""
    biometric = db.query(BiometricData).filter(
        and_(
            BiometricData.id == biometric_id,
            BiometricData.tenant_id == tenant_id
        )
    ).first()
    
    if not biometric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Biometric data not found"
        )
    
    return biometric


@router.get("/biometric", response_model=List[BiometricDataResponse])
@limiter.limit("200/minute")
async def list_biometric_data(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    user_id: Optional[str] = Query(None, description="User ID"),
    user_type: Optional[str] = Query(None, description="User type"),
    biometric_type: Optional[str] = Query(None, description="Biometric type"),
    is_active: Optional[bool] = Query(None, description="Is active")
):
    """List biometric data with filtering."""
    query = db.query(BiometricData).filter(
        BiometricData.tenant_id == tenant_id
    )
    
    if user_id:
        query = query.filter(BiometricData.user_id == user_id)
    if user_type:
        query = query.filter(BiometricData.user_type == user_type)
    if biometric_type:
        query = query.filter(BiometricData.biometric_type == biometric_type)
    if is_active is not None:
        query = query.filter(BiometricData.is_active == is_active)
    
    return query.all()


@router.put("/biometric/{biometric_id}", response_model=BiometricDataResponse)
@limiter.limit("50/minute")
async def update_biometric_data(
    biometric_update: BiometricDataUpdate,
    biometric_id: str = Path(..., description="Biometric data ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update biometric data."""
    biometric = db.query(BiometricData).filter(
        and_(
            BiometricData.id == biometric_id,
            BiometricData.tenant_id == tenant_id
        )
    ).first()
    
    if not biometric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Biometric data not found"
        )
    
    try:
        update_data = biometric_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(biometric, field, value)
        
        biometric.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(biometric)
        return biometric
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update biometric data: {str(e)}"
        )


@router.delete("/biometric/{biometric_id}", response_model=SuccessResponse)
@limiter.limit("30/minute")
async def delete_biometric_data(
    biometric_id: str = Path(..., description="Biometric data ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete biometric data."""
    biometric = db.query(BiometricData).filter(
        and_(
            BiometricData.id == biometric_id,
            BiometricData.tenant_id == tenant_id
        )
    ).first()
    
    if not biometric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Biometric data not found"
        )
    
    try:
        db.delete(biometric)
        db.commit()
        return SuccessResponse(message="Biometric data deleted successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete biometric data: {str(e)}"
        )


# ============================================================================
# ATTENDANCE RULES
# ============================================================================

@router.post("/rules", response_model=AttendanceRuleResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("50/minute")
async def create_attendance_rule(
    rule: AttendanceRuleCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create an attendance rule."""
    try:
        db_rule = AttendanceRule(
            tenant_id=tenant_id,
            **rule.dict()
        )
        db.add(db_rule)
        db.commit()
        db.refresh(db_rule)
        return db_rule
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create attendance rule: {str(e)}"
        )


@router.get("/rules/{rule_id}", response_model=AttendanceRuleResponse)
@limiter.limit("200/minute")
async def get_attendance_rule(
    rule_id: str = Path(..., description="Attendance rule ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific attendance rule."""
    rule = db.query(AttendanceRule).filter(
        and_(
            AttendanceRule.id == rule_id,
            AttendanceRule.tenant_id == tenant_id
        )
    ).first()
    
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance rule not found"
        )
    
    return rule


@router.get("/rules", response_model=List[AttendanceRuleResponse])
@limiter.limit("200/minute")
async def list_attendance_rules(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    rule_type: Optional[str] = Query(None, description="Rule type"),
    target_id: Optional[str] = Query(None, description="Target ID"),
    is_active: Optional[bool] = Query(None, description="Is active")
):
    """List attendance rules with filtering."""
    query = db.query(AttendanceRule).filter(
        AttendanceRule.tenant_id == tenant_id
    )
    
    if rule_type:
        query = query.filter(AttendanceRule.rule_type == rule_type)
    if target_id:
        query = query.filter(AttendanceRule.target_id == target_id)
    if is_active is not None:
        query = query.filter(AttendanceRule.is_active == is_active)
    
    return query.all()


@router.put("/rules/{rule_id}", response_model=AttendanceRuleResponse)
@limiter.limit("50/minute")
async def update_attendance_rule(
    rule_update: AttendanceRuleUpdate,
    rule_id: str = Path(..., description="Attendance rule ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update an attendance rule."""
    rule = db.query(AttendanceRule).filter(
        and_(
            AttendanceRule.id == rule_id,
            AttendanceRule.tenant_id == tenant_id
        )
    ).first()
    
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance rule not found"
        )
    
    try:
        update_data = rule_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(rule, field, value)
        
        rule.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(rule)
        return rule
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update attendance rule: {str(e)}"
        )


@router.delete("/rules/{rule_id}", response_model=SuccessResponse)
@limiter.limit("30/minute")
async def delete_attendance_rule(
    rule_id: str = Path(..., description="Attendance rule ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete an attendance rule."""
    rule = db.query(AttendanceRule).filter(
        and_(
            AttendanceRule.id == rule_id,
            AttendanceRule.tenant_id == tenant_id
        )
    ).first()
    
    if not rule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance rule not found"
        )
    
    try:
        db.delete(rule)
        db.commit()
        return SuccessResponse(message="Attendance rule deleted successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete attendance rule: {str(e)}"
        )


# ============================================================================
# ATTENDANCE DEVICES
# ============================================================================

@router.post("/devices", response_model=AttendanceDeviceResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
async def create_attendance_device(
    device: AttendanceDeviceCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create an attendance device."""
    try:
        db_device = AttendanceDevice(
            tenant_id=tenant_id,
            **device.dict()
        )
        db.add(db_device)
        db.commit()
        db.refresh(db_device)
        return db_device
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create attendance device: {str(e)}"
        )


@router.get("/devices/{device_id}", response_model=AttendanceDeviceResponse)
@limiter.limit("200/minute")
async def get_attendance_device(
    device_id: str = Path(..., description="Attendance device ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific attendance device."""
    device = db.query(AttendanceDevice).filter(
        and_(
            AttendanceDevice.id == device_id,
            AttendanceDevice.tenant_id == tenant_id
        )
    ).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance device not found"
        )
    
    return device


@router.get("/devices", response_model=List[AttendanceDeviceResponse])
@limiter.limit("200/minute")
async def list_attendance_devices(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    device_type: Optional[str] = Query(None, description="Device type"),
    location: Optional[str] = Query(None, description="Location"),
    is_active: Optional[bool] = Query(None, description="Is active"),
    is_online: Optional[bool] = Query(None, description="Is online")
):
    """List attendance devices with filtering."""
    query = db.query(AttendanceDevice).filter(
        AttendanceDevice.tenant_id == tenant_id
    )
    
    if device_type:
        query = query.filter(AttendanceDevice.device_type == device_type)
    if location:
        query = query.filter(AttendanceDevice.location == location)
    if is_active is not None:
        query = query.filter(AttendanceDevice.is_active == is_active)
    if is_online is not None:
        query = query.filter(AttendanceDevice.is_online == is_online)
    
    return query.all()


@router.put("/devices/{device_id}", response_model=AttendanceDeviceResponse)
@limiter.limit("50/minute")
async def update_attendance_device(
    device_update: AttendanceDeviceUpdate,
    device_id: str = Path(..., description="Attendance device ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update an attendance device."""
    device = db.query(AttendanceDevice).filter(
        and_(
            AttendanceDevice.id == device_id,
            AttendanceDevice.tenant_id == tenant_id
        )
    ).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance device not found"
        )
    
    try:
        update_data = device_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(device, field, value)
        
        device.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(device)
        return device
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update attendance device: {str(e)}"
        )


@router.delete("/devices/{device_id}", response_model=SuccessResponse)
@limiter.limit("20/minute")
async def delete_attendance_device(
    device_id: str = Path(..., description="Attendance device ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete an attendance device."""
    device = db.query(AttendanceDevice).filter(
        and_(
            AttendanceDevice.id == device_id,
            AttendanceDevice.tenant_id == tenant_id
        )
    ).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance device not found"
        )
    
    try:
        db.delete(device)
        db.commit()
        return SuccessResponse(message="Attendance device deleted successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete attendance device: {str(e)}"
        )


# ============================================================================
# ATTENDANCE EXCEPTIONS
# ============================================================================

@router.post("/exceptions", response_model=AttendanceExceptionResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("50/minute")
async def create_attendance_exception(
    exception: AttendanceExceptionCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create an attendance exception."""
    try:
        db_exception = AttendanceException(
            tenant_id=tenant_id,
            **exception.dict()
        )
        db.add(db_exception)
        db.commit()
        db.refresh(db_exception)
        return db_exception
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create attendance exception: {str(e)}"
        )


@router.get("/exceptions/{exception_id}", response_model=AttendanceExceptionResponse)
@limiter.limit("200/minute")
async def get_attendance_exception(
    exception_id: str = Path(..., description="Attendance exception ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific attendance exception."""
    exception = db.query(AttendanceException).filter(
        and_(
            AttendanceException.id == exception_id,
            AttendanceException.tenant_id == tenant_id
        )
    ).first()
    
    if not exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance exception not found"
        )
    
    return exception


@router.get("/exceptions", response_model=List[AttendanceExceptionResponse])
@limiter.limit("200/minute")
async def list_attendance_exceptions(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    student_id: Optional[str] = Query(None, description="Student ID"),
    exception_type: Optional[str] = Query(None, description="Exception type"),
    approval_status: Optional[str] = Query(None, description="Approval status"),
    start_date: Optional[date] = Query(None, description="Start date"),
    end_date: Optional[date] = Query(None, description="End date")
):
    """List attendance exceptions with filtering."""
    query = db.query(AttendanceException).filter(
        AttendanceException.tenant_id == tenant_id
    )
    
    if student_id:
        query = query.filter(AttendanceException.student_id == student_id)
    if exception_type:
        query = query.filter(AttendanceException.exception_type == exception_type)
    if approval_status:
        query = query.filter(AttendanceException.approval_status == approval_status)
    if start_date and end_date:
        query = query.filter(
            and_(
                AttendanceException.start_date >= start_date,
                AttendanceException.end_date <= end_date
            )
        )
    
    return query.all()


@router.put("/exceptions/{exception_id}", response_model=AttendanceExceptionResponse)
@limiter.limit("50/minute")
async def update_attendance_exception(
    exception_update: AttendanceExceptionUpdate,
    exception_id: str = Path(..., description="Attendance exception ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update an attendance exception."""
    exception = db.query(AttendanceException).filter(
        and_(
            AttendanceException.id == exception_id,
            AttendanceException.tenant_id == tenant_id
        )
    ).first()
    
    if not exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance exception not found"
        )
    
    try:
        update_data = exception_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(exception, field, value)
        
        exception.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(exception)
        return exception
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update attendance exception: {str(e)}"
        )


@router.delete("/exceptions/{exception_id}", response_model=SuccessResponse)
@limiter.limit("30/minute")
async def delete_attendance_exception(
    exception_id: str = Path(..., description="Attendance exception ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete an attendance exception."""
    exception = db.query(AttendanceException).filter(
        and_(
            AttendanceException.id == exception_id,
            AttendanceException.tenant_id == tenant_id
        )
    ).first()
    
    if not exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance exception not found"
        )
    
    try:
        db.delete(exception)
        db.commit()
        return SuccessResponse(message="Attendance exception deleted successfully")
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete attendance exception: {str(e)}"
        )


# ============================================================================
# REPORTS AND ANALYTICS
# ============================================================================

@router.post("/reports", response_model=AttendanceReportResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
async def create_attendance_report(
    report: AttendanceReportCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create an attendance report."""
    try:
        db_report = AttendanceReport(
            tenant_id=tenant_id,
            **report.dict()
        )
        db.add(db_report)
        db.commit()
        db.refresh(db_report)
        return db_report
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create attendance report: {str(e)}"
        )


@router.get("/reports/{report_id}", response_model=AttendanceReportResponse)
@limiter.limit("200/minute")
async def get_attendance_report(
    report_id: str = Path(..., description="Attendance report ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific attendance report."""
    report = db.query(AttendanceReport).filter(
        and_(
            AttendanceReport.id == report_id,
            AttendanceReport.tenant_id == tenant_id
        )
    ).first()
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance report not found"
        )
    
    return report


@router.get("/reports", response_model=List[AttendanceReportResponse])
@limiter.limit("200/minute")
async def list_attendance_reports(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    report_type: Optional[str] = Query(None, description="Report type"),
    target_type: Optional[str] = Query(None, description="Target type"),
    generated_by: Optional[str] = Query(None, description="Generated by")
):
    """List attendance reports with filtering."""
    query = db.query(AttendanceReport).filter(
        AttendanceReport.tenant_id == tenant_id
    )
    
    if report_type:
        query = query.filter(AttendanceReport.report_type == report_type)
    if target_type:
        query = query.filter(AttendanceReport.target_type == target_type)
    if generated_by:
        query = query.filter(AttendanceReport.generated_by == generated_by)
    
    return query.order_by(desc(AttendanceReport.generated_at)).all()


@router.post("/analytics", response_model=AttendanceAnalyticsResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
async def create_attendance_analytics(
    analytics: AttendanceAnalyticsCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create attendance analytics."""
    try:
        db_analytics = AttendanceAnalytics(
            tenant_id=tenant_id,
            **analytics.dict()
        )
        db.add(db_analytics)
        db.commit()
        db.refresh(db_analytics)
        return db_analytics
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create attendance analytics: {str(e)}"
        )


@router.get("/analytics/{analytics_id}", response_model=AttendanceAnalyticsResponse)
@limiter.limit("200/minute")
async def get_attendance_analytics(
    analytics_id: str = Path(..., description="Attendance analytics ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get specific attendance analytics."""
    analytics = db.query(AttendanceAnalytics).filter(
        and_(
            AttendanceAnalytics.id == analytics_id,
            AttendanceAnalytics.tenant_id == tenant_id
        )
    ).first()
    
    if not analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance analytics not found"
        )
    
    return analytics


@router.get("/analytics", response_model=List[AttendanceAnalyticsResponse])
@limiter.limit("200/minute")
async def list_attendance_analytics(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    analytics_date: Optional[date] = Query(None, description="Analytics date"),
    analytics_period: Optional[str] = Query(None, description="Analytics period")
):
    """List attendance analytics with filtering."""
    query = db.query(AttendanceAnalytics).filter(
        AttendanceAnalytics.tenant_id == tenant_id
    )
    
    if analytics_date:
        query = query.filter(AttendanceAnalytics.analytics_date == analytics_date)
    if analytics_period:
        query = query.filter(AttendanceAnalytics.analytics_period == analytics_period)
    
    return query.order_by(desc(AttendanceAnalytics.analytics_date)).all()


@router.put("/analytics/{analytics_id}", response_model=AttendanceAnalyticsResponse)
@limiter.limit("30/minute")
async def update_attendance_analytics(
    analytics_update: AttendanceAnalyticsUpdate,
    analytics_id: str = Path(..., description="Attendance analytics ID"),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update attendance analytics."""
    analytics = db.query(AttendanceAnalytics).filter(
        and_(
            AttendanceAnalytics.id == analytics_id,
            AttendanceAnalytics.tenant_id == tenant_id
        )
    ).first()
    
    if not analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance analytics not found"
        )
    
    try:
        update_data = analytics_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(analytics, field, value)
        
        analytics.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(analytics)
        return analytics
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update attendance analytics: {str(e)}"
        ) 