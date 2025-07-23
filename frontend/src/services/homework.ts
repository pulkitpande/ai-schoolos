import { apiService, ApiResponse } from './api';

// Homework Types
export interface Homework {
  id: string;
  title: string;
  description: string;
  subjectId: string;
  classId: string;
  assignedBy: string;
  assignedDate: string;
  dueDate: string;
  totalMarks: number;
  instructions?: string;
  attachments?: string[];
  isActive: boolean;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface HomeworkSubmission {
  id: string;
  homeworkId: string;
  studentId: string;
  submittedAt: string;
  submittedContent: string;
  attachments?: string[];
  marksObtained?: number;
  feedback?: string;
  gradedAt?: string;
  gradedBy?: string;
  status: 'submitted' | 'graded' | 'late' | 'not_submitted';
  createdAt: string;
  updatedAt: string;
}

export interface HomeworkGrade {
  id: string;
  submissionId: string;
  homeworkId: string;
  studentId: string;
  marksObtained: number;
  totalMarks: number;
  percentage: number;
  grade: string;
  feedback?: string;
  gradedBy: string;
  gradedAt: string;
  createdAt: string;
  updatedAt: string;
}

export interface HomeworkFilters {
  subjectId?: string;
  classId?: string;
  assignedBy?: string;
  status?: string;
  dateFrom?: string;
  dateTo?: string;
  schoolId?: string;
}

export interface HomeworkListResponse {
  homework: Homework[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Homework Service class
export class HomeworkService {
  private readonly HOMEWORK_ENDPOINTS = {
    HOMEWORK: '/api/v1/homework',
    SUBMISSIONS: '/api/v1/homework/submissions',
    GRADES: '/api/v1/homework/grades',
    STUDENT_HOMEWORK: '/api/v1/homework/students',
    CLASS_HOMEWORK: '/api/v1/homework/classes',
    REPORTS: '/api/v1/homework/reports',
  };

  // Get homework assignments
  async getHomework(filters?: HomeworkFilters): Promise<HomeworkListResponse> {
    const response = await apiService.get<HomeworkListResponse>(this.HOMEWORK_ENDPOINTS.HOMEWORK, filters);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch homework assignments');
  }

  // Get homework by ID
  async getHomeworkById(id: string): Promise<Homework> {
    const response = await apiService.get<Homework>(`${this.HOMEWORK_ENDPOINTS.HOMEWORK}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch homework assignment');
  }

  // Create homework assignment
  async createHomework(data: Partial<Homework>): Promise<Homework> {
    const response = await apiService.post<Homework>(this.HOMEWORK_ENDPOINTS.HOMEWORK, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create homework assignment');
  }

  // Update homework assignment
  async updateHomework(id: string, data: Partial<Homework>): Promise<Homework> {
    const response = await apiService.put<Homework>(`${this.HOMEWORK_ENDPOINTS.HOMEWORK}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update homework assignment');
  }

  // Delete homework assignment
  async deleteHomework(id: string): Promise<void> {
    const response = await apiService.delete(`${this.HOMEWORK_ENDPOINTS.HOMEWORK}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete homework assignment');
    }
  }

  // Get homework submissions
  async getHomeworkSubmissions(homeworkId?: string, filters?: any): Promise<HomeworkSubmission[]> {
    const params = { ...filters, homeworkId };
    const response = await apiService.get<HomeworkSubmission[]>(this.HOMEWORK_ENDPOINTS.SUBMISSIONS, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch homework submissions');
  }

  // Get homework submission by ID
  async getHomeworkSubmission(id: string): Promise<HomeworkSubmission> {
    const response = await apiService.get<HomeworkSubmission>(`${this.HOMEWORK_ENDPOINTS.SUBMISSIONS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch homework submission');
  }

  // Create homework submission
  async createHomeworkSubmission(data: Partial<HomeworkSubmission>): Promise<HomeworkSubmission> {
    const response = await apiService.post<HomeworkSubmission>(this.HOMEWORK_ENDPOINTS.SUBMISSIONS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create homework submission');
  }

  // Update homework submission
  async updateHomeworkSubmission(id: string, data: Partial<HomeworkSubmission>): Promise<HomeworkSubmission> {
    const response = await apiService.put<HomeworkSubmission>(`${this.HOMEWORK_ENDPOINTS.SUBMISSIONS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update homework submission');
  }

  // Delete homework submission
  async deleteHomeworkSubmission(id: string): Promise<void> {
    const response = await apiService.delete(`${this.HOMEWORK_ENDPOINTS.SUBMISSIONS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete homework submission');
    }
  }

  // Get student homework
  async getStudentHomework(studentId: string, filters?: any): Promise<Homework[]> {
    const params = { ...filters, studentId };
    const response = await apiService.get<Homework[]>(`${this.HOMEWORK_ENDPOINTS.STUDENT_HOMEWORK}/${studentId}`, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch student homework');
  }

  // Get student submissions
  async getStudentSubmissions(studentId: string, filters?: any): Promise<HomeworkSubmission[]> {
    const params = { ...filters, studentId };
    const response = await apiService.get<HomeworkSubmission[]>(`${this.HOMEWORK_ENDPOINTS.STUDENT_HOMEWORK}/${studentId}/submissions`, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch student submissions');
  }

  // Get class homework
  async getClassHomework(classId: string, filters?: any): Promise<Homework[]> {
    const params = { ...filters, classId };
    const response = await apiService.get<Homework[]>(`${this.HOMEWORK_ENDPOINTS.CLASS_HOMEWORK}/${classId}`, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch class homework');
  }

  // Get homework grades
  async getHomeworkGrades(homeworkId?: string, studentId?: string): Promise<HomeworkGrade[]> {
    const params = { homeworkId, studentId };
    const response = await apiService.get<HomeworkGrade[]>(this.HOMEWORK_ENDPOINTS.GRADES, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch homework grades');
  }

  // Get homework grade by ID
  async getHomeworkGrade(id: string): Promise<HomeworkGrade> {
    const response = await apiService.get<HomeworkGrade>(`${this.HOMEWORK_ENDPOINTS.GRADES}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch homework grade');
  }

  // Create homework grade
  async createHomeworkGrade(data: Partial<HomeworkGrade>): Promise<HomeworkGrade> {
    const response = await apiService.post<HomeworkGrade>(this.HOMEWORK_ENDPOINTS.GRADES, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create homework grade');
  }

  // Update homework grade
  async updateHomeworkGrade(id: string, data: Partial<HomeworkGrade>): Promise<HomeworkGrade> {
    const response = await apiService.put<HomeworkGrade>(`${this.HOMEWORK_ENDPOINTS.GRADES}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update homework grade');
  }

  // Delete homework grade
  async deleteHomeworkGrade(id: string): Promise<void> {
    const response = await apiService.delete(`${this.HOMEWORK_ENDPOINTS.GRADES}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete homework grade');
    }
  }

  // Get homework reports
  async getHomeworkReports(schoolId?: string, dateFrom?: string, dateTo?: string): Promise<any> {
    const params = { schoolId, dateFrom, dateTo };
    const response = await apiService.get<any>(this.HOMEWORK_ENDPOINTS.REPORTS, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch homework reports');
  }

  // Get homework statistics
  async getHomeworkStats(schoolId?: string): Promise<any> {
    const params = schoolId ? { schoolId } : {};
    const response = await apiService.get<any>(`${this.HOMEWORK_ENDPOINTS.REPORTS}/stats`, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch homework statistics');
  }

  // Get student homework statistics
  async getStudentHomeworkStats(studentId: string): Promise<any> {
    const response = await apiService.get<any>(`${this.HOMEWORK_ENDPOINTS.STUDENT_HOMEWORK}/${studentId}/stats`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch student homework statistics');
  }
}

// Export singleton instance
export const homeworkService = new HomeworkService();
export default homeworkService; 