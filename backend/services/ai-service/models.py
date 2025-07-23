"""
SQLAlchemy models for AI Service (AI SchoolOS)
"""

from datetime import datetime
import uuid
import json
from sqlalchemy import (
    Column, String, DateTime, Boolean, ForeignKey, Table, Index, Text, Integer, Float, Numeric
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


class AIModel(Base):
    __tablename__ = "ai_models"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Model Information
    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    model_type: Mapped[str] = mapped_column(String(50), nullable=False)  # classification, regression, vision, nlp
    model_version: Mapped[str] = mapped_column(String(20), default="1.0")
    model_path: Mapped[str] = mapped_column(String(500), nullable=False)
    
    # Model Configuration
    model_config: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    performance_metrics: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    training_data_info: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_ai_models_tenant_id", "tenant_id"),
        Index("ix_ai_models_model_type", "model_type"),
        Index("ix_ai_models_is_active", "is_active"),
    )


class AIInference(Base):
    __tablename__ = "ai_inferences"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    model_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("ai_models.id"), nullable=False)
    
    # Inference Data
    input_data: Mapped[dict] = mapped_column(JSONEncodedDict, nullable=False)
    output_data: Mapped[dict] = mapped_column(JSONEncodedDict, nullable=False)
    
    # Performance Metrics
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    processing_time: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Inference Details
    inference_type: Mapped[str] = mapped_column(String(50), nullable=False)
    metadata: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_ai_inferences_tenant_id", "tenant_id"),
        Index("ix_ai_inferences_model_id", "model_id"),
        Index("ix_ai_inferences_inference_type", "inference_type"),
        Index("ix_ai_inferences_created_at", "created_at"),
    )


class AITraining(Base):
    __tablename__ = "ai_training"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    model_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("ai_models.id"), nullable=False)
    dataset_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("ai_datasets.id"), nullable=False)
    
    # Training Configuration
    training_config: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    hyperparameters: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    training_metrics: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Training Status
    training_status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, running, completed, failed
    
    # Additional Information
    training_notes: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_ai_training_tenant_id", "tenant_id"),
        Index("ix_ai_training_model_id", "model_id"),
        Index("ix_ai_training_dataset_id", "dataset_id"),
        Index("ix_ai_training_status", "training_status"),
    )


class AIDataset(Base):
    __tablename__ = "ai_datasets"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Dataset Information
    dataset_name: Mapped[str] = mapped_column(String(100), nullable=False)
    dataset_type: Mapped[str] = mapped_column(String(50), nullable=False)  # training, validation, test
    dataset_path: Mapped[str] = mapped_column(String(500), nullable=False)
    dataset_size: Mapped[int] = mapped_column(Integer, nullable=False)
    data_format: Mapped[str] = mapped_column(String(20), nullable=False)  # csv, json, parquet, etc.
    
    # Dataset Details
    schema_info: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    quality_metrics: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_ai_datasets_tenant_id", "tenant_id"),
        Index("ix_ai_datasets_dataset_type", "dataset_type"),
        Index("ix_ai_datasets_dataset_name", "dataset_name"),
    )


class AIFeature(Base):
    __tablename__ = "ai_features"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Feature Information
    feature_name: Mapped[str] = mapped_column(String(100), nullable=False)
    feature_type: Mapped[str] = mapped_column(String(50), nullable=False)  # prediction, vision, nlp, recommendation
    feature_config: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Feature Status
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    performance_metrics: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_ai_features_tenant_id", "tenant_id"),
        Index("ix_ai_features_feature_type", "feature_type"),
        Index("ix_ai_features_is_enabled", "is_enabled"),
    )


class AIPrediction(Base):
    __tablename__ = "ai_predictions"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    model_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("ai_models.id"), nullable=False)
    
    # Prediction Data
    prediction_type: Mapped[str] = mapped_column(String(50), nullable=False)  # grade_prediction, attendance_prediction, etc.
    input_data: Mapped[dict] = mapped_column(JSONEncodedDict, nullable=False)
    prediction_result: Mapped[dict] = mapped_column(JSONEncodedDict, nullable=False)
    
    # Performance Metrics
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    accuracy_metrics: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    metadata: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_ai_predictions_tenant_id", "tenant_id"),
        Index("ix_ai_predictions_model_id", "model_id"),
        Index("ix_ai_predictions_prediction_type", "prediction_type"),
        Index("ix_ai_predictions_created_at", "created_at"),
    )


class AIVision(Base):
    __tablename__ = "ai_vision"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    model_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("ai_models.id"), nullable=False)
    
    # Vision Data
    image_path: Mapped[str] = mapped_column(String(500), nullable=False)
    vision_type: Mapped[str] = mapped_column(String(50), nullable=False)  # object_detection, face_recognition, etc.
    
    # Detection Results
    detection_results: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    confidence_scores: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Performance Metrics
    processing_time: Mapped[float] = mapped_column(Float, nullable=False)
    metadata: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_ai_vision_tenant_id", "tenant_id"),
        Index("ix_ai_vision_model_id", "model_id"),
        Index("ix_ai_vision_vision_type", "vision_type"),
        Index("ix_ai_vision_created_at", "created_at"),
    )


class AINLP(Base):
    __tablename__ = "ai_nlp"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    model_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("ai_models.id"), nullable=False)
    
    # NLP Data
    text_input: Mapped[str] = mapped_column(Text, nullable=False)
    nlp_task: Mapped[str] = mapped_column(String(50), nullable=False)  # sentiment_analysis, text_classification, etc.
    
    # Processing Results
    processing_result: Mapped[dict] = mapped_column(JSONEncodedDict, nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)
    
    # Performance Metrics
    processing_time: Mapped[float] = mapped_column(Float, nullable=False)
    metadata: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_ai_nlp_tenant_id", "tenant_id"),
        Index("ix_ai_nlp_model_id", "model_id"),
        Index("ix_ai_nlp_nlp_task", "nlp_task"),
        Index("ix_ai_nlp_created_at", "created_at"),
    )


class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    model_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("ai_models.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Recommendation Data
    recommendation_type: Mapped[str] = mapped_column(String(50), nullable=False)  # content, course, book, etc.
    recommended_items: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # List of recommended items
    confidence_scores: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Context Information
    context_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    metadata: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_ai_recommendations_tenant_id", "tenant_id"),
        Index("ix_ai_recommendations_model_id", "model_id"),
        Index("ix_ai_recommendations_user_id", "user_id"),
        Index("ix_ai_recommendations_recommendation_type", "recommendation_type"),
        Index("ix_ai_recommendations_created_at", "created_at"),
    ) 