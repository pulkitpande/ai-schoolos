// Export all services
export { default as apiService, ApiService } from './api';
export type { ApiResponse } from './api';
export { default as authService, AuthService } from './auth';
export type { User, LoginCredentials, LoginResponse, RegisterData } from './auth';
export { default as studentService, StudentService } from './student';
export type { Student, CreateStudentData, UpdateStudentData, StudentFilters, StudentListResponse } from './student';
export { default as staffService, StaffService } from './staff';
export type { Staff, CreateStaffData, UpdateStaffData, StaffFilters, StaffListResponse } from './staff';