"""
Homework router for Homework Service (AI SchoolOS)
"""

import logging
from typing import List, Optional
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from decimal import Decimal

from database import get_db
from models import Assignment, AssignmentSubmission, AssignmentGrade, AssignmentComment, AssignmentTemplate, AssignmentAnalytics
from schemas import (
    AssignmentCreate, AssignmentUpdate, AssignmentResponse, AssignmentListResponse,
    AssignmentSubmissionCreate, AssignmentSubmissionUpdate, AssignmentSubmissionResponse, AssignmentSubmissionListResponse,
    AssignmentGradeCreate, AssignmentGradeUpdate, AssignmentGradeResponse, AssignmentGradeListResponse,
    AssignmentCommentCreate, AssignmentCommentUpdate, AssignmentCommentResponse, AssignmentCommentListResponse,
    AssignmentTemplateCreate, AssignmentTemplateUpdate, AssignmentTemplateResponse, AssignmentTemplateListResponse,
    AssignmentAnalyticsCreate, AssignmentAnalyticsUpdate, AssignmentAnalyticsResponse, AssignmentAnalyticsListResponse,
    AssignmentSummary, StudentAssignmentSummary
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/homework", tags=["homework"])


@router.get("/")
async def root():
    return {"message": "Homework Service is running"}


# Assignment CRUD Operations
@router.post("/assignments", response_model=AssignmentResponse)
async def create_assignment(
    assignment_data: AssignmentCreate,
    db: Session = Depends(get_db)
):
    """Create a new assignment."""
    try:
        # Create new assignment
        assignment = Assignment(**assignment_data.dict())
        db.add(assignment)
        db.commit()
        db.refresh(assignment)
        
        logger.info(f"New assignment created: {assignment.title}")
        return assignment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating assignment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/assignments", response_model=AssignmentListResponse)
async def get_assignments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    academic_year: Optional[str] = None,
    class_name: Optional[str] = None,
    section: Optional[str] = None,
    subject: Optional[str] = None,
    teacher_id: Optional[str] = None,
    assignment_type: Optional[str] = None,
    status: Optional[str] = None,
    is_online: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of assignments with filtering and pagination."""
    try:
        query = db.query(Assignment)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Assignment.tenant_id == tenant_id)
        
        if academic_year:
            query = query.filter(Assignment.academic_year == academic_year)
        
        if class_name:
            query = query.filter(Assignment.class_name == class_name)
        
        if section:
            query = query.filter(Assignment.section == section)
        
        if subject:
            query = query.filter(Assignment.subject == subject)
        
        if teacher_id:
            query = query.filter(Assignment.teacher_id == teacher_id)
        
        if assignment_type:
            query = query.filter(Assignment.assignment_type == assignment_type)
        
        if status:
            query = query.filter(Assignment.status == status)
        
        if is_online is not None:
            query = query.filter(Assignment.is_online == is_online)
        
        # Search functionality
        if search:
            search_filter = or_(
                Assignment.title.ilike(f"%{search}%"),
                Assignment.description.ilike(f"%{search}%"),
                Assignment.subject.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        assignments = query.offset(skip).limit(limit).all()
        
        return AssignmentListResponse(
            assignments=assignments,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting assignments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(
    assignment_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific assignment by ID."""
    try:
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        return assignment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting assignment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/assignments/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: str,
    assignment_data: AssignmentUpdate,
    db: Session = Depends(get_db)
):
    """Update an assignment."""
    try:
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        # Update fields
        update_data = assignment_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(assignment, field, value)
        
        assignment.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(assignment)
        
        logger.info(f"Assignment updated: {assignment.title}")
        return assignment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating assignment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/assignments/{assignment_id}")
async def delete_assignment(
    assignment_id: str,
    db: Session = Depends(get_db)
):
    """Delete an assignment (soft delete)."""
    try:
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        # Soft delete
        assignment.status = "archived"
        assignment.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Assignment deleted: {assignment.title}")
        return {"message": "Assignment deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting assignment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Assignment Submission Operations
@router.post("/assignments/{assignment_id}/submissions", response_model=AssignmentSubmissionResponse)
async def create_submission(
    assignment_id: str,
    submission_data: AssignmentSubmissionCreate,
    db: Session = Depends(get_db)
):
    """Create a new assignment submission."""
    try:
        # Check if assignment exists
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        # Check if student has reached max attempts
        existing_submissions = db.query(AssignmentSubmission).filter(
            AssignmentSubmission.assignment_id == assignment_id,
            AssignmentSubmission.student_id == submission_data.student_id
        ).count()
        
        if existing_submissions >= assignment.max_attempts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student has reached maximum attempts ({assignment.max_attempts}) for this assignment"
            )
        
        # Check if submission is late
        is_late = submission_data.submission_date > assignment.submission_deadline
        
        # Create new submission
        submission = AssignmentSubmission(
            **submission_data.dict(),
            is_late=is_late
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)
        
        logger.info(f"New submission created for assignment {assignment_id}")
        return submission
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating submission: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/assignments/{assignment_id}/submissions", response_model=AssignmentSubmissionListResponse)
async def get_assignment_submissions(
    assignment_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    student_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get submissions for a specific assignment."""
    try:
        # Check if assignment exists
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        query = db.query(AssignmentSubmission).filter(AssignmentSubmission.assignment_id == assignment_id)
        
        # Apply filters
        if student_id:
            query = query.filter(AssignmentSubmission.student_id == student_id)
        
        if status:
            query = query.filter(AssignmentSubmission.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        submissions = query.offset(skip).limit(limit).all()
        
        return AssignmentSubmissionListResponse(
            submissions=submissions,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting assignment submissions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Assignment Grade Operations
@router.post("/submissions/{submission_id}/grades", response_model=AssignmentGradeResponse)
async def create_grade(
    submission_id: str,
    grade_data: AssignmentGradeCreate,
    db: Session = Depends(get_db)
):
    """Create a new grade for an assignment submission."""
    try:
        # Check if submission exists
        submission = db.query(AssignmentSubmission).filter(AssignmentSubmission.id == submission_id).first()
        if not submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment submission not found"
            )
        
        # Create new grade
        grade = AssignmentGrade(**grade_data.dict())
        db.add(grade)
        db.commit()
        db.refresh(grade)
        
        logger.info(f"New grade created for submission {submission_id}")
        return grade
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating grade: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/submissions/{submission_id}/grades", response_model=AssignmentGradeListResponse)
async def get_submission_grades(
    submission_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get grades for a specific assignment submission."""
    try:
        # Check if submission exists
        submission = db.query(AssignmentSubmission).filter(AssignmentSubmission.id == submission_id).first()
        if not submission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment submission not found"
            )
        
        query = db.query(AssignmentGrade).filter(AssignmentGrade.submission_id == submission_id)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        grades = query.offset(skip).limit(limit).all()
        
        return AssignmentGradeListResponse(
            grades=grades,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting submission grades: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Assignment Comment Operations
@router.post("/assignments/{assignment_id}/comments", response_model=AssignmentCommentResponse)
async def create_comment(
    assignment_id: str,
    comment_data: AssignmentCommentCreate,
    db: Session = Depends(get_db)
):
    """Create a new comment for an assignment."""
    try:
        # Check if assignment exists
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        # Create new comment
        comment = AssignmentComment(**comment_data.dict())
        db.add(comment)
        db.commit()
        db.refresh(comment)
        
        logger.info(f"New comment created for assignment {assignment_id}")
        return comment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating comment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/assignments/{assignment_id}/comments", response_model=AssignmentCommentListResponse)
async def get_assignment_comments(
    assignment_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    comment_type: Optional[str] = None,
    user_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get comments for a specific assignment."""
    try:
        # Check if assignment exists
        assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        query = db.query(AssignmentComment).filter(AssignmentComment.assignment_id == assignment_id)
        
        # Apply filters
        if comment_type:
            query = query.filter(AssignmentComment.comment_type == comment_type)
        
        if user_type:
            query = query.filter(AssignmentComment.user_type == user_type)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        comments = query.offset(skip).limit(limit).all()
        
        return AssignmentCommentListResponse(
            comments=comments,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting assignment comments: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Assignment Template Operations
@router.post("/templates", response_model=AssignmentTemplateResponse)
async def create_template(
    template_data: AssignmentTemplateCreate,
    db: Session = Depends(get_db)
):
    """Create a new assignment template."""
    try:
        # Create new template
        template = AssignmentTemplate(**template_data.dict())
        db.add(template)
        db.commit()
        db.refresh(template)
        
        logger.info(f"New assignment template created: {template.name}")
        return template
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating template: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/templates", response_model=AssignmentTemplateListResponse)
async def get_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    template_type: Optional[str] = None,
    subject: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_public: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get assignment templates with filtering and pagination."""
    try:
        query = db.query(AssignmentTemplate)
        
        # Apply filters
        if tenant_id:
            query = query.filter(AssignmentTemplate.tenant_id == tenant_id)
        
        if template_type:
            query = query.filter(AssignmentTemplate.template_type == template_type)
        
        if subject:
            query = query.filter(AssignmentTemplate.subject == subject)
        
        if is_active is not None:
            query = query.filter(AssignmentTemplate.is_active == is_active)
        
        if is_public is not None:
            query = query.filter(AssignmentTemplate.is_public == is_public)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        templates = query.offset(skip).limit(limit).all()
        
        return AssignmentTemplateListResponse(
            templates=templates,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting templates: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Assignment Analytics Operations
@router.post("/analytics", response_model=AssignmentAnalyticsResponse)
async def create_analytics(
    analytics_data: AssignmentAnalyticsCreate,
    db: Session = Depends(get_db)
):
    """Create new assignment analytics."""
    try:
        # Check if assignment exists
        assignment = db.query(Assignment).filter(Assignment.id == analytics_data.assignment_id).first()
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found"
            )
        
        # Create new analytics
        analytics = AssignmentAnalytics(**analytics_data.dict())
        db.add(analytics)
        db.commit()
        db.refresh(analytics)
        
        logger.info(f"New analytics created for assignment {analytics_data.assignment_id}")
        return analytics
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating analytics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/analytics", response_model=AssignmentAnalyticsListResponse)
async def get_analytics(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    assignment_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get assignment analytics with filtering and pagination."""
    try:
        query = db.query(AssignmentAnalytics)
        
        # Apply filters
        if assignment_id:
            query = query.filter(AssignmentAnalytics.assignment_id == assignment_id)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        analytics = query.offset(skip).limit(limit).all()
        
        return AssignmentAnalyticsListResponse(
            analytics=analytics,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting analytics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Summary Endpoints
@router.get("/summary", response_model=AssignmentSummary)
async def get_assignment_summary(
    tenant_id: Optional[str] = None,
    academic_year: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get assignment summary statistics."""
    try:
        # Build base queries
        assignments_query = db.query(Assignment)
        submissions_query = db.query(AssignmentSubmission)
        
        # Apply filters
        if tenant_id:
            assignments_query = assignments_query.filter(Assignment.tenant_id == tenant_id)
        
        if academic_year:
            assignments_query = assignments_query.filter(Assignment.academic_year == academic_year)
        
        # Get assignment statistics
        total_assignments = assignments_query.count()
        active_assignments = assignments_query.filter(Assignment.status == "active").count()
        completed_assignments = assignments_query.filter(Assignment.status == "completed").count()
        
        # Get submission statistics
        total_submissions = submissions_query.count()
        graded_submissions = submissions_query.filter(AssignmentSubmission.status == "graded").count()
        
        # Calculate averages
        avg_submission_rate = (total_submissions / max(total_assignments, 1)) * 100 if total_assignments > 0 else Decimal('0.00')
        avg_grade = submissions_query.with_entities(func.avg(AssignmentSubmission.percentage)).scalar() or Decimal('0.00')
        
        return AssignmentSummary(
            total_assignments=total_assignments,
            active_assignments=active_assignments,
            completed_assignments=completed_assignments,
            total_submissions=total_submissions,
            graded_submissions=graded_submissions,
            average_submission_rate=Decimal(str(avg_submission_rate)),
            average_grade=avg_grade
        )
        
    except Exception as e:
        logger.error(f"Error getting assignment summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/students/{student_id}/summary", response_model=StudentAssignmentSummary)
async def get_student_assignment_summary(
    student_id: str,
    db: Session = Depends(get_db)
):
    """Get assignment summary for a specific student."""
    try:
        # Get assignment statistics for student
        assignments_query = db.query(Assignment)
        submissions_query = db.query(AssignmentSubmission).filter(AssignmentSubmission.student_id == student_id)
        
        total_assignments = assignments_query.count()
        submitted_assignments = submissions_query.count()
        graded_assignments = submissions_query.filter(AssignmentSubmission.status == "graded").count()
        late_submissions = submissions_query.filter(AssignmentSubmission.is_late == True).count()
        
        # Calculate averages
        avg_grade = submissions_query.with_entities(func.avg(AssignmentSubmission.percentage)).scalar() or Decimal('0.00')
        
        # Calculate total marks
        total_marks = submissions_query.with_entities(func.sum(AssignmentSubmission.marks_awarded)).scalar() or Decimal('0.00')
        obtained_marks = submissions_query.with_entities(func.sum(AssignmentSubmission.marks_awarded)).scalar() or Decimal('0.00')
        
        return StudentAssignmentSummary(
            student_id=student_id,
            total_assignments=total_assignments,
            submitted_assignments=submitted_assignments,
            graded_assignments=graded_assignments,
            average_grade=avg_grade,
            total_marks=total_marks,
            obtained_marks=obtained_marks,
            late_submissions=late_submissions
        )
        
    except Exception as e:
        logger.error(f"Error getting student assignment summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 