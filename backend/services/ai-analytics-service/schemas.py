from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID

# AI Analytics Schemas
class AIAnalyticsBase(BaseModel):
    analytics_type: str = Field(..., description="Type of analytics")
    data_source: str = Field(..., description="Data source for analytics")
    analysis_period: str = Field(..., description="Analysis period")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Analytics metrics")
    insights: Optional[Dict[str, Any]] = Field(None, description="Analytics insights")
    visualizations: Optional[Dict[str, Any]] = Field(None, description="Visualization data")
    confidence_score: Optional[float] = Field(None, description="Confidence score")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class AIAnalyticsCreate(AIAnalyticsBase):
    pass

class AIAnalyticsResponse(AIAnalyticsBase):
    id: UUID
    tenant_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# AI Prediction Schemas
class AIPredictionBase(BaseModel):
    prediction_type: str = Field(..., description="Type of prediction")
    target_entity: str = Field(..., description="Target entity for prediction")
    prediction_horizon: str = Field(..., description="Prediction time horizon")
    input_features: Optional[Dict[str, Any]] = Field(None, description="Input features")
    prediction_result: Dict[str, Any] = Field(..., description="Prediction result")
    confidence_score: Optional[float] = Field(None, description="Confidence score")
    accuracy_metrics: Optional[Dict[str, Any]] = Field(None, description="Accuracy metrics")
    model_info: Optional[Dict[str, Any]] = Field(None, description="Model information")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class AIPredictionCreate(AIPredictionBase):
    pass

class AIPredictionResponse(AIPredictionBase):
    id: UUID
    tenant_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# AI Insight Schemas
class AIInsightBase(BaseModel):
    insight_type: str = Field(..., description="Type of insight")
    insight_category: str = Field(..., description="Insight category")
    insight_title: str = Field(..., description="Insight title")
    insight_description: Optional[str] = Field(None, description="Insight description")
    insight_data: Optional[Dict[str, Any]] = Field(None, description="Insight data")
    confidence_score: Optional[float] = Field(None, description="Confidence score")
    impact_score: Optional[float] = Field(None, description="Impact score")
    recommendations: Optional[Dict[str, Any]] = Field(None, description="Recommendations")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class AIInsightCreate(AIInsightBase):
    pass

class AIInsightResponse(AIInsightBase):
    id: UUID
    tenant_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# AI Trend Schemas
class AITrendBase(BaseModel):
    trend_type: str = Field(..., description="Type of trend")
    trend_category: str = Field(..., description="Trend category")
    trend_period: str = Field(..., description="Trend period")
    trend_data: Optional[Dict[str, Any]] = Field(None, description="Trend data")
    trend_direction: str = Field(..., description="Trend direction")
    trend_strength: Optional[float] = Field(None, description="Trend strength")
    trend_confidence: Optional[float] = Field(None, description="Trend confidence")
    trend_implications: Optional[Dict[str, Any]] = Field(None, description="Trend implications")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class AITrendCreate(AITrendBase):
    pass

class AITrendResponse(AITrendBase):
    id: UUID
    tenant_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# AI Pattern Schemas
class AIPatternBase(BaseModel):
    pattern_type: str = Field(..., description="Type of pattern")
    pattern_category: str = Field(..., description="Pattern category")
    pattern_name: str = Field(..., description="Pattern name")
    pattern_description: Optional[str] = Field(None, description="Pattern description")
    pattern_data: Optional[Dict[str, Any]] = Field(None, description="Pattern data")
    pattern_frequency: Optional[float] = Field(None, description="Pattern frequency")
    pattern_significance: Optional[float] = Field(None, description="Pattern significance")
    pattern_implications: Optional[Dict[str, Any]] = Field(None, description="Pattern implications")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class AIPatternCreate(AIPatternBase):
    pass

class AIPatternResponse(AIPatternBase):
    id: UUID
    tenant_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# AI Recommendation Schemas
class AIRecommendationBase(BaseModel):
    recommendation_type: str = Field(..., description="Type of recommendation")
    target_audience: str = Field(..., description="Target audience")
    recommendation_title: str = Field(..., description="Recommendation title")
    recommendation_description: Optional[str] = Field(None, description="Recommendation description")
    recommendation_actions: Optional[Dict[str, Any]] = Field(None, description="Recommended actions")
    priority_level: str = Field(..., description="Priority level")
    expected_impact: Optional[float] = Field(None, description="Expected impact")
    implementation_difficulty: Optional[str] = Field(None, description="Implementation difficulty")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class AIRecommendationCreate(AIRecommendationBase):
    pass

class AIRecommendationResponse(AIRecommendationBase):
    id: UUID
    tenant_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# AI Alert Schemas
class AIAlertBase(BaseModel):
    alert_type: str = Field(..., description="Type of alert")
    alert_severity: str = Field(..., description="Alert severity")
    alert_title: str = Field(..., description="Alert title")
    alert_description: Optional[str] = Field(None, description="Alert description")
    alert_data: Optional[Dict[str, Any]] = Field(None, description="Alert data")
    alert_status: str = Field(default="active", description="Alert status")
    alert_acknowledged: bool = Field(default=False, description="Alert acknowledged")
    alert_resolved: bool = Field(default=False, description="Alert resolved")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class AIAlertCreate(AIAlertBase):
    pass

class AIAlertResponse(AIAlertBase):
    id: UUID
    tenant_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# AI Metric Schemas
class AIMetricBase(BaseModel):
    metric_type: str = Field(..., description="Type of metric")
    metric_category: str = Field(..., description="Metric category")
    metric_name: str = Field(..., description="Metric name")
    metric_value: float = Field(..., description="Metric value")
    metric_unit: Optional[str] = Field(None, description="Metric unit")
    metric_trend: Optional[str] = Field(None, description="Metric trend")
    metric_threshold: Optional[float] = Field(None, description="Metric threshold")
    metric_status: Optional[str] = Field(None, description="Metric status")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class AIMetricCreate(AIMetricBase):
    pass

class AIMetricResponse(AIMetricBase):
    id: UUID
    tenant_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# AI Report Schemas
class AIReportBase(BaseModel):
    report_type: str = Field(..., description="Type of report")
    report_title: str = Field(..., description="Report title")
    report_description: Optional[str] = Field(None, description="Report description")
    report_data: Optional[Dict[str, Any]] = Field(None, description="Report data")
    report_status: str = Field(default="draft", description="Report status")
    report_scheduled: bool = Field(default=False, description="Report scheduled")
    report_frequency: Optional[str] = Field(None, description="Report frequency")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

class AIReportCreate(AIReportBase):
    pass

class AIReportResponse(AIReportBase):
    id: UUID
    tenant_id: str
    report_generated_at: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 