import { apiService, ApiResponse } from './api';

// Student types
export interface Student {
  id: string;
  studentId: string;
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  dateOfBirth: string;
  gender: 'male' | 'female' | 'other';
  address: {
    street: string;
    city: string;
    state: string;
    zipCode: string;
    country: string;
  };
  parentId?: string;
  schoolId: string;
  classId?: string;
  grade: string;
  section: string;
  enrollmentDate: string;
  status: 'active' | 'inactive' | 'graduated' | 'transferred';
  avatar?: string;
  emergencyContact?: {
    name: string;
    relationship: string;
    phone: string;
  };
  medicalInfo?: {
    allergies: string[];
    conditions: string[];
    medications: string[];
  };
  createdAt: string;
  updatedAt: string;
}

export interface CreateStudentData {
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  dateOfBirth: string;
  gender: 'male' | 'female' | 'other';
  address: {
    street: string;
    city: string;
    state: string;
    zipCode: string;
    country: string;
  };
  parentId?: string;
  schoolId: string;
  classId?: string;
  grade: string;
  section: string;
  emergencyContact?: {
    name: string;
    relationship: string;
    phone: string;
  };
  medicalInfo?: {
    allergies: string[];
    conditions: string[];
    medications: string[];
  };
}

export interface UpdateStudentData extends Partial<CreateStudentData> {
  id: string;
}

export interface StudentFilters {
  schoolId?: string;
  classId?: string;
  grade?: string;
  section?: string;
  status?: string;
  search?: string;
  page?: number;
  limit?: number;
}

export interface StudentListResponse {
  students: Student[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Student Service class
export class StudentService {
  private readonly STUDENT_ENDPOINTS = {
    BASE: '/api/v1/students',
    BY_ID: (id: string) => `/api/v1/students/${id}`,
    BY_SCHOOL: (schoolId: string) => `/api/v1/students/school/${schoolId}`,
    BY_CLASS: (classId: string) => `/api/v1/students/class/${classId}`,
    BY_PARENT: (parentId: string) => `/api/v1/students/parent/${parentId}`,
    BULK_CREATE: '/api/v1/students/bulk',
    BULK_UPDATE: '/api/v1/students/bulk-update',
    BULK_DELETE: '/api/v1/students/bulk-delete',
    EXPORT: '/api/v1/students/export',
    IMPORT: '/api/v1/students/import',
  };

  // Get all students with filters
  async getStudents(filters?: StudentFilters): Promise<StudentListResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<StudentListResponse>(
      `${this.STUDENT_ENDPOINTS.BASE}?${params.toString()}`
    );
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch students');
  }

  // Get student by ID
  async getStudent(id: string): Promise<Student> {
    const response = await apiService.get<Student>(this.STUDENT_ENDPOINTS.BY_ID(id));
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch student');
  }

  // Create new student
  async createStudent(data: CreateStudentData): Promise<Student> {
    const response = await apiService.post<Student>(this.STUDENT_ENDPOINTS.BASE, data);
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create student');
  }

  // Update student
  async updateStudent(data: UpdateStudentData): Promise<Student> {
    const { id, ...updateData } = data;
    const response = await apiService.put<Student>(this.STUDENT_ENDPOINTS.BY_ID(id), updateData);
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update student');
  }

  // Delete student
  async deleteStudent(id: string): Promise<void> {
    const response = await apiService.delete(this.STUDENT_ENDPOINTS.BY_ID(id));
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete student');
    }
  }

  // Get students by school
  async getStudentsBySchool(schoolId: string, filters?: StudentFilters): Promise<StudentListResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<StudentListResponse>(
      `${this.STUDENT_ENDPOINTS.BY_SCHOOL(schoolId)}?${params.toString()}`
    );
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch students by school');
  }

  // Get students by class
  async getStudentsByClass(classId: string): Promise<Student[]> {
    const response = await apiService.get<Student[]>(this.STUDENT_ENDPOINTS.BY_CLASS(classId));
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch students by class');
  }

  // Get students by parent
  async getStudentsByParent(parentId: string): Promise<Student[]> {
    const response = await apiService.get<Student[]>(this.STUDENT_ENDPOINTS.BY_PARENT(parentId));
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch students by parent');
  }

  // Bulk create students
  async bulkCreateStudents(students: CreateStudentData[]): Promise<Student[]> {
    const response = await apiService.post<Student[]>(this.STUDENT_ENDPOINTS.BULK_CREATE, { students });
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to bulk create students');
  }

  // Bulk update students
  async bulkUpdateStudents(updates: UpdateStudentData[]): Promise<Student[]> {
    const response = await apiService.put<Student[]>(this.STUDENT_ENDPOINTS.BULK_UPDATE, { updates });
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to bulk update students');
  }

  // Bulk delete students
  async bulkDeleteStudents(ids: string[]): Promise<void> {
    const response = await apiService.delete(this.STUDENT_ENDPOINTS.BULK_DELETE, { data: { ids } });
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to bulk delete students');
    }
  }

  // Export students
  async exportStudents(filters?: StudentFilters, format: 'csv' | 'excel' = 'csv'): Promise<Blob> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }
    
    params.append('format', format);

    const response = await apiService.get(`${this.STUDENT_ENDPOINTS.EXPORT}?${params.toString()}`, {
      responseType: 'blob',
    });
    
    if (response.success) {
      return response.data as Blob;
    }
    
    throw new Error(response.message || 'Failed to export students');
  }

  // Import students
  async importStudents(file: File): Promise<{ success: number; failed: number; errors: string[] }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiService.post<{ success: number; failed: number; errors: string[] }>(
      this.STUDENT_ENDPOINTS.IMPORT,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to import students');
  }

  // Get student statistics
  async getStudentStats(schoolId?: string): Promise<{
    total: number;
    active: number;
    inactive: number;
    graduated: number;
    transferred: number;
    byGrade: Record<string, number>;
    byGender: Record<string, number>;
  }> {
    const params = schoolId ? `?schoolId=${schoolId}` : '';
    const response = await apiService.get(`${this.STUDENT_ENDPOINTS.BASE}/stats${params}`);
    
    if (response.success) {
      return response.data as {
        total: number;
        active: number;
        inactive: number;
        graduated: number;
        transferred: number;
        byGrade: Record<string, number>;
        byGender: Record<string, number>;
      };
    }
    
    throw new Error(response.message || 'Failed to fetch student statistics');
  }
}

// Export singleton instance
export const studentService = new StudentService();
export default studentService; 