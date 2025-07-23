import { apiService, ApiResponse } from './api';

// Staff types
export interface Staff {
  id: string;
  staffId: string;
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
  schoolId: string;
  department: string;
  position: string;
  role: 'teacher' | 'admin' | 'principal' | 'vice_principal' | 'counselor' | 'librarian' | 'nurse' | 'other';
  hireDate: string;
  salary?: number;
  status: 'active' | 'inactive' | 'terminated' | 'retired';
  avatar?: string;
  qualifications?: {
    degree: string;
    institution: string;
    year: string;
  }[];
  certifications?: {
    name: string;
    issuingAuthority: string;
    issueDate: string;
    expiryDate?: string;
  }[];
  emergencyContact?: {
    name: string;
    relationship: string;
    phone: string;
  };
  createdAt: string;
  updatedAt: string;
}

export interface CreateStaffData {
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
  schoolId: string;
  department: string;
  position: string;
  role: 'teacher' | 'admin' | 'principal' | 'vice_principal' | 'counselor' | 'librarian' | 'nurse' | 'other';
  hireDate: string;
  salary?: number;
  qualifications?: {
    degree: string;
    institution: string;
    year: string;
  }[];
  certifications?: {
    name: string;
    issuingAuthority: string;
    issueDate: string;
    expiryDate?: string;
  }[];
  emergencyContact?: {
    name: string;
    relationship: string;
    phone: string;
  };
}

export interface UpdateStaffData extends Partial<CreateStaffData> {
  id: string;
}

export interface StaffFilters {
  schoolId?: string;
  department?: string;
  role?: string;
  status?: string;
  search?: string;
  page?: number;
  limit?: number;
}

export interface StaffListResponse {
  staff: Staff[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Staff Service class
export class StaffService {
  private readonly STAFF_ENDPOINTS = {
    BASE: '/api/v1/staff',
    BY_ID: (id: string) => `/api/v1/staff/${id}`,
    BY_SCHOOL: (schoolId: string) => `/api/v1/staff/school/${schoolId}`,
    BY_DEPARTMENT: (department: string) => `/api/v1/staff/department/${department}`,
    BY_ROLE: (role: string) => `/api/v1/staff/role/${role}`,
    TEACHERS: '/api/v1/staff/teachers',
    ADMINS: '/api/v1/staff/admins',
    BULK_CREATE: '/api/v1/staff/bulk',
    BULK_UPDATE: '/api/v1/staff/bulk-update',
    BULK_DELETE: '/api/v1/staff/bulk-delete',
    EXPORT: '/api/v1/staff/export',
    IMPORT: '/api/v1/staff/import',
  };

  // Get all staff with filters
  async getStaff(filters?: StaffFilters): Promise<StaffListResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<StaffListResponse>(
      `${this.STAFF_ENDPOINTS.BASE}?${params.toString()}`
    );
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch staff');
  }

  // Get staff by ID
  async getStaffMember(id: string): Promise<Staff> {
    const response = await apiService.get<Staff>(this.STAFF_ENDPOINTS.BY_ID(id));
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch staff member');
  }

  // Create new staff member
  async createStaff(data: CreateStaffData): Promise<Staff> {
    const response = await apiService.post<Staff>(this.STAFF_ENDPOINTS.BASE, data);
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create staff member');
  }

  // Update staff member
  async updateStaff(data: UpdateStaffData): Promise<Staff> {
    const { id, ...updateData } = data;
    const response = await apiService.put<Staff>(this.STAFF_ENDPOINTS.BY_ID(id), updateData);
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update staff member');
  }

  // Delete staff member
  async deleteStaff(id: string): Promise<void> {
    const response = await apiService.delete(this.STAFF_ENDPOINTS.BY_ID(id));
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete staff member');
    }
  }

  // Get staff by school
  async getStaffBySchool(schoolId: string, filters?: StaffFilters): Promise<StaffListResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<StaffListResponse>(
      `${this.STAFF_ENDPOINTS.BY_SCHOOL(schoolId)}?${params.toString()}`
    );
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch staff by school');
  }

  // Get staff by department
  async getStaffByDepartment(department: string): Promise<Staff[]> {
    const response = await apiService.get<Staff[]>(this.STAFF_ENDPOINTS.BY_DEPARTMENT(department));
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch staff by department');
  }

  // Get staff by role
  async getStaffByRole(role: string): Promise<Staff[]> {
    const response = await apiService.get<Staff[]>(this.STAFF_ENDPOINTS.BY_ROLE(role));
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch staff by role');
  }

  // Get all teachers
  async getTeachers(filters?: StaffFilters): Promise<StaffListResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<StaffListResponse>(
      `${this.STAFF_ENDPOINTS.TEACHERS}?${params.toString()}`
    );
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch teachers');
  }

  // Get all admins
  async getAdmins(filters?: StaffFilters): Promise<StaffListResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<StaffListResponse>(
      `${this.STAFF_ENDPOINTS.ADMINS}?${params.toString()}`
    );
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch admins');
  }

  // Bulk create staff
  async bulkCreateStaff(staff: CreateStaffData[]): Promise<Staff[]> {
    const response = await apiService.post<Staff[]>(this.STAFF_ENDPOINTS.BULK_CREATE, { staff });
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to bulk create staff');
  }

  // Bulk update staff
  async bulkUpdateStaff(updates: UpdateStaffData[]): Promise<Staff[]> {
    const response = await apiService.put<Staff[]>(this.STAFF_ENDPOINTS.BULK_UPDATE, { updates });
    
    if (response.success) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to bulk update staff');
  }

  // Bulk delete staff
  async bulkDeleteStaff(ids: string[]): Promise<void> {
    const response = await apiService.delete(this.STAFF_ENDPOINTS.BULK_DELETE, { data: { ids } });
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to bulk delete staff');
    }
  }

  // Export staff
  async exportStaff(filters?: StaffFilters, format: 'csv' | 'excel' = 'csv'): Promise<Blob> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }
    
    params.append('format', format);

    const response = await apiService.get(`${this.STAFF_ENDPOINTS.EXPORT}?${params.toString()}`, {
      responseType: 'blob',
    });
    
    if (response.success) {
      return response.data as Blob;
    }
    
    throw new Error(response.message || 'Failed to export staff');
  }

  // Import staff
  async importStaff(file: File): Promise<{ success: number; failed: number; errors: string[] }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiService.post<{ success: number; failed: number; errors: string[] }>(
      this.STAFF_ENDPOINTS.IMPORT,
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
    
    throw new Error(response.message || 'Failed to import staff');
  }

  // Get staff statistics
  async getStaffStats(schoolId?: string): Promise<{
    total: number;
    active: number;
    inactive: number;
    terminated: number;
    retired: number;
    byRole: Record<string, number>;
    byDepartment: Record<string, number>;
    byGender: Record<string, number>;
  }> {
    const params = schoolId ? `?schoolId=${schoolId}` : '';
    const response = await apiService.get(`${this.STAFF_ENDPOINTS.BASE}/stats${params}`);
    
    if (response.success) {
      return response.data as {
        total: number;
        active: number;
        inactive: number;
        terminated: number;
        retired: number;
        byRole: Record<string, number>;
        byDepartment: Record<string, number>;
        byGender: Record<string, number>;
      };
    }
    
    throw new Error(response.message || 'Failed to fetch staff statistics');
  }
}

// Export singleton instance
export const staffService = new StaffService();
export default staffService; 