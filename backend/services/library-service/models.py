"""
SQLAlchemy models for Library Service (AI SchoolOS)
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


class Book(Base):
    __tablename__ = "books"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Book Information
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    author: Mapped[str] = mapped_column(String(200), nullable=False)
    isbn: Mapped[str] = mapped_column(String(20), nullable=True)
    publisher: Mapped[str] = mapped_column(String(200), nullable=True)
    publication_year: Mapped[int] = mapped_column(Integer, nullable=True)
    edition: Mapped[str] = mapped_column(String(50), nullable=True)
    language: Mapped[str] = mapped_column(String(50), nullable=False, default="English")
    
    # Book Details
    description: Mapped[str] = mapped_column(Text, nullable=True)
    genre: Mapped[str] = mapped_column(String(100), nullable=True)
    subject: Mapped[str] = mapped_column(String(100), nullable=True)
    reading_level: Mapped[str] = mapped_column(String(50), nullable=True)  # elementary, middle, high, adult
    page_count: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # Physical Details
    format: Mapped[str] = mapped_column(String(50), nullable=False, default="hardcover")  # hardcover, paperback, ebook, audiobook
    location: Mapped[str] = mapped_column(String(100), nullable=True)  # Shelf location
    call_number: Mapped[str] = mapped_column(String(50), nullable=True)
    
    # Inventory
    total_copies: Mapped[int] = mapped_column(Integer, default=1)
    available_copies: Mapped[int] = mapped_column(Integer, default=1)
    reserved_copies: Mapped[int] = mapped_column(Integer, default=0)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, inactive, lost, damaged
    is_reference: Mapped[bool] = mapped_column(Boolean, default=False)
    is_digital: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Additional Information
    cover_image: Mapped[str] = mapped_column(String(500), nullable=True)
    metadata: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_books_tenant_id", "tenant_id"),
        Index("ix_books_title", "title"),
        Index("ix_books_author", "author"),
        Index("ix_books_isbn", "isbn"),
        Index("ix_books_genre", "genre"),
        Index("ix_books_subject", "subject"),
        Index("ix_books_status", "status"),
        Index("ix_books_format", "format"),
    )


class BookCopy(Base):
    __tablename__ = "book_copies"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    book_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    
    # Copy Information
    copy_number: Mapped[int] = mapped_column(Integer, nullable=False)
    barcode: Mapped[str] = mapped_column(String(50), nullable=True)
    condition: Mapped[str] = mapped_column(String(50), default="good")  # new, good, fair, poor, damaged
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="available")  # available, borrowed, reserved, lost, damaged
    location: Mapped[str] = mapped_column(String(100), nullable=True)
    
    # Notes
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_book_copies_book_id", "book_id"),
        Index("ix_book_copies_status", "status"),
        Index("ix_book_copies_barcode", "barcode"),
    )


class BorrowingRecord(Base):
    __tablename__ = "borrowing_records"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    book_copy_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("book_copies.id", ondelete="CASCADE"), nullable=False)
    borrower_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    borrower_type: Mapped[str] = mapped_column(String(20), nullable=False)  # student, teacher, staff, parent
    
    # Borrowing Details
    borrowed_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    returned_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="borrowed")  # borrowed, returned, overdue, lost
    
    # Fines and Fees
    fine_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    fine_paid: Mapped[bool] = mapped_column(Boolean, default=False)
    fine_paid_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Notes
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    returned_by: Mapped[str] = mapped_column(UUIDString, nullable=True)  # Staff who processed return
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_borrowing_records_book_copy_id", "book_copy_id"),
        Index("ix_borrowing_records_borrower_id", "borrower_id"),
        Index("ix_borrowing_records_status", "status"),
        Index("ix_borrowing_records_due_date", "due_date"),
        Index("ix_borrowing_records_borrowed_date", "borrowed_date"),
    )


class Reservation(Base):
    __tablename__ = "reservations"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    book_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    user_type: Mapped[str] = mapped_column(String(20), nullable=False)  # student, teacher, staff, parent
    
    # Reservation Details
    reservation_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expiry_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    pickup_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="active")  # active, fulfilled, expired, cancelled
    
    # Notes
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_reservations_book_id", "book_id"),
        Index("ix_reservations_user_id", "user_id"),
        Index("ix_reservations_status", "status"),
        Index("ix_reservations_expiry_date", "expiry_date"),
    )


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Category Information
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    parent_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_categories_tenant_id", "tenant_id"),
        Index("ix_categories_name", "name"),
        Index("ix_categories_parent_id", "parent_id"),
        Index("ix_categories_is_active", "is_active"),
    )


class BookCategory(Base):
    __tablename__ = "book_categories"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    book_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_book_categories_book_id", "book_id"),
        Index("ix_book_categories_category_id", "category_id"),
    )


class Fine(Base):
    __tablename__ = "fines"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    borrowing_record_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("borrowing_records.id", ondelete="CASCADE"), nullable=False)
    
    # Fine Information
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    reason: Mapped[str] = mapped_column(String(200), nullable=False)  # overdue, damage, lost
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, paid, waived
    paid_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    waived_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    waived_by: Mapped[str] = mapped_column(UUIDString, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_fines_borrowing_record_id", "borrowing_record_id"),
        Index("ix_fines_status", "status"),
        Index("ix_fines_created_at", "created_at"),
    )


class LibrarySettings(Base):
    __tablename__ = "library_settings"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Borrowing Rules
    max_books_per_user: Mapped[int] = mapped_column(Integer, default=5)
    max_borrowing_days: Mapped[int] = mapped_column(Integer, default=14)
    max_renewals: Mapped[int] = mapped_column(Integer, default=2)
    renewal_days: Mapped[int] = mapped_column(Integer, default=7)
    
    # Fine Rules
    daily_fine_rate: Mapped[float] = mapped_column(Numeric(5, 2), default=0.50)
    max_fine_amount: Mapped[float] = mapped_column(Numeric(10, 2), default=10.00)
    grace_period_days: Mapped[int] = mapped_column(Integer, default=3)
    
    # Reservation Rules
    max_reservations_per_user: Mapped[int] = mapped_column(Integer, default=3)
    reservation_expiry_days: Mapped[int] = mapped_column(Integer, default=7)
    
    # Notifications
    send_overdue_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    send_due_reminders: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_library_settings_tenant_id", "tenant_id"),
    )


class LibraryAnalytics(Base):
    __tablename__ = "library_analytics"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Analytics Data
    total_books: Mapped[int] = mapped_column(Integer, default=0)
    total_copies: Mapped[int] = mapped_column(Integer, default=0)
    active_borrowings: Mapped[int] = mapped_column(Integer, default=0)
    overdue_borrowings: Mapped[int] = mapped_column(Integer, default=0)
    total_fines: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    paid_fines: Mapped[float] = mapped_column(Numeric(10, 2), default=0.0)
    
    # Popular Books
    most_borrowed_books: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    popular_categories: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # User Statistics
    active_borrowers: Mapped[int] = mapped_column(Integer, default=0)
    total_borrowers: Mapped[int] = mapped_column(Integer, default=0)
    
    # Time Analytics
    borrowing_trends: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    return_trends: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_library_analytics_tenant_id", "tenant_id"),
        Index("ix_library_analytics_created_at", "created_at"),
    ) 