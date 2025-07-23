"""
SQLAlchemy models for Homework Service (AI SchoolOS)
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


class Assignment(Base):
    __tablename__ = "assignments"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Assignment Information
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    instructions: Mapped[str] = mapped_column(Text, nullable=True)
    assignment_type: Mapped[str] = mapped_column(String(50), nullable=False)  # homework, project, essay, quiz
    
    # Academic Details
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    class_name: Mapped[str] = mapped_column(String(50), nullable=False)
    section: Mapped[str] = mapped_column(String(10), nullable=False)
    subject: Mapped[str] = mapped_column(String(100), nullable=False)
    teacher_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Scheduling
    assigned_date: Mapped[Date] = mapped_column(Date, nullable=False)
    due_date: Mapped[Date] = mapped_column(Date, nullable=False)
    submission_deadline: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    
    # Grading
    total_marks: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    passing_marks: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    weight_percentage: Mapped[float] = mapped_column(Numeric(5, 2), default=10.0)  # Weight in final grade
    
    # Assignment Settings
    allow_late_submission: Mapped[bool] = mapped_column(Boolean, default=False)
    late_submission_penalty: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0)  # Percentage penalty
    allow_resubmission: Mapped[bool] = mapped_column(Boolean, default=False)
    max_attempts: Mapped[Integer] = mapped_column(Integer, default=1)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, published, active, closed, archived
    is_online: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Additional Settings
    attachments: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # File attachments
    rubric: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Grading rubric
    settings: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Additional settings
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_assignments_tenant_id", "tenant_id"),
        Index("ix_assignments_academic_year", "academic_year"),
        Index("ix_assignments_class_section", "class_name", "section"),
        Index("ix_assignments_subject", "subject"),
        Index("ix_assignments_teacher_id", "teacher_id"),
        Index("ix_assignments_status", "status"),
        Index("ix_assignments_due_date", "due_date"),
    )


class AssignmentSubmission(Base):
    __tablename__ = "assignment_submissions"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    assignment_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False)
    student_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Submission Information
    submission_text: Mapped[str] = mapped_column(Text, nullable=True)
    attachments: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # File attachments
    submission_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Additional submission data
    
    # Submission Details
    submission_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    is_late: Mapped[bool] = mapped_column(Boolean, default=False)
    attempt_number: Mapped[Integer] = mapped_column(Integer, default=1)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="submitted")  # submitted, graded, returned, resubmitted
    
    # Grading
    marks_awarded: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    percentage: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    grade: Mapped[str] = mapped_column(String(10), nullable=True)
    feedback: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Grading Details
    graded_by: Mapped[str] = mapped_column(UUIDString, nullable=True)
    graded_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    grading_notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_assignment_submissions_assignment_id", "assignment_id"),
        Index("ix_assignment_submissions_student_id", "student_id"),
        Index("ix_assignment_submissions_status", "status"),
        Index("ix_assignment_submissions_submission_date", "submission_date"),
        Index("ix_assignment_submissions_student_assignment", "student_id", "assignment_id"),
    )


class AssignmentGrade(Base):
    __tablename__ = "assignment_grades"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    submission_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("assignment_submissions.id", ondelete="CASCADE"), nullable=False)
    
    # Grading Information
    criterion: Mapped[str] = mapped_column(String(100), nullable=False)  # Grading criterion
    max_marks: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    marks_awarded: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    feedback: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Grading Details
    graded_by: Mapped[str] = mapped_column(UUIDString, nullable=True)
    graded_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_assignment_grades_submission_id", "submission_id"),
        Index("ix_assignment_grades_criterion", "criterion"),
    )


class AssignmentComment(Base):
    __tablename__ = "assignment_comments"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    assignment_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False)
    submission_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("assignment_submissions.id", ondelete="CASCADE"), nullable=True)
    
    # Comment Information
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    comment_type: Mapped[str] = mapped_column(String(50), nullable=False)  # general, feedback, instruction, question
    
    # User Information
    user_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    user_type: Mapped[str] = mapped_column(String(20), nullable=False)  # student, teacher, admin
    
    # Visibility
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    is_internal: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_assignment_comments_assignment_id", "assignment_id"),
        Index("ix_assignment_comments_submission_id", "submission_id"),
        Index("ix_assignment_comments_user_id", "user_id"),
        Index("ix_assignment_comments_comment_type", "comment_type"),
    )


class AssignmentTemplate(Base):
    __tablename__ = "assignment_templates"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Template Information
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    template_type: Mapped[str] = mapped_column(String(50), nullable=False)  # essay, project, quiz, lab
    
    # Template Content
    instructions_template: Mapped[str] = mapped_column(Text, nullable=True)
    rubric_template: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    settings_template: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Academic Details
    subject: Mapped[str] = mapped_column(String(100), nullable=True)  # NULL for general templates
    class_level: Mapped[str] = mapped_column(String(50), nullable=True)  # NULL for all levels
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Usage Statistics
    usage_count: Mapped[Integer] = mapped_column(Integer, default=0)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_assignment_templates_tenant_id", "tenant_id"),
        Index("ix_assignment_templates_template_type", "template_type"),
        Index("ix_assignment_templates_subject", "subject"),
        Index("ix_assignment_templates_is_active", "is_active"),
    )


class AssignmentAnalytics(Base):
    __tablename__ = "assignment_analytics"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    assignment_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("assignments.id", ondelete="CASCADE"), nullable=False)
    
    # Analytics Data
    total_students: Mapped[Integer] = mapped_column(Integer, default=0)
    submitted_count: Mapped[Integer] = mapped_column(Integer, default=0)
    graded_count: Mapped[Integer] = mapped_column(Integer, default=0)
    late_submissions: Mapped[Integer] = mapped_column(Integer, default=0)
    
    # Performance Metrics
    average_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    highest_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    lowest_score: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    pass_rate: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    
    # Time Analytics
    average_submission_time: Mapped[Integer] = mapped_column(Integer, nullable=True)  # Minutes before deadline
    submission_timeline: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Hourly submission data
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_assignment_analytics_assignment_id", "assignment_id"),
        Index("ix_assignment_analytics_created_at", "created_at"),
    ) 