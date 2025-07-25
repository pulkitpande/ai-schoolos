import { apiService, ApiResponse } from './api';

// Fee Types
export interface FeeStructure {
  id: string;
  name: string;
  description: string;
  amount: number;
  frequency: 'monthly' | 'quarterly' | 'semester' | 'annual';
  category: 'tuition' | 'transport' | 'library' | 'laboratory' | 'other';
  schoolId: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface FeePayment {
  id: string;
  studentId: string;
  feeStructureId: string;
  amount: number;
  paidAmount: number;
  discountAmount: number;
  paymentMethod: 'cash' | 'card' | 'bank_transfer' | 'online';
  paymentStatus: 'pending' | 'paid' | 'partial' | 'overdue' | 'cancelled';
  dueDate: string;
  paidDate?: string;
  receiptNumber: string;
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

export interface FeeDiscount {
  id: string;
  name: string;
  description: string;
  discountType: 'percentage' | 'fixed';
  discountValue: number;
  applicableFrom: string;
  applicableTo: string;
  conditions?: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface FinancialRecord {
  id: string;
  type: 'income' | 'expense';
  category: string;
  amount: number;
  description: string;
  date: string;
  reference?: string;
  schoolId: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}

export interface FeeFilters {
  studentId?: string;
  schoolId?: string;
  paymentStatus?: string;
  dateFrom?: string;
  dateTo?: string;
  category?: string;
}

export interface FeeListResponse {
  payments: FeePayment[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Fee Service class
export class FeeService {
  private readonly FEE_ENDPOINTS = {
    STRUCTURES: '/api/v1/fees/structures',
    PAYMENTS: '/api/v1/fees/payments',
    DISCOUNTS: '/api/v1/fees/discounts',
    RECORDS: '/api/v1/fees/records',
    STUDENT_PAYMENTS: '/api/v1/fees/students',
    REPORTS: '/api/v1/fees/reports',
  };

  // Get fee structures
  async getFeeStructures(schoolId?: string, classId?: string): Promise<FeeStructure[]> {
    const params = new URLSearchParams();
    
    if (schoolId) {
      params.append('schoolId', schoolId);
    }
    
    if (classId) {
      params.append('classId', classId);
    }

    const response = await apiService.get<FeeStructure[]>(
      `${this.FEE_ENDPOINTS.STRUCTURES}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch fee structures');
  }

  // Get fee structure by ID
  async getFeeStructure(id: string): Promise<FeeStructure> {
    const response = await apiService.get<FeeStructure>(`${this.FEE_ENDPOINTS.STRUCTURES}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch fee structure');
  }

  // Create fee structure
  async createFeeStructure(data: Partial<FeeStructure>): Promise<FeeStructure> {
    const response = await apiService.post<FeeStructure>(this.FEE_ENDPOINTS.STRUCTURES, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create fee structure');
  }

  // Update fee structure
  async updateFeeStructure(id: string, data: Partial<FeeStructure>): Promise<FeeStructure> {
    const response = await apiService.put<FeeStructure>(`${this.FEE_ENDPOINTS.STRUCTURES}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update fee structure');
  }

  // Delete fee structure
  async deleteFeeStructure(id: string): Promise<void> {
    const response = await apiService.delete(`${this.FEE_ENDPOINTS.STRUCTURES}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete fee structure');
    }
  }

  // Get fee payments
  async getFeePayments(filters?: FeeFilters): Promise<FeeListResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<FeeListResponse>(
      `${this.FEE_ENDPOINTS.PAYMENTS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch fee payments');
  }

  // Get fee payment by ID
  async getFeePayment(id: string): Promise<FeePayment> {
    const response = await apiService.get<FeePayment>(`${this.FEE_ENDPOINTS.PAYMENTS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch fee payment');
  }

  // Create fee payment
  async createFeePayment(data: Partial<FeePayment>): Promise<FeePayment> {
    const response = await apiService.post<FeePayment>(this.FEE_ENDPOINTS.PAYMENTS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create fee payment');
  }

  // Update fee payment
  async updateFeePayment(id: string, data: Partial<FeePayment>): Promise<FeePayment> {
    const response = await apiService.put<FeePayment>(`${this.FEE_ENDPOINTS.PAYMENTS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update fee payment');
  }

  // Delete fee payment
  async deleteFeePayment(id: string): Promise<void> {
    const response = await apiService.delete(`${this.FEE_ENDPOINTS.PAYMENTS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete fee payment');
    }
  }

  // Get student payments
  async getStudentPayments(studentId: string): Promise<FeePayment[]> {
    const response = await apiService.get<FeePayment[]>(`${this.FEE_ENDPOINTS.STUDENT_PAYMENTS}/${studentId}/payments`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch student payments');
  }

  // Get fee discounts
  async getFeeDiscounts(): Promise<FeeDiscount[]> {
    const response = await apiService.get<FeeDiscount[]>(this.FEE_ENDPOINTS.DISCOUNTS);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch fee discounts');
  }

  // Get fee discount by ID
  async getFeeDiscount(id: string): Promise<FeeDiscount> {
    const response = await apiService.get<FeeDiscount>(`${this.FEE_ENDPOINTS.DISCOUNTS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch fee discount');
  }

  // Create fee discount
  async createFeeDiscount(data: Partial<FeeDiscount>): Promise<FeeDiscount> {
    const response = await apiService.post<FeeDiscount>(this.FEE_ENDPOINTS.DISCOUNTS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create fee discount');
  }

  // Update fee discount
  async updateFeeDiscount(id: string, data: Partial<FeeDiscount>): Promise<FeeDiscount> {
    const response = await apiService.put<FeeDiscount>(`${this.FEE_ENDPOINTS.DISCOUNTS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update fee discount');
  }

  // Delete fee discount
  async deleteFeeDiscount(id: string): Promise<void> {
    const response = await apiService.delete(`${this.FEE_ENDPOINTS.DISCOUNTS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete fee discount');
    }
  }

  // Get financial records
  async getFinancialRecords(schoolId?: string, dateFrom?: string, dateTo?: string): Promise<FinancialRecord[]> {
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

    const response = await apiService.get<FinancialRecord[]>(
      `${this.FEE_ENDPOINTS.RECORDS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch financial records');
  }

  // Get financial record by ID
  async getFinancialRecord(id: string): Promise<FinancialRecord> {
    const response = await apiService.get<FinancialRecord>(`${this.FEE_ENDPOINTS.RECORDS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch financial record');
  }

  // Create financial record
  async createFinancialRecord(data: Partial<FinancialRecord>): Promise<FinancialRecord> {
    const response = await apiService.post<FinancialRecord>(this.FEE_ENDPOINTS.RECORDS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create financial record');
  }

  // Update financial record
  async updateFinancialRecord(id: string, data: Partial<FinancialRecord>): Promise<FinancialRecord> {
    const response = await apiService.put<FinancialRecord>(`${this.FEE_ENDPOINTS.RECORDS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update financial record');
  }

  // Delete financial record
  async deleteFinancialRecord(id: string): Promise<void> {
    const response = await apiService.delete(`${this.FEE_ENDPOINTS.RECORDS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete financial record');
    }
  }

  // Get fee reports
  async getFeeReports(schoolId?: string, dateFrom?: string, dateTo?: string): Promise<any> {
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
      `${this.FEE_ENDPOINTS.REPORTS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch fee reports');
  }

  // Get fee stats
  async getFeeStats(schoolId?: string): Promise<any> {
    const params = new URLSearchParams();
    
    if (schoolId) {
      params.append('schoolId', schoolId);
    }

    const response = await apiService.get<any>(
      `${this.FEE_ENDPOINTS.REPORTS}/stats?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch fee stats');
  }
}

// Export singleton instance
export const feeService = new FeeService();
export default feeService; 