"""
Pydantic schemas for Analytics Service (AI SchoolOS)
"""

from datetime import datetime, date
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from decimal import Decimal


# Analytics Data schemas
class AnalyticsDataBase(BaseModel):
    data_type: str = Field(..., min_length=1, max_length=50)
    data_source: str = Field(..., min_length=1, max_length=50)
    data_period: str = Field(..., min_length=1, max_length=20)
    metrics: Optional[Dict[str, Any]] = {}
    dimensions: Optional[Dict[str, Any]] = {}
    aggregations: Optional[Dict[str, Any]] = {}
    start_date: date
    end_date: date
    collected_at: datetime
    is_processed: bool = False
    is_valid: bool = True


class AnalyticsDataCreate(AnalyticsDataBase):
    tenant_id: str


class AnalyticsDataUpdate(BaseModel):
    metrics: Optional[Dict[str, Any]] = None
    dimensions: Optional[Dict[str, Any]] = None
    aggregations: Optional[Dict[str, Any]] = None
    is_processed: Optional[bool] = None
    is_valid: Optional[bool] = None


class AnalyticsDataResponse(AnalyticsDataBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnalyticsDataListResponse(BaseModel):
    analytics_data: List[AnalyticsDataResponse]
    total: int
    page: int
    size: int


# Report schemas
class ReportBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    report_type: str = Field(..., min_length=1, max_length=50)
    query_config: Optional[Dict[str, Any]] = {}
    visualization_config: Optional[Dict[str, Any]] = {}
    filters: Optional[Dict[str, Any]] = {}
    is_scheduled: bool = False
    schedule_frequency: Optional[str] = Field(None, max_length=20)
    is_active: bool = True
    is_public: bool = False
    created_by: str
    created_by_type: str = Field(..., min_length=1, max_length=20)


class ReportCreate(ReportBase):
    tenant_id: str


class ReportUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    report_type: Optional[str] = Field(None, min_length=1, max_length=50)
    query_config: Optional[Dict[str, Any]] = None
    visualization_config: Optional[Dict[str, Any]] = None
    filters: Optional[Dict[str, Any]] = None
    is_scheduled: Optional[bool] = None
    schedule_frequency: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None
    is_public: Optional[bool] = None
    last_generated: Optional[datetime] = None
    next_generation: Optional[datetime] = None


class ReportResponse(ReportBase):
    id: str
    tenant_id: str
    last_generated: Optional[datetime] = None
    next_generation: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ReportListResponse(BaseModel):
    reports: List[ReportResponse]
    total: int
    page: int
    size: int


# Report Execution schemas
class ReportExecutionBase(BaseModel):
    report_id: str
    execution_status: str = Field("pending", max_length=20)
    execution_type: str = Field("manual", max_length=20)
    execution_params: Optional[Dict[str, Any]] = {}


class ReportExecutionCreate(ReportExecutionBase):
    pass


class ReportExecutionUpdate(BaseModel):
    execution_status: Optional[str] = Field(None, max_length=20)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time: Optional[int] = Field(None, ge=0)
    result_data: Optional[Dict[str, Any]] = None
    result_file_path: Optional[str] = Field(None, max_length=500)
    error_message: Optional[str] = None


class ReportExecutionResponse(ReportExecutionBase):
    id: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    execution_time: int
    result_data: Dict[str, Any]
    result_file_path: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ReportExecutionListResponse(BaseModel):
    executions: List[ReportExecutionResponse]
    total: int
    page: int
    size: int


# Dashboard schemas
class DashboardBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    dashboard_type: str = Field(..., min_length=1, max_length=50)
    layout_config: Optional[Dict[str, Any]] = {}
    widget_configs: Optional[Dict[str, Any]] = {}
    is_active: bool = True
    is_public: bool = False
    refresh_interval: int = Field(300, ge=30, le=3600)
    created_by: str
    created_by_type: str = Field(..., min_length=1, max_length=20)


class DashboardCreate(DashboardBase):
    tenant_id: str


class DashboardUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    dashboard_type: Optional[str] = Field(None, min_length=1, max_length=50)
    layout_config: Optional[Dict[str, Any]] = None
    widget_configs: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_public: Optional[bool] = None
    refresh_interval: Optional[int] = Field(None, ge=30, le=3600)


class DashboardResponse(DashboardBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DashboardListResponse(BaseModel):
    dashboards: List[DashboardResponse]
    total: int
    page: int
    size: int


# Metric schemas
class MetricBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    metric_type: str = Field(..., min_length=1, max_length=50)
    calculation_formula: str = Field(..., min_length=1)
    data_source: str = Field(..., min_length=1, max_length=50)
    aggregation_period: str = Field("daily", max_length=20)
    display_name: str = Field(..., min_length=1, max_length=100)
    unit: Optional[str] = Field(None, max_length=20)
    decimal_places: int = Field(2, ge=0, le=10)
    is_active: bool = True
    is_system: bool = False


class MetricCreate(MetricBase):
    tenant_id: str


class MetricUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    metric_type: Optional[str] = Field(None, min_length=1, max_length=50)
    calculation_formula: Optional[str] = Field(None, min_length=1)
    data_source: Optional[str] = Field(None, min_length=1, max_length=50)
    aggregation_period: Optional[str] = Field(None, max_length=20)
    display_name: Optional[str] = Field(None, min_length=1, max_length=100)
    unit: Optional[str] = Field(None, max_length=20)
    decimal_places: Optional[int] = Field(None, ge=0, le=10)
    is_active: Optional[bool] = None
    is_system: Optional[bool] = None


class MetricResponse(MetricBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MetricListResponse(BaseModel):
    metrics: List[MetricResponse]
    total: int
    page: int
    size: int


# Metric Value schemas
class MetricValueBase(BaseModel):
    metric_id: str
    value: Decimal = Field(..., ge=0)
    period_start: datetime
    period_end: datetime
    dimensions: Optional[Dict[str, Any]] = {}
    metadata: Optional[Dict[str, Any]] = {}


class MetricValueCreate(MetricValueBase):
    tenant_id: str


class MetricValueUpdate(BaseModel):
    value: Optional[Decimal] = Field(None, ge=0)
    dimensions: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class MetricValueResponse(MetricValueBase):
    id: str
    tenant_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class MetricValueListResponse(BaseModel):
    metric_values: List[MetricValueResponse]
    total: int
    page: int
    size: int


# Insight schemas
class InsightBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    insight_type: str = Field(..., min_length=1, max_length=50)
    data_points: Optional[Dict[str, Any]] = {}
    confidence_score: Decimal = Field(0.0, ge=0, le=100)
    impact_score: Decimal = Field(0.0, ge=0, le=100)
    is_active: bool = True
    is_acknowledged: bool = False


class InsightCreate(InsightBase):
    tenant_id: str


class InsightUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    insight_type: Optional[str] = Field(None, min_length=1, max_length=50)
    data_points: Optional[Dict[str, Any]] = None
    confidence_score: Optional[Decimal] = Field(None, ge=0, le=100)
    impact_score: Optional[Decimal] = Field(None, ge=0, le=100)
    is_active: Optional[bool] = None
    is_acknowledged: Optional[bool] = None
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None


class InsightResponse(InsightBase):
    id: str
    tenant_id: str
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InsightListResponse(BaseModel):
    insights: List[InsightResponse]
    total: int
    page: int
    size: int


# Analytics Job schemas
class AnalyticsJobBase(BaseModel):
    job_name: str = Field(..., min_length=1, max_length=100)
    job_type: str = Field(..., min_length=1, max_length=50)
    job_config: Optional[Dict[str, Any]] = {}
    schedule_config: Optional[Dict[str, Any]] = {}
    status: str = Field("pending", max_length=20)
    is_active: bool = True
    retry_count: int = Field(0, ge=0)
    max_retries: int = Field(3, ge=0, le=10)


class AnalyticsJobCreate(AnalyticsJobBase):
    tenant_id: str


class AnalyticsJobUpdate(BaseModel):
    job_name: Optional[str] = Field(None, min_length=1, max_length=100)
    job_type: Optional[str] = Field(None, min_length=1, max_length=50)
    job_config: Optional[Dict[str, Any]] = None
    schedule_config: Optional[Dict[str, Any]] = None
    status: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    last_result: Optional[Dict[str, Any]] = None
    error_count: Optional[int] = Field(None, ge=0)
    success_count: Optional[int] = Field(None, ge=0)
    retry_count: Optional[int] = Field(None, ge=0)
    max_retries: Optional[int] = Field(None, ge=0, le=10)


class AnalyticsJobResponse(AnalyticsJobBase):
    id: str
    tenant_id: str
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    last_result: Dict[str, Any]
    error_count: int
    success_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnalyticsJobListResponse(BaseModel):
    jobs: List[AnalyticsJobResponse]
    total: int
    page: int
    size: int


# Analytics Export schemas
class AnalyticsExportBase(BaseModel):
    export_name: str = Field(..., min_length=1, max_length=200)
    export_type: str = Field(..., min_length=1, max_length=50)
    query_config: Optional[Dict[str, Any]] = {}
    format_config: Optional[Dict[str, Any]] = {}
    status: str = Field("pending", max_length=20)
    requested_by: str
    requested_by_type: str = Field(..., min_length=1, max_length=20)


class AnalyticsExportCreate(AnalyticsExportBase):
    tenant_id: str


class AnalyticsExportUpdate(BaseModel):
    export_name: Optional[str] = Field(None, min_length=1, max_length=200)
    export_type: Optional[str] = Field(None, min_length=1, max_length=50)
    query_config: Optional[Dict[str, Any]] = None
    format_config: Optional[Dict[str, Any]] = None
    status: Optional[str] = Field(None, max_length=20)
    file_path: Optional[str] = Field(None, max_length=500)
    file_size: Optional[int] = Field(None, ge=0)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    processing_time: Optional[int] = Field(None, ge=0)
    error_message: Optional[str] = None


class AnalyticsExportResponse(AnalyticsExportBase):
    id: str
    tenant_id: str
    file_path: Optional[str] = None
    file_size: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    processing_time: int
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnalyticsExportListResponse(BaseModel):
    exports: List[AnalyticsExportResponse]
    total: int
    page: int
    size: int


# Summary schemas
class AnalyticsSummary(BaseModel):
    total_reports: int
    active_reports: int
    total_dashboards: int
    active_dashboards: int
    total_metrics: int
    active_metrics: int
    total_insights: int
    active_insights: int
    total_jobs: int
    running_jobs: int
    total_exports: int
    pending_exports: int


class ReportSummary(BaseModel):
    report_id: str
    report_name: str
    report_type: str
    execution_count: int
    last_execution: Optional[datetime] = None
    average_execution_time: int
    success_rate: Decimal
    is_active: bool
    created_at: datetime


class DashboardSummary(BaseModel):
    dashboard_id: str
    dashboard_name: str
    dashboard_type: str
    widget_count: int
    refresh_interval: int
    is_active: bool
    is_public: bool
    created_at: datetime


class MetricSummary(BaseModel):
    metric_id: str
    metric_name: str
    metric_type: str
    data_points_count: int
    last_updated: Optional[datetime] = None
    average_value: Decimal
    trend_direction: str  # up, down, stable
    is_active: bool
    created_at: datetime 