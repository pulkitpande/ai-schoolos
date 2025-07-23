"""
SQLAlchemy models for Fee Service (AI SchoolOS)
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


class FeeStructure(Base):
    __tablename__ = "fee_structures"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Fee Structure Information
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Academic Details
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    class_name: Mapped[str] = mapped_column(String(50), nullable=True)  # NULL for all classes
    section: Mapped[str] = mapped_column(String(10), nullable=True)  # NULL for all sections
    
    # Fee Components
    tuition_fee: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    library_fee: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    laboratory_fee: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    sports_fee: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    transport_fee: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    hostel_fee: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    other_fees: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Payment Schedule
    payment_schedule: Mapped[str] = mapped_column(String(20), default="monthly")  # monthly, quarterly, yearly
    due_date: Mapped[Integer] = mapped_column(Integer, default=5)  # Day of month for payment
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_fee_structures_tenant_id", "tenant_id"),
        Index("ix_fee_structures_code", "code"),
        Index("ix_fee_structures_academic_year", "academic_year"),
        Index("ix_fee_structures_class_section", "class_name", "section"),
    )


class StudentFee(Base):
    __tablename__ = "student_fees"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    student_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    fee_structure_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("fee_structures.id"), nullable=False)
    
    # Fee Assignment
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    class_name: Mapped[str] = mapped_column(String(50), nullable=False)
    section: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # Fee Amounts
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    discount_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    scholarship_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    final_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_student_fees_tenant_id", "tenant_id"),
        Index("ix_student_fees_student_id", "student_id"),
        Index("ix_student_fees_fee_structure_id", "fee_structure_id"),
        Index("ix_student_fees_academic_year", "academic_year"),
    )


class Bill(Base):
    __tablename__ = "bills"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    student_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    student_fee_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("student_fees.id"), nullable=False)
    
    # Bill Information
    bill_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    bill_date: Mapped[Date] = mapped_column(Date, nullable=False)
    due_date: Mapped[Date] = mapped_column(Date, nullable=False)
    
    # Amount Details
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    paid_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    balance_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    # Bill Details
    bill_type: Mapped[str] = mapped_column(String(20), nullable=False)  # monthly, quarterly, yearly, one-time
    period: Mapped[str] = mapped_column(String(20), nullable=False)  # Jan-2024, Q1-2024, 2024, etc.
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, partial, paid, overdue
    
    # Additional Information
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_bills_tenant_id", "tenant_id"),
        Index("ix_bills_student_id", "student_id"),
        Index("ix_bills_student_fee_id", "student_fee_id"),
        Index("ix_bills_bill_number", "bill_number"),
        Index("ix_bills_status", "status"),
        Index("ix_bills_due_date", "due_date"),
    )


class Payment(Base):
    __tablename__ = "payments"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    student_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    bill_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("bills.id"), nullable=False)
    
    # Payment Information
    payment_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    payment_date: Mapped[Date] = mapped_column(Date, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    # Payment Method
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)  # cash, card, bank_transfer, online
    payment_gateway: Mapped[str] = mapped_column(String(50), nullable=True)  # stripe, paypal, etc.
    transaction_id: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Payment Status
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, completed, failed, refunded
    
    # Additional Information
    receipt_number: Mapped[str] = mapped_column(String(50), nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_payments_tenant_id", "tenant_id"),
        Index("ix_payments_student_id", "student_id"),
        Index("ix_payments_bill_id", "bill_id"),
        Index("ix_payments_payment_number", "payment_number"),
        Index("ix_payments_status", "status"),
        Index("ix_payments_transaction_id", "transaction_id"),
    )


class Discount(Base):
    __tablename__ = "discounts"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    student_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Discount Information
    discount_type: Mapped[str] = mapped_column(String(50), nullable=False)  # sibling, merit, need_based, etc.
    discount_percentage: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    discount_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    # Validity
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Additional Information
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    approved_by: Mapped[str] = mapped_column(UUIDString, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_discounts_tenant_id", "tenant_id"),
        Index("ix_discounts_student_id", "student_id"),
        Index("ix_discounts_discount_type", "discount_type"),
        Index("ix_discounts_dates", "start_date", "end_date"),
    )


class FinancialRecord(Base):
    __tablename__ = "financial_records"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Record Information
    record_type: Mapped[str] = mapped_column(String(50), nullable=False)  # income, expense, refund
    category: Mapped[str] = mapped_column(String(100), nullable=False)  # tuition, transport, library, etc.
    
    # Amount Details
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    
    # Reference Information
    reference_type: Mapped[str] = mapped_column(String(50), nullable=True)  # payment, bill, discount
    reference_id: Mapped[str] = mapped_column(UUIDString, nullable=True)
    
    # Record Details
    description: Mapped[str] = mapped_column(Text, nullable=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_financial_records_tenant_id", "tenant_id"),
        Index("ix_financial_records_record_type", "record_type"),
        Index("ix_financial_records_category", "category"),
        Index("ix_financial_records_date", "date"),
        Index("ix_financial_records_reference", "reference_type", "reference_id"),
    ) 