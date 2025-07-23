"""
Pydantic schemas for Homework Service (AI SchoolOS)
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from decimal import Decimal


# Assignment schemas
class AssignmentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    instructions: Optional[str] = None
    assignment_type: str = Field(..., min_length=1, max_length=50)
    academic_year: str = Field(..., min_length=1, max_length=20)
    class_name: str = Field(..., min_length=1, max_length=50)
    section: str = Field(..., min_length=1, max_length=10)
    subject: str = Field(..., min_length=1, max_length=100)
    teacher_id: str
    assigned_date: date
    due_date: date
    submission_deadline: datetime
    total_marks: Decimal = Field(..., ge=0)
    passing_marks: Decimal = Field(..., ge=0)
    weight_percentage: Decimal = Field(10.0, ge=0, le=100)
    allow_late_submission: bool = False
    late_submission_penalty: Decimal = Field(0.0, ge=0, le=100)
    allow_resubmission: bool = False
    max_attempts: int = Field(1, ge=1)
    is_online: bool = False
    attachments: Optional[Dict[str, Any]] = {}
    rubric: Optional[Dict[str, Any]] = {}
    settings: Optional[Dict[str, Any]] = {}


class AssignmentCreate(AssignmentBase):
    tenant_id: str


class AssignmentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    instructions: Optional[str] = None
    assignment_type: Optional[str] = Field(None, min_length=1, max_length=50)
    academic_year: Optional[str] = Field(None, min_length=1, max_length=20)
    class_name: Optional[str] = Field(None, min_length=1, max_length=50)
    section: Optional[str] = Field(None, min_length=1, max_length=10)
    subject: Optional[str] = Field(None, min_length=1, max_length=100)
    teacher_id: Optional[str] = None
    assigned_date: Optional[date] = None
    due_date: Optional[date] = None
    submission_deadline: Optional[datetime] = None
    total_marks: Optional[Decimal] = Field(None, ge=0)
    passing_marks: Optional[Decimal] = Field(None, ge=0)
    weight_percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    allow_late_submission: Optional[bool] = None
    late_submission_penalty: Optional[Decimal] = Field(None, ge=0, le=100)
    allow_resubmission: Optional[bool] = None
    max_attempts: Optional[int] = Field(None, ge=1)
    is_online: Optional[bool] = None
    attachments: Optional[Dict[str, Any]] = None
    rubric: Optional[Dict[str, Any]] = None
    settings: Optional[Dict[str, Any]] = None
    status: Optional[str] = Field(None, max_length=20)


class AssignmentResponse(AssignmentBase):
    id: str
    tenant_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssignmentListResponse(BaseModel):
    assignments: List[AssignmentResponse]
    total: int
    page: int
    size: int


# Assignment Submission schemas
class AssignmentSubmissionBase(BaseModel):
    assignment_id: str
    student_id: str
    submission_text: Optional[str] = None
    attachments: Optional[Dict[str, Any]] = {}
    submission_data: Optional[Dict[str, Any]] = {}
    submission_date: datetime
    is_late: bool = False
    attempt_number: int = Field(1, ge=1)


class AssignmentSubmissionCreate(AssignmentSubmissionBase):
    pass


class AssignmentSubmissionUpdate(BaseModel):
    submission_text: Optional[str] = None
    attachments: Optional[Dict[str, Any]] = None
    submission_data: Optional[Dict[str, Any]] = None
    status: Optional[str] = Field(None, max_length=20)
    marks_awarded: Optional[Decimal] = Field(None, ge=0)
    percentage: Optional[Decimal] = Field(None, ge=0, le=100)
    grade: Optional[str] = Field(None, max_length=10)
    feedback: Optional[str] = None
    graded_by: Optional[str] = None
    grading_notes: Optional[str] = None


class AssignmentSubmissionResponse(AssignmentSubmissionBase):
    id: str
    status: str
    marks_awarded: Optional[Decimal] = None
    percentage: Optional[Decimal] = None
    grade: Optional[str] = None
    feedback: Optional[str] = None
    graded_by: Optional[str] = None
    graded_at: Optional[datetime] = None
    grading_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssignmentSubmissionListResponse(BaseModel):
    submissions: List[AssignmentSubmissionResponse]
    total: int
    page: int
    size: int


# Assignment Grade schemas
class AssignmentGradeBase(BaseModel):
    submission_id: str
    criterion: str = Field(..., min_length=1, max_length=100)
    max_marks: Decimal = Field(..., ge=0)
    marks_awarded: Decimal = Field(..., ge=0)
    feedback: Optional[str] = None
    graded_by: Optional[str] = None


class AssignmentGradeCreate(AssignmentGradeBase):
    pass


class AssignmentGradeUpdate(BaseModel):
    criterion: Optional[str] = Field(None, min_length=1, max_length=100)
    max_marks: Optional[Decimal] = Field(None, ge=0)
    marks_awarded: Optional[Decimal] = Field(None, ge=0)
    feedback: Optional[str] = None
    graded_by: Optional[str] = None


class AssignmentGradeResponse(AssignmentGradeBase):
    id: str
    graded_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssignmentGradeListResponse(BaseModel):
    grades: List[AssignmentGradeResponse]
    total: int
    page: int
    size: int


# Assignment Comment schemas
class AssignmentCommentBase(BaseModel):
    assignment_id: str
    submission_id: Optional[str] = None
    comment_text: str = Field(..., min_length=1)
    comment_type: str = Field(..., min_length=1, max_length=50)
    user_id: str
    user_type: str = Field(..., min_length=1, max_length=20)
    is_public: bool = True
    is_internal: bool = False


class AssignmentCommentCreate(AssignmentCommentBase):
    pass


class AssignmentCommentUpdate(BaseModel):
    comment_text: Optional[str] = Field(None, min_length=1)
    comment_type: Optional[str] = Field(None, min_length=1, max_length=50)
    is_public: Optional[bool] = None
    is_internal: Optional[bool] = None


class AssignmentCommentResponse(AssignmentCommentBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssignmentCommentListResponse(BaseModel):
    comments: List[AssignmentCommentResponse]
    total: int
    page: int
    size: int


# Assignment Template schemas
class AssignmentTemplateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    template_type: str = Field(..., min_length=1, max_length=50)
    instructions_template: Optional[str] = None
    rubric_template: Optional[Dict[str, Any]] = {}
    settings_template: Optional[Dict[str, Any]] = {}
    subject: Optional[str] = Field(None, max_length=100)
    class_level: Optional[str] = Field(None, max_length=50)
    is_active: bool = True
    is_public: bool = False


class AssignmentTemplateCreate(AssignmentTemplateBase):
    tenant_id: str


class AssignmentTemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    template_type: Optional[str] = Field(None, min_length=1, max_length=50)
    instructions_template: Optional[str] = None
    rubric_template: Optional[Dict[str, Any]] = None
    settings_template: Optional[Dict[str, Any]] = None
    subject: Optional[str] = Field(None, max_length=100)
    class_level: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None
    is_public: Optional[bool] = None


class AssignmentTemplateResponse(AssignmentTemplateBase):
    id: str
    tenant_id: str
    usage_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssignmentTemplateListResponse(BaseModel):
    templates: List[AssignmentTemplateResponse]
    total: int
    page: int
    size: int


# Assignment Analytics schemas
class AssignmentAnalyticsBase(BaseModel):
    assignment_id: str
    total_students: int = Field(0, ge=0)
    submitted_count: int = Field(0, ge=0)
    graded_count: int = Field(0, ge=0)
    late_submissions: int = Field(0, ge=0)
    average_score: Optional[Decimal] = Field(None, ge=0, le=100)
    highest_score: Optional[Decimal] = Field(None, ge=0, le=100)
    lowest_score: Optional[Decimal] = Field(None, ge=0, le=100)
    pass_rate: Optional[Decimal] = Field(None, ge=0, le=100)
    average_submission_time: Optional[int] = Field(None, ge=0)  # Minutes before deadline
    submission_timeline: Optional[Dict[str, Any]] = {}


class AssignmentAnalyticsCreate(AssignmentAnalyticsBase):
    pass


class AssignmentAnalyticsUpdate(BaseModel):
    total_students: Optional[int] = Field(None, ge=0)
    submitted_count: Optional[int] = Field(None, ge=0)
    graded_count: Optional[int] = Field(None, ge=0)
    late_submissions: Optional[int] = Field(None, ge=0)
    average_score: Optional[Decimal] = Field(None, ge=0, le=100)
    highest_score: Optional[Decimal] = Field(None, ge=0, le=100)
    lowest_score: Optional[Decimal] = Field(None, ge=0, le=100)
    pass_rate: Optional[Decimal] = Field(None, ge=0, le=100)
    average_submission_time: Optional[int] = Field(None, ge=0)
    submission_timeline: Optional[Dict[str, Any]] = None


class AssignmentAnalyticsResponse(AssignmentAnalyticsBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssignmentAnalyticsListResponse(BaseModel):
    analytics: List[AssignmentAnalyticsResponse]
    total: int
    page: int
    size: int


# Summary schemas
class AssignmentSummary(BaseModel):
    total_assignments: int
    active_assignments: int
    completed_assignments: int
    total_submissions: int
    graded_submissions: int
    average_submission_rate: Decimal
    average_grade: Decimal


class StudentAssignmentSummary(BaseModel):
    student_id: str
    total_assignments: int
    submitted_assignments: int
    graded_assignments: int
    average_grade: Decimal
    total_marks: Decimal
    obtained_marks: Decimal
    late_submissions: int 