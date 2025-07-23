"""
Pydantic schemas for AI Service (AI SchoolOS)
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from sqlalchemy.orm import Query


# Base schemas
class AIModelBase(BaseModel):
    model_name: str = Field(..., description="Model name")
    model_type: str = Field(..., description="Model type (classification, regression, vision, nlp)")
    model_version: str = Field("1.0", description="Model version")
    model_path: str = Field(..., description="Model file path")
    model_config: Dict[str, Any] = Field(default_factory=dict, description="Model configuration")
    performance_metrics: Dict[str, Any] = Field(default_factory=dict, description="Performance metrics")
    training_data_info: Dict[str, Any] = Field(default_factory=dict, description="Training data information")
    is_active: bool = Field(True, description="Is model active")


class AIModelCreate(AIModelBase):
    pass


class AIModelUpdate(BaseModel):
    model_name: Optional[str] = None
    model_type: Optional[str] = None
    model_version: Optional[str] = None
    model_path: Optional[str] = None
    model_config: Optional[Dict[str, Any]] = None
    performance_metrics: Optional[Dict[str, Any]] = None
    training_data_info: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class AIModelResponse(AIModelBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# AI Inference schemas
class AIInferenceBase(BaseModel):
    model_id: str = Field(..., description="Model ID")
    input_data: Dict[str, Any] = Field(..., description="Input data")
    output_data: Dict[str, Any] = Field(..., description="Output data")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    processing_time: float = Field(..., description="Processing time in seconds")
    inference_type: str = Field(..., description="Inference type")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AIInferenceCreate(AIInferenceBase):
    pass


class AIInferenceResponse(AIInferenceBase):
    id: str
    tenant_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# AI Training schemas
class AITrainingBase(BaseModel):
    model_id: str = Field(..., description="Model ID")
    dataset_id: str = Field(..., description="Dataset ID")
    training_config: Dict[str, Any] = Field(default_factory=dict, description="Training configuration")
    hyperparameters: Dict[str, Any] = Field(default_factory=dict, description="Hyperparameters")
    training_metrics: Dict[str, Any] = Field(default_factory=dict, description="Training metrics")
    training_status: str = Field("pending", description="Training status")
    training_notes: Optional[str] = Field(None, description="Training notes")


class AITrainingCreate(AITrainingBase):
    pass


class AITrainingUpdate(BaseModel):
    model_id: Optional[str] = None
    dataset_id: Optional[str] = None
    training_config: Optional[Dict[str, Any]] = None
    hyperparameters: Optional[Dict[str, Any]] = None
    training_metrics: Optional[Dict[str, Any]] = None
    training_status: Optional[str] = None
    training_notes: Optional[str] = None


class AITrainingResponse(AITrainingBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# AI Dataset schemas
class AIDatasetBase(BaseModel):
    dataset_name: str = Field(..., description="Dataset name")
    dataset_type: str = Field(..., description="Dataset type")
    dataset_path: str = Field(..., description="Dataset file path")
    dataset_size: int = Field(..., description="Dataset size in records")
    data_format: str = Field(..., description="Data format")
    schema_info: Dict[str, Any] = Field(default_factory=dict, description="Schema information")
    quality_metrics: Dict[str, Any] = Field(default_factory=dict, description="Quality metrics")
    description: Optional[str] = Field(None, description="Dataset description")


class AIDatasetCreate(AIDatasetBase):
    pass


class AIDatasetUpdate(BaseModel):
    dataset_name: Optional[str] = None
    dataset_type: Optional[str] = None
    dataset_path: Optional[str] = None
    dataset_size: Optional[int] = None
    data_format: Optional[str] = None
    schema_info: Optional[Dict[str, Any]] = None
    quality_metrics: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class AIDatasetResponse(AIDatasetBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# AI Feature schemas
class AIFeatureBase(BaseModel):
    feature_name: str = Field(..., description="Feature name")
    feature_type: str = Field(..., description="Feature type")
    feature_config: Dict[str, Any] = Field(default_factory=dict, description="Feature configuration")
    is_enabled: bool = Field(True, description="Is feature enabled")
    performance_metrics: Dict[str, Any] = Field(default_factory=dict, description="Performance metrics")
    description: Optional[str] = Field(None, description="Feature description")


class AIFeatureCreate(AIFeatureBase):
    pass


class AIFeatureUpdate(BaseModel):
    feature_name: Optional[str] = None
    feature_type: Optional[str] = None
    feature_config: Optional[Dict[str, Any]] = None
    is_enabled: Optional[bool] = None
    performance_metrics: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class AIFeatureResponse(AIFeatureBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# AI Prediction schemas
class AIPredictionBase(BaseModel):
    model_id: str = Field(..., description="Model ID")
    prediction_type: str = Field(..., description="Prediction type")
    input_data: Dict[str, Any] = Field(..., description="Input data")
    prediction_result: Dict[str, Any] = Field(..., description="Prediction result")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    accuracy_metrics: Dict[str, Any] = Field(default_factory=dict, description="Accuracy metrics")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AIPredictionCreate(AIPredictionBase):
    pass


class AIPredictionResponse(AIPredictionBase):
    id: str
    tenant_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# AI Vision schemas
class AIVisionBase(BaseModel):
    model_id: str = Field(..., description="Model ID")
    image_path: str = Field(..., description="Image file path")
    vision_type: str = Field(..., description="Vision type (object_detection, face_recognition, etc.)")
    detection_results: Dict[str, Any] = Field(default_factory=dict, description="Detection results")
    confidence_scores: Dict[str, float] = Field(default_factory=dict, description="Confidence scores")
    processing_time: float = Field(..., description="Processing time in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AIVisionCreate(AIVisionBase):
    pass


class AIVisionResponse(AIVisionBase):
    id: str
    tenant_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# AI NLP schemas
class AINLPBase(BaseModel):
    model_id: str = Field(..., description="Model ID")
    text_input: str = Field(..., description="Input text")
    nlp_task: str = Field(..., description="NLP task (sentiment_analysis, text_classification, etc.)")
    processing_result: Dict[str, Any] = Field(..., description="Processing result")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    processing_time: float = Field(..., description="Processing time in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AINLPCreate(AINLPBase):
    pass


class AINLPResponse(AINLPBase):
    id: str
    tenant_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# AI Recommendation schemas
class AIRecommendationBase(BaseModel):
    model_id: str = Field(..., description="Model ID")
    user_id: str = Field(..., description="User ID")
    recommendation_type: str = Field(..., description="Recommendation type")
    recommended_items: List[str] = Field(default_factory=list, description="Recommended items")
    confidence_scores: Dict[str, float] = Field(default_factory=dict, description="Confidence scores")
    context_data: Dict[str, Any] = Field(default_factory=dict, description="Context data")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class AIRecommendationCreate(AIRecommendationBase):
    pass


class AIRecommendationResponse(AIRecommendationBase):
    id: str
    tenant_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# Health check response
class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str
    ai_models_loaded: int
    gpu_available: bool
    memory_usage: str 