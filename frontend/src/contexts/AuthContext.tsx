'use client';

import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import { authService, User } from '../services/auth';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<any>;
  logout: () => void;
  register: (userData: any) => Promise<any>;
  updateProfile: (profileData: any) => Promise<any>;
  changePassword: (passwordData: any) => Promise<any>;
  refreshToken: () => Promise<any>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Initialize auth state
  useEffect(() => {
    const initAuth = () => {
      try {
        const storedUser = authService.getStoredUser();
        const token = authService.getToken();
        const loginTime = localStorage.getItem('loginTime');
        
        console.log('Auth init - storedUser:', storedUser);
        console.log('Auth init - token:', token);
        console.log('Auth init - loginTime:', loginTime);
        
        // Check if session has expired (24 hours for development)
        const sessionExpiry = 24 * 60 * 60 * 1000; // 24 hours in milliseconds
        const isSessionExpired = loginTime && (Date.now() - parseInt(loginTime)) > sessionExpiry;
        
        if (storedUser && token && !isSessionExpired) {
          console.log('Setting authenticated user:', storedUser);
          setUser(storedUser);
          setIsAuthenticated(true);
        } else {
          console.log('No stored user, token, or session expired');
          // Clear expired session data
          if (isSessionExpired) {
            console.log('Session expired, clearing data');
            authService.logout();
          }
          setUser(null);
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
        // Clear any invalid data
        authService.logout();
        setUser(null);
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    try {
      console.log('Login attempt:', email);
      
      // Clear any existing session data before new login
      if (typeof window !== 'undefined') {
        localStorage.removeItem('authToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('user');
        localStorage.removeItem('loginTime'); // Clear login time on new login
      }
      
      // For development, we'll use mock authentication
      const role = email.includes('superadmin') ? 'super_admin' : 
                   email.includes('admin') ? 'admin' : 
                   email.includes('teacher') ? 'teacher' : 
                   email.includes('student') ? 'student' : 
                   email.includes('parent') ? 'parent' : 'admin';
      
      const mockUser = {
        id: '1',
        email: email,
        firstName: email.split('@')[0].charAt(0).toUpperCase() + email.split('@')[0].slice(1),
        lastName: 'User',
        role: role as 'admin' | 'teacher' | 'student' | 'parent' | 'super_admin',
        schoolId: 'school-1',
        tenantId: 'tenant-1',
        avatar: '',
        isActive: true,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      const mockResponse = {
        user: mockUser,
        token: 'mock-jwt-token',
        refreshToken: 'mock-refresh-token',
        expiresIn: 3600,
      };

      console.log('Setting user after login:', mockUser);

      // Store in localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem('authToken', mockResponse.token);
        localStorage.setItem('refreshToken', mockResponse.refreshToken);
        localStorage.setItem('user', JSON.stringify(mockResponse.user));
        localStorage.setItem('loginTime', Date.now().toString()); // Store login time
      }

      setUser(mockResponse.user);
      setIsAuthenticated(true);
      return mockResponse;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }, []);

  const logout = useCallback(() => {
    try {
      console.log('Logging out');
      authService.logout();
      // Also clear login time
      if (typeof window !== 'undefined') {
        localStorage.removeItem('loginTime');
      }
      setUser(null);
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Logout error:', error);
    }
  }, []);

  const register = useCallback(async (userData: any) => {
    try {
      const response = await authService.register(userData);
      setUser(response.user);
      setIsAuthenticated(true);
      return response;
    } catch (error) {
      console.error('Register error:', error);
      throw error;
    }
  }, []);

  const updateProfile = useCallback(async (profileData: any) => {
    try {
      const response = await authService.updateProfile(profileData);
      setUser(response.user);
      return response;
    } catch (error) {
      console.error('Profile update error:', error);
      throw error;
    }
  }, []);

  const changePassword = useCallback(async (passwordData: any) => {
    try {
      const response = await authService.changePassword(passwordData);
      return response;
    } catch (error) {
      console.error('Password change error:', error);
      throw error;
    }
  }, []);

  const refreshToken = useCallback(async () => {
    try {
      const response = await authService.refreshToken();
      setUser(response.user);
      setIsAuthenticated(true);
      return response;
    } catch (error) {
      console.error('Token refresh error:', error);
      logout();
      throw error;
    }
  }, [logout]);

  const value: AuthContextType = {
    user,
    isAuthenticated,
    isLoading,
    login,
    logout,
    register,
    updateProfile,
    changePassword,
    refreshToken,
  };

  console.log('AuthContext value:', { user, isAuthenticated, isLoading });

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}; 