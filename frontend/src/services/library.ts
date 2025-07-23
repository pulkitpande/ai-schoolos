import { apiService, ApiResponse } from './api';

// Library Types
export interface Book {
  id: string;
  title: string;
  author: string;
  isbn: string;
  publisher: string;
  publicationYear: number;
  category: string;
  subcategory?: string;
  language: string;
  pages: number;
  description?: string;
  coverImage?: string;
  totalCopies: number;
  availableCopies: number;
  location: string;
  isActive: boolean;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface BookBorrowing {
  id: string;
  bookId: string;
  studentId: string;
  borrowedDate: string;
  dueDate: string;
  returnedDate?: string;
  status: 'borrowed' | 'returned' | 'overdue' | 'lost';
  fineAmount?: number;
  notes?: string;
  issuedBy: string;
  receivedBy?: string;
  createdAt: string;
  updatedAt: string;
}

export interface LibraryMember {
  id: string;
  userId: string;
  memberType: 'student' | 'teacher' | 'staff' | 'parent';
  membershipNumber: string;
  joinDate: string;
  expiryDate: string;
  status: 'active' | 'inactive' | 'suspended';
  maxBooksAllowed: number;
  currentBooksBorrowed: number;
  totalFineAmount: number;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface LibraryTransaction {
  id: string;
  memberId: string;
  bookId: string;
  transactionType: 'borrow' | 'return' | 'renew' | 'reserve';
  transactionDate: string;
  dueDate?: string;
  returnedDate?: string;
  fineAmount?: number;
  processedBy: string;
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

export interface LibraryFilters {
  category?: string;
  author?: string;
  title?: string;
  isbn?: string;
  status?: string;
  schoolId?: string;
}

export interface LibraryListResponse {
  books: Book[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Library Service class
export class LibraryService {
  private readonly LIBRARY_ENDPOINTS = {
    BOOKS: '/api/v1/library/books',
    BORROWINGS: '/api/v1/library/borrowings',
    MEMBERS: '/api/v1/library/members',
    TRANSACTIONS: '/api/v1/library/transactions',
    CATEGORIES: '/api/v1/library/categories',
    REPORTS: '/api/v1/library/reports',
  };

  // Get books
  async getBooks(filters?: LibraryFilters): Promise<LibraryListResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<LibraryListResponse>(
      `${this.LIBRARY_ENDPOINTS.BOOKS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch books');
  }

  // Get book by ID
  async getBook(id: string): Promise<Book> {
    const response = await apiService.get<Book>(`${this.LIBRARY_ENDPOINTS.BOOKS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch book');
  }

  // Create book
  async createBook(data: Partial<Book>): Promise<Book> {
    const response = await apiService.post<Book>(this.LIBRARY_ENDPOINTS.BOOKS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create book');
  }

  // Update book
  async updateBook(id: string, data: Partial<Book>): Promise<Book> {
    const response = await apiService.put<Book>(`${this.LIBRARY_ENDPOINTS.BOOKS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update book');
  }

  // Delete book
  async deleteBook(id: string): Promise<void> {
    const response = await apiService.delete(`${this.LIBRARY_ENDPOINTS.BOOKS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete book');
    }
  }

  // Get book borrowings
  async getBookBorrowings(filters?: any): Promise<BookBorrowing[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<BookBorrowing[]>(
      `${this.LIBRARY_ENDPOINTS.BORROWINGS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch book borrowings');
  }

  // Get book borrowing by ID
  async getBookBorrowing(id: string): Promise<BookBorrowing> {
    const response = await apiService.get<BookBorrowing>(`${this.LIBRARY_ENDPOINTS.BORROWINGS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch book borrowing');
  }

  // Create book borrowing
  async createBookBorrowing(data: Partial<BookBorrowing>): Promise<BookBorrowing> {
    const response = await apiService.post<BookBorrowing>(this.LIBRARY_ENDPOINTS.BORROWINGS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create book borrowing');
  }

  // Update book borrowing
  async updateBookBorrowing(id: string, data: Partial<BookBorrowing>): Promise<BookBorrowing> {
    const response = await apiService.put<BookBorrowing>(`${this.LIBRARY_ENDPOINTS.BORROWINGS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update book borrowing');
  }

  // Delete book borrowing
  async deleteBookBorrowing(id: string): Promise<void> {
    const response = await apiService.delete(`${this.LIBRARY_ENDPOINTS.BORROWINGS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete book borrowing');
    }
  }

  // Get library members
  async getLibraryMembers(filters?: any): Promise<LibraryMember[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<LibraryMember[]>(
      `${this.LIBRARY_ENDPOINTS.MEMBERS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch library members');
  }

  // Get library member by ID
  async getLibraryMember(id: string): Promise<LibraryMember> {
    const response = await apiService.get<LibraryMember>(`${this.LIBRARY_ENDPOINTS.MEMBERS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch library member');
  }

  // Create library member
  async createLibraryMember(data: Partial<LibraryMember>): Promise<LibraryMember> {
    const response = await apiService.post<LibraryMember>(this.LIBRARY_ENDPOINTS.MEMBERS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create library member');
  }

  // Update library member
  async updateLibraryMember(id: string, data: Partial<LibraryMember>): Promise<LibraryMember> {
    const response = await apiService.put<LibraryMember>(`${this.LIBRARY_ENDPOINTS.MEMBERS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update library member');
  }

  // Delete library member
  async deleteLibraryMember(id: string): Promise<void> {
    const response = await apiService.delete(`${this.LIBRARY_ENDPOINTS.MEMBERS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete library member');
    }
  }

  // Get library transactions
  async getLibraryTransactions(filters?: any): Promise<LibraryTransaction[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<LibraryTransaction[]>(
      `${this.LIBRARY_ENDPOINTS.TRANSACTIONS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch library transactions');
  }

  // Get library transaction by ID
  async getLibraryTransaction(id: string): Promise<LibraryTransaction> {
    const response = await apiService.get<LibraryTransaction>(`${this.LIBRARY_ENDPOINTS.TRANSACTIONS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch library transaction');
  }

  // Create library transaction
  async createLibraryTransaction(data: Partial<LibraryTransaction>): Promise<LibraryTransaction> {
    const response = await apiService.post<LibraryTransaction>(this.LIBRARY_ENDPOINTS.TRANSACTIONS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create library transaction');
  }

  // Update library transaction
  async updateLibraryTransaction(id: string, data: Partial<LibraryTransaction>): Promise<LibraryTransaction> {
    const response = await apiService.put<LibraryTransaction>(`${this.LIBRARY_ENDPOINTS.TRANSACTIONS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update library transaction');
  }

  // Delete library transaction
  async deleteLibraryTransaction(id: string): Promise<void> {
    const response = await apiService.delete(`${this.LIBRARY_ENDPOINTS.TRANSACTIONS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete library transaction');
    }
  }

  // Get book categories
  async getBookCategories(): Promise<string[]> {
    const response = await apiService.get<string[]>(this.LIBRARY_ENDPOINTS.CATEGORIES);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch book categories');
  }

  // Get student borrowings
  async getStudentBorrowings(studentId: string): Promise<BookBorrowing[]> {
    const response = await apiService.get<BookBorrowing[]>(`${this.LIBRARY_ENDPOINTS.BORROWINGS}/student/${studentId}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch student borrowings');
  }

  // Get overdue books
  async getOverdueBooks(): Promise<BookBorrowing[]> {
    const response = await apiService.get<BookBorrowing[]>(`${this.LIBRARY_ENDPOINTS.BORROWINGS}/overdue`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch overdue books');
  }

  // Get library reports
  async getLibraryReports(schoolId?: string, dateFrom?: string, dateTo?: string): Promise<any> {
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
      `${this.LIBRARY_ENDPOINTS.REPORTS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch library reports');
  }

  // Get library stats
  async getLibraryStats(schoolId?: string): Promise<any> {
    const params = new URLSearchParams();
    
    if (schoolId) {
      params.append('schoolId', schoolId);
    }

    const response = await apiService.get<any>(
      `${this.LIBRARY_ENDPOINTS.REPORTS}/stats?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch library stats');
  }
}

// Export singleton instance
export const libraryService = new LibraryService();
export default libraryService; 