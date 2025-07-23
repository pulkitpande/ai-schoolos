"""
Fees router for Fee Service (AI SchoolOS)
"""

import logging
from typing import List, Optional
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from decimal import Decimal

from database import get_db
from models import FeeStructure, StudentFee, Bill, Payment, Discount, FinancialRecord
from schemas import (
    FeeStructureCreate, FeeStructureUpdate, FeeStructureResponse, FeeStructureListResponse,
    StudentFeeCreate, StudentFeeUpdate, StudentFeeResponse, StudentFeeListResponse,
    BillCreate, BillUpdate, BillResponse, BillListResponse,
    PaymentCreate, PaymentUpdate, PaymentResponse, PaymentListResponse,
    DiscountCreate, DiscountUpdate, DiscountResponse, DiscountListResponse,
    FinancialRecordCreate, FinancialRecordUpdate, FinancialRecordResponse, FinancialRecordListResponse,
    FeeSummary, StudentFeeSummary
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/fees", tags=["fees"])


# Fee Structure CRUD Operations
@router.post("/structures", response_model=FeeStructureResponse)
async def create_fee_structure(
    fee_structure_data: FeeStructureCreate,
    db: Session = Depends(get_db)
):
    """Create a new fee structure."""
    try:
        # Check if fee structure code already exists
        existing_structure = db.query(FeeStructure).filter(
            FeeStructure.code == fee_structure_data.code,
            FeeStructure.tenant_id == fee_structure_data.tenant_id
        ).first()
        
        if existing_structure:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Fee structure with this code already exists"
            )
        
        # Create new fee structure
        fee_structure = FeeStructure(**fee_structure_data.dict())
        db.add(fee_structure)
        db.commit()
        db.refresh(fee_structure)
        
        logger.info(f"New fee structure created: {fee_structure.code}")
        return fee_structure
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating fee structure: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/structures", response_model=FeeStructureListResponse)
async def get_fee_structures(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    academic_year: Optional[str] = None,
    class_name: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of fee structures with filtering and pagination."""
    try:
        query = db.query(FeeStructure)
        
        # Apply filters
        if tenant_id:
            query = query.filter(FeeStructure.tenant_id == tenant_id)
        
        if academic_year:
            query = query.filter(FeeStructure.academic_year == academic_year)
        
        if class_name:
            query = query.filter(FeeStructure.class_name == class_name)
        
        if is_active is not None:
            query = query.filter(FeeStructure.is_active == is_active)
        
        # Search functionality
        if search:
            search_filter = or_(
                FeeStructure.name.ilike(f"%{search}%"),
                FeeStructure.code.ilike(f"%{search}%"),
                FeeStructure.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        fee_structures = query.offset(skip).limit(limit).all()
        
        return FeeStructureListResponse(
            fee_structures=fee_structures,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting fee structures: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/structures/{structure_id}", response_model=FeeStructureResponse)
async def get_fee_structure(
    structure_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific fee structure by ID."""
    try:
        fee_structure = db.query(FeeStructure).filter(FeeStructure.id == structure_id).first()
        
        if not fee_structure:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fee structure not found"
            )
        
        return fee_structure
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting fee structure: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Student Fee Operations
@router.post("/students", response_model=StudentFeeResponse)
async def create_student_fee(
    student_fee_data: StudentFeeCreate,
    db: Session = Depends(get_db)
):
    """Create a new student fee assignment."""
    try:
        # Check if fee structure exists
        fee_structure = db.query(FeeStructure).filter(
            FeeStructure.id == student_fee_data.fee_structure_id
        ).first()
        
        if not fee_structure:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fee structure not found"
            )
        
        # Check if student already has a fee assignment for this academic year
        existing_fee = db.query(StudentFee).filter(
            StudentFee.student_id == student_fee_data.student_id,
            StudentFee.academic_year == student_fee_data.academic_year,
            StudentFee.tenant_id == student_fee_data.tenant_id
        ).first()
        
        if existing_fee:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student already has a fee assignment for this academic year"
            )
        
        # Create new student fee assignment
        student_fee = StudentFee(**student_fee_data.dict())
        db.add(student_fee)
        db.commit()
        db.refresh(student_fee)
        
        logger.info(f"New student fee assignment created for student {student_fee.student_id}")
        return student_fee
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating student fee: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/students/{student_id}", response_model=StudentFeeListResponse)
async def get_student_fees(
    student_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    academic_year: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get fee assignments for a student."""
    try:
        query = db.query(StudentFee).filter(StudentFee.student_id == student_id)
        
        # Apply filters
        if academic_year:
            query = query.filter(StudentFee.academic_year == academic_year)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        student_fees = query.offset(skip).limit(limit).all()
        
        return StudentFeeListResponse(
            student_fees=student_fees,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting student fees: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Bill Operations
@router.post("/bills", response_model=BillResponse)
async def create_bill(
    bill_data: BillCreate,
    db: Session = Depends(get_db)
):
    """Create a new bill."""
    try:
        # Check if bill number already exists
        existing_bill = db.query(Bill).filter(
            Bill.bill_number == bill_data.bill_number,
            Bill.tenant_id == bill_data.tenant_id
        ).first()
        
        if existing_bill:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bill with this number already exists"
            )
        
        # Check if student fee exists
        student_fee = db.query(StudentFee).filter(
            StudentFee.id == bill_data.student_fee_id
        ).first()
        
        if not student_fee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student fee assignment not found"
            )
        
        # Create new bill
        bill = Bill(
            **bill_data.dict(),
            paid_amount=Decimal('0.00'),
            balance_amount=bill_data.total_amount
        )
        db.add(bill)
        db.commit()
        db.refresh(bill)
        
        logger.info(f"New bill created: {bill.bill_number}")
        return bill
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating bill: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/bills", response_model=BillListResponse)
async def get_bills(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    student_id: Optional[str] = None,
    status: Optional[str] = None,
    bill_type: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Get list of bills with filtering and pagination."""
    try:
        query = db.query(Bill)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Bill.tenant_id == tenant_id)
        
        if student_id:
            query = query.filter(Bill.student_id == student_id)
        
        if status:
            query = query.filter(Bill.status == status)
        
        if bill_type:
            query = query.filter(Bill.bill_type == bill_type)
        
        if start_date:
            query = query.filter(Bill.bill_date >= start_date)
        
        if end_date:
            query = query.filter(Bill.bill_date <= end_date)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        bills = query.offset(skip).limit(limit).all()
        
        return BillListResponse(
            bills=bills,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting bills: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/bills/{bill_id}", response_model=BillResponse)
async def get_bill(
    bill_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific bill by ID."""
    try:
        bill = db.query(Bill).filter(Bill.id == bill_id).first()
        
        if not bill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bill not found"
            )
        
        return bill
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting bill: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Payment Operations
@router.post("/payments", response_model=PaymentResponse)
async def create_payment(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db)
):
    """Create a new payment."""
    try:
        # Check if payment number already exists
        existing_payment = db.query(Payment).filter(
            Payment.payment_number == payment_data.payment_number,
            Payment.tenant_id == payment_data.tenant_id
        ).first()
        
        if existing_payment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment with this number already exists"
            )
        
        # Check if bill exists
        bill = db.query(Bill).filter(Bill.id == payment_data.bill_id).first()
        
        if not bill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bill not found"
            )
        
        # Create new payment
        payment = Payment(**payment_data.dict())
        db.add(payment)
        
        # Update bill paid amount
        bill.paid_amount += payment_data.amount
        bill.balance_amount = bill.total_amount - bill.paid_amount
        
        # Update bill status
        if bill.balance_amount <= 0:
            bill.status = "paid"
        elif bill.paid_amount > 0:
            bill.status = "partial"
        
        db.commit()
        db.refresh(payment)
        
        logger.info(f"New payment created: {payment.payment_number}")
        return payment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating payment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/payments", response_model=PaymentListResponse)
async def get_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    student_id: Optional[str] = None,
    bill_id: Optional[str] = None,
    status: Optional[str] = None,
    payment_method: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Get list of payments with filtering and pagination."""
    try:
        query = db.query(Payment)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Payment.tenant_id == tenant_id)
        
        if student_id:
            query = query.filter(Payment.student_id == student_id)
        
        if bill_id:
            query = query.filter(Payment.bill_id == bill_id)
        
        if status:
            query = query.filter(Payment.status == status)
        
        if payment_method:
            query = query.filter(Payment.payment_method == payment_method)
        
        if start_date:
            query = query.filter(Payment.payment_date >= start_date)
        
        if end_date:
            query = query.filter(Payment.payment_date <= end_date)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        payments = query.offset(skip).limit(limit).all()
        
        return PaymentListResponse(
            payments=payments,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting payments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Discount Operations
@router.post("/discounts", response_model=DiscountResponse)
async def create_discount(
    discount_data: DiscountCreate,
    db: Session = Depends(get_db)
):
    """Create a new discount."""
    try:
        # Create new discount
        discount = Discount(**discount_data.dict())
        db.add(discount)
        db.commit()
        db.refresh(discount)
        
        logger.info(f"New discount created for student {discount.student_id}")
        return discount
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating discount: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/discounts", response_model=DiscountListResponse)
async def get_discounts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    student_id: Optional[str] = None,
    discount_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get list of discounts with filtering and pagination."""
    try:
        query = db.query(Discount)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Discount.tenant_id == tenant_id)
        
        if student_id:
            query = query.filter(Discount.student_id == student_id)
        
        if discount_type:
            query = query.filter(Discount.discount_type == discount_type)
        
        if is_active is not None:
            query = query.filter(Discount.is_active == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        discounts = query.offset(skip).limit(limit).all()
        
        return DiscountListResponse(
            discounts=discounts,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting discounts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Financial Records Operations
@router.post("/financial-records", response_model=FinancialRecordResponse)
async def create_financial_record(
    record_data: FinancialRecordCreate,
    db: Session = Depends(get_db)
):
    """Create a new financial record."""
    try:
        # Create new financial record
        record = FinancialRecord(**record_data.dict())
        db.add(record)
        db.commit()
        db.refresh(record)
        
        logger.info(f"New financial record created: {record.record_type}")
        return record
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating financial record: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/financial-records", response_model=FinancialRecordListResponse)
async def get_financial_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    record_type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Get list of financial records with filtering and pagination."""
    try:
        query = db.query(FinancialRecord)
        
        # Apply filters
        if tenant_id:
            query = query.filter(FinancialRecord.tenant_id == tenant_id)
        
        if record_type:
            query = query.filter(FinancialRecord.record_type == record_type)
        
        if category:
            query = query.filter(FinancialRecord.category == category)
        
        if start_date:
            query = query.filter(FinancialRecord.date >= start_date)
        
        if end_date:
            query = query.filter(FinancialRecord.date <= end_date)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        records = query.offset(skip).limit(limit).all()
        
        return FinancialRecordListResponse(
            financial_records=records,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting financial records: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Summary Endpoints
@router.get("/summary", response_model=FeeSummary)
async def get_fee_summary(
    tenant_id: Optional[str] = None,
    academic_year: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get fee summary statistics."""
    try:
        # Build base queries
        bills_query = db.query(Bill)
        payments_query = db.query(Payment)
        discounts_query = db.query(Discount)
        
        # Apply filters
        if tenant_id:
            bills_query = bills_query.filter(Bill.tenant_id == tenant_id)
            payments_query = payments_query.filter(Payment.tenant_id == tenant_id)
            discounts_query = discounts_query.filter(Discount.tenant_id == tenant_id)
        
        # Get bill statistics
        total_bills = bills_query.count()
        total_amount = bills_query.with_entities(func.sum(Bill.total_amount)).scalar() or Decimal('0.00')
        paid_amount = bills_query.with_entities(func.sum(Bill.paid_amount)).scalar() or Decimal('0.00')
        pending_amount = bills_query.filter(Bill.status == "pending").with_entities(func.sum(Bill.balance_amount)).scalar() or Decimal('0.00')
        overdue_amount = bills_query.filter(Bill.status == "overdue").with_entities(func.sum(Bill.balance_amount)).scalar() or Decimal('0.00')
        
        # Get payment statistics
        total_payments = payments_query.count()
        
        # Get discount statistics
        total_discounts = discounts_query.filter(Discount.is_active == True).count()
        discount_amount = discounts_query.filter(Discount.is_active == True).with_entities(func.sum(Discount.discount_amount)).scalar() or Decimal('0.00')
        
        return FeeSummary(
            total_bills=total_bills,
            total_amount=total_amount,
            paid_amount=paid_amount,
            pending_amount=pending_amount,
            overdue_amount=overdue_amount,
            total_payments=total_payments,
            total_discounts=total_discounts,
            discount_amount=discount_amount
        )
        
    except Exception as e:
        logger.error(f"Error getting fee summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/students/{student_id}/summary", response_model=StudentFeeSummary)
async def get_student_fee_summary(
    student_id: str,
    db: Session = Depends(get_db)
):
    """Get fee summary for a specific student."""
    try:
        # Get bill statistics for student
        bills_query = db.query(Bill).filter(Bill.student_id == student_id)
        total_bills = bills_query.count()
        total_amount = bills_query.with_entities(func.sum(Bill.total_amount)).scalar() or Decimal('0.00')
        paid_amount = bills_query.with_entities(func.sum(Bill.paid_amount)).scalar() or Decimal('0.00')
        pending_amount = bills_query.filter(Bill.status == "pending").with_entities(func.sum(Bill.balance_amount)).scalar() or Decimal('0.00')
        overdue_amount = bills_query.filter(Bill.status == "overdue").with_entities(func.sum(Bill.balance_amount)).scalar() or Decimal('0.00')
        
        # Get payment statistics for student
        payments_query = db.query(Payment).filter(Payment.student_id == student_id)
        total_payments = payments_query.count()
        
        # Get discount statistics for student
        discounts_query = db.query(Discount).filter(Discount.student_id == student_id)
        total_discounts = discounts_query.filter(Discount.is_active == True).count()
        discount_amount = discounts_query.filter(Discount.is_active == True).with_entities(func.sum(Discount.discount_amount)).scalar() or Decimal('0.00')
        
        return StudentFeeSummary(
            student_id=student_id,
            total_bills=total_bills,
            total_amount=total_amount,
            paid_amount=paid_amount,
            pending_amount=pending_amount,
            overdue_amount=overdue_amount,
            total_payments=total_payments,
            total_discounts=total_discounts,
            discount_amount=discount_amount
        )
        
    except Exception as e:
        logger.error(f"Error getting student fee summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 