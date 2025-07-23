import { apiService, ApiResponse } from './api';

// Exam Types
export interface Exam {
  id: string;
  name: string;
  description: string;
  subjectId: string;
  classId: string;
  examType: 'midterm' | 'final' | 'quiz' | 'assignment' | 'project';
  totalMarks: number;
  duration: number; // in minutes
  examDate: string;
  startTime: string;
  endTime: string;
  roomId?: string;
  instructions?: string;
  isActive: boolean;
  schoolId: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}

export interface ExamResult {
  id: string;
  examId: string;
  studentId: string;
  marksObtained: number;
  percentage: number;
  grade: string;
  remarks?: string;
  submittedAt?: string;
  gradedAt?: string;
  gradedBy?: string;
  createdAt: string;
  updatedAt: string;
}

export interface ExamSchedule {
  id: string;
  examId: string;
  classId: string;
  subjectId: string;
  examDate: string;
  startTime: string;
  endTime: string;
  roomId?: string;
  invigilatorId?: string;
  status: 'scheduled' | 'ongoing' | 'completed' | 'cancelled';
  createdAt: string;
  updatedAt: string;
}

export interface Grade {
  id: string;
  studentId: string;
  subjectId: string;
  classId: string;
  examId: string;
  marksObtained: number;
  totalMarks: number;
  percentage: number;
  grade: string;
  remarks?: string;
  academicYear: string;
  semester?: string;
  createdAt: string;
  updatedAt: string;
}

export interface ExamFilters {
  schoolId?: string;
  classId?: string;
  subjectId?: string;
  examType?: string;
  dateFrom?: string;
  dateTo?: string;
  status?: string;
}

export interface ExamListResponse {
  exams: Exam[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Exam Service class
export class ExamService {
  private readonly EXAM_ENDPOINTS = {
    EXAMS: '/api/v1/exams',
    RESULTS: '/api/v1/exams/results',
    SCHEDULES: '/api/v1/exams/schedules',
    GRADES: '/api/v1/exams/grades',
    REPORTS: '/api/v1/exams/reports',
    STUDENT_RESULTS: '/api/v1/exams/students',
  };

  // Get exams
  async getExams(filters?: ExamFilters): Promise<ExamListResponse> {
    const response = await apiService.get<ExamListResponse>(this.EXAM_ENDPOINTS.EXAMS, filters);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch exams');
  }

  // Get exam by ID
  async getExam(id: string): Promise<Exam> {
    const response = await apiService.get<Exam>(`${this.EXAM_ENDPOINTS.EXAMS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch exam');
  }

  // Create exam
  async createExam(data: Partial<Exam>): Promise<Exam> {
    const response = await apiService.post<Exam>(this.EXAM_ENDPOINTS.EXAMS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create exam');
  }

  // Update exam
  async updateExam(id: string, data: Partial<Exam>): Promise<Exam> {
    const response = await apiService.put<Exam>(`${this.EXAM_ENDPOINTS.EXAMS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update exam');
  }

  // Delete exam
  async deleteExam(id: string): Promise<void> {
    const response = await apiService.delete(`${this.EXAM_ENDPOINTS.EXAMS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete exam');
    }
  }

  // Get exam results
  async getExamResults(examId?: string, filters?: any): Promise<ExamResult[]> {
    const params = { ...filters, examId };
    const response = await apiService.get<ExamResult[]>(this.EXAM_ENDPOINTS.RESULTS, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch exam results');
  }

  // Get exam result by ID
  async getExamResult(id: string): Promise<ExamResult> {
    const response = await apiService.get<ExamResult>(`${this.EXAM_ENDPOINTS.RESULTS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch exam result');
  }

  // Create exam result
  async createExamResult(data: Partial<ExamResult>): Promise<ExamResult> {
    const response = await apiService.post<ExamResult>(this.EXAM_ENDPOINTS.RESULTS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create exam result');
  }

  // Update exam result
  async updateExamResult(id: string, data: Partial<ExamResult>): Promise<ExamResult> {
    const response = await apiService.put<ExamResult>(`${this.EXAM_ENDPOINTS.RESULTS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update exam result');
  }

  // Delete exam result
  async deleteExamResult(id: string): Promise<void> {
    const response = await apiService.delete(`${this.EXAM_ENDPOINTS.RESULTS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete exam result');
    }
  }

  // Get exam schedules
  async getExamSchedules(filters?: any): Promise<ExamSchedule[]> {
    const response = await apiService.get<ExamSchedule[]>(this.EXAM_ENDPOINTS.SCHEDULES, filters);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch exam schedules');
  }

  // Create exam schedule
  async createExamSchedule(data: Partial<ExamSchedule>): Promise<ExamSchedule> {
    const response = await apiService.post<ExamSchedule>(this.EXAM_ENDPOINTS.SCHEDULES, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create exam schedule');
  }

  // Update exam schedule
  async updateExamSchedule(id: string, data: Partial<ExamSchedule>): Promise<ExamSchedule> {
    const response = await apiService.put<ExamSchedule>(`${this.EXAM_ENDPOINTS.SCHEDULES}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update exam schedule');
  }

  // Delete exam schedule
  async deleteExamSchedule(id: string): Promise<void> {
    const response = await apiService.delete(`${this.EXAM_ENDPOINTS.SCHEDULES}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete exam schedule');
    }
  }

  // Get grades
  async getGrades(studentId?: string, filters?: any): Promise<Grade[]> {
    const params = { ...filters, studentId };
    const response = await apiService.get<Grade[]>(this.EXAM_ENDPOINTS.GRADES, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch grades');
  }

  // Get grade by ID
  async getGrade(id: string): Promise<Grade> {
    const response = await apiService.get<Grade>(`${this.EXAM_ENDPOINTS.GRADES}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch grade');
  }

  // Create grade
  async createGrade(data: Partial<Grade>): Promise<Grade> {
    const response = await apiService.post<Grade>(this.EXAM_ENDPOINTS.GRADES, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create grade');
  }

  // Update grade
  async updateGrade(id: string, data: Partial<Grade>): Promise<Grade> {
    const response = await apiService.put<Grade>(`${this.EXAM_ENDPOINTS.GRADES}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update grade');
  }

  // Delete grade
  async deleteGrade(id: string): Promise<void> {
    const response = await apiService.delete(`${this.EXAM_ENDPOINTS.GRADES}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete grade');
    }
  }

  // Get student results
  async getStudentResults(studentId: string): Promise<ExamResult[]> {
    const response = await apiService.get<ExamResult[]>(`${this.EXAM_ENDPOINTS.STUDENT_RESULTS}/${studentId}/results`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch student results');
  }

  // Get student grades
  async getStudentGrades(studentId: string): Promise<Grade[]> {
    const response = await apiService.get<Grade[]>(`${this.EXAM_ENDPOINTS.STUDENT_RESULTS}/${studentId}/grades`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch student grades');
  }

  // Get exam reports
  async getExamReports(schoolId?: string, dateFrom?: string, dateTo?: string): Promise<any> {
    const params = { schoolId, dateFrom, dateTo };
    const response = await apiService.get<any>(this.EXAM_ENDPOINTS.REPORTS, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch exam reports');
  }

  // Get exam statistics
  async getExamStats(schoolId?: string): Promise<any> {
    const params = schoolId ? { schoolId } : {};
    const response = await apiService.get<any>(`${this.EXAM_ENDPOINTS.REPORTS}/stats`, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch exam statistics');
  }
}

// Export singleton instance
export const examService = new ExamService();
export default examService; 