"""
Pydantic schemas for Library Service (AI SchoolOS)
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from decimal import Decimal


# Book schemas
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    author: str = Field(..., min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, max_length=20)
    publisher: Optional[str] = Field(None, max_length=200)
    publication_year: Optional[int] = Field(None, ge=1800, le=2100)
    edition: Optional[str] = Field(None, max_length=50)
    language: str = Field("English", max_length=50)
    description: Optional[str] = None
    genre: Optional[str] = Field(None, max_length=100)
    subject: Optional[str] = Field(None, max_length=100)
    reading_level: Optional[str] = Field(None, max_length=50)
    page_count: Optional[int] = Field(None, ge=1)
    format: str = Field("hardcover", max_length=50)
    location: Optional[str] = Field(None, max_length=100)
    call_number: Optional[str] = Field(None, max_length=50)
    total_copies: int = Field(1, ge=1)
    available_copies: int = Field(1, ge=0)
    reserved_copies: int = Field(0, ge=0)
    is_reference: bool = False
    is_digital: bool = False
    cover_image: Optional[str] = Field(None, max_length=500)
    metadata: Optional[Dict[str, Any]] = {}


class BookCreate(BookBase):
    tenant_id: str


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    author: Optional[str] = Field(None, min_length=1, max_length=200)
    isbn: Optional[str] = Field(None, max_length=20)
    publisher: Optional[str] = Field(None, max_length=200)
    publication_year: Optional[int] = Field(None, ge=1800, le=2100)
    edition: Optional[str] = Field(None, max_length=50)
    language: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    genre: Optional[str] = Field(None, max_length=100)
    subject: Optional[str] = Field(None, max_length=100)
    reading_level: Optional[str] = Field(None, max_length=50)
    page_count: Optional[int] = Field(None, ge=1)
    format: Optional[str] = Field(None, max_length=50)
    location: Optional[str] = Field(None, max_length=100)
    call_number: Optional[str] = Field(None, max_length=50)
    total_copies: Optional[int] = Field(None, ge=1)
    available_copies: Optional[int] = Field(None, ge=0)
    reserved_copies: Optional[int] = Field(None, ge=0)
    status: Optional[str] = Field(None, max_length=20)
    is_reference: Optional[bool] = None
    is_digital: Optional[bool] = None
    cover_image: Optional[str] = Field(None, max_length=500)
    metadata: Optional[Dict[str, Any]] = None


class BookResponse(BookBase):
    id: str
    tenant_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookListResponse(BaseModel):
    books: List[BookResponse]
    total: int
    page: int
    size: int


# Book Copy schemas
class BookCopyBase(BaseModel):
    book_id: str
    copy_number: int = Field(..., ge=1)
    barcode: Optional[str] = Field(None, max_length=50)
    condition: str = Field("good", max_length=50)
    location: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class BookCopyCreate(BookCopyBase):
    pass


class BookCopyUpdate(BaseModel):
    copy_number: Optional[int] = Field(None, ge=1)
    barcode: Optional[str] = Field(None, max_length=50)
    condition: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = Field(None, max_length=20)
    location: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None


class BookCopyResponse(BookCopyBase):
    id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookCopyListResponse(BaseModel):
    copies: List[BookCopyResponse]
    total: int
    page: int
    size: int


# Borrowing Record schemas
class BorrowingRecordBase(BaseModel):
    book_copy_id: str
    borrower_id: str
    borrower_type: str = Field(..., max_length=20)
    borrowed_date: datetime
    due_date: datetime
    notes: Optional[str] = None


class BorrowingRecordCreate(BorrowingRecordBase):
    pass


class BorrowingRecordUpdate(BaseModel):
    returned_date: Optional[datetime] = None
    status: Optional[str] = Field(None, max_length=20)
    fine_amount: Optional[Decimal] = Field(None, ge=0)
    fine_paid: Optional[bool] = None
    fine_paid_date: Optional[datetime] = None
    notes: Optional[str] = None
    returned_by: Optional[str] = None


class BorrowingRecordResponse(BorrowingRecordBase):
    id: str
    returned_date: Optional[datetime] = None
    status: str
    fine_amount: Decimal
    fine_paid: bool
    fine_paid_date: Optional[datetime] = None
    returned_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BorrowingRecordListResponse(BaseModel):
    borrowing_records: List[BorrowingRecordResponse]
    total: int
    page: int
    size: int


# Reservation schemas
class ReservationBase(BaseModel):
    book_id: str
    user_id: str
    user_type: str = Field(..., max_length=20)
    reservation_date: datetime
    expiry_date: datetime
    notes: Optional[str] = None


class ReservationCreate(ReservationBase):
    pass


class ReservationUpdate(BaseModel):
    pickup_date: Optional[datetime] = None
    status: Optional[str] = Field(None, max_length=20)
    notes: Optional[str] = None


class ReservationResponse(ReservationBase):
    id: str
    pickup_date: Optional[datetime] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReservationListResponse(BaseModel):
    reservations: List[ReservationResponse]
    total: int
    page: int
    size: int


# Category schemas
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[str] = None
    is_active: bool = True


class CategoryCreate(CategoryBase):
    tenant_id: str


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryResponse(CategoryBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryListResponse(BaseModel):
    categories: List[CategoryResponse]
    total: int
    page: int
    size: int


# Book Category schemas
class BookCategoryBase(BaseModel):
    book_id: str
    category_id: str


class BookCategoryCreate(BookCategoryBase):
    pass


class BookCategoryResponse(BookCategoryBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class BookCategoryListResponse(BaseModel):
    book_categories: List[BookCategoryResponse]
    total: int
    page: int
    size: int


# Fine schemas
class FineBase(BaseModel):
    borrowing_record_id: str
    amount: Decimal = Field(..., ge=0)
    reason: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None


class FineCreate(FineBase):
    pass


class FineUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, ge=0)
    reason: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(None, max_length=20)
    paid_date: Optional[datetime] = None
    waived_date: Optional[datetime] = None
    waived_by: Optional[str] = None


class FineResponse(FineBase):
    id: str
    status: str
    paid_date: Optional[datetime] = None
    waived_date: Optional[datetime] = None
    waived_by: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FineListResponse(BaseModel):
    fines: List[FineResponse]
    total: int
    page: int
    size: int


# Library Settings schemas
class LibrarySettingsBase(BaseModel):
    max_books_per_user: int = Field(5, ge=1)
    max_borrowing_days: int = Field(14, ge=1)
    max_renewals: int = Field(2, ge=0)
    renewal_days: int = Field(7, ge=1)
    daily_fine_rate: Decimal = Field(0.50, ge=0)
    max_fine_amount: Decimal = Field(10.00, ge=0)
    grace_period_days: int = Field(3, ge=0)
    max_reservations_per_user: int = Field(3, ge=1)
    reservation_expiry_days: int = Field(7, ge=1)
    send_overdue_notifications: bool = True
    send_due_reminders: bool = True


class LibrarySettingsCreate(LibrarySettingsBase):
    tenant_id: str


class LibrarySettingsUpdate(BaseModel):
    max_books_per_user: Optional[int] = Field(None, ge=1)
    max_borrowing_days: Optional[int] = Field(None, ge=1)
    max_renewals: Optional[int] = Field(None, ge=0)
    renewal_days: Optional[int] = Field(None, ge=1)
    daily_fine_rate: Optional[Decimal] = Field(None, ge=0)
    max_fine_amount: Optional[Decimal] = Field(None, ge=0)
    grace_period_days: Optional[int] = Field(None, ge=0)
    max_reservations_per_user: Optional[int] = Field(None, ge=1)
    reservation_expiry_days: Optional[int] = Field(None, ge=1)
    send_overdue_notifications: Optional[bool] = None
    send_due_reminders: Optional[bool] = None


class LibrarySettingsResponse(LibrarySettingsBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Library Analytics schemas
class LibraryAnalyticsBase(BaseModel):
    tenant_id: str
    total_books: int = Field(0, ge=0)
    total_copies: int = Field(0, ge=0)
    active_borrowings: int = Field(0, ge=0)
    overdue_borrowings: int = Field(0, ge=0)
    total_fines: Decimal = Field(0.0, ge=0)
    paid_fines: Decimal = Field(0.0, ge=0)
    most_borrowed_books: Optional[Dict[str, Any]] = {}
    popular_categories: Optional[Dict[str, Any]] = {}
    active_borrowers: int = Field(0, ge=0)
    total_borrowers: int = Field(0, ge=0)
    borrowing_trends: Optional[Dict[str, Any]] = {}
    return_trends: Optional[Dict[str, Any]] = {}


class LibraryAnalyticsCreate(LibraryAnalyticsBase):
    pass


class LibraryAnalyticsUpdate(BaseModel):
    total_books: Optional[int] = Field(None, ge=0)
    total_copies: Optional[int] = Field(None, ge=0)
    active_borrowings: Optional[int] = Field(None, ge=0)
    overdue_borrowings: Optional[int] = Field(None, ge=0)
    total_fines: Optional[Decimal] = Field(None, ge=0)
    paid_fines: Optional[Decimal] = Field(None, ge=0)
    most_borrowed_books: Optional[Dict[str, Any]] = None
    popular_categories: Optional[Dict[str, Any]] = None
    active_borrowers: Optional[int] = Field(None, ge=0)
    total_borrowers: Optional[int] = Field(None, ge=0)
    borrowing_trends: Optional[Dict[str, Any]] = None
    return_trends: Optional[Dict[str, Any]] = None


class LibraryAnalyticsResponse(LibraryAnalyticsBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LibraryAnalyticsListResponse(BaseModel):
    analytics: List[LibraryAnalyticsResponse]
    total: int
    page: int
    size: int


# Summary schemas
class LibrarySummary(BaseModel):
    total_books: int
    total_copies: int
    available_copies: int
    borrowed_copies: int
    overdue_copies: int
    total_borrowers: int
    active_borrowers: int
    total_fines: Decimal
    paid_fines: Decimal
    pending_fines: Decimal


class UserLibrarySummary(BaseModel):
    user_id: str
    user_type: str
    total_borrowed: int
    currently_borrowed: int
    overdue_items: int
    total_fines: Decimal
    paid_fines: Decimal
    pending_fines: Decimal
    total_reservations: int
    active_reservations: int 