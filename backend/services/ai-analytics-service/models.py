from sqlalchemy import Column, String, DateTime, JSON, Float, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from shared.database.models import Base

class AIAnalytics(Base):
    __tablename__ = "ai_analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String, nullable=False, index=True)
    analytics_type = Column(String, nullable=False)
    data_source = Column(String, nullable=False)
    analysis_period = Column(String, nullable=False)
    metrics = Column(JSON, nullable=True)
    insights = Column(JSON, nullable=True)
    visualizations = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=True)
    meta_info = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AIPrediction(Base):
    __tablename__ = "ai_predictions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String, nullable=False, index=True)
    prediction_type = Column(String, nullable=False)
    target_entity = Column(String, nullable=False)
    prediction_horizon = Column(String, nullable=False)
    input_features = Column(JSON, nullable=True)
    prediction_result = Column(JSON, nullable=False)
    confidence_score = Column(Float, nullable=True)
    accuracy_metrics = Column(JSON, nullable=True)
    model_info = Column(JSON, nullable=True)
    meta_info = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AIInsight(Base):
    __tablename__ = "ai_insights"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String, nullable=False, index=True)
    insight_type = Column(String, nullable=False)
    insight_category = Column(String, nullable=False)
    insight_title = Column(String, nullable=False)
    insight_description = Column(Text, nullable=True)
    insight_data = Column(JSON, nullable=True)
    confidence_score = Column(Float, nullable=True)
    impact_score = Column(Float, nullable=True)
    recommendations = Column(JSON, nullable=True)
    meta_info = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AITrend(Base):
    __tablename__ = "ai_trends"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String, nullable=False, index=True)
    trend_type = Column(String, nullable=False)
    trend_category = Column(String, nullable=False)
    trend_period = Column(String, nullable=False)
    trend_data = Column(JSON, nullable=True)
    trend_direction = Column(String, nullable=False)
    trend_strength = Column(Float, nullable=True)
    trend_confidence = Column(Float, nullable=True)
    trend_implications = Column(JSON, nullable=True)
    meta_info = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AIPattern(Base):
    __tablename__ = "ai_patterns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String, nullable=False, index=True)
    pattern_type = Column(String, nullable=False)
    pattern_category = Column(String, nullable=False)
    pattern_name = Column(String, nullable=False)
    pattern_description = Column(Text, nullable=True)
    pattern_data = Column(JSON, nullable=True)
    pattern_frequency = Column(Float, nullable=True)
    pattern_significance = Column(Float, nullable=True)
    pattern_implications = Column(JSON, nullable=True)
    meta_info = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String, nullable=False, index=True)
    recommendation_type = Column(String, nullable=False)
    target_audience = Column(String, nullable=False)
    recommendation_title = Column(String, nullable=False)
    recommendation_description = Column(Text, nullable=True)
    recommendation_actions = Column(JSON, nullable=True)
    priority_level = Column(String, nullable=False)
    expected_impact = Column(Float, nullable=True)
    implementation_difficulty = Column(String, nullable=True)
    meta_info = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AIAlert(Base):
    __tablename__ = "ai_alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String, nullable=False, index=True)
    alert_type = Column(String, nullable=False)
    alert_severity = Column(String, nullable=False)
    alert_title = Column(String, nullable=False)
    alert_description = Column(Text, nullable=True)
    alert_data = Column(JSON, nullable=True)
    alert_status = Column(String, nullable=False, default="active")
    alert_acknowledged = Column(Boolean, default=False)
    alert_resolved = Column(Boolean, default=False)
    meta_info = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AIMetric(Base):
    __tablename__ = "ai_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String, nullable=False, index=True)
    metric_type = Column(String, nullable=False)
    metric_category = Column(String, nullable=False)
    metric_name = Column(String, nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String, nullable=True)
    metric_trend = Column(String, nullable=True)
    metric_threshold = Column(Float, nullable=True)
    metric_status = Column(String, nullable=True)
    meta_info = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AIReport(Base):
    __tablename__ = "ai_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String, nullable=False, index=True)
    report_type = Column(String, nullable=False)
    report_title = Column(String, nullable=False)
    report_description = Column(Text, nullable=True)
    report_data = Column(JSON, nullable=True)
    report_status = Column(String, nullable=False, default="draft")
    report_generated_at = Column(DateTime(timezone=True), server_default=func.now())
    report_scheduled = Column(Boolean, default=False)
    report_frequency = Column(String, nullable=True)
    meta_info = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 