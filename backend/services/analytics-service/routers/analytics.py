"""
Analytics router for Analytics Service (AI SchoolOS)
"""

import logging
from typing import List, Optional
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from decimal import Decimal

from database import get_db
from models import AnalyticsData, Report, ReportExecution, Dashboard, Metric, MetricValue, Insight, AnalyticsJob, AnalyticsExport
from schemas import (
    AnalyticsDataCreate, AnalyticsDataUpdate, AnalyticsDataResponse, AnalyticsDataListResponse,
    ReportCreate, ReportUpdate, ReportResponse, ReportListResponse,
    ReportExecutionCreate, ReportExecutionUpdate, ReportExecutionResponse, ReportExecutionListResponse,
    DashboardCreate, DashboardUpdate, DashboardResponse, DashboardListResponse,
    MetricCreate, MetricUpdate, MetricResponse, MetricListResponse,
    MetricValueCreate, MetricValueUpdate, MetricValueResponse, MetricValueListResponse,
    InsightCreate, InsightUpdate, InsightResponse, InsightListResponse,
    AnalyticsJobCreate, AnalyticsJobUpdate, AnalyticsJobResponse, AnalyticsJobListResponse,
    AnalyticsExportCreate, AnalyticsExportUpdate, AnalyticsExportResponse, AnalyticsExportListResponse,
    AnalyticsSummary, ReportSummary, DashboardSummary, MetricSummary
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/analytics", tags=["analytics"])


# Analytics Data CRUD Operations
@router.post("/data", response_model=AnalyticsDataResponse)
async def create_analytics_data(
    data: AnalyticsDataCreate,
    db: Session = Depends(get_db)
):
    """Create new analytics data."""
    try:
        # Create new analytics data
        analytics_data = AnalyticsData(**data.dict())
        db.add(analytics_data)
        db.commit()
        db.refresh(analytics_data)
        
        logger.info(f"New analytics data created: {analytics_data.data_type}")
        return analytics_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating analytics data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/data", response_model=AnalyticsDataListResponse)
async def get_analytics_data(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    data_type: Optional[str] = None,
    data_source: Optional[str] = None,
    data_period: Optional[str] = None,
    is_processed: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get analytics data with filtering and pagination."""
    try:
        query = db.query(AnalyticsData)
        
        # Apply filters
        if tenant_id:
            query = query.filter(AnalyticsData.tenant_id == tenant_id)
        
        if data_type:
            query = query.filter(AnalyticsData.data_type == data_type)
        
        if data_source:
            query = query.filter(AnalyticsData.data_source == data_source)
        
        if data_period:
            query = query.filter(AnalyticsData.data_period == data_period)
        
        if is_processed is not None:
            query = query.filter(AnalyticsData.is_processed == is_processed)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        analytics_data = query.offset(skip).limit(limit).all()
        
        return AnalyticsDataListResponse(
            analytics_data=analytics_data,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting analytics data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Report CRUD Operations
@router.post("/reports", response_model=ReportResponse)
async def create_report(
    report_data: ReportCreate,
    db: Session = Depends(get_db)
):
    """Create a new report."""
    try:
        # Create new report
        report = Report(**report_data.dict())
        db.add(report)
        db.commit()
        db.refresh(report)
        
        logger.info(f"New report created: {report.name}")
        return report
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/reports", response_model=ReportListResponse)
async def get_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    report_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_public: Optional[bool] = None,
    created_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get reports with filtering and pagination."""
    try:
        query = db.query(Report)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Report.tenant_id == tenant_id)
        
        if report_type:
            query = query.filter(Report.report_type == report_type)
        
        if is_active is not None:
            query = query.filter(Report.is_active == is_active)
        
        if is_public is not None:
            query = query.filter(Report.is_public == is_public)
        
        if created_by:
            query = query.filter(Report.created_by == created_by)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        reports = query.offset(skip).limit(limit).all()
        
        return ReportListResponse(
            reports=reports,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting reports: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/reports/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific report by ID."""
    try:
        report = db.query(Report).filter(Report.id == report_id).first()
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        return report
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.put("/reports/{report_id}", response_model=ReportResponse)
async def update_report(
    report_id: str,
    report_data: ReportUpdate,
    db: Session = Depends(get_db)
):
    """Update a report."""
    try:
        report = db.query(Report).filter(Report.id == report_id).first()
        
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        # Update fields
        update_data = report_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(report, field, value)
        
        report.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(report)
        
        logger.info(f"Report updated: {report.name}")
        return report
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Report Execution Operations
@router.post("/reports/{report_id}/execute", response_model=ReportExecutionResponse)
async def execute_report(
    report_id: str,
    execution_data: ReportExecutionCreate,
    db: Session = Depends(get_db)
):
    """Execute a report."""
    try:
        # Check if report exists
        report = db.query(Report).filter(Report.id == report_id).first()
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Report not found"
            )
        
        # Create execution record
        execution = ReportExecution(**execution_data.dict())
        execution.started_at = datetime.utcnow()
        db.add(execution)
        db.commit()
        db.refresh(execution)
        
        logger.info(f"Report execution started: {report.name}")
        return execution
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error executing report: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/reports/{report_id}/executions", response_model=ReportExecutionListResponse)
async def get_report_executions(
    report_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    execution_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get executions for a specific report."""
    try:
        query = db.query(ReportExecution).filter(ReportExecution.report_id == report_id)
        
        if execution_status:
            query = query.filter(ReportExecution.execution_status == execution_status)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        executions = query.order_by(ReportExecution.created_at.desc()).offset(skip).limit(limit).all()
        
        return ReportExecutionListResponse(
            executions=executions,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting report executions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Dashboard CRUD Operations
@router.post("/dashboards", response_model=DashboardResponse)
async def create_dashboard(
    dashboard_data: DashboardCreate,
    db: Session = Depends(get_db)
):
    """Create a new dashboard."""
    try:
        # Create new dashboard
        dashboard = Dashboard(**dashboard_data.dict())
        db.add(dashboard)
        db.commit()
        db.refresh(dashboard)
        
        logger.info(f"New dashboard created: {dashboard.name}")
        return dashboard
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating dashboard: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/dashboards", response_model=DashboardListResponse)
async def get_dashboards(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    dashboard_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_public: Optional[bool] = None,
    created_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get dashboards with filtering and pagination."""
    try:
        query = db.query(Dashboard)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Dashboard.tenant_id == tenant_id)
        
        if dashboard_type:
            query = query.filter(Dashboard.dashboard_type == dashboard_type)
        
        if is_active is not None:
            query = query.filter(Dashboard.is_active == is_active)
        
        if is_public is not None:
            query = query.filter(Dashboard.is_public == is_public)
        
        if created_by:
            query = query.filter(Dashboard.created_by == created_by)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        dashboards = query.offset(skip).limit(limit).all()
        
        return DashboardListResponse(
            dashboards=dashboards,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting dashboards: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Metric CRUD Operations
@router.post("/metrics", response_model=MetricResponse)
async def create_metric(
    metric_data: MetricCreate,
    db: Session = Depends(get_db)
):
    """Create a new metric."""
    try:
        # Create new metric
        metric = Metric(**metric_data.dict())
        db.add(metric)
        db.commit()
        db.refresh(metric)
        
        logger.info(f"New metric created: {metric.name}")
        return metric
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating metric: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/metrics", response_model=MetricListResponse)
async def get_metrics(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    metric_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_system: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get metrics with filtering and pagination."""
    try:
        query = db.query(Metric)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Metric.tenant_id == tenant_id)
        
        if metric_type:
            query = query.filter(Metric.metric_type == metric_type)
        
        if is_active is not None:
            query = query.filter(Metric.is_active == is_active)
        
        if is_system is not None:
            query = query.filter(Metric.is_system == is_system)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        metrics = query.offset(skip).limit(limit).all()
        
        return MetricListResponse(
            metrics=metrics,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting metrics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Metric Value Operations
@router.post("/metrics/{metric_id}/values", response_model=MetricValueResponse)
async def create_metric_value(
    metric_id: str,
    value_data: MetricValueCreate,
    db: Session = Depends(get_db)
):
    """Create a new metric value."""
    try:
        # Check if metric exists
        metric = db.query(Metric).filter(Metric.id == metric_id).first()
        if not metric:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Metric not found"
            )
        
        # Create new metric value
        metric_value = MetricValue(**value_data.dict())
        db.add(metric_value)
        db.commit()
        db.refresh(metric_value)
        
        logger.info(f"New metric value created for metric: {metric.name}")
        return metric_value
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating metric value: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/metrics/{metric_id}/values", response_model=MetricValueListResponse)
async def get_metric_values(
    metric_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Get values for a specific metric."""
    try:
        query = db.query(MetricValue).filter(MetricValue.metric_id == metric_id)
        
        if start_date:
            query = query.filter(MetricValue.period_start >= start_date)
        
        if end_date:
            query = query.filter(MetricValue.period_end <= end_date)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and order by period
        metric_values = query.order_by(MetricValue.period_start.desc()).offset(skip).limit(limit).all()
        
        return MetricValueListResponse(
            metric_values=metric_values,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting metric values: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Insight CRUD Operations
@router.post("/insights", response_model=InsightResponse)
async def create_insight(
    insight_data: InsightCreate,
    db: Session = Depends(get_db)
):
    """Create a new insight."""
    try:
        # Create new insight
        insight = Insight(**insight_data.dict())
        db.add(insight)
        db.commit()
        db.refresh(insight)
        
        logger.info(f"New insight created: {insight.title}")
        return insight
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating insight: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/insights", response_model=InsightListResponse)
async def get_insights(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    insight_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_acknowledged: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get insights with filtering and pagination."""
    try:
        query = db.query(Insight)
        
        # Apply filters
        if tenant_id:
            query = query.filter(Insight.tenant_id == tenant_id)
        
        if insight_type:
            query = query.filter(Insight.insight_type == insight_type)
        
        if is_active is not None:
            query = query.filter(Insight.is_active == is_active)
        
        if is_acknowledged is not None:
            query = query.filter(Insight.is_acknowledged == is_acknowledged)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        insights = query.order_by(Insight.created_at.desc()).offset(skip).limit(limit).all()
        
        return InsightListResponse(
            insights=insights,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting insights: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Analytics Job Operations
@router.post("/jobs", response_model=AnalyticsJobResponse)
async def create_job(
    job_data: AnalyticsJobCreate,
    db: Session = Depends(get_db)
):
    """Create a new analytics job."""
    try:
        # Create new job
        job = AnalyticsJob(**job_data.dict())
        db.add(job)
        db.commit()
        db.refresh(job)
        
        logger.info(f"New analytics job created: {job.job_name}")
        return job
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating job: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/jobs", response_model=AnalyticsJobListResponse)
async def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    job_type: Optional[str] = None,
    status: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get analytics jobs with filtering and pagination."""
    try:
        query = db.query(AnalyticsJob)
        
        # Apply filters
        if tenant_id:
            query = query.filter(AnalyticsJob.tenant_id == tenant_id)
        
        if job_type:
            query = query.filter(AnalyticsJob.job_type == job_type)
        
        if status:
            query = query.filter(AnalyticsJob.status == status)
        
        if is_active is not None:
            query = query.filter(AnalyticsJob.is_active == is_active)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        jobs = query.offset(skip).limit(limit).all()
        
        return AnalyticsJobListResponse(
            jobs=jobs,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting jobs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Analytics Export Operations
@router.post("/exports", response_model=AnalyticsExportResponse)
async def create_export(
    export_data: AnalyticsExportCreate,
    db: Session = Depends(get_db)
):
    """Create a new analytics export."""
    try:
        # Create new export
        export = AnalyticsExport(**export_data.dict())
        db.add(export)
        db.commit()
        db.refresh(export)
        
        logger.info(f"New analytics export created: {export.export_name}")
        return export
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating export: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/exports", response_model=AnalyticsExportListResponse)
async def get_exports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    tenant_id: Optional[str] = None,
    export_type: Optional[str] = None,
    status: Optional[str] = None,
    requested_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get analytics exports with filtering and pagination."""
    try:
        query = db.query(AnalyticsExport)
        
        # Apply filters
        if tenant_id:
            query = query.filter(AnalyticsExport.tenant_id == tenant_id)
        
        if export_type:
            query = query.filter(AnalyticsExport.export_type == export_type)
        
        if status:
            query = query.filter(AnalyticsExport.status == status)
        
        if requested_by:
            query = query.filter(AnalyticsExport.requested_by == requested_by)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        exports = query.order_by(AnalyticsExport.created_at.desc()).offset(skip).limit(limit).all()
        
        return AnalyticsExportListResponse(
            exports=exports,
            total=total,
            page=skip // limit + 1,
            size=limit
        )
        
    except Exception as e:
        logger.error(f"Error getting exports: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Summary Endpoints
@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    tenant_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get analytics summary statistics."""
    try:
        # Build base queries
        reports_query = db.query(Report)
        dashboards_query = db.query(Dashboard)
        metrics_query = db.query(Metric)
        insights_query = db.query(Insight)
        jobs_query = db.query(AnalyticsJob)
        exports_query = db.query(AnalyticsExport)
        
        # Apply filters
        if tenant_id:
            reports_query = reports_query.filter(Report.tenant_id == tenant_id)
            dashboards_query = dashboards_query.filter(Dashboard.tenant_id == tenant_id)
            metrics_query = metrics_query.filter(Metric.tenant_id == tenant_id)
            insights_query = insights_query.filter(Insight.tenant_id == tenant_id)
            jobs_query = jobs_query.filter(AnalyticsJob.tenant_id == tenant_id)
            exports_query = exports_query.filter(AnalyticsExport.tenant_id == tenant_id)
        
        # Get statistics
        total_reports = reports_query.count()
        active_reports = reports_query.filter(Report.is_active == True).count()
        total_dashboards = dashboards_query.count()
        active_dashboards = dashboards_query.filter(Dashboard.is_active == True).count()
        total_metrics = metrics_query.count()
        active_metrics = metrics_query.filter(Metric.is_active == True).count()
        total_insights = insights_query.count()
        active_insights = insights_query.filter(Insight.is_active == True).count()
        total_jobs = jobs_query.count()
        running_jobs = jobs_query.filter(AnalyticsJob.status == "running").count()
        total_exports = exports_query.count()
        pending_exports = exports_query.filter(AnalyticsExport.status == "pending").count()
        
        return AnalyticsSummary(
            total_reports=total_reports,
            active_reports=active_reports,
            total_dashboards=total_dashboards,
            active_dashboards=active_dashboards,
            total_metrics=total_metrics,
            active_metrics=active_metrics,
            total_insights=total_insights,
            active_insights=active_insights,
            total_jobs=total_jobs,
            running_jobs=running_jobs,
            total_exports=total_exports,
            pending_exports=pending_exports
        )
        
    except Exception as e:
        logger.error(f"Error getting analytics summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        ) 