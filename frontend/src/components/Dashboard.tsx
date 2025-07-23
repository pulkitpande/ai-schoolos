'use client';

import React from 'react';
import { 
  Users, 
  GraduationCap, 
  BookOpen, 
  Calendar, 
  DollarSign, 
  TrendingUp,
  Clock,
  CheckCircle,
  AlertCircle,
  UserCheck,
  Library,
  Bus,
  MessageSquare,
  BarChart3,
  Bell
} from 'lucide-react';
import { useStudents } from '../hooks/useApi';
import { useStaff } from '../hooks/useApi';
import { useFeePayments } from '../hooks/useApi';
import { useAttendance } from '../hooks/useApi';
import { useExams } from '../hooks/useApi';
import { useBooks } from '../hooks/useApi';
import { useVehicles } from '../hooks/useApi';
import { useMessages } from '../hooks/useApi';
import { useAnalyticsData } from '../hooks/useApi';
import { useNotifications } from '../hooks/useApi';

interface DashboardProps {
  userRole?: string;
}

export default function Dashboard({ userRole = 'admin' }: DashboardProps) {
  // Fetch data from all services
  const { data: studentsData, isLoading: studentsLoading } = useStudents();
  const { data: staffData, isLoading: staffLoading } = useStaff();
  const { data: feePaymentsData, isLoading: feesLoading } = useFeePayments();
  const { data: attendanceData, isLoading: attendanceLoading } = useAttendance();
  const { data: examsData, isLoading: examsLoading } = useExams();
  const { data: booksData, isLoading: booksLoading } = useBooks();
  const { data: vehiclesData, isLoading: vehiclesLoading } = useVehicles();
  const { data: messagesData, isLoading: messagesLoading } = useMessages();
  const { data: analyticsData, isLoading: analyticsLoading } = useAnalyticsData();
  const { data: notificationsData, isLoading: notificationsLoading } = useNotifications();

  // Calculate metrics
  const totalStudents = studentsData?.total || 0;
  const totalStaff = staffData?.total || 0;
  const totalFees = feePaymentsData?.total || 0;
  const totalAttendance = attendanceData?.total || 0;
  const totalExams = examsData?.total || 0;
  const totalBooks = booksData?.total || 0;
  const totalVehicles = vehiclesData?.total || 0;
  const totalMessages = messagesData?.total || 0;
  const totalNotifications = notificationsData?.total || 0;

  // Mock data for demonstration
  const mockMetrics = {
    attendanceRate: 95.2,
    feeCollectionRate: 87.5,
    examPassRate: 92.1,
    libraryUtilization: 78.3,
    transportEfficiency: 89.7,
    communicationResponse: 94.2,
  };

  const isLoading = studentsLoading || staffLoading || feesLoading || attendanceLoading || 
                   examsLoading || booksLoading || vehiclesLoading || messagesLoading || 
                   analyticsLoading || notificationsLoading;

  if (isLoading) {
    return (
      <div className="p-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[...Array(8)].map((_, i) => (
            <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
              <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-1/2 mb-4"></div>
              <div className="h-8 bg-gray-200 rounded w-1/3"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Welcome back! Here's what's happening in your school.</p>
        </div>
        <div className="flex space-x-2">
          <button className="flex items-center px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
            <Calendar className="w-4 h-4 mr-2" />
            Today
          </button>
          <button className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700">
            <TrendingUp className="w-4 h-4 mr-2" />
            View Reports
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-gray-500">Total Students</h3>
            <Users className="h-4 w-4 text-gray-400" />
          </div>
          <div className="mt-2">
            <div className="text-2xl font-bold text-gray-900">{totalStudents.toLocaleString()}</div>
            <p className="text-xs text-gray-500">+12% from last month</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-gray-500">Total Staff</h3>
            <GraduationCap className="h-4 w-4 text-gray-400" />
          </div>
          <div className="mt-2">
            <div className="text-2xl font-bold text-gray-900">{totalStaff.toLocaleString()}</div>
            <p className="text-xs text-gray-500">+5% from last month</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-gray-500">Fee Collections</h3>
            <DollarSign className="h-4 w-4 text-gray-400" />
          </div>
          <div className="mt-2">
            <div className="text-2xl font-bold text-gray-900">₹{totalFees.toLocaleString()}</div>
            <p className="text-xs text-gray-500">{mockMetrics.feeCollectionRate}% collection rate</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-gray-500">Attendance Rate</h3>
            <UserCheck className="h-4 w-4 text-gray-400" />
          </div>
          <div className="mt-2">
            <div className="text-2xl font-bold text-gray-900">{mockMetrics.attendanceRate}%</div>
            <p className="text-xs text-gray-500">{totalAttendance} records today</p>
          </div>
        </div>
      </div>

      {/* Academic Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-gray-500">Exams</h3>
            <BookOpen className="h-4 w-4 text-gray-400" />
          </div>
          <div className="mt-2">
            <div className="text-2xl font-bold text-gray-900">{totalExams}</div>
            <p className="text-xs text-gray-500">{mockMetrics.examPassRate}% pass rate</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-gray-500">Library Books</h3>
            <Library className="h-4 w-4 text-gray-400" />
          </div>
          <div className="mt-2">
            <div className="text-2xl font-bold text-gray-900">{totalBooks}</div>
            <p className="text-xs text-gray-500">{mockMetrics.libraryUtilization}% utilization</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-gray-500">Transport Vehicles</h3>
            <Bus className="h-4 w-4 text-gray-400" />
          </div>
          <div className="mt-2">
            <div className="text-2xl font-bold text-gray-900">{totalVehicles}</div>
            <p className="text-xs text-gray-500">{mockMetrics.transportEfficiency}% efficiency</p>
          </div>
        </div>
      </div>

      {/* Communication & Notifications */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-gray-500">Messages</h3>
            <MessageSquare className="h-4 w-4 text-gray-400" />
          </div>
          <div className="mt-2">
            <div className="text-2xl font-bold text-gray-900">{totalMessages}</div>
            <p className="text-xs text-gray-500">{mockMetrics.communicationResponse}% response rate</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-gray-500">Notifications</h3>
            <Bell className="h-4 w-4 text-gray-400" />
          </div>
          <div className="mt-2">
            <div className="text-2xl font-bold text-gray-900">{totalNotifications}</div>
            <p className="text-xs text-gray-500">Active notifications</p>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            <div className="flex items-center space-x-4">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                  <CheckCircle className="h-4 w-4 text-green-600" />
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">New student enrolled</p>
                <p className="text-sm text-gray-500">Sarah Johnson • 2 hours ago</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <DollarSign className="h-4 w-4 text-blue-600" />
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">Fee payment received</p>
                <p className="text-sm text-gray-500">Mike Chen • 4 hours ago</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                  <BookOpen className="h-4 w-4 text-purple-600" />
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">Exam results published</p>
                <p className="text-sm text-gray-500">Dr. Williams • 6 hours ago</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 