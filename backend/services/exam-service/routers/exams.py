"""
Exams router for Exam Service (AI SchoolOS)
"""

import logging
from typing import List, Optional
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from decimal import Decimal

from database import get_db
from models import Exam, Question, ExamAttempt, Answer, ExamResult, ExamSchedule
from schemas import (
    ExamCreate, ExamUpdate, ExamResponse, ExamListResponse,
    QuestionCreate, QuestionUpdate, QuestionResponse, QuestionListResponse,
    ExamAttemptCreate, ExamAttemptUpdate, ExamAttemptResponse, ExamAttemptListResponse,
    AnswerCreate, AnswerUpdate, AnswerResponse, AnswerListResponse,
    ExamResultCreate, ExamResultUpdate, ExamResultResponse, ExamResultListResponse,
    ExamScheduleCreate, ExamScheduleUpdate, ExamScheduleResponse, ExamScheduleListResponse,
    ExamSummary, StudentExamSummary
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/exams", tags=["exams"])


# Exam CRUD Operations
@router.post("/", response_model=ExamResponse)
async def create_exam(
    exam_data: ExamCreate,
    db: Session = Depends(get_db)
):
    """Create a new exam."""
    try:
        # Create new exam
        exam = Exam(**exam_data.dict())
        db.add(exam)
        db.commit()
        db.refresh(exam)
        
        logger.info(f"New exam created: {exam.title}")
        return exam
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating exam: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/", response_model=ExamListResponse)
async def get_exams(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    academic_year: Optional[str] = None,
    class_name: Optional[str] = None,
    section: Optional[str] = None,
    subject: Optional[str] = None,
    exam_type: Optional[str] = None,
    status: Optional[str] = None,
    is_online: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of exams with filtering and pagination."""
    try:
        query = db.query(Exam)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Exam.tenant_id == tenant_id)
        
        if academic_year:
            query = query.filter(Exam.academic_year == academic_year)
        
        if class_name:
            query = query.filter(Exam.class_name == class_name)
        
        if section:
            query = query.filter(Exam.section == section)
        
        if subject:
            query = query.filter(Exam.subject == subject)
        
        if exam_type:
            query = query.filter(Exam.exam_type == exam_type)
        
        if status:
            query = query.filter(Exam.status == status)
        
        if is_online is not None:
            query = query.filter(Exam.is_online == is_online)
        
        # Search functionality
        if search:
            search_filter = or_(
                Exam.title.ilike(f"%{search}%"),
                Exam.description.ilike(f"%{search}%"),
                Exam.subject.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        exams = query.offset(skip).limit(limit).all()
        
        return ExamListResponse(
            exams=exams,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting exams: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{exam_id}", response_model=ExamResponse)
async def get_exam(
    exam_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific exam by ID."""
    try:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam not found"
            )
        
        return exam
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting exam: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/{exam_id}", response_model=ExamResponse)
async def update_exam(
    exam_id: str,
    exam_data: ExamUpdate,
    db: Session = Depends(get_db)
):
    """Update an exam."""
    try:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam not found"
            )
        
        # Update fields
        update_data = exam_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(exam, field, value)
        
        exam.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(exam)
        
        logger.info(f"Exam updated: {exam.title}")
        return exam
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating exam: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.delete("/{exam_id}")
async def delete_exam(
    exam_id: str,
    db: Session = Depends(get_db)
):
    """Delete an exam (soft delete)."""
    try:
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam not found"
            )
        
        # Soft delete
        exam.status = "archived"
        exam.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Exam deleted: {exam.title}")
        return {"message": "Exam deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting exam: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Question Operations
@router.post("/{exam_id}/questions", response_model=QuestionResponse)
async def create_question(
    exam_id: str,
    question_data: QuestionCreate,
    db: Session = Depends(get_db)
):
    """Create a new question for an exam."""
    try:
        # Check if exam exists
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam not found"
            )
        
        # Create new question
        question = Question(**question_data.dict())
        db.add(question)
        db.commit()
        db.refresh(question)
        
        logger.info(f"New question created for exam {exam_id}")
        return question
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating question: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{exam_id}/questions", response_model=QuestionListResponse)
async def get_exam_questions(
    exam_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    question_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get questions for a specific exam."""
    try:
        # Check if exam exists
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam not found"
            )
        
        query = db.query(Question).filter(Question.exam_id == exam_id)
        
        # Apply filters
        if question_type:
            query = query.filter(Question.question_type == question_type)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        questions = query.order_by(Question.order_number).offset(skip).limit(limit).all()
        
        return QuestionListResponse(
            questions=questions,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting exam questions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Exam Attempt Operations
@router.post("/{exam_id}/attempts", response_model=ExamAttemptResponse)
async def create_exam_attempt(
    exam_id: str,
    attempt_data: ExamAttemptCreate,
    db: Session = Depends(get_db)
):
    """Create a new exam attempt."""
    try:
        # Check if exam exists
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam not found"
            )
        
        # Check if student has reached max attempts
        existing_attempts = db.query(ExamAttempt).filter(
            ExamAttempt.exam_id == exam_id,
            ExamAttempt.student_id == attempt_data.student_id
        ).count()
        
        if existing_attempts >= exam.max_attempts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student has reached maximum attempts ({exam.max_attempts}) for this exam"
            )
        
        # Create new attempt
        attempt = ExamAttempt(**attempt_data.dict())
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        
        logger.info(f"New exam attempt created for student {attempt_data.student_id}")
        return attempt
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating exam attempt: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/{exam_id}/attempts", response_model=ExamAttemptListResponse)
async def get_exam_attempts(
    exam_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    student_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get attempts for a specific exam."""
    try:
        # Check if exam exists
        exam = db.query(Exam).filter(Exam.id == exam_id).first()
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam not found"
            )
        
        query = db.query(ExamAttempt).filter(ExamAttempt.exam_id == exam_id)
        
        # Apply filters
        if student_id:
            query = query.filter(ExamAttempt.student_id == student_id)
        
        if status:
            query = query.filter(ExamAttempt.status == status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        attempts = query.offset(skip).limit(limit).all()
        
        return ExamAttemptListResponse(
            exam_attempts=attempts,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting exam attempts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Answer Operations
@router.post("/attempts/{attempt_id}/answers", response_model=AnswerResponse)
async def create_answer(
    attempt_id: str,
    answer_data: AnswerCreate,
    db: Session = Depends(get_db)
):
    """Create a new answer for an exam attempt."""
    try:
        # Check if attempt exists
        attempt = db.query(ExamAttempt).filter(ExamAttempt.id == attempt_id).first()
        if not attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam attempt not found"
            )
        
        # Check if answer already exists for this question
        existing_answer = db.query(Answer).filter(
            Answer.exam_attempt_id == attempt_id,
            Answer.question_id == answer_data.question_id
        ).first()
        
        if existing_answer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Answer already exists for this question"
            )
        
        # Create new answer
        answer = Answer(**answer_data.dict())
        db.add(answer)
        db.commit()
        db.refresh(answer)
        
        logger.info(f"New answer created for attempt {attempt_id}")
        return answer
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating answer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/attempts/{attempt_id}/answers", response_model=AnswerListResponse)
async def get_attempt_answers(
    attempt_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get answers for a specific exam attempt."""
    try:
        # Check if attempt exists
        attempt = db.query(ExamAttempt).filter(ExamAttempt.id == attempt_id).first()
        if not attempt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam attempt not found"
            )
        
        query = db.query(Answer).filter(Answer.exam_attempt_id == attempt_id)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        answers = query.offset(skip).limit(limit).all()
        
        return AnswerListResponse(
            answers=answers,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting attempt answers: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Exam Result Operations
@router.post("/results", response_model=ExamResultResponse)
async def create_exam_result(
    result_data: ExamResultCreate,
    db: Session = Depends(get_db)
):
    """Create a new exam result."""
    try:
        # Check if exam exists
        exam = db.query(Exam).filter(Exam.id == result_data.exam_id).first()
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam not found"
            )
        
        # Check if result already exists
        existing_result = db.query(ExamResult).filter(
            ExamResult.exam_id == result_data.exam_id,
            ExamResult.student_id == result_data.student_id
        ).first()
        
        if existing_result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Exam result already exists for this student"
            )
        
        # Create new result
        result = ExamResult(**result_data.dict())
        db.add(result)
        db.commit()
        db.refresh(result)
        
        logger.info(f"New exam result created for student {result_data.student_id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating exam result: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/results", response_model=ExamResultListResponse)
async def get_exam_results(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    exam_id: Optional[str] = None,
    student_id: Optional[str] = None,
    is_passed: Optional[bool] = None,
    is_published: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get exam results with filtering and pagination."""
    try:
        query = db.query(ExamResult)
        
        # Apply filters
        if exam_id:
            query = query.filter(ExamResult.exam_id == exam_id)
        
        if student_id:
            query = query.filter(ExamResult.student_id == student_id)
        
        if is_passed is not None:
            query = query.filter(ExamResult.is_passed == is_passed)
        
        if is_published is not None:
            query = query.filter(ExamResult.is_published == is_published)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        results = query.offset(skip).limit(limit).all()
        
        return ExamResultListResponse(
            exam_results=results,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting exam results: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Exam Schedule Operations
@router.post("/schedules", response_model=ExamScheduleResponse)
async def create_exam_schedule(
    schedule_data: ExamScheduleCreate,
    db: Session = Depends(get_db)
):
    """Create a new exam schedule."""
    try:
        # Create new schedule
        schedule = ExamSchedule(**schedule_data.dict())
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        
        logger.info(f"New exam schedule created: {schedule.title}")
        return schedule
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating exam schedule: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/schedules", response_model=ExamScheduleListResponse)
async def get_exam_schedules(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    academic_year: Optional[str] = None,
    schedule_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get exam schedules with filtering and pagination."""
    try:
        query = db.query(ExamSchedule)
        
        # Apply filters
        if tenant_id:
            query = query.filter(ExamSchedule.tenant_id == tenant_id)
        
        if academic_year:
            query = query.filter(ExamSchedule.academic_year == academic_year)
        
        if schedule_type:
            query = query.filter(ExamSchedule.schedule_type == schedule_type)
        
        if is_active is not None:
            query = query.filter(ExamSchedule.is_active == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        schedules = query.offset(skip).limit(limit).all()
        
        return ExamScheduleListResponse(
            exam_schedules=schedules,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting exam schedules: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Summary Endpoints
@router.get("/summary", response_model=ExamSummary)
async def get_exam_summary(
    tenant_id: Optional[str] = None,
    academic_year: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get exam summary statistics."""
    try:
        # Build base queries
        exams_query = db.query(Exam)
        attempts_query = db.query(ExamAttempt)
        results_query = db.query(ExamResult)
        
        # Apply filters
        if tenant_id:
            exams_query = exams_query.filter(Exam.tenant_id == tenant_id)
        
        if academic_year:
            exams_query = exams_query.filter(Exam.academic_year == academic_year)
        
        # Get exam statistics
        total_exams = exams_query.count()
        active_exams = exams_query.filter(Exam.status == "active").count()
        completed_exams = exams_query.filter(Exam.status == "completed").count()
        
        # Get attempt statistics
        total_attempts = attempts_query.count()
        
        # Get result statistics
        total_results = results_query.count()
        
        # Calculate averages
        avg_percentage = results_query.with_entities(func.avg(ExamResult.percentage)).scalar() or Decimal('0.00')
        pass_rate = results_query.filter(ExamResult.is_passed == True).count() / max(total_results, 1) * 100
        
        return ExamSummary(
            total_exams=total_exams,
            active_exams=active_exams,
            completed_exams=completed_exams,
            total_attempts=total_attempts,
            total_results=total_results,
            average_percentage=avg_percentage,
            pass_rate=Decimal(str(pass_rate))
        )
        
    except Exception as e:
        logger.error(f"Error getting exam summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/students/{student_id}/summary", response_model=StudentExamSummary)
async def get_student_exam_summary(
    student_id: str,
    db: Session = Depends(get_db)
):
    """Get exam summary for a specific student."""
    try:
        # Get exam statistics for student
        exams_query = db.query(Exam)
        attempts_query = db.query(ExamAttempt).filter(ExamAttempt.student_id == student_id)
        results_query = db.query(ExamResult).filter(ExamResult.student_id == student_id)
        
        total_exams = exams_query.count()
        attempted_exams = attempts_query.count()
        completed_exams = attempts_query.filter(ExamAttempt.status == "completed").count()
        passed_exams = results_query.filter(ExamResult.is_passed == True).count()
        
        # Calculate averages
        avg_percentage = results_query.with_entities(func.avg(ExamResult.percentage)).scalar() or Decimal('0.00')
        best_percentage = results_query.with_entities(func.max(ExamResult.percentage)).scalar() or Decimal('0.00')
        
        # Calculate total marks
        total_marks = results_query.with_entities(func.sum(ExamResult.total_marks)).scalar() or Decimal('0.00')
        obtained_marks = results_query.with_entities(func.sum(ExamResult.obtained_marks)).scalar() or Decimal('0.00')
        
        return StudentExamSummary(
            student_id=student_id,
            total_exams=total_exams,
            attempted_exams=attempted_exams,
            completed_exams=completed_exams,
            passed_exams=passed_exams,
            average_percentage=avg_percentage,
            best_percentage=best_percentage,
            total_marks=total_marks,
            obtained_marks=obtained_marks
        )
        
    except Exception as e:
        logger.error(f"Error getting student exam summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 