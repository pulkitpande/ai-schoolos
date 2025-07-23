"""
SQLAlchemy models for Exam Service (AI SchoolOS)
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


class Exam(Base):
    __tablename__ = "exams"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Exam Information
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    exam_type: Mapped[str] = mapped_column(String(50), nullable=False)  # midterm, final, quiz, assignment
    
    # Academic Details
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    class_name: Mapped[str] = mapped_column(String(50), nullable=False)
    section: Mapped[str] = mapped_column(String(10), nullable=False)
    subject: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Scheduling
    exam_date: Mapped[Date] = mapped_column(Date, nullable=False)
    start_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    duration_minutes: Mapped[Integer] = mapped_column(Integer, nullable=False)
    
    # Exam Settings
    total_marks: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    passing_marks: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    max_attempts: Mapped[Integer] = mapped_column(Integer, default=1)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft, published, active, completed, archived
    is_online: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Additional Settings
    settings: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # randomization, time limits, etc.
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_exams_tenant_id", "tenant_id"),
        Index("ix_exams_academic_year", "academic_year"),
        Index("ix_exams_class_section", "class_name", "section"),
        Index("ix_exams_subject", "subject"),
        Index("ix_exams_status", "status"),
        Index("ix_exams_date", "exam_date"),
    )


class Question(Base):
    __tablename__ = "questions"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    
    # Question Information
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[str] = mapped_column(String(50), nullable=False)  # multiple_choice, true_false, essay, short_answer
    marks: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    # Question Options (for multiple choice)
    options: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    correct_answer: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Question Settings
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)
    order_number: Mapped[Integer] = mapped_column(Integer, nullable=False)
    
    # Additional Data
    explanation: Mapped[str] = mapped_column(Text, nullable=True)
    metadata: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_questions_exam_id", "exam_id"),
        Index("ix_questions_question_type", "question_type"),
        Index("ix_questions_order", "exam_id", "order_number"),
    )


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    student_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Attempt Information
    attempt_number: Mapped[Integer] = mapped_column(Integer, default=1)
    start_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    duration_minutes: Mapped[Integer] = mapped_column(Integer, nullable=True)
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="in_progress")  # in_progress, completed, submitted, graded
    
    # Results
    total_marks: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    obtained_marks: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    percentage: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)
    grade: Mapped[str] = mapped_column(String(10), nullable=True)
    
    # Additional Information
    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str] = mapped_column(Text, nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_exam_attempts_exam_id", "exam_id"),
        Index("ix_exam_attempts_student_id", "student_id"),
        Index("ix_exam_attempts_status", "status"),
        Index("ix_exam_attempts_student_exam", "student_id", "exam_id"),
    )


class Answer(Base):
    __tablename__ = "answers"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_attempt_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("exam_attempts.id", ondelete="CASCADE"), nullable=False)
    question_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    
    # Answer Information
    answer_text: Mapped[str] = mapped_column(Text, nullable=True)
    selected_options: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Grading
    marks_awarded: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=True)
    
    # Feedback
    feedback: Mapped[str] = mapped_column(Text, nullable=True)
    graded_by: Mapped[str] = mapped_column(UUIDString, nullable=True)
    graded_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_answers_exam_attempt_id", "exam_attempt_id"),
        Index("ix_answers_question_id", "question_id"),
        Index("ix_answers_attempt_question", "exam_attempt_id", "question_id", unique=True),
    )


class ExamResult(Base):
    __tablename__ = "exam_results"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    student_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    exam_attempt_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("exam_attempts.id", ondelete="CASCADE"), nullable=False)
    
    # Result Information
    total_questions: Mapped[Integer] = mapped_column(Integer, nullable=False)
    answered_questions: Mapped[Integer] = mapped_column(Integer, nullable=False)
    correct_answers: Mapped[Integer] = mapped_column(Integer, nullable=False)
    
    # Marks
    total_marks: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    obtained_marks: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    percentage: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    
    # Grade and Rank
    grade: Mapped[str] = mapped_column(String(10), nullable=True)
    rank: Mapped[Integer] = mapped_column(Integer, nullable=True)
    
    # Status
    is_passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Additional Information
    remarks: Mapped[str] = mapped_column(Text, nullable=True)
    reviewed_by: Mapped[str] = mapped_column(UUIDString, nullable=True)
    reviewed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_exam_results_exam_id", "exam_id"),
        Index("ix_exam_results_student_id", "student_id"),
        Index("ix_exam_results_exam_attempt_id", "exam_attempt_id"),
        Index("ix_exam_results_grade", "grade"),
        Index("ix_exam_results_percentage", "percentage"),
        Index("ix_exam_results_student_exam", "student_id", "exam_id", unique=True),
    )


class ExamSchedule(Base):
    __tablename__ = "exam_schedules"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Schedule Information
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    schedule_type: Mapped[str] = mapped_column(String(50), nullable=False)  # regular, makeup, retest
    
    # Academic Details
    academic_year: Mapped[str] = mapped_column(String(20), nullable=False)
    class_name: Mapped[str] = mapped_column(String(50), nullable=True)  # NULL for all classes
    section: Mapped[str] = mapped_column(String(10), nullable=True)  # NULL for all sections
    subject: Mapped[str] = mapped_column(String(100), nullable=True)  # NULL for all subjects
    
    # Scheduling
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_exam_schedules_tenant_id", "tenant_id"),
        Index("ix_exam_schedules_academic_year", "academic_year"),
        Index("ix_exam_schedules_dates", "start_date", "end_date"),
    ) 