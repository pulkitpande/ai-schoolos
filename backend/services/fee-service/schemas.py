"""
Pydantic schemas for Fee Service (AI SchoolOS)
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from decimal import Decimal


# Fee Structure schemas
class FeeStructureBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    academic_year: str = Field(..., min_length=1, max_length=20)
    class_name: Optional[str] = Field(None, max_length=50)
    section: Optional[str] = Field(None, max_length=10)
    tuition_fee: Decimal = Field(..., ge=0)
    library_fee: Decimal = Field(0, ge=0)
    laboratory_fee: Decimal = Field(0, ge=0)
    sports_fee: Decimal = Field(0, ge=0)
    transport_fee: Decimal = Field(0, ge=0)
    hostel_fee: Decimal = Field(0, ge=0)
    other_fees: Optional[Dict[str, Any]] = {}
    payment_schedule: str = Field("monthly", max_length=20)
    due_date: int = Field(5, ge=1, le=31)


class FeeStructureCreate(FeeStructureBase):
    tenant_id: str


class FeeStructureUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = None
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    class_name: Optional[str] = Field(None, max_length=50)
    section: Optional[str] = Field(None, max_length=10)
    tuition_fee: Optional[Decimal] = Field(None, ge=0)
    library_fee: Optional[Decimal] = Field(None, ge=0)
    laboratory_fee: Optional[Decimal] = Field(None, ge=0)
    sports_fee: Optional[Decimal] = Field(None, ge=0)
    transport_fee: Optional[Decimal] = Field(None, ge=0)
    hostel_fee: Optional[Decimal] = Field(None, ge=0)
    other_fees: Optional[Dict[str, Any]] = None
    payment_schedule: Optional[str] = Field(None, max_length=20)
    due_date: Optional[int] = Field(None, ge=1, le=31)
    is_active: Optional[bool] = None


class FeeStructureResponse(FeeStructureBase):
    id: str
    tenant_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FeeStructureListResponse(BaseModel):
    fee_structures: List[FeeStructureResponse]
    total: int
    page: int
    size: int


# Student Fee schemas
class StudentFeeBase(BaseModel):
    student_id: str
    fee_structure_id: str
    academic_year: str = Field(..., min_length=1, max_length=20)
    class_name: str = Field(..., min_length=1, max_length=50)
    section: str = Field(..., min_length=1, max_length=10)
    total_amount: Decimal = Field(..., ge=0)
    discount_amount: Decimal = Field(0, ge=0)
    scholarship_amount: Decimal = Field(0, ge=0)
    final_amount: Decimal = Field(..., ge=0)


class StudentFeeCreate(StudentFeeBase):
    tenant_id: str


class StudentFeeUpdate(BaseModel):
    total_amount: Optional[Decimal] = Field(None, ge=0)
    discount_amount: Optional[Decimal] = Field(None, ge=0)
    scholarship_amount: Optional[Decimal] = Field(None, ge=0)
    final_amount: Optional[Decimal] = Field(None, ge=0)
    is_active: Optional[bool] = None


class StudentFeeResponse(StudentFeeBase):
    id: str
    tenant_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StudentFeeListResponse(BaseModel):
    student_fees: List[StudentFeeResponse]
    total: int
    page: int
    size: int


# Bill schemas
class BillBase(BaseModel):
    student_id: str
    student_fee_id: str
    bill_date: date
    due_date: date
    total_amount: Decimal = Field(..., ge=0)
    bill_type: str = Field(..., min_length=1, max_length=20)
    period: str = Field(..., min_length=1, max_length=20)
    notes: Optional[str] = None


class BillCreate(BillBase):
    tenant_id: str
    bill_number: str = Field(..., min_length=1, max_length=50)


class BillUpdate(BaseModel):
    bill_date: Optional[date] = None
    due_date: Optional[date] = None
    total_amount: Optional[Decimal] = Field(None, ge=0)
    bill_type: Optional[str] = Field(None, min_length=1, max_length=20)
    period: Optional[str] = Field(None, min_length=1, max_length=20)
    status: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None


class BillResponse(BillBase):
    id: str
    tenant_id: str
    bill_number: str
    paid_amount: Decimal
    balance_amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BillListResponse(BaseModel):
    bills: List[BillResponse]
    total: int
    page: int
    size: int


# Payment schemas
class PaymentBase(BaseModel):
    student_id: str
    bill_id: str
    payment_date: date
    amount: Decimal = Field(..., ge=0)
    payment_method: str = Field(..., min_length=1, max_length=50)
    payment_gateway: Optional[str] = Field(None, max_length=50)
    transaction_id: Optional[str] = Field(None, max_length=100)
    receipt_number: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    tenant_id: str
    payment_number: str = Field(..., min_length=1, max_length=50)


class PaymentUpdate(BaseModel):
    payment_date: Optional[date] = None
    amount: Optional[Decimal] = Field(None, ge=0)
    payment_method: Optional[str] = Field(None, min_length=1, max_length=50)
    payment_gateway: Optional[str] = Field(None, max_length=50)
    transaction_id: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, max_length=20)
    receipt_number: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None


class PaymentResponse(PaymentBase):
    id: str
    tenant_id: str
    payment_number: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaymentListResponse(BaseModel):
    payments: List[PaymentResponse]
    total: int
    page: int
    size: int


# Discount schemas
class DiscountBase(BaseModel):
    student_id: str
    discount_type: str = Field(..., min_length=1, max_length=50)
    discount_percentage: Decimal = Field(..., ge=0, le=100)
    discount_amount: Decimal = Field(..., ge=0)
    start_date: date
    end_date: Optional[date] = None
    reason: Optional[str] = None
    approved_by: Optional[str] = None


class DiscountCreate(DiscountBase):
    tenant_id: str


class DiscountUpdate(BaseModel):
    discount_type: Optional[str] = Field(None, min_length=1, max_length=50)
    discount_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    discount_amount: Optional[Decimal] = Field(None, ge=0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None
    approved_by: Optional[str] = None
    is_active: Optional[bool] = None


class DiscountResponse(DiscountBase):
    id: str
    tenant_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DiscountListResponse(BaseModel):
    discounts: List[DiscountResponse]
    total: int
    page: int
    size: int


# Financial Record schemas
class FinancialRecordBase(BaseModel):
    record_type: str = Field(..., min_length=1, max_length=50)
    category: str = Field(..., min_length=1, max_length=100)
    amount: Decimal = Field(..., ge=0)
    currency: str = Field("USD", max_length=3)
    reference_type: Optional[str] = Field(None, max_length=50)
    reference_id: Optional[str] = None
    description: Optional[str] = None
    date: date


class FinancialRecordCreate(FinancialRecordBase):
    tenant_id: str


class FinancialRecordUpdate(BaseModel):
    record_type: Optional[str] = Field(None, min_length=1, max_length=50)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=3)
    reference_type: Optional[str] = Field(None, max_length=50)
    reference_id: Optional[str] = None
    description: Optional[str] = None
    date: Optional[date] = None


class FinancialRecordResponse(FinancialRecordBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FinancialRecordListResponse(BaseModel):
    financial_records: List[FinancialRecordResponse]
    total: int
    page: int
    size: int


# Summary schemas
class FeeSummary(BaseModel):
    total_bills: int
    total_amount: Decimal
    paid_amount: Decimal
    pending_amount: Decimal
    overdue_amount: Decimal
    total_payments: int
    total_discounts: int
    discount_amount: Decimal


class StudentFeeSummary(BaseModel):
    student_id: str
    total_bills: int
    total_amount: Decimal
    paid_amount: Decimal
    pending_amount: Decimal
    overdue_amount: Decimal
    total_payments: int
    total_discounts: int
    discount_amount: Decimal 