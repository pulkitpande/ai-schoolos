'use client';

import { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useStudents, useStaff } from '../../hooks/useApi';

export default function TestApiPage() {
  const { user, login, logout, isAuthenticated } = useAuth();
  const { data: students, isLoading: studentsLoading } = useStudents();
  const { data: staff, isLoading: staffLoading } = useStaff();
  
  const [email, setEmail] = useState('admin@schoolos.com');
  const [password, setPassword] = useState('admin123');

  const handleLogin = async () => {
    try {
      await login(email, password);
    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">API Test Page</h1>
        
        {/* Authentication Status */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Authentication Status</h2>
          <div className="space-y-2">
            <p><strong>Is Authenticated:</strong> {isAuthenticated ? 'Yes' : 'No'}</p>
            {user && (
              <div>
                <p><strong>User:</strong> {user.firstName} {user.lastName}</p>
                <p><strong>Role:</strong> {user.role}</p>
                <p><strong>Email:</strong> {user.email}</p>
              </div>
            )}
          </div>
          
          {!isAuthenticated ? (
            <div className="mt-4 space-y-4">
              <div>
                <input
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="border rounded px-3 py-2 mr-2"
                />
                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="border rounded px-3 py-2 mr-2"
                />
                <button
                  onClick={handleLogin}
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                  Login
                </button>
              </div>
            </div>
          ) : (
            <button
              onClick={logout}
              className="mt-4 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
            >
              Logout
            </button>
          )}
        </div>

        {/* API Test Results */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Students API */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Students API</h2>
            {studentsLoading ? (
              <p>Loading students...</p>
            ) : students ? (
              <div>
                <p><strong>Total Students:</strong> {students.total}</p>
                <p><strong>Students Loaded:</strong> {students.students.length}</p>
                <div className="mt-4 max-h-40 overflow-y-auto">
                  {students.students.slice(0, 5).map((student) => (
                    <div key={student.id} className="text-sm p-2 bg-gray-50 rounded mb-2">
                      {student.firstName} {student.lastName} - {student.grade}
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <p className="text-red-600">Failed to load students</p>
            )}
          </div>

          {/* Staff API */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Staff API</h2>
            {staffLoading ? (
              <p>Loading staff...</p>
            ) : staff ? (
              <div>
                <p><strong>Total Staff:</strong> {staff.total}</p>
                <p><strong>Staff Loaded:</strong> {staff.staff.length}</p>
                <div className="mt-4 max-h-40 overflow-y-auto">
                  {staff.staff.slice(0, 5).map((member) => (
                    <div key={member.id} className="text-sm p-2 bg-gray-50 rounded mb-2">
                      {member.firstName} {member.lastName} - {member.position}
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <p className="text-red-600">Failed to load staff</p>
            )}
          </div>
        </div>

        {/* Quick Navigation */}
        <div className="mt-8 bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Quick Navigation</h2>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <a href="/admin" className="bg-blue-600 text-white p-3 rounded text-center hover:bg-blue-700">
              Admin Portal
            </a>
            <a href="/teacher" className="bg-green-600 text-white p-3 rounded text-center hover:bg-green-700">
              Teacher Portal
            </a>
            <a href="/student" className="bg-purple-600 text-white p-3 rounded text-center hover:bg-purple-700">
              Student Portal
            </a>
            <a href="/parent" className="bg-orange-600 text-white p-3 rounded text-center hover:bg-orange-700">
              Parent Portal
            </a>
            <a href="/super-admin" className="bg-red-600 text-white p-3 rounded text-center hover:bg-red-700">
              Super Admin
            </a>
          </div>
        </div>
      </div>
    </div>
  );
} 