"""
Pydantic schemas for Exam Service (AI SchoolOS)
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from decimal import Decimal


# Exam schemas
class ExamBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    exam_type: str = Field(..., min_length=1, max_length=50)
    academic_year: str = Field(..., min_length=1, max_length=20)
    class_name: str = Field(..., min_length=1, max_length=50)
    section: str = Field(..., min_length=1, max_length=10)
    subject: str = Field(..., min_length=1, max_length=100)
    exam_date: date
    start_time: datetime
    end_time: datetime
    duration_minutes: int = Field(..., ge=1)
    total_marks: Decimal = Field(..., ge=0)
    passing_marks: Decimal = Field(..., ge=0)
    max_attempts: int = Field(1, ge=1)
    is_online: bool = False
    settings: Optional[Dict[str, Any]] = {}


class ExamCreate(ExamBase):
    tenant_id: str


class ExamUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    exam_type: Optional[str] = Field(None, min_length=1, max_length=50)
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    class_name: Optional[str] = Field(None, min_length=1, max_length=50)
    section: Optional[str] = Field(None, min_length=1, max_length=10)
    subject: Optional[str] = Field(None, min_length=1, max_length=100)
    exam_date: Optional[date] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=1)
    total_marks: Optional[Decimal] = Field(None, ge=0)
    passing_marks: Optional[Decimal] = Field(None, ge=0)
    max_attempts: Optional[int] = Field(None, ge=1)
    is_online: Optional[bool] = None
    settings: Optional[Dict[str, Any]] = None
    status: Optional[str] = Field(None, max_length=20)


class ExamResponse(ExamBase):
    id: str
    tenant_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExamListResponse(BaseModel):
    exams: List[ExamResponse]
    total: int
    page: int
    size: int


# Question schemas
class QuestionBase(BaseModel):
    question_text: str = Field(..., min_length=1)
    question_type: str = Field(..., min_length=1, max_length=50)
    marks: Decimal = Field(..., ge=0)
    options: Optional[Dict[str, Any]] = {}
    correct_answer: Optional[str] = None
    is_required: bool = True
    order_number: int = Field(..., ge=1)
    explanation: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}


class QuestionCreate(QuestionBase):
    exam_id: str


class QuestionUpdate(BaseModel):
    question_text: Optional[str] = Field(None, min_length=1)
    question_type: Optional[str] = Field(None, min_length=1, max_length=50)
    marks: Optional[Decimal] = Field(None, ge=0)
    options: Optional[Dict[str, Any]] = None
    correct_answer: Optional[str] = None
    is_required: Optional[bool] = None
    order_number: Optional[int] = Field(None, ge=1)
    explanation: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class QuestionResponse(QuestionBase):
    id: str
    exam_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuestionListResponse(BaseModel):
    questions: List[QuestionResponse]
    total: int
    page: int
    size: int


# Exam Attempt schemas
class ExamAttemptBase(BaseModel):
    exam_id: str
    student_id: str
    attempt_number: int = Field(1, ge=1)
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=0)
    ip_address: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = None
    notes: Optional[str] = None


class ExamAttemptCreate(ExamAttemptBase):
    pass


class ExamAttemptUpdate(BaseModel):
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = Field(None, ge=0)
    status: Optional[str] = Field(None, max_length=20)
    total_marks: Optional[Decimal] = Field(None, ge=0)
    obtained_marks: Optional[Decimal] = Field(None, ge=0)
    percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    grade: Optional[str] = Field(None, max_length=10)
    notes: Optional[str] = None


class ExamAttemptResponse(ExamAttemptBase):
    id: str
    status: str
    total_marks: Optional[Decimal] = None
    obtained_marks: Optional[Decimal] = None
    percentage: Optional[Decimal] = None
    grade: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExamAttemptListResponse(BaseModel):
    exam_attempts: List[ExamAttemptResponse]
    total: int
    page: int
    size: int


# Answer schemas
class AnswerBase(BaseModel):
    exam_attempt_id: str
    question_id: str
    answer_text: Optional[str] = None
    selected_options: Optional[Dict[str, Any]] = {}
    marks_awarded: Optional[Decimal] = Field(None, ge=0)
    is_correct: Optional[bool] = None
    feedback: Optional[str] = None
    graded_by: Optional[str] = None


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(BaseModel):
    answer_text: Optional[str] = None
    selected_options: Optional[Dict[str, Any]] = None
    marks_awarded: Optional[Decimal] = Field(None, ge=0)
    is_correct: Optional[bool] = None
    feedback: Optional[str] = None
    graded_by: Optional[str] = None


class AnswerResponse(AnswerBase):
    id: str
    graded_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnswerListResponse(BaseModel):
    answers: List[AnswerResponse]
    total: int
    page: int
    size: int


# Exam Result schemas
class ExamResultBase(BaseModel):
    exam_id: str
    student_id: str
    exam_attempt_id: str
    total_questions: int = Field(..., ge=0)
    answered_questions: int = Field(..., ge=0)
    correct_answers: int = Field(..., ge=0)
    total_marks: Decimal = Field(..., ge=0)
    obtained_marks: Decimal = Field(..., ge=0)
    percentage: Decimal = Field(..., ge=0, le=100)
    grade: Optional[str] = Field(None, max_length=10)
    rank: Optional[int] = Field(None, ge=1)
    is_passed: bool
    is_published: bool = False
    remarks: Optional[str] = None
    reviewed_by: Optional[str] = None


class ExamResultCreate(ExamResultBase):
    pass


class ExamResultUpdate(BaseModel):
    total_questions: Optional[int] = Field(None, ge=0)
    answered_questions: Optional[int] = Field(None, ge=0)
    correct_answers: Optional[int] = Field(None, ge=0)
    total_marks: Optional[Decimal] = Field(None, ge=0)
    obtained_marks: Optional[Decimal] = Field(None, ge=0)
    percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    grade: Optional[str] = Field(None, max_length=10)
    rank: Optional[int] = Field(None, ge=1)
    is_passed: Optional[bool] = None
    is_published: Optional[bool] = None
    remarks: Optional[str] = None
    reviewed_by: Optional[str] = None


class ExamResultResponse(ExamResultBase):
    id: str
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExamResultListResponse(BaseModel):
    exam_results: List[ExamResultResponse]
    total: int
    page: int
    size: int


# Exam Schedule schemas
class ExamScheduleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    schedule_type: str = Field(..., min_length=1, max_length=50)
    academic_year: str = Field(..., min_length=1, max_length=20)
    class_name: Optional[str] = Field(None, max_length=50)
    section: Optional[str] = Field(None, max_length=10)
    subject: Optional[str] = Field(None, max_length=100)
    start_date: date
    end_date: date
    is_active: bool = True


class ExamScheduleCreate(ExamScheduleBase):
    tenant_id: str


class ExamScheduleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    schedule_type: Optional[str] = Field(None, min_length=1, max_length=50)
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    class_name: Optional[str] = Field(None, max_length=50)
    section: Optional[str] = Field(None, max_length=10)
    subject: Optional[str] = Field(None, max_length=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None


class ExamScheduleResponse(ExamScheduleBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExamScheduleListResponse(BaseModel):
    exam_schedules: List[ExamScheduleResponse]
    total: int
    page: int
    size: int


# Summary schemas
class ExamSummary(BaseModel):
    total_exams: int
    active_exams: int
    completed_exams: int
    total_attempts: int
    total_results: int
    average_percentage: Decimal
    pass_rate: Decimal


class StudentExamSummary(BaseModel):
    student_id: str
    total_exams: int
    attempted_exams: int
    completed_exams: int
    passed_exams: int
    average_percentage: Decimal
    best_percentage: Decimal
    total_marks: Decimal
    obtained_marks: Decimal 