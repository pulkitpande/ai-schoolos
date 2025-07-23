import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Service URLs
const SERVICE_URLS = {
  auth: process.env.NEXT_PUBLIC_AUTH_SERVICE_URL || 'http://localhost:8001',
  student: process.env.NEXT_PUBLIC_STUDENT_SERVICE_URL || 'http://localhost:8002',
  staff: process.env.NEXT_PUBLIC_STAFF_SERVICE_URL || 'http://localhost:8003',
  fee: process.env.NEXT_PUBLIC_FEE_SERVICE_URL || 'http://localhost:8004',
  homework: process.env.NEXT_PUBLIC_HOMEWORK_SERVICE_URL || 'http://localhost:8005',
  library: process.env.NEXT_PUBLIC_LIBRARY_SERVICE_URL || 'http://localhost:8006',
  exam: process.env.NEXT_PUBLIC_EXAM_SERVICE_URL || 'http://localhost:8007',
  timetable: process.env.NEXT_PUBLIC_TIMETABLE_SERVICE_URL || 'http://localhost:8008',
  attendance: process.env.NEXT_PUBLIC_ATTENDANCE_SERVICE_URL || 'http://localhost:8009',
  transport: process.env.NEXT_PUBLIC_TRANSPORT_SERVICE_URL || 'http://localhost:8010',
  communication: process.env.NEXT_PUBLIC_COMMUNICATION_SERVICE_URL || 'http://localhost:8011',
  analytics: process.env.NEXT_PUBLIC_ANALYTICS_SERVICE_URL || 'http://localhost:8012',
  notification: process.env.NEXT_PUBLIC_NOTIFICATION_SERVICE_URL || 'http://localhost:8013',
  config: process.env.NEXT_PUBLIC_CONFIG_SERVICE_URL || 'http://localhost:8014',
  superAdmin: process.env.NEXT_PUBLIC_SUPER_ADMIN_SERVICE_URL || 'http://localhost:8015',
  ai: process.env.NEXT_PUBLIC_AI_SERVICE_URL || 'http://localhost:8016',
  aiAnalytics: process.env.NEXT_PUBLIC_AI_ANALYTICS_SERVICE_URL || 'http://localhost:8017',
};

// Create axios instance with default config
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Generic API response type
export interface ApiResponse<T = any> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
}

// Service-specific API clients
export const createServiceClient = (baseURL: string): AxiosInstance => {
  const client = axios.create({
    baseURL,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Add auth token to service requests
  client.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  return client;
};

// Export service clients
export const authClient = createServiceClient(SERVICE_URLS.auth);
export const studentClient = createServiceClient(SERVICE_URLS.student);
export const staffClient = createServiceClient(SERVICE_URLS.staff);
export const feeClient = createServiceClient(SERVICE_URLS.fee);
export const homeworkClient = createServiceClient(SERVICE_URLS.homework);
export const libraryClient = createServiceClient(SERVICE_URLS.library);
export const examClient = createServiceClient(SERVICE_URLS.exam);
export const timetableClient = createServiceClient(SERVICE_URLS.timetable);
export const attendanceClient = createServiceClient(SERVICE_URLS.attendance);
export const transportClient = createServiceClient(SERVICE_URLS.transport);
export const communicationClient = createServiceClient(SERVICE_URLS.communication);
export const analyticsClient = createServiceClient(SERVICE_URLS.analytics);
export const notificationClient = createServiceClient(SERVICE_URLS.notification);
export const configClient = createServiceClient(SERVICE_URLS.config);
export const superAdminClient = createServiceClient(SERVICE_URLS.superAdmin);
export const aiClient = createServiceClient(SERVICE_URLS.ai);
export const aiAnalyticsClient = createServiceClient(SERVICE_URLS.aiAnalytics);

// API Service class
export class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = apiClient;
  }

  // Generic GET request
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.get<ApiResponse<T>>(url, config);
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  // Generic POST request
  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.post<ApiResponse<T>>(url, data, config);
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  // Generic PUT request
  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.put<ApiResponse<T>>(url, data, config);
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  // Generic DELETE request
  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<ApiResponse<T>> {
    try {
      const response = await this.client.delete<ApiResponse<T>>(url, config);
      return response.data;
    } catch (error: any) {
      throw this.handleError(error);
    }
  }

  // Error handler
  private handleError(error: any): Error {
    if (error.response) {
      const message = error.response.data?.message || error.response.data?.error || 'An error occurred';
      return new Error(message);
    }
    return new Error(error.message || 'Network error');
  }
}

// Export singleton instance
export const apiService = new ApiService();
export default apiService; 