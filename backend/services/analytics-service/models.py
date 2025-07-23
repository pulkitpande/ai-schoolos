"""
SQLAlchemy models for Analytics Service (AI SchoolOS)
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


class AnalyticsData(Base):
    __tablename__ = "analytics_data"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Data Information
    data_type: Mapped[str] = mapped_column(String(50), nullable=False)  # student, academic, financial, attendance
    data_source: Mapped[str] = mapped_column(String(50), nullable=False)  # service name
    data_period: Mapped[str] = mapped_column(String(20), nullable=False)  # daily, weekly, monthly, yearly
    
    # Data Content
    metrics: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Key metrics
    dimensions: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Data dimensions
    aggregations: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Aggregated data
    
    # Time Information
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    collected_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Status
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_valid: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_analytics_data_tenant_id", "tenant_id"),
        Index("ix_analytics_data_data_type", "data_type"),
        Index("ix_analytics_data_data_source", "data_source"),
        Index("ix_analytics_data_start_date", "start_date"),
        Index("ix_analytics_data_end_date", "end_date"),
    )


class Report(Base):
    __tablename__ = "reports"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Report Information
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    report_type: Mapped[str] = mapped_column(String(50), nullable=False)  # academic, financial, attendance, custom
    
    # Report Configuration
    query_config: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Query parameters
    visualization_config: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Chart/graph settings
    filters: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Report filters
    
    # Scheduling
    is_scheduled: Mapped[bool] = mapped_column(Boolean, default=False)
    schedule_frequency: Mapped[str] = mapped_column(String(20), nullable=True)  # daily, weekly, monthly
    last_generated: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    next_generation: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Author Information
    created_by: Mapped[str] = mapped_column(UUIDString, nullable=False)
    created_by_type: Mapped[str] = mapped_column(String(20), nullable=False)  # teacher, admin
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_reports_tenant_id", "tenant_id"),
        Index("ix_reports_report_type", "report_type"),
        Index("ix_reports_is_active", "is_active"),
        Index("ix_reports_created_by", "created_by"),
    )


class ReportExecution(Base):
    __tablename__ = "report_executions"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    report_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("reports.id", ondelete="CASCADE"), nullable=False)
    
    # Execution Information
    execution_status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, running, completed, failed
    execution_type: Mapped[str] = mapped_column(String(20), default="manual")  # manual, scheduled, api
    
    # Execution Details
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    execution_time: Mapped[int] = mapped_column(Integer, default=0)  # Seconds
    
    # Results
    result_data: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    result_file_path: Mapped[str] = mapped_column(String(500), nullable=True)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Parameters
    execution_params: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_report_executions_report_id", "report_id"),
        Index("ix_report_executions_execution_status", "execution_status"),
        Index("ix_report_executions_started_at", "started_at"),
    )


class Dashboard(Base):
    __tablename__ = "dashboards"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Dashboard Information
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    dashboard_type: Mapped[str] = mapped_column(String(50), nullable=False)  # academic, financial, operational, custom
    
    # Layout Configuration
    layout_config: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Dashboard layout
    widget_configs: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Widget configurations
    
    # Settings
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    refresh_interval: Mapped[int] = mapped_column(Integer, default=300)  # Seconds
    
    # Author Information
    created_by: Mapped[str] = mapped_column(UUIDString, nullable=False)
    created_by_type: Mapped[str] = mapped_column(String(20), nullable=False)  # teacher, admin
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_dashboards_tenant_id", "tenant_id"),
        Index("ix_dashboards_dashboard_type", "dashboard_type"),
        Index("ix_dashboards_is_active", "is_active"),
        Index("ix_dashboards_created_by", "created_by"),
    )


class Metric(Base):
    __tablename__ = "metrics"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Metric Information
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    metric_type: Mapped[str] = mapped_column(String(50), nullable=False)  # count, sum, average, percentage
    
    # Metric Configuration
    calculation_formula: Mapped[str] = mapped_column(Text, nullable=False)
    data_source: Mapped[str] = mapped_column(String(50), nullable=False)
    aggregation_period: Mapped[str] = mapped_column(String(20), default="daily")  # hourly, daily, weekly, monthly
    
    # Display Settings
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    unit: Mapped[str] = mapped_column(String(20), nullable=True)  # %, $, count, etc.
    decimal_places: Mapped[int] = mapped_column(Integer, default=2)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_metrics_tenant_id", "tenant_id"),
        Index("ix_metrics_metric_type", "metric_type"),
        Index("ix_metrics_is_active", "is_active"),
    )


class MetricValue(Base):
    __tablename__ = "metric_values"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    metric_id: Mapped[str] = mapped_column(UUIDString, ForeignKey("metrics.id", ondelete="CASCADE"), nullable=False)
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Value Information
    value: Mapped[float] = mapped_column(Numeric(15, 4), nullable=False)
    period_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    period_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    # Additional Data
    dimensions: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Dimension values
    metadata: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Additional metadata
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_metric_values_metric_id", "metric_id"),
        Index("ix_metric_values_tenant_id", "tenant_id"),
        Index("ix_metric_values_period_start", "period_start"),
        Index("ix_metric_values_period_end", "period_end"),
    )


class Insight(Base):
    __tablename__ = "insights"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Insight Information
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    insight_type: Mapped[str] = mapped_column(String(50), nullable=False)  # trend, anomaly, recommendation
    
    # Insight Data
    data_points: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # Supporting data
    confidence_score: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0)  # 0-100
    impact_score: Mapped[float] = mapped_column(Numeric(5, 2), default=0.0)  # 0-100
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)
    acknowledged_by: Mapped[str] = mapped_column(UUIDString, nullable=True)
    acknowledged_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_insights_tenant_id", "tenant_id"),
        Index("ix_insights_insight_type", "insight_type"),
        Index("ix_insights_is_active", "is_active"),
        Index("ix_insights_created_at", "created_at"),
    )


class AnalyticsJob(Base):
    __tablename__ = "analytics_jobs"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Job Information
    job_name: Mapped[str] = mapped_column(String(100), nullable=False)
    job_type: Mapped[str] = mapped_column(String(50), nullable=False)  # data_collection, report_generation, metric_calculation
    
    # Job Configuration
    job_config: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    schedule_config: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    
    # Execution Status
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, running, completed, failed
    last_run: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    next_run: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Results
    last_result: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    error_count: Mapped[int] = mapped_column(Integer, default=0)
    success_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Settings
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_analytics_jobs_tenant_id", "tenant_id"),
        Index("ix_analytics_jobs_job_type", "job_type"),
        Index("ix_analytics_jobs_status", "status"),
        Index("ix_analytics_jobs_is_active", "is_active"),
    )


class AnalyticsExport(Base):
    __tablename__ = "analytics_exports"
    id: Mapped[str] = mapped_column(UUIDString, primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id: Mapped[str] = mapped_column(UUIDString, nullable=False)
    
    # Export Information
    export_name: Mapped[str] = mapped_column(String(200), nullable=False)
    export_type: Mapped[str] = mapped_column(String(50), nullable=False)  # report, dashboard, data
    
    # Export Configuration
    query_config: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    format_config: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)  # PDF, Excel, CSV
    
    # Status
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, processing, completed, failed
    file_path: Mapped[str] = mapped_column(String(500), nullable=True)
    file_size: Mapped[int] = mapped_column(Integer, default=0)  # Bytes
    
    # Request Information
    requested_by: Mapped[str] = mapped_column(UUIDString, nullable=False)
    requested_by_type: Mapped[str] = mapped_column(String(20), nullable=False)
    
    # Timing
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    processing_time: Mapped[int] = mapped_column(Integer, default=0)  # Seconds
    
    # Error Information
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("ix_analytics_exports_tenant_id", "tenant_id"),
        Index("ix_analytics_exports_export_type", "export_type"),
        Index("ix_analytics_exports_status", "status"),
        Index("ix_analytics_exports_requested_by", "requested_by"),
    ) 