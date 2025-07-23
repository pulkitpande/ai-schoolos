import { apiService, ApiResponse } from './api';

// User types
export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: 'admin' | 'teacher' | 'student' | 'parent' | 'super_admin';
  schoolId?: string;
  tenantId?: string;
  avatar?: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface LoginResponse {
  user: User;
  token: string;
  refreshToken: string;
  expiresIn: number;
}

export interface RegisterData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role: 'admin' | 'teacher' | 'student' | 'parent';
  schoolId?: string;
  tenantId?: string;
}

// Auth Service class
export class AuthService {
  private readonly AUTH_ENDPOINTS = {
    LOGIN: '/api/v1/auth/login',
    REGISTER: '/api/v1/auth/register',
    LOGOUT: '/api/v1/auth/logout',
    REFRESH: '/api/v1/auth/refresh',
    ME: '/api/v1/auth/me',
    VERIFY_EMAIL: '/api/v1/auth/verify-email',
    FORGOT_PASSWORD: '/api/v1/auth/forgot-password',
    RESET_PASSWORD: '/api/v1/auth/reset-password',
  };

  // Login user
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await apiService.post<LoginResponse>(this.AUTH_ENDPOINTS.LOGIN, credentials);
    
    if (response.success && response.data) {
      // Store tokens
      if (typeof window !== 'undefined') {
        localStorage.setItem('authToken', response.data.token);
        localStorage.setItem('refreshToken', response.data.refreshToken);
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      
      return response.data;
    }
    
    throw new Error(response.message || 'Login failed');
  }

  // Register user
  async register(data: RegisterData): Promise<LoginResponse> {
    const response = await apiService.post<LoginResponse>(this.AUTH_ENDPOINTS.REGISTER, data);
    
    if (response.success && response.data) {
      // Store tokens
      if (typeof window !== 'undefined') {
        localStorage.setItem('authToken', response.data.token);
        localStorage.setItem('refreshToken', response.data.refreshToken);
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      
      return response.data;
    }
    
    throw new Error(response.message || 'Registration failed');
  }

  // Logout user
  async logout(): Promise<void> {
    try {
      await apiService.post(this.AUTH_ENDPOINTS.LOGOUT);
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local storage
      if (typeof window !== 'undefined') {
        localStorage.removeItem('authToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('user');
      }
    }
  }

  // Get current user
  async getCurrentUser(): Promise<User> {
    const response = await apiService.get<User>(this.AUTH_ENDPOINTS.ME);
    
    if (response.success && response.data) {
      // Update stored user data
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(response.data));
      }
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to get user data');
  }

  // Refresh token
  async refreshToken(): Promise<LoginResponse> {
    if (typeof window === 'undefined') {
      throw new Error('Cannot refresh token on server side');
    }
    
    const refreshToken = localStorage.getItem('refreshToken');
    
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await apiService.post<LoginResponse>(this.AUTH_ENDPOINTS.REFRESH, {
      refreshToken,
    });
    
    if (response.success && response.data) {
      // Update tokens
      localStorage.setItem('authToken', response.data.token);
      localStorage.setItem('refreshToken', response.data.refreshToken);
      
      return response.data;
    }
    
    throw new Error(response.message || 'Token refresh failed');
  }

  // Verify email
  async verifyEmail(token: string): Promise<void> {
    const response = await apiService.post(this.AUTH_ENDPOINTS.VERIFY_EMAIL, { token });
    
    if (!response.success) {
      throw new Error(response.message || 'Email verification failed');
    }
  }

  // Forgot password
  async forgotPassword(email: string): Promise<void> {
    const response = await apiService.post(this.AUTH_ENDPOINTS.FORGOT_PASSWORD, { email });
    
    if (!response.success) {
      throw new Error(response.message || 'Password reset request failed');
    }
  }

  // Reset password
  async resetPassword(token: string, newPassword: string): Promise<void> {
    const response = await apiService.post(this.AUTH_ENDPOINTS.RESET_PASSWORD, {
      token,
      newPassword,
    });
    
    if (!response.success) {
      throw new Error(response.message || 'Password reset failed');
    }
  }

  // Update user profile
  async updateProfile(profileData: any): Promise<LoginResponse> {
    const response = await apiService.put<LoginResponse>('/api/v1/auth/profile', profileData);
    
    if (response.success && response.data) {
      // Update stored user data
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(response.data.user));
      }
      return response.data;
    }
    
    throw new Error(response.message || 'Profile update failed');
  }

  // Change password
  async changePassword(passwordData: any): Promise<void> {
    const response = await apiService.post('/api/v1/auth/change-password', passwordData);
    
    if (!response.success) {
      throw new Error(response.message || 'Password change failed');
    }
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    if (typeof window === 'undefined') {
      return false; // Server-side rendering
    }
    const token = localStorage.getItem('authToken');
    return !!token;
  }

  // Get stored user data
  getStoredUser(): User | null {
    if (typeof window === 'undefined') {
      return null; // Server-side rendering
    }
    const userData = localStorage.getItem('user');
    return userData ? JSON.parse(userData) : null;
  }

  // Check if token is expired
  isTokenExpired(): boolean {
    if (typeof window === 'undefined') {
      return true; // Server-side rendering
    }
    const token = localStorage.getItem('authToken');
    if (!token) return true;

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      return payload.exp * 1000 < Date.now();
    } catch {
      return true;
    }
  }

  // Get user role
  getUserRole(): string | null {
    const user = this.getStoredUser();
    return user?.role || null;
  }

  // Get stored token
  getToken(): string | null {
    if (typeof window === 'undefined') {
      return null; // Server-side rendering
    }
    return localStorage.getItem('authToken');
  }

  // Check if user has specific role
  hasRole(role: string): boolean {
    const userRole = this.getUserRole();
    return userRole === role;
  }

  // Check if user has any of the specified roles
  hasAnyRole(roles: string[]): boolean {
    const userRole = this.getUserRole();
    return userRole ? roles.includes(userRole) : false;
  }
}

// Export singleton instance
export const authService = new AuthService();
export default authService; 