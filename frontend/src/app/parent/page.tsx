'use client';

import { useState } from 'react';
import { 
  Users, 
  BookOpen, 
  Calendar, 
  FileText, 
  Clock, 
  BarChart3, 
  Settings, 
  Bell,
  DollarSign,
  MessageSquare,
  TrendingUp
} from 'lucide-react';
import { ParentRoute } from '../../components/ProtectedRoute';
import { useAuth } from '../../contexts/AuthContext';
import Navigation from '../../components/Navigation';
import { useRouter } from 'next/navigation';
import { Dialog } from '@headlessui/react';
import { useStudents, useStaff, useStudentStats, useStaffStats, useCreateStudent, useUpdateStudent, useDeleteStudent, useCreateStaff, useUpdateStaff, useDeleteStaff, useFeePayments, useCreateFeePayment, useUpdateFeePayment, useDeleteFeePayment, useExams, useCreateExam, useUpdateExam, useDeleteExam, useAttendance, useCreateAttendance, useUpdateAttendance, useDeleteAttendance, useHomework, useCreateHomework, useUpdateHomework, useDeleteHomework, useTimetables, useCreateTimetable, useUpdateTimetable, useDeleteTimetable, useBooks, useCreateBook, useUpdateBook, useDeleteBook, useVehicles, useCreateVehicle, useUpdateVehicle, useDeleteVehicle, useMessages, useCreateMessage, useUpdateMessage, useDeleteMessage } from '../../hooks/useApi';

export default function ParentPortal() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const router = useRouter();

  // Modal states
  const [isMessageModalOpen, setMessageModalOpen] = useState(false);
  const [isPaymentModalOpen, setPaymentModalOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState<any>(null);
  const [formState, setFormState] = useState<any>({});
  const [formError, setFormError] = useState<string | null>(null);

  // API hooks
  const { data: studentsData, isLoading: studentsLoading, error: studentsError } = useStudents();
  const { data: attendanceData, isLoading: attendanceLoading, error: attendanceError } = useAttendance();
  const { data: homeworkData, isLoading: homeworkLoading, error: homeworkError } = useHomework();
  const { data: messageData, isLoading: messageLoading, error: messageError } = useMessages();
  const { data: feeData, isLoading: feeLoading, error: feeError } = useFeePayments();
  const { data: timetableData, isLoading: timetableLoading, error: timetableError } = useTimetables();
  const { data: transportData, isLoading: transportLoading, error: transportError } = useVehicles();
  const createMessage = useCreateMessage();
  const createFeePayment = useCreateFeePayment();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  const handleContactTeacher = () => {
    setFormState({});
    setFormError(null);
    setSelectedItem(null);
    setMessageModalOpen(true);
  };

  const handlePayFees = () => {
    setFormState({});
    setFormError(null);
    setSelectedItem(null);
    setPaymentModalOpen(true);
  };

  const handleViewSchedule = () => {
    setActiveTab('timetable');
  };

  const handleFormChange = (e: any) => {
    setFormState({ ...formState, [e.target.name]: e.target.value });
  };

  const handleMessageSubmit = async (e: any) => {
    e.preventDefault();
    setFormError(null);
    try {
      await createMessage.mutateAsync(formState);
      setMessageModalOpen(false);
    } catch (err: any) {
      setFormError(err.message || 'Failed to send message');
    }
  };

  const handlePaymentSubmit = async (e: any) => {
    e.preventDefault();
    setFormError(null);
    try {
      await createFeePayment.mutateAsync(formState);
      setPaymentModalOpen(false);
    } catch (err: any) {
      setFormError(err.message || 'Failed to process payment');
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Not Authenticated</h2>
          <p className="text-gray-600">Please log in to access the parent portal.</p>
        </div>
      </div>
    );
  }

  const stats = [
    { 
      title: 'My Children', 
      value: studentsData?.students?.length || '0', 
      change: '', 
      icon: Users,
      loading: studentsLoading 
    },
    { 
      title: 'Fee Balance', 
      value: feeData?.total ? `$${feeData.total}` : '$0', 
      change: '-$50', 
      icon: DollarSign,
      loading: feeLoading 
    },
    { 
      title: 'Attendance', 
      value: attendanceData?.attendance?.length ? '95%' : '0%', 
      change: '+2%', 
      icon: Clock,
      loading: attendanceLoading 
    },
    { 
      title: 'Average Grade', 
      value: 'A-', 
      change: '+5%', 
      icon: BarChart3,
      loading: false 
    },
  ];

  const serviceTabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'children', label: 'My Children', icon: Users },
    { id: 'grades', label: 'Grades', icon: BarChart3 },
    { id: 'attendance', label: 'Attendance', icon: Clock },
    { id: 'fees', label: 'Fees', icon: DollarSign },
    { id: 'assignments', label: 'Assignments', icon: FileText },
    { id: 'timetable', label: 'Timetable', icon: Calendar },
    { id: 'communication', label: 'Messages', icon: MessageSquare },
    { id: 'transport', label: 'Transport', icon: Calendar },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <ParentRoute>
      <div className="flex h-screen bg-gray-50">
        {/* Sidebar */}
        <aside className="w-64 bg-white shadow-lg">
          <div className="p-6">
            <h1 className="text-2xl font-bold text-gray-900">AI SchoolOS</h1>
            <p className="text-sm text-gray-600">Parent Portal</p>
          </div>
          <Navigation />
        </aside>

        {/* Main Content */}
        <main className="flex-1 flex flex-col overflow-hidden">
          {/* Header */}
          <header className="bg-white shadow-sm border-b">
            <div className="px-6 py-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">
                    Parent Dashboard
                  </h2>
                  <p className="text-sm text-gray-600">
                    Welcome back, {user?.firstName} {user?.lastName}
                  </p>
                </div>
                <div className="flex items-center space-x-4">
                  <button className="p-2 text-gray-400 hover:text-gray-600">
                    <Bell className="h-6 w-6" />
                  </button>
                  <button 
                    onClick={handleLogout}
                    className="text-sm text-gray-600 hover:text-gray-900"
                  >
                    Logout
                  </button>
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-medium">P</span>
                    </div>
                    <span className="text-sm font-medium text-gray-700">Parent</span>
                  </div>
                </div>
              </div>
            </div>
          </header>

          {/* Page Content */}
          <div className="flex-1 overflow-auto">
            <div className="p-6">
              {/* Navigation Tabs */}
              <nav className="flex space-x-8 mb-8 overflow-x-auto">
                {serviceTabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors whitespace-nowrap ${
                      activeTab === tab.id
                        ? 'bg-orange-100 text-orange-700'
                        : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <tab.icon className="h-4 w-4" />
                    <span>{tab.label}</span>
                  </button>
                ))}
              </nav>

              {/* Dashboard Content */}
              {activeTab === 'dashboard' && (
                <div className="space-y-6">
                  {/* Stats Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {stats.map((stat, index) => (
                      <div key={index} className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center">
                          <div className="flex-shrink-0">
                            <stat.icon className="h-8 w-8 text-orange-600" />
                          </div>
                          <div className="ml-5 w-0 flex-1">
                            <dl>
                              <dt className="text-sm font-medium text-gray-500 truncate">
                                {stat.title}
                              </dt>
                              <dd className="flex items-baseline">
                                <div className="text-2xl font-semibold text-gray-900">
                                  {stat.loading ? '...' : stat.value}
                                </div>
                                {stat.change && (
                                  <div className="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                                    {stat.change}
                                  </div>
                                )}
                              </dd>
                            </dl>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Quick Actions */}
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
                    </div>
                    <div className="p-6">
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <button 
                          onClick={handlePayFees}
                          className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-orange-600 hover:bg-orange-700 transition-colors"
                        >
                          <DollarSign className="h-4 w-4 mr-2" />
                          Pay Fees
                        </button>
                        <button 
                          onClick={handleContactTeacher}
                          className="flex items-center justify-center px-4 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
                        >
                          <MessageSquare className="h-4 w-4 mr-2" />
                          Contact Teacher
                        </button>
                        <button 
                          onClick={handleViewSchedule}
                          className="flex items-center justify-center px-4 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
                        >
                          <Calendar className="h-4 w-4 mr-2" />
                          View Schedule
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Recent Activities */}
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-medium text-gray-900">Recent Activities</h3>
                    </div>
                    <div className="p-6">
                      <div className="space-y-4">
                        {studentsLoading ? (
                          <div className="text-center text-gray-500">Loading activities...</div>
                        ) : (
                          <>
                            <div className="flex items-center space-x-4">
                              <div className="flex-shrink-0">
                                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                                  <BarChart3 className="h-4 w-4 text-green-600" />
                                </div>
                              </div>
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900">
                                  Grade received for {studentsData?.students?.[0]?.firstName || 'Child'}
                                </p>
                                <p className="text-sm text-gray-500">
                                  Math Test • 1 day ago
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center space-x-4">
                              <div className="flex-shrink-0">
                                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                                  <DollarSign className="h-4 w-4 text-blue-600" />
                                </div>
                              </div>
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900">
                                  Fee payment made
                                </p>
                                <p className="text-sm text-gray-500">
                                  ${feeData?.total || 0} • 2 days ago
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center space-x-4">
                              <div className="flex-shrink-0">
                                <div className="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                                  <MessageSquare className="h-4 w-4 text-yellow-600" />
                                </div>
                              </div>
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900">
                                  Message from teacher
                                </p>
                                <p className="text-sm text-gray-500">
                                  {messageData?.messages?.length || 0} messages • 3 days ago
                                </p>
                              </div>
                            </div>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Children Tab */}
              {activeTab === 'children' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-medium text-gray-900">My Children</h3>
                    </div>
                    <div className="p-6">
                      {studentsLoading ? (
                        <div className="text-center text-gray-500">Loading children...</div>
                      ) : studentsError ? (
                        <div className="text-center text-red-500">{studentsError.message || 'Failed to load children'}</div>
                      ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                          {(studentsData?.students || []).map((student: any) => (
                            <div key={student.id} className="border border-gray-200 rounded-lg p-4">
                              <h4 className="font-semibold text-gray-900 mb-2">{student.firstName} {student.lastName}</h4>
                              <p className="text-sm text-gray-600 mb-2">Class: {student.className || 'N/A'}</p>
                              <p className="text-sm text-gray-600 mb-2">Status: {student.isActive ? 'Active' : 'Inactive'}</p>
                              <div className="flex space-x-2">
                                <button className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded hover:bg-blue-200">
                                  View Details
                                </button>
                                <button className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded hover:bg-green-200">
                                  Contact
                                </button>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Attendance Tab */}
              {activeTab === 'attendance' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-medium text-gray-900">Attendance</h3>
                    </div>
                    <div className="p-6">
                      {attendanceLoading ? (
                        <div className="text-center text-gray-500">Loading attendance...</div>
                      ) : attendanceError ? (
                        <div className="text-center text-red-500">{attendanceError.message || 'Failed to load attendance'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Student</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(attendanceData?.attendance || []).map((record: any) => (
                                <tr key={record.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{record.studentId}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{record.date}</td>
                                  <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                      record.status === 'present' ? 'bg-green-100 text-green-800' : 
                                      record.status === 'absent' ? 'bg-red-100 text-red-800' : 
                                      record.status === 'late' ? 'bg-yellow-100 text-yellow-800' : 
                                      'bg-gray-100 text-gray-500'
                                    }`}>
                                      {record.status}
                                    </span>
                                  </td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{record.time}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Fees Tab */}
              {activeTab === 'fees' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Fees</h3>
                        <button 
                          onClick={handlePayFees}
                          className="bg-orange-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-orange-700"
                        >
                          Pay Fees
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {feeLoading ? (
                        <div className="text-center text-gray-500">Loading fees...</div>
                      ) : feeError ? (
                        <div className="text-center text-red-500">{feeError.message || 'Failed to load fees'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Student</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(feeData?.payments || []).map((payment: any) => (
                                <tr key={payment.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{payment.studentId}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${payment.amount}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{payment.dueDate}</td>
                                  <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                      payment.paymentStatus === 'paid' ? 'bg-green-100 text-green-800' : 
                                      payment.paymentStatus === 'pending' ? 'bg-yellow-100 text-yellow-800' : 
                                      payment.paymentStatus === 'overdue' ? 'bg-red-100 text-red-800' : 
                                      'bg-gray-100 text-gray-500'
                                    }`}>
                                      {payment.paymentStatus}
                                    </span>
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Assignments Tab */}
              {activeTab === 'assignments' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-medium text-gray-900">Assignments</h3>
                    </div>
                    <div className="p-6">
                      {homeworkLoading ? (
                        <div className="text-center text-gray-500">Loading assignments...</div>
                      ) : homeworkError ? (
                        <div className="text-center text-red-500">{homeworkError.message || 'Failed to load assignments'}</div>
                      ) : (
                        <div className="space-y-4">
                          {(homeworkData?.homework || []).map((assignment: any) => (
                            <div key={assignment.id} className="border border-gray-200 rounded-lg p-4">
                              <h4 className="font-semibold text-gray-900 mb-2">{assignment.title}</h4>
                              <p className="text-sm text-gray-600 mb-2">Subject: {assignment.subject}</p>
                              <p className="text-sm text-gray-600 mb-2">Due Date: {assignment.dueDate}</p>
                              <div className="flex justify-between items-center">
                                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                  assignment.status === 'active' ? 'bg-green-100 text-green-800' : 
                                  assignment.status === 'completed' ? 'bg-blue-100 text-blue-800' : 
                                  assignment.status === 'overdue' ? 'bg-red-100 text-red-800' : 
                                  'bg-gray-100 text-gray-500'
                                }`}>
                                  {assignment.status}
                                </span>
                                <span className="text-sm text-gray-600">Grade: -</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Timetable Tab */}
              {activeTab === 'timetable' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-medium text-gray-900">Timetable</h3>
                    </div>
                    <div className="p-6">
                      {timetableLoading ? (
                        <div className="text-center text-gray-500">Loading timetable...</div>
                      ) : timetableError ? (
                        <div className="text-center text-red-500">{timetableError.message || 'Failed to load timetable'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Day</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Subject</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Class</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(timetableData?.timetables || []).map((timetable: any) => (
                                <tr key={timetable.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{timetable.day}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{timetable.startTime} - {timetable.endTime}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{timetable.subject}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{timetable.className}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Communication Tab */}
              {activeTab === 'communication' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Messages</h3>
                        <button 
                          onClick={handleContactTeacher}
                          className="bg-orange-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-orange-700"
                        >
                          Send Message
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {messageLoading ? (
                        <div className="text-center text-gray-500">Loading messages...</div>
                      ) : messageError ? (
                        <div className="text-center text-red-500">{messageError.message || 'Failed to load messages'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Subject</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">From</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(messageData?.messages || []).map((message: any) => (
                                <tr key={message.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{message.subject}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{message.from}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{message.date}</td>
                                  <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                      message.status === 'sent' ? 'bg-green-100 text-green-800' : 
                                      message.status === 'pending' ? 'bg-yellow-100 text-yellow-800' : 
                                      message.status === 'failed' ? 'bg-red-100 text-red-800' : 
                                      'bg-gray-100 text-gray-500'
                                    }`}>
                                      {message.status}
                                    </span>
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Transport Tab */}
              {activeTab === 'transport' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-medium text-gray-900">Transport</h3>
                    </div>
                    <div className="p-6">
                      {transportLoading ? (
                        <div className="text-center text-gray-500">Loading transport...</div>
                      ) : transportError ? (
                        <div className="text-center text-red-500">{transportError.message || 'Failed to load transport'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vehicle Number</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Driver</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Route</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(transportData?.vehicles || []).map((vehicle: any) => (
                                <tr key={vehicle.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{vehicle.vehicleNumber}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{vehicle.driverName}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{vehicle.route}</td>
                                  <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                      vehicle.status === 'active' ? 'bg-green-100 text-green-800' : 
                                      vehicle.status === 'maintenance' ? 'bg-yellow-100 text-yellow-800' : 
                                      vehicle.status === 'inactive' ? 'bg-red-100 text-red-800' : 
                                      'bg-gray-100 text-gray-500'
                                    }`}>
                                      {vehicle.status}
                                    </span>
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              )}

              {/* Other tabs show placeholder */}
              {!['dashboard', 'children', 'attendance', 'fees', 'assignments', 'timetable', 'communication', 'transport'].includes(activeTab) && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">{serviceTabs.find(tab => tab.id === activeTab)?.label}</h3>
                  <p className="text-gray-600">This feature is coming soon...</p>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>

      {/* Message Modal */}
      <Dialog open={isMessageModalOpen} onClose={() => setMessageModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
        <div className="flex items-center justify-center min-h-screen px-4">
          <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
            <Dialog.Title className="text-lg font-bold mb-4">Send Message</Dialog.Title>
            <form onSubmit={handleMessageSubmit} className="space-y-4">
              <input type="text" name="subject" value={formState.subject || ''} onChange={handleFormChange} placeholder="Subject" className="w-full border rounded px-3 py-2" required />
              <input type="text" name="to" value={formState.to || ''} onChange={handleFormChange} placeholder="To" className="w-full border rounded px-3 py-2" required />
              <textarea name="message" value={formState.message || ''} onChange={handleFormChange} placeholder="Message" className="w-full border rounded px-3 py-2" rows={4} />
              <select name="type" value={formState.type || ''} onChange={handleFormChange} className="w-full border rounded px-3 py-2">
                <option value="">Select Type</option>
                <option value="email">Email</option>
                <option value="sms">SMS</option>
                <option value="notification">Notification</option>
              </select>
              {formError && <div className="text-red-600 text-sm">{formError}</div>}
              <button type="submit" className="w-full bg-orange-600 text-white py-2 rounded hover:bg-orange-700">Send Message</button>
              <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setMessageModalOpen(false)}>Close</button>
            </form>
          </div>
        </div>
      </Dialog>

      {/* Payment Modal */}
      <Dialog open={isPaymentModalOpen} onClose={() => setPaymentModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
        <div className="flex items-center justify-center min-h-screen px-4">
          <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
            <Dialog.Title className="text-lg font-bold mb-4">Pay Fees</Dialog.Title>
            <form onSubmit={handlePaymentSubmit} className="space-y-4">
              <input type="text" name="studentId" value={formState.studentId || ''} onChange={handleFormChange} placeholder="Student ID" className="w-full border rounded px-3 py-2" required />
              <input type="number" name="amount" value={formState.amount || ''} onChange={handleFormChange} placeholder="Amount" className="w-full border rounded px-3 py-2" required />
              <input type="date" name="paymentDate" value={formState.paymentDate || ''} onChange={handleFormChange} placeholder="Payment Date" className="w-full border rounded px-3 py-2" />
              <select name="paymentMethod" value={formState.paymentMethod || ''} onChange={handleFormChange} className="w-full border rounded px-3 py-2">
                <option value="">Select Payment Method</option>
                <option value="credit_card">Credit Card</option>
                <option value="debit_card">Debit Card</option>
                <option value="bank_transfer">Bank Transfer</option>
                <option value="cash">Cash</option>
              </select>
              {formError && <div className="text-red-600 text-sm">{formError}</div>}
              <button type="submit" className="w-full bg-orange-600 text-white py-2 rounded hover:bg-orange-700">Process Payment</button>
              <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setPaymentModalOpen(false)}>Close</button>
            </form>
          </div>
        </div>
      </Dialog>
    </ParentRoute>
  );
} 