import { apiService, ApiResponse } from './api';

// Analytics Types
export interface AnalyticsData {
  id: string;
  metricName: string;
  metricValue: number;
  metricUnit: string;
  category: string;
  subcategory?: string;
  date: string;
  period: 'daily' | 'weekly' | 'monthly' | 'quarterly' | 'yearly';
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface Dashboard {
  id: string;
  name: string;
  description: string;
  dashboardType: 'academic' | 'financial' | 'attendance' | 'transport' | 'library' | 'general';
  widgets: DashboardWidget[];
  isActive: boolean;
  schoolId: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}

export interface DashboardWidget {
  id: string;
  dashboardId: string;
  widgetType: 'chart' | 'table' | 'metric' | 'list' | 'gauge';
  title: string;
  dataSource: string;
  config: any;
  position: {
    x: number;
    y: number;
    width: number;
    height: number;
  };
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Report {
  id: string;
  name: string;
  description: string;
  reportType: 'academic' | 'financial' | 'attendance' | 'transport' | 'library' | 'custom';
  template: string;
  parameters: any;
  schedule?: string;
  recipients: string[];
  status: 'draft' | 'scheduled' | 'generated' | 'sent';
  generatedAt?: string;
  fileUrl?: string;
  schoolId: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}

export interface PerformanceMetric {
  id: string;
  studentId: string;
  classId: string;
  subjectId: string;
  metricType: 'attendance' | 'academic' | 'behavior' | 'participation';
  value: number;
  maxValue: number;
  percentage: number;
  grade?: string;
  period: string;
  academicYear: string;
  semester?: string;
  createdAt: string;
  updatedAt: string;
}

export interface AnalyticsFilters {
  metricName?: string;
  category?: string;
  dateFrom?: string;
  dateTo?: string;
  period?: string;
  schoolId?: string;
}

export interface AnalyticsListResponse {
  analytics: AnalyticsData[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Analytics Service class
export class AnalyticsService {
  private readonly ANALYTICS_ENDPOINTS = {
    ANALYTICS: '/api/v1/analytics/data',
    DASHBOARDS: '/api/v1/analytics/dashboards',
    REPORTS: '/api/v1/analytics/reports',
    METRICS: '/api/v1/analytics/metrics',
    INSIGHTS: '/api/v1/analytics/insights',
    EXPORTS: '/api/v1/analytics/exports',
  };

  // Get analytics data
  async getAnalyticsData(filters?: AnalyticsFilters): Promise<AnalyticsListResponse> {
    const response = await apiService.get<AnalyticsListResponse>(this.ANALYTICS_ENDPOINTS.ANALYTICS, filters);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch analytics data');
  }

  // Get analytics data by ID
  async getAnalyticsDataById(id: string): Promise<AnalyticsData> {
    const response = await apiService.get<AnalyticsData>(`${this.ANALYTICS_ENDPOINTS.ANALYTICS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch analytics data');
  }

  // Create analytics data
  async createAnalyticsData(data: Partial<AnalyticsData>): Promise<AnalyticsData> {
    const response = await apiService.post<AnalyticsData>(this.ANALYTICS_ENDPOINTS.ANALYTICS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create analytics data');
  }

  // Update analytics data
  async updateAnalyticsData(id: string, data: Partial<AnalyticsData>): Promise<AnalyticsData> {
    const response = await apiService.put<AnalyticsData>(`${this.ANALYTICS_ENDPOINTS.ANALYTICS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update analytics data');
  }

  // Delete analytics data
  async deleteAnalyticsData(id: string): Promise<void> {
    const response = await apiService.delete(`${this.ANALYTICS_ENDPOINTS.ANALYTICS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete analytics data');
    }
  }

  // Get dashboards
  async getDashboards(schoolId?: string): Promise<Dashboard[]> {
    const params = schoolId ? { schoolId } : {};
    const response = await apiService.get<Dashboard[]>(this.ANALYTICS_ENDPOINTS.DASHBOARDS, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch dashboards');
  }

  // Get dashboard by ID
  async getDashboard(id: string): Promise<Dashboard> {
    const response = await apiService.get<Dashboard>(`${this.ANALYTICS_ENDPOINTS.DASHBOARDS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch dashboard');
  }

  // Create dashboard
  async createDashboard(data: Partial<Dashboard>): Promise<Dashboard> {
    const response = await apiService.post<Dashboard>(this.ANALYTICS_ENDPOINTS.DASHBOARDS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create dashboard');
  }

  // Update dashboard
  async updateDashboard(id: string, data: Partial<Dashboard>): Promise<Dashboard> {
    const response = await apiService.put<Dashboard>(`${this.ANALYTICS_ENDPOINTS.DASHBOARDS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update dashboard');
  }

  // Delete dashboard
  async deleteDashboard(id: string): Promise<void> {
    const response = await apiService.delete(`${this.ANALYTICS_ENDPOINTS.DASHBOARDS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete dashboard');
    }
  }

  // Get dashboard widgets
  async getDashboardWidgets(dashboardId: string): Promise<DashboardWidget[]> {
    const response = await apiService.get<DashboardWidget[]>(`${this.ANALYTICS_ENDPOINTS.DASHBOARDS}/${dashboardId}/widgets`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch dashboard widgets');
  }

  // Create dashboard widget
  async createDashboardWidget(dashboardId: string, data: Partial<DashboardWidget>): Promise<DashboardWidget> {
    const response = await apiService.post<DashboardWidget>(`${this.ANALYTICS_ENDPOINTS.DASHBOARDS}/${dashboardId}/widgets`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create dashboard widget');
  }

  // Update dashboard widget
  async updateDashboardWidget(dashboardId: string, widgetId: string, data: Partial<DashboardWidget>): Promise<DashboardWidget> {
    const response = await apiService.put<DashboardWidget>(`${this.ANALYTICS_ENDPOINTS.DASHBOARDS}/${dashboardId}/widgets/${widgetId}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update dashboard widget');
  }

  // Delete dashboard widget
  async deleteDashboardWidget(dashboardId: string, widgetId: string): Promise<void> {
    const response = await apiService.delete(`${this.ANALYTICS_ENDPOINTS.DASHBOARDS}/${dashboardId}/widgets/${widgetId}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete dashboard widget');
    }
  }

  // Get reports
  async getReports(filters?: any): Promise<Report[]> {
    const response = await apiService.get<Report[]>(this.ANALYTICS_ENDPOINTS.REPORTS, filters);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch reports');
  }

  // Get report by ID
  async getReport(id: string): Promise<Report> {
    const response = await apiService.get<Report>(`${this.ANALYTICS_ENDPOINTS.REPORTS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch report');
  }

  // Create report
  async createReport(data: Partial<Report>): Promise<Report> {
    const response = await apiService.post<Report>(this.ANALYTICS_ENDPOINTS.REPORTS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create report');
  }

  // Update report
  async updateReport(id: string, data: Partial<Report>): Promise<Report> {
    const response = await apiService.put<Report>(`${this.ANALYTICS_ENDPOINTS.REPORTS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update report');
  }

  // Delete report
  async deleteReport(id: string): Promise<void> {
    const response = await apiService.delete(`${this.ANALYTICS_ENDPOINTS.REPORTS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete report');
    }
  }

  // Generate report
  async generateReport(id: string): Promise<Report> {
    const response = await apiService.post<Report>(`${this.ANALYTICS_ENDPOINTS.REPORTS}/${id}/generate`, {});
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to generate report');
  }

  // Get performance metrics
  async getPerformanceMetrics(studentId?: string, filters?: any): Promise<PerformanceMetric[]> {
    const params = { ...filters, studentId };
    const response = await apiService.get<PerformanceMetric[]>(this.ANALYTICS_ENDPOINTS.METRICS, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch performance metrics');
  }

  // Get performance metric by ID
  async getPerformanceMetric(id: string): Promise<PerformanceMetric> {
    const response = await apiService.get<PerformanceMetric>(`${this.ANALYTICS_ENDPOINTS.METRICS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch performance metric');
  }

  // Create performance metric
  async createPerformanceMetric(data: Partial<PerformanceMetric>): Promise<PerformanceMetric> {
    const response = await apiService.post<PerformanceMetric>(this.ANALYTICS_ENDPOINTS.METRICS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create performance metric');
  }

  // Update performance metric
  async updatePerformanceMetric(id: string, data: Partial<PerformanceMetric>): Promise<PerformanceMetric> {
    const response = await apiService.put<PerformanceMetric>(`${this.ANALYTICS_ENDPOINTS.METRICS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update performance metric');
  }

  // Delete performance metric
  async deletePerformanceMetric(id: string): Promise<void> {
    const response = await apiService.delete(`${this.ANALYTICS_ENDPOINTS.METRICS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete performance metric');
    }
  }

  // Get insights
  async getInsights(schoolId?: string, filters?: any): Promise<any> {
    const params = { ...filters, schoolId };
    const response = await apiService.get<any>(this.ANALYTICS_ENDPOINTS.INSIGHTS, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch insights');
  }

  // Get analytics summary
  async getAnalyticsSummary(schoolId?: string): Promise<any> {
    const params = schoolId ? { schoolId } : {};
    const response = await apiService.get<any>(`${this.ANALYTICS_ENDPOINTS.ANALYTICS}/summary`, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch analytics summary');
  }

  // Export analytics data
  async exportAnalyticsData(format: 'csv' | 'excel' | 'pdf', filters?: any): Promise<any> {
    const params = { ...filters, format };
    const response = await apiService.get<any>(this.ANALYTICS_ENDPOINTS.EXPORTS, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to export analytics data');
  }

  // Get real-time analytics
  async getRealTimeAnalytics(schoolId?: string): Promise<any> {
    const params = schoolId ? { schoolId } : {};
    const response = await apiService.get<any>(`${this.ANALYTICS_ENDPOINTS.ANALYTICS}/realtime`, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch real-time analytics');
  }
}

// Export singleton instance
export const analyticsService = new AnalyticsService();
export default analyticsService; 