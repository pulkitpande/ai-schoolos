'use client';

import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function TestSuperAdminPage() {
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    console.log('Test Super Admin Debug:', { user, isAuthenticated, isLoading });
  }, [user, isAuthenticated, isLoading]);

  const handleSuperAdminLogin = async () => {
    try {
      // Simulate super admin login
      const response = await fetch('/api/test-login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: 'superadmin@schoolos.com', password: 'password' })
      });
      
      if (response.ok) {
        router.push('/super-admin');
      }
    } catch (error) {
      console.error('Test login failed:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Super Admin Login Test</h1>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Debug Information</h2>
          <div className="space-y-2">
            <p><strong>Is Loading:</strong> {isLoading ? 'Yes' : 'No'}</p>
            <p><strong>Is Authenticated:</strong> {isAuthenticated ? 'Yes' : 'No'}</p>
            {user && (
              <div>
                <p><strong>User Email:</strong> {user.email}</p>
                <p><strong>User Role:</strong> {user.role}</p>
                <p><strong>User Name:</strong> {user.firstName} {user.lastName}</p>
              </div>
            )}
          </div>
          
          <div className="mt-6 space-y-4">
            <button
              onClick={handleSuperAdminLogin}
              className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
            >
              Test Super Admin Login
            </button>
            
            <button
              onClick={() => router.push('/super-admin')}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 ml-2"
            >
              Go to Super Admin Portal
            </button>
            
            <button
              onClick={() => router.push('/login')}
              className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 ml-2"
            >
              Go to Login Page
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 