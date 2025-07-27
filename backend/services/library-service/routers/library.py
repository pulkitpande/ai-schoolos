"""
Library router for Library Service (AI SchoolOS)
"""

import logging
from typing import List, Optional
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from decimal import Decimal

from database import get_db
from models import Book, BookCopy, BorrowingRecord, Reservation, Category, BookCategory, Fine, LibrarySettings, LibraryAnalytics
from schemas import (
    BookCreate, BookUpdate, BookResponse, BookListResponse,
    BookCopyCreate, BookCopyUpdate, BookCopyResponse, BookCopyListResponse,
    BorrowingRecordCreate, BorrowingRecordUpdate, BorrowingRecordResponse, BorrowingRecordListResponse,
    ReservationCreate, ReservationUpdate, ReservationResponse, ReservationListResponse,
    CategoryCreate, CategoryUpdate, CategoryResponse, CategoryListResponse,
    BookCategoryCreate, BookCategoryResponse, BookCategoryListResponse,
    FineCreate, FineUpdate, FineResponse, FineListResponse,
    LibrarySettingsCreate, LibrarySettingsUpdate, LibrarySettingsResponse,
    LibraryAnalyticsCreate, LibraryAnalyticsUpdate, LibraryAnalyticsResponse, LibraryAnalyticsListResponse,
    LibrarySummary, UserLibrarySummary
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/library", tags=["library"])


@router.get("/status")
async def service_status():
    return {"message": "Library Service is running"}

@router.get("/", response_model=BookListResponse)
async def get_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    author: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of books with filtering and pagination."""
    try:
        query = db.query(Book)
        
        # Apply filters
        if category:
            query = query.filter(Book.category == category)
        
        if author:
            query = query.filter(Book.author.ilike(f"%{author}%"))
        
        # Search functionality
        if search:
            search_filter = or_(
                Book.title.ilike(f"%{search}%"),
                Book.author.ilike(f"%{search}%"),
                Book.description.ilike(f"%{search}%"),
                Book.isbn.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        books = query.offset(skip).limit(limit).all()
        
        return BookListResponse(
            books=books,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting books: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(
    book_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific book by ID."""
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        return book
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/books/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: str,
    book_data: BookUpdate,
    db: Session = Depends(get_db)
):
    """Update a book."""
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        # Update fields
        update_data = book_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(book, field, value)
        
        book.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(book)
        
        logger.info(f"Book updated: {book.title}")
        return book
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/books/{book_id}")
async def delete_book(
    book_id: str,
    db: Session = Depends(get_db)
):
    """Delete a book (soft delete)."""
    try:
        book = db.query(Book).filter(Book.id == book_id).first()
        
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        # Soft delete
        book.status = "inactive"
        book.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Book deleted: {book.title}")
        return {"message": "Book deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Book Copy Operations
@router.post("/books/{book_id}/copies", response_model=BookCopyResponse)
async def create_book_copy(
    book_id: str,
    copy_data: BookCopyCreate,
    db: Session = Depends(get_db)
):
    """Create a new book copy."""
    try:
        # Check if book exists
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        # Create new copy
        copy = BookCopy(**copy_data.dict())
        db.add(copy)
        db.commit()
        db.refresh(copy)
        
        # Update book inventory
        book.total_copies += 1
        book.available_copies += 1
        db.commit()
        
        logger.info(f"New book copy created for book {book_id}")
        return copy
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating book copy: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/books/{book_id}/copies", response_model=BookCopyListResponse)
async def get_book_copies(
    book_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get copies for a specific book."""
    try:
        # Check if book exists
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        query = db.query(BookCopy).filter(BookCopy.book_id == book_id)
        
        # Apply filters
        if status:
            query = query.filter(BookCopy.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        copies = query.offset(skip).limit(limit).all()
        
        return BookCopyListResponse(
            copies=copies,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting book copies: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Borrowing Operations
@router.post("/borrow", response_model=BorrowingRecordResponse)
async def borrow_book(
    borrowing_data: BorrowingRecordCreate,
    db: Session = Depends(get_db)
):
    """Borrow a book copy."""
    try:
        # Check if book copy exists and is available
        book_copy = db.query(BookCopy).filter(BookCopy.id == borrowing_data.book_copy_id).first()
        if not book_copy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book copy not found"
            )
        
        if book_copy.status != "available":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book copy is not available for borrowing"
            )
        
        # Check if user has reached borrowing limit
        settings = db.query(LibrarySettings).filter(LibrarySettings.tenant_id == "default").first()
        if settings:
            current_borrowings = db.query(BorrowingRecord).filter(
                BorrowingRecord.borrower_id == borrowing_data.borrower_id,
                BorrowingRecord.status == "borrowed"
            ).count()
            
            if current_borrowings >= settings.max_books_per_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"User has reached maximum borrowing limit ({settings.max_books_per_user})"
                )
        
        # Create borrowing record
        borrowing = BorrowingRecord(**borrowing_data.dict())
        db.add(borrowing)
        
        # Update book copy status
        book_copy.status = "borrowed"
        
        # Update book inventory
        book = db.query(Book).filter(Book.id == book_copy.book_id).first()
        if book:
            book.available_copies -= 1
        
        db.commit()
        db.refresh(borrowing)
        
        logger.info(f"Book borrowed: {borrowing_data.book_copy_id}")
        return borrowing
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error borrowing book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/return/{borrowing_id}", response_model=BorrowingRecordResponse)
async def return_book(
    borrowing_id: str,
    returned_by: str,
    db: Session = Depends(get_db)
):
    """Return a borrowed book."""
    try:
        # Get borrowing record
        borrowing = db.query(BorrowingRecord).filter(BorrowingRecord.id == borrowing_id).first()
        if not borrowing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Borrowing record not found"
            )
        
        if borrowing.status == "returned":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book has already been returned"
            )
        
        # Update borrowing record
        borrowing.returned_date = datetime.utcnow()
        borrowing.status = "returned"
        borrowing.returned_by = returned_by
        
        # Calculate fines if overdue
        if borrowing.due_date < datetime.utcnow():
            settings = db.query(LibrarySettings).filter(LibrarySettings.tenant_id == "default").first()
            if settings:
                days_overdue = (datetime.utcnow() - borrowing.due_date).days
                fine_amount = min(days_overdue * settings.daily_fine_rate, settings.max_fine_amount)
                borrowing.fine_amount = fine_amount
        
        # Update book copy status
        book_copy = db.query(BookCopy).filter(BookCopy.id == borrowing.book_copy_id).first()
        if book_copy:
            book_copy.status = "available"
        
        # Update book inventory
        book = db.query(Book).filter(Book.id == book_copy.book_id).first()
        if book:
            book.available_copies += 1
        
        db.commit()
        db.refresh(borrowing)
        
        logger.info(f"Book returned: {borrowing_id}")
        return borrowing
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error returning book: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/borrowings", response_model=BorrowingRecordListResponse)
async def get_borrowings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    borrower_id: Optional[str] = None,
    status: Optional[str] = None,
    overdue_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get borrowing records with filtering and pagination."""
    try:
        query = db.query(BorrowingRecord)
        
        # Apply filters
        if borrower_id:
            query = query.filter(BorrowingRecord.borrower_id == borrower_id)
        
        if status:
            query = query.filter(BorrowingRecord.status == status)
        
        if overdue_only:
            query = query.filter(
                and_(
                    BorrowingRecord.status == "borrowed",
                    BorrowingRecord.due_date < datetime.utcnow()
                )
            )
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        borrowings = query.offset(skip).limit(limit).all()
        
        return BorrowingRecordListResponse(
            borrowing_records=borrowings,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting borrowings: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Reservation Operations
@router.post("/reservations", response_model=ReservationResponse)
async def create_reservation(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db)
):
    """Create a new book reservation."""
    try:
        # Check if book exists
        book = db.query(Book).filter(Book.id == reservation_data.book_id).first()
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        
        # Check if user has reached reservation limit
        settings = db.query(LibrarySettings).filter(LibrarySettings.tenant_id == "default").first()
        if settings:
            current_reservations = db.query(Reservation).filter(
                Reservation.user_id == reservation_data.user_id,
                Reservation.status == "active"
            ).count()
            
            if current_reservations >= settings.max_reservations_per_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"User has reached maximum reservation limit ({settings.max_reservations_per_user})"
                )
        
        # Create reservation
        reservation = Reservation(**reservation_data.dict())
        db.add(reservation)
        
        # Update book reserved copies
        book.reserved_copies += 1
        
        db.commit()
        db.refresh(reservation)
        
        logger.info(f"Reservation created for book {reservation_data.book_id}")
        return reservation
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating reservation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/reservations", response_model=ReservationListResponse)
async def get_reservations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: Optional[str] = None,
    book_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get reservations with filtering and pagination."""
    try:
        query = db.query(Reservation)
        
        # Apply filters
        if user_id:
            query = query.filter(Reservation.user_id == user_id)
        
        if book_id:
            query = query.filter(Reservation.book_id == book_id)
        
        if status:
            query = query.filter(Reservation.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        reservations = query.offset(skip).limit(limit).all()
        
        return ReservationListResponse(
            reservations=reservations,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting reservations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Category Operations
@router.post("/categories", response_model=CategoryResponse)
async def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new category."""
    try:
        # Create new category
        category = Category(**category_data.dict())
        db.add(category)
        db.commit()
        db.refresh(category)
        
        logger.info(f"New category created: {category.name}")
        return category
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating category: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/categories", response_model=CategoryListResponse)
async def get_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    parent_id: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get categories with filtering and pagination."""
    try:
        query = db.query(Category)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Category.tenant_id == tenant_id)
        
        if parent_id:
            query = query.filter(Category.parent_id == parent_id)
        
        if is_active is not None:
            query = query.filter(Category.is_active == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        categories = query.offset(skip).limit(limit).all()
        
        return CategoryListResponse(
            categories=categories,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting categories: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Fine Operations
@router.post("/fines", response_model=FineResponse)
async def create_fine(
    fine_data: FineCreate,
    db: Session = Depends(get_db)
):
    """Create a new fine."""
    try:
        # Check if borrowing record exists
        borrowing = db.query(BorrowingRecord).filter(BorrowingRecord.id == fine_data.borrowing_record_id).first()
        if not borrowing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Borrowing record not found"
            )
        
        # Create fine
        fine = Fine(**fine_data.dict())
        db.add(fine)
        db.commit()
        db.refresh(fine)
        
        logger.info(f"New fine created: {fine.reason}")
        return fine
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating fine: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/fines", response_model=FineListResponse)
async def get_fines(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    borrowing_record_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get fines with filtering and pagination."""
    try:
        query = db.query(Fine)
        
        # Apply filters
        if borrowing_record_id:
            query = query.filter(Fine.borrowing_record_id == borrowing_record_id)
        
        if status:
            query = query.filter(Fine.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        fines = query.offset(skip).limit(limit).all()
        
        return FineListResponse(
            fines=fines,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting fines: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Summary Endpoints
@router.get("/summary", response_model=LibrarySummary)
async def get_library_summary(
    tenant_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get library summary statistics."""
    try:
        # Build base queries
        books_query = db.query(Book)
        copies_query = db.query(BookCopy)
        borrowings_query = db.query(BorrowingRecord)
        fines_query = db.query(Fine)
        
        # Apply filters
        if tenant_id:
            books_query = books_query.filter(Book.tenant_id == tenant_id)
        
        # Get book statistics
        total_books = books_query.count()
        total_copies = copies_query.count()
        available_copies = copies_query.filter(BookCopy.status == "available").count()
        borrowed_copies = copies_query.filter(BookCopy.status == "borrowed").count()
        overdue_copies = borrowings_query.filter(
            and_(
                BorrowingRecord.status == "borrowed",
                BorrowingRecord.due_date < datetime.utcnow()
            )
        ).count()
        
        # Get user statistics
        total_borrowers = borrowings_query.with_entities(func.count(func.distinct(BorrowingRecord.borrower_id))).scalar() or 0
        active_borrowers = borrowings_query.filter(
            BorrowingRecord.status == "borrowed"
        ).with_entities(func.count(func.distinct(BorrowingRecord.borrower_id))).scalar() or 0
        
        # Get fine statistics
        total_fines = fines_query.with_entities(func.sum(Fine.amount)).scalar() or Decimal('0.00')
        paid_fines = fines_query.filter(Fine.status == "paid").with_entities(func.sum(Fine.amount)).scalar() or Decimal('0.00')
        pending_fines = fines_query.filter(Fine.status == "pending").with_entities(func.sum(Fine.amount)).scalar() or Decimal('0.00')
        
        return LibrarySummary(
            total_books=total_books,
            total_copies=total_copies,
            available_copies=available_copies,
            borrowed_copies=borrowed_copies,
            overdue_copies=overdue_copies,
            total_borrowers=total_borrowers,
            active_borrowers=active_borrowers,
            total_fines=total_fines,
            paid_fines=paid_fines,
            pending_fines=pending_fines
        )
        
    except Exception as e:
        logger.error(f"Error getting library summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/users/{user_id}/summary", response_model=UserLibrarySummary)
async def get_user_library_summary(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get library summary for a specific user."""
    try:
        # Get borrowing statistics
        total_borrowed = db.query(BorrowingRecord).filter(BorrowingRecord.borrower_id == user_id).count()
        currently_borrowed = db.query(BorrowingRecord).filter(
            and_(
                BorrowingRecord.borrower_id == user_id,
                BorrowingRecord.status == "borrowed"
            )
        ).count()
        overdue_items = db.query(BorrowingRecord).filter(
            and_(
                BorrowingRecord.borrower_id == user_id,
                BorrowingRecord.status == "borrowed",
                BorrowingRecord.due_date < datetime.utcnow()
            )
        ).count()
        
        # Get fine statistics
        total_fines = db.query(Fine).join(BorrowingRecord).filter(
            BorrowingRecord.borrower_id == user_id
        ).with_entities(func.sum(Fine.amount)).scalar() or Decimal('0.00')
        
        paid_fines = db.query(Fine).join(BorrowingRecord).filter(
            and_(
                BorrowingRecord.borrower_id == user_id,
                Fine.status == "paid"
            )
        ).with_entities(func.sum(Fine.amount)).scalar() or Decimal('0.00')
        
        pending_fines = db.query(Fine).join(BorrowingRecord).filter(
            and_(
                BorrowingRecord.borrower_id == user_id,
                Fine.status == "pending"
            )
        ).with_entities(func.sum(Fine.amount)).scalar() or Decimal('0.00')
        
        # Get reservation statistics
        total_reservations = db.query(Reservation).filter(Reservation.user_id == user_id).count()
        active_reservations = db.query(Reservation).filter(
            and_(
                Reservation.user_id == user_id,
                Reservation.status == "active"
            )
        ).count()
        
        # Get user type from first borrowing record
        user_type = db.query(BorrowingRecord.borrower_type).filter(
            BorrowingRecord.borrower_id == user_id
        ).first()
        user_type = user_type[0] if user_type else "unknown"
        
        return UserLibrarySummary(
            user_id=user_id,
            user_type=user_type,
            total_borrowed=total_borrowed,
            currently_borrowed=currently_borrowed,
            overdue_items=overdue_items,
            total_fines=total_fines,
            paid_fines=paid_fines,
            pending_fines=pending_fines,
            total_reservations=total_reservations,
            active_reservations=active_reservations
        )
        
    except Exception as e:
        logger.error(f"Error getting user library summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 