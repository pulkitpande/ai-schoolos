"""
AI Service Router

Handles all AI-related operations including NLP, computer vision, predictive analytics, and intelligent automation.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Depends, Query, status, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..database import get_db
from ..models import (
    AIModel, AIInference, AITraining, AIDataset, AIFeature, 
    AIPrediction, AIVision, AINLP, AIRecommendation
)
from ..schemas import (
    AIModelCreate, AIModelUpdate, AIModelResponse,
    AIInferenceCreate, AIInferenceResponse,
    AITrainingCreate, AITrainingUpdate, AITrainingResponse,
    AIDatasetCreate, AIDatasetUpdate, AIDatasetResponse,
    AIFeatureCreate, AIFeatureUpdate, AIFeatureResponse,
    AIPredictionCreate, AIPredictionResponse,
    AIVisionCreate, AIVisionResponse,
    AINLPCreate, AINLPResponse,
    AIRecommendationCreate, AIRecommendationResponse
)

router = APIRouter(prefix="/ai", tags=["ai"])


@router.get("/")
async def root():
    return {"message": "AI Service is running"}


# AI Model Management
@router.post("/models", response_model=AIModelResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_model(
    model: AIModelCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new AI model."""
    try:
        db_model = AIModel(
            tenant_id=tenant_id,
            model_name=model.model_name,
            model_type=model.model_type,
            model_version=model.model_version,
            model_path=model.model_path,
            model_config=model.model_config,
            performance_metrics=model.performance_metrics,
            training_data_info=model.training_data_info,
            is_active=model.is_active
        )
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return AIModelResponse.from_orm(db_model)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/models", response_model=List[AIModelResponse])
async def get_ai_models(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    model_type: Optional[str] = None,
    is_active: Optional[bool] = None
):
    """Get all AI models with optional filters."""
    query = db.query(AIModel).filter(AIModel.tenant_id == tenant_id)
    
    if model_type:
        query = query.filter(AIModel.model_type == model_type)
    if is_active is not None:
        query = query.filter(AIModel.is_active == is_active)
    
    models = query.offset(skip).limit(limit).all()
    return [AIModelResponse.from_orm(model) for model in models]


@router.get("/models/{model_id}", response_model=AIModelResponse)
async def get_ai_model(
    model_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific AI model by ID."""
    model = db.query(AIModel).filter(
        and_(AIModel.id == model_id, AIModel.tenant_id == tenant_id)
    ).first()
    
    if not model:
        raise HTTPException(status_code=404, detail="AI model not found")
    
    return AIModelResponse.from_orm(model)


@router.put("/models/{model_id}", response_model=AIModelResponse)
async def update_ai_model(
    model_id: str,
    model: AIModelUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update an AI model."""
    db_model = db.query(AIModel).filter(
        and_(AIModel.id == model_id, AIModel.tenant_id == tenant_id)
    ).first()
    
    if not db_model:
        raise HTTPException(status_code=404, detail="AI model not found")
    
    for field, value in model.dict(exclude_unset=True).items():
        setattr(db_model, field, value)
    
    db_model.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_model)
    return AIModelResponse.from_orm(db_model)


@router.delete("/models/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ai_model(
    model_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete an AI model."""
    model = db.query(AIModel).filter(
        and_(AIModel.id == model_id, AIModel.tenant_id == tenant_id)
    ).first()
    
    if not model:
        raise HTTPException(status_code=404, detail="AI model not found")
    
    db.delete(model)
    db.commit()


# AI Inference
@router.post("/inference", response_model=AIInferenceResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_inference(
    inference: AIInferenceCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new AI inference."""
    try:
        db_inference = AIInference(
            tenant_id=tenant_id,
            model_id=inference.model_id,
            input_data=inference.input_data,
            output_data=inference.output_data,
            confidence_score=inference.confidence_score,
            processing_time=inference.processing_time,
            inference_type=inference.inference_type,
            metadata=inference.metadata
        )
        db.add(db_inference)
        db.commit()
        db.refresh(db_inference)
        return AIInferenceResponse.from_orm(db_inference)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/inference", response_model=List[AIInferenceResponse])
async def get_ai_inferences(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    model_id: Optional[str] = None,
    inference_type: Optional[str] = None
):
    """Get all AI inferences with optional filters."""
    query = db.query(AIInference).filter(AIInference.tenant_id == tenant_id)
    
    if model_id:
        query = query.filter(AIInference.model_id == model_id)
    if inference_type:
        query = query.filter(AIInference.inference_type == inference_type)
    
    inferences = query.order_by(AIInference.created_at.desc()).offset(skip).limit(limit).all()
    return [AIInferenceResponse.from_orm(inference) for inference in inferences]


# AI Training Management
@router.post("/training", response_model=AITrainingResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_training(
    training: AITrainingCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new AI training session."""
    try:
        db_training = AITraining(
            tenant_id=tenant_id,
            model_id=training.model_id,
            dataset_id=training.dataset_id,
            training_config=training.training_config,
            hyperparameters=training.hyperparameters,
            training_metrics=training.training_metrics,
            training_status=training.training_status,
            training_notes=training.training_notes
        )
        db.add(db_training)
        db.commit()
        db.refresh(db_training)
        return AITrainingResponse.from_orm(db_training)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/training", response_model=List[AITrainingResponse])
async def get_ai_training_sessions(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    training_status: Optional[str] = None
):
    """Get all AI training sessions with optional filters."""
    query = db.query(AITraining).filter(AITraining.tenant_id == tenant_id)
    
    if training_status:
        query = query.filter(AITraining.training_status == training_status)
    
    training_sessions = query.order_by(AITraining.created_at.desc()).offset(skip).limit(limit).all()
    return [AITrainingResponse.from_orm(session) for session in training_sessions]


@router.get("/training/{training_id}", response_model=AITrainingResponse)
async def get_ai_training(
    training_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific AI training session by ID."""
    training = db.query(AITraining).filter(
        and_(AITraining.id == training_id, AITraining.tenant_id == tenant_id)
    ).first()
    
    if not training:
        raise HTTPException(status_code=404, detail="AI training session not found")
    
    return AITrainingResponse.from_orm(training)


@router.put("/training/{training_id}", response_model=AITrainingResponse)
async def update_ai_training(
    training_id: str,
    training: AITrainingUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update an AI training session."""
    db_training = db.query(AITraining).filter(
        and_(AITraining.id == training_id, AITraining.tenant_id == tenant_id)
    ).first()
    
    if not db_training:
        raise HTTPException(status_code=404, detail="AI training session not found")
    
    for field, value in training.dict(exclude_unset=True).items():
        setattr(db_training, field, value)
    
    db_training.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_training)
    return AITrainingResponse.from_orm(db_training)


# AI Dataset Management
@router.post("/datasets", response_model=AIDatasetResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_dataset(
    dataset: AIDatasetCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new AI dataset."""
    try:
        db_dataset = AIDataset(
            tenant_id=tenant_id,
            dataset_name=dataset.dataset_name,
            dataset_type=dataset.dataset_type,
            dataset_path=dataset.dataset_path,
            dataset_size=dataset.dataset_size,
            data_format=dataset.data_format,
            schema_info=dataset.schema_info,
            quality_metrics=dataset.quality_metrics,
            description=dataset.description
        )
        db.add(db_dataset)
        db.commit()
        db.refresh(db_dataset)
        return AIDatasetResponse.from_orm(db_dataset)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/datasets", response_model=List[AIDatasetResponse])
async def get_ai_datasets(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    dataset_type: Optional[str] = None
):
    """Get all AI datasets with optional filters."""
    query = db.query(AIDataset).filter(AIDataset.tenant_id == tenant_id)
    
    if dataset_type:
        query = query.filter(AIDataset.dataset_type == dataset_type)
    
    datasets = query.offset(skip).limit(limit).all()
    return [AIDatasetResponse.from_orm(dataset) for dataset in datasets]


@router.get("/datasets/{dataset_id}", response_model=AIDatasetResponse)
async def get_ai_dataset(
    dataset_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific AI dataset by ID."""
    dataset = db.query(AIDataset).filter(
        and_(AIDataset.id == dataset_id, AIDataset.tenant_id == tenant_id)
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="AI dataset not found")
    
    return AIDatasetResponse.from_orm(dataset)


@router.put("/datasets/{dataset_id}", response_model=AIDatasetResponse)
async def update_ai_dataset(
    dataset_id: str,
    dataset: AIDatasetUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update an AI dataset."""
    db_dataset = db.query(AIDataset).filter(
        and_(AIDataset.id == dataset_id, AIDataset.tenant_id == tenant_id)
    ).first()
    
    if not db_dataset:
        raise HTTPException(status_code=404, detail="AI dataset not found")
    
    for field, value in dataset.dict(exclude_unset=True).items():
        setattr(db_dataset, field, value)
    
    db_dataset.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_dataset)
    return AIDatasetResponse.from_orm(db_dataset)


@router.delete("/datasets/{dataset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ai_dataset(
    dataset_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete an AI dataset."""
    dataset = db.query(AIDataset).filter(
        and_(AIDataset.id == dataset_id, AIDataset.tenant_id == tenant_id)
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="AI dataset not found")
    
    db.delete(dataset)
    db.commit()


# AI Features Management
@router.post("/features", response_model=AIFeatureResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_feature(
    feature: AIFeatureCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new AI feature."""
    try:
        db_feature = AIFeature(
            tenant_id=tenant_id,
            feature_name=feature.feature_name,
            feature_type=feature.feature_type,
            feature_config=feature.feature_config,
            is_enabled=feature.is_enabled,
            performance_metrics=feature.performance_metrics,
            description=feature.description
        )
        db.add(db_feature)
        db.commit()
        db.refresh(db_feature)
        return AIFeatureResponse.from_orm(db_feature)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/features", response_model=List[AIFeatureResponse])
async def get_ai_features(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    feature_type: Optional[str] = None,
    is_enabled: Optional[bool] = None
):
    """Get all AI features with optional filters."""
    query = db.query(AIFeature).filter(AIFeature.tenant_id == tenant_id)
    
    if feature_type:
        query = query.filter(AIFeature.feature_type == feature_type)
    if is_enabled is not None:
        query = query.filter(AIFeature.is_enabled == is_enabled)
    
    features = query.offset(skip).limit(limit).all()
    return [AIFeatureResponse.from_orm(feature) for feature in features]


@router.get("/features/{feature_id}", response_model=AIFeatureResponse)
async def get_ai_feature(
    feature_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Get a specific AI feature by ID."""
    feature = db.query(AIFeature).filter(
        and_(AIFeature.id == feature_id, AIFeature.tenant_id == tenant_id)
    ).first()
    
    if not feature:
        raise HTTPException(status_code=404, detail="AI feature not found")
    
    return AIFeatureResponse.from_orm(feature)


@router.put("/features/{feature_id}", response_model=AIFeatureResponse)
async def update_ai_feature(
    feature_id: str,
    feature: AIFeatureUpdate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Update an AI feature."""
    db_feature = db.query(AIFeature).filter(
        and_(AIFeature.id == feature_id, AIFeature.tenant_id == tenant_id)
    ).first()
    
    if not db_feature:
        raise HTTPException(status_code=404, detail="AI feature not found")
    
    for field, value in feature.dict(exclude_unset=True).items():
        setattr(db_feature, field, value)
    
    db_feature.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_feature)
    return AIFeatureResponse.from_orm(db_feature)


@router.delete("/features/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ai_feature(
    feature_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Delete an AI feature."""
    feature = db.query(AIFeature).filter(
        and_(AIFeature.id == feature_id, AIFeature.tenant_id == tenant_id)
    ).first()
    
    if not feature:
        raise HTTPException(status_code=404, detail="AI feature not found")
    
    db.delete(feature)
    db.commit()


# AI Predictions
@router.post("/predictions", response_model=AIPredictionResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_prediction(
    prediction: AIPredictionCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new AI prediction."""
    try:
        db_prediction = AIPrediction(
            tenant_id=tenant_id,
            model_id=prediction.model_id,
            prediction_type=prediction.prediction_type,
            input_data=prediction.input_data,
            prediction_result=prediction.prediction_result,
            confidence_score=prediction.confidence_score,
            accuracy_metrics=prediction.accuracy_metrics,
            metadata=prediction.metadata
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        return AIPredictionResponse.from_orm(db_prediction)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/predictions", response_model=List[AIPredictionResponse])
async def get_ai_predictions(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    prediction_type: Optional[str] = None,
    model_id: Optional[str] = None
):
    """Get all AI predictions with optional filters."""
    query = db.query(AIPrediction).filter(AIPrediction.tenant_id == tenant_id)
    
    if prediction_type:
        query = query.filter(AIPrediction.prediction_type == prediction_type)
    if model_id:
        query = query.filter(AIPrediction.model_id == model_id)
    
    predictions = query.order_by(AIPrediction.created_at.desc()).offset(skip).limit(limit).all()
    return [AIPredictionResponse.from_orm(prediction) for prediction in predictions]


# AI Vision Processing
@router.post("/vision", response_model=AIVisionResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_vision(
    vision: AIVisionCreate,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Process image with AI vision."""
    try:
        # Read image file
        image_content = await image.read()
        
        db_vision = AIVision(
            tenant_id=tenant_id,
            model_id=vision.model_id,
            image_path=vision.image_path,
            vision_type=vision.vision_type,
            detection_results=vision.detection_results,
            confidence_scores=vision.confidence_scores,
            processing_time=vision.processing_time,
            metadata=vision.metadata
        )
        db.add(db_vision)
        db.commit()
        db.refresh(db_vision)
        return AIVisionResponse.from_orm(db_vision)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/vision", response_model=List[AIVisionResponse])
async def get_ai_vision_results(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    vision_type: Optional[str] = None
):
    """Get all AI vision results with optional filters."""
    query = db.query(AIVision).filter(AIVision.tenant_id == tenant_id)
    
    if vision_type:
        query = query.filter(AIVision.vision_type == vision_type)
    
    vision_results = query.order_by(AIVision.created_at.desc()).offset(skip).limit(limit).all()
    return [AIVisionResponse.from_orm(result) for result in vision_results]


# AI NLP Processing
@router.post("/nlp", response_model=AINLPResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_nlp(
    nlp: AINLPCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Process text with AI NLP."""
    try:
        db_nlp = AINLP(
            tenant_id=tenant_id,
            model_id=nlp.model_id,
            text_input=nlp.text_input,
            nlp_task=nlp.nlp_task,
            processing_result=nlp.processing_result,
            confidence_score=nlp.confidence_score,
            processing_time=nlp.processing_time,
            metadata=nlp.metadata
        )
        db.add(db_nlp)
        db.commit()
        db.refresh(db_nlp)
        return AINLPResponse.from_orm(db_nlp)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/nlp", response_model=List[AINLPResponse])
async def get_ai_nlp_results(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    nlp_task: Optional[str] = None
):
    """Get all AI NLP results with optional filters."""
    query = db.query(AINLP).filter(AINLP.tenant_id == tenant_id)
    
    if nlp_task:
        query = query.filter(AINLP.nlp_task == nlp_task)
    
    nlp_results = query.order_by(AINLP.created_at.desc()).offset(skip).limit(limit).all()
    return [AINLPResponse.from_orm(result) for result in nlp_results]


# AI Recommendations
@router.post("/recommendations", response_model=AIRecommendationResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_recommendation(
    recommendation: AIRecommendationCreate,
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID")
):
    """Create a new AI recommendation."""
    try:
        db_recommendation = AIRecommendation(
            tenant_id=tenant_id,
            model_id=recommendation.model_id,
            user_id=recommendation.user_id,
            recommendation_type=recommendation.recommendation_type,
            recommended_items=recommendation.recommended_items,
            confidence_scores=recommendation.confidence_scores,
            context_data=recommendation.context_data,
            metadata=recommendation.metadata
        )
        db.add(db_recommendation)
        db.commit()
        db.refresh(db_recommendation)
        return AIRecommendationResponse.from_orm(db_recommendation)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/recommendations", response_model=List[AIRecommendationResponse])
async def get_ai_recommendations(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: Optional[str] = None,
    recommendation_type: Optional[str] = None
):
    """Get all AI recommendations with optional filters."""
    query = db.query(AIRecommendation).filter(AIRecommendation.tenant_id == tenant_id)
    
    if user_id:
        query = query.filter(AIRecommendation.user_id == user_id)
    if recommendation_type:
        query = query.filter(AIRecommendation.recommendation_type == recommendation_type)
    
    recommendations = query.order_by(AIRecommendation.created_at.desc()).offset(skip).limit(limit).all()
    return [AIRecommendationResponse.from_orm(recommendation) for recommendation in recommendations]


# AI Analytics and Insights
@router.get("/analytics/performance")
async def get_ai_performance_analytics(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    model_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Get AI performance analytics."""
    # This would implement actual analytics logic
    return {
        "model_performance": {
            "accuracy": 0.95,
            "precision": 0.92,
            "recall": 0.89,
            "f1_score": 0.90
        },
        "inference_metrics": {
            "total_inferences": 1500,
            "average_response_time": 0.15,
            "success_rate": 0.98
        },
        "training_metrics": {
            "total_training_sessions": 25,
            "average_training_time": 120,
            "models_deployed": 8
        }
    }


@router.get("/analytics/usage")
async def get_ai_usage_analytics(
    db: Session = Depends(get_db),
    tenant_id: str = Query(..., description="Tenant ID"),
    period: str = Query("7d", description="Analytics period")
):
    """Get AI usage analytics."""
    # This would implement actual usage analytics
    return {
        "daily_usage": {
            "inferences": 150,
            "predictions": 75,
            "vision_processing": 30,
            "nlp_processing": 45
        },
        "feature_usage": {
            "attendance_prediction": 0.4,
            "grade_prediction": 0.3,
            "behavior_analysis": 0.2,
            "content_recommendation": 0.1
        },
        "user_engagement": {
            "active_users": 85,
            "ai_feature_adoption": 0.78
        }
    }


# Health Check
@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "ai-service",
        "timestamp": datetime.utcnow().isoformat(),
        "ai_models_loaded": 5,
        "gpu_available": True,
        "memory_usage": "2.1GB"
    } 