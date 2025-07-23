import { apiService, ApiResponse } from './api';

// Attendance Types
export interface Attendance {
  id: string;
  studentId: string;
  classId: string;
  subjectId?: string;
  date: string;
  status: 'present' | 'absent' | 'late' | 'excused' | 'half_day';
  timeIn?: string;
  timeOut?: string;
  remarks?: string;
  markedBy: string;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface AttendanceReport {
  id: string;
  studentId: string;
  classId: string;
  month: number;
  year: number;
  totalDays: number;
  presentDays: number;
  absentDays: number;
  lateDays: number;
  excusedDays: number;
  attendancePercentage: number;
  createdAt: string;
  updatedAt: string;
}

export interface AttendanceStats {
  totalStudents: number;
  presentToday: number;
  absentToday: number;
  lateToday: number;
  attendanceRate: number;
  date: string;
}

export interface AttendanceFilters {
  studentId?: string;
  classId?: string;
  subjectId?: string;
  dateFrom?: string;
  dateTo?: string;
  status?: string;
  schoolId?: string;
}

export interface AttendanceListResponse {
  attendance: Attendance[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Attendance Service class
export class AttendanceService {
  private readonly ATTENDANCE_ENDPOINTS = {
    ATTENDANCE: '/api/v1/attendance',
    REPORTS: '/api/v1/attendance/reports',
    STATS: '/api/v1/attendance/stats',
    STUDENT_ATTENDANCE: '/api/v1/attendance/students',
    CLASS_ATTENDANCE: '/api/v1/attendance/classes',
    BULK_MARK: '/api/v1/attendance/bulk',
  };

  // Get attendance records
  async getAttendance(filters?: AttendanceFilters): Promise<AttendanceListResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<AttendanceListResponse>(
      `${this.ATTENDANCE_ENDPOINTS.ATTENDANCE}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch attendance records');
  }

  // Get attendance by ID
  async getAttendanceRecord(id: string): Promise<Attendance> {
    const response = await apiService.get<Attendance>(`${this.ATTENDANCE_ENDPOINTS.ATTENDANCE}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch attendance record');
  }

  // Create attendance record
  async createAttendance(data: Partial<Attendance>): Promise<Attendance> {
    const response = await apiService.post<Attendance>(this.ATTENDANCE_ENDPOINTS.ATTENDANCE, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create attendance record');
  }

  // Update attendance record
  async updateAttendance(id: string, data: Partial<Attendance>): Promise<Attendance> {
    const response = await apiService.put<Attendance>(`${this.ATTENDANCE_ENDPOINTS.ATTENDANCE}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update attendance record');
  }

  // Delete attendance record
  async deleteAttendance(id: string): Promise<void> {
    const response = await apiService.delete(`${this.ATTENDANCE_ENDPOINTS.ATTENDANCE}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete attendance record');
    }
  }

  // Bulk mark attendance
  async bulkMarkAttendance(data: { classId: string; date: string; attendance: Array<{ studentId: string; status: string; remarks?: string }> }): Promise<Attendance[]> {
    const response = await apiService.post<Attendance[]>(this.ATTENDANCE_ENDPOINTS.BULK_MARK, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to bulk mark attendance');
  }

  // Get student attendance
  async getStudentAttendance(studentId: string, filters?: any): Promise<Attendance[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<Attendance[]>(
      `${this.ATTENDANCE_ENDPOINTS.STUDENT_ATTENDANCE}/${studentId}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch student attendance');
  }

  // Get class attendance
  async getClassAttendance(classId: string, date?: string): Promise<Attendance[]> {
    const params = new URLSearchParams();
    
    if (date) {
      params.append('date', date);
    }

    const response = await apiService.get<Attendance[]>(
      `${this.ATTENDANCE_ENDPOINTS.CLASS_ATTENDANCE}/${classId}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch class attendance');
  }

  // Get attendance reports
  async getAttendanceReports(studentId?: string, classId?: string, month?: number, year?: number): Promise<AttendanceReport[]> {
    const params = new URLSearchParams();
    
    if (studentId) {
      params.append('studentId', studentId);
    }
    
    if (classId) {
      params.append('classId', classId);
    }
    
    if (month) {
      params.append('month', month.toString());
    }
    
    if (year) {
      params.append('year', year.toString());
    }

    const response = await apiService.get<AttendanceReport[]>(
      `${this.ATTENDANCE_ENDPOINTS.REPORTS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch attendance reports');
  }

  // Get attendance report by ID
  async getAttendanceReport(id: string): Promise<AttendanceReport> {
    const response = await apiService.get<AttendanceReport>(`${this.ATTENDANCE_ENDPOINTS.REPORTS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch attendance report');
  }

  // Create attendance report
  async createAttendanceReport(data: Partial<AttendanceReport>): Promise<AttendanceReport> {
    const response = await apiService.post<AttendanceReport>(this.ATTENDANCE_ENDPOINTS.REPORTS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create attendance report');
  }

  // Update attendance report
  async updateAttendanceReport(id: string, data: Partial<AttendanceReport>): Promise<AttendanceReport> {
    const response = await apiService.put<AttendanceReport>(`${this.ATTENDANCE_ENDPOINTS.REPORTS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update attendance report');
  }

  // Delete attendance report
  async deleteAttendanceReport(id: string): Promise<void> {
    const response = await apiService.delete(`${this.ATTENDANCE_ENDPOINTS.REPORTS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete attendance report');
    }
  }

  // Get attendance stats
  async getAttendanceStats(schoolId?: string, date?: string): Promise<AttendanceStats> {
    const params = new URLSearchParams();
    
    if (schoolId) {
      params.append('schoolId', schoolId);
    }
    
    if (date) {
      params.append('date', date);
    }

    const response = await apiService.get<AttendanceStats>(
      `${this.ATTENDANCE_ENDPOINTS.STATS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch attendance stats');
  }

  // Get student attendance stats
  async getStudentAttendanceStats(studentId: string, dateFrom?: string, dateTo?: string): Promise<any> {
    const params = new URLSearchParams();
    
    if (dateFrom) {
      params.append('dateFrom', dateFrom);
    }
    
    if (dateTo) {
      params.append('dateTo', dateTo);
    }

    const response = await apiService.get<any>(
      `${this.ATTENDANCE_ENDPOINTS.STUDENT_ATTENDANCE}/${studentId}/stats?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch student attendance stats');
  }

  // Get class attendance stats
  async getClassAttendanceStats(classId: string, dateFrom?: string, dateTo?: string): Promise<any> {
    const params = new URLSearchParams();
    
    if (dateFrom) {
      params.append('dateFrom', dateFrom);
    }
    
    if (dateTo) {
      params.append('dateTo', dateTo);
    }

    const response = await apiService.get<any>(
      `${this.ATTENDANCE_ENDPOINTS.CLASS_ATTENDANCE}/${classId}/stats?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch class attendance stats');
  }

  // Get attendance analytics
  async getAttendanceAnalytics(schoolId?: string, dateFrom?: string, dateTo?: string): Promise<any> {
    const params = new URLSearchParams();
    
    if (schoolId) {
      params.append('schoolId', schoolId);
    }
    
    if (dateFrom) {
      params.append('dateFrom', dateFrom);
    }
    
    if (dateTo) {
      params.append('dateTo', dateTo);
    }

    const response = await apiService.get<any>(
      `${this.ATTENDANCE_ENDPOINTS.STATS}/analytics?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch attendance analytics');
  }
}

// Export singleton instance
export const attendanceService = new AttendanceService();
export default attendanceService; 