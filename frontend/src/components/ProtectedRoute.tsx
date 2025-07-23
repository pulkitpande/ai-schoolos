'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../contexts/AuthContext';

interface ProtectedRouteProps {
  children: React.ReactNode;
  allowedRoles?: string[];
  redirectTo?: string;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  allowedRoles = [],
  redirectTo = '/login',
}) => {
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (!isAuthenticated) {
        router.push(redirectTo);
        return;
      }

      if (allowedRoles.length > 0 && user && !allowedRoles.includes(user.role)) {
        // Redirect to appropriate portal based on user role
        const roleRedirects: Record<string, string> = {
          admin: '/admin',
          teacher: '/teacher',
          student: '/student',
          parent: '/parent',
          super_admin: '/super-admin',
        };

        const redirectPath = roleRedirects[user.role] || '/login';
        router.push(redirectPath);
        return;
      }
    }
  }, [isAuthenticated, isLoading, user, allowedRoles, router, redirectTo]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Will redirect to login
  }

  if (allowedRoles.length > 0 && user && !allowedRoles.includes(user.role)) {
    return null; // Will redirect to appropriate portal
  }

  return <>{children}</>;
};

// Role-specific route components
export const AdminRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <ProtectedRoute allowedRoles={['admin', 'super_admin']} redirectTo="/admin">
    {children}
  </ProtectedRoute>
);

export const TeacherRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <ProtectedRoute allowedRoles={['teacher', 'admin', 'super_admin']} redirectTo="/teacher">
    {children}
  </ProtectedRoute>
);

export const StudentRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <ProtectedRoute allowedRoles={['student']} redirectTo="/student">
    {children}
  </ProtectedRoute>
);

export const ParentRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <ProtectedRoute allowedRoles={['parent']} redirectTo="/parent">
    {children}
  </ProtectedRoute>
);

export const SuperAdminRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <ProtectedRoute allowedRoles={['super_admin']} redirectTo="/super-admin">
    {children}
  </ProtectedRoute>
); 