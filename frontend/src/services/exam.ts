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
    QUESTIONS: '/api/v1/exams/questions',
  };

  // Get exams
  async getExams(filters?: ExamFilters): Promise<ExamListResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<ExamListResponse>(
      `${this.EXAM_ENDPOINTS.EXAMS}?${params.toString()}`
    );
    
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

  // Get exam schedules
  async getExamSchedules(filters?: any): Promise<ExamSchedule[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<ExamSchedule[]>(
      `${this.EXAM_ENDPOINTS.SCHEDULES}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch exam schedules');
  }

  // Get exam schedule by ID
  async getExamSchedule(id: string): Promise<ExamSchedule> {
    const response = await apiService.get<ExamSchedule>(`${this.EXAM_ENDPOINTS.SCHEDULES}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch exam schedule');
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

  // Get exam results
  async getExamResults(filters?: any): Promise<ExamResult[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<ExamResult[]>(
      `${this.EXAM_ENDPOINTS.RESULTS}?${params.toString()}`
    );
    
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

  // Get grades
  async getGrades(studentId?: string, filters?: any): Promise<Grade[]> {
    const params = new URLSearchParams();
    
    if (studentId) {
      params.append('studentId', studentId);
    }
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<Grade[]>(
      `${this.EXAM_ENDPOINTS.GRADES}?${params.toString()}`
    );
    
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

  // Get exam questions
  async getExamQuestions(examId: string): Promise<any[]> { // Assuming ExamQuestion is not defined, using 'any' for now
    const response = await apiService.get<any[]>(`${this.EXAM_ENDPOINTS.QUESTIONS}/${examId}/questions`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch exam questions');
  }

  // Get exam question by ID
  async getExamQuestion(id: string): Promise<any> { // Assuming ExamQuestion is not defined, using 'any' for now
    const response = await apiService.get<any>(`${this.EXAM_ENDPOINTS.QUESTIONS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch exam question');
  }

  // Create exam question
  async createExamQuestion(data: Partial<any>): Promise<any> { // Assuming ExamQuestion is not defined, using 'any' for now
    const response = await apiService.post<any>(this.EXAM_ENDPOINTS.QUESTIONS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create exam question');
  }

  // Update exam question
  async updateExamQuestion(id: string, data: Partial<any>): Promise<any> { // Assuming ExamQuestion is not defined, using 'any' for now
    const response = await apiService.put<any>(`${this.EXAM_ENDPOINTS.QUESTIONS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update exam question');
  }

  // Delete exam question
  async deleteExamQuestion(id: string): Promise<void> {
    const response = await apiService.delete(`${this.EXAM_ENDPOINTS.QUESTIONS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete exam question');
    }
  }

  // Get exam reports
  async getExamReports(schoolId?: string, dateFrom?: string, dateTo?: string): Promise<any> {
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
      `${this.EXAM_ENDPOINTS.REPORTS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch exam reports');
  }

  // Get exam stats
  async getExamStats(schoolId?: string): Promise<any> {
    const params = new URLSearchParams();
    
    if (schoolId) {
      params.append('schoolId', schoolId);
    }

    const response = await apiService.get<any>(
      `${this.EXAM_ENDPOINTS.REPORTS}/stats?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch exam stats');
  }
}

// Export singleton instance
export const examService = new ExamService();
export default examService; 