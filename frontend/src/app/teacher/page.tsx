'use client';

import { useState } from 'react';
import { 
  Users, 
  GraduationCap, 
  Calendar, 
  BookOpen, 
  DollarSign, 
  BarChart3, 
  Settings, 
  Bell,
  FileText,
  Clock,
  MessageSquare,
  TrendingUp
} from 'lucide-react';
import { TeacherRoute } from '../../components/ProtectedRoute';
import { useAuth } from '../../contexts/AuthContext';
import Navigation from '../../components/Navigation';
import { useRouter } from 'next/navigation';
import { Dialog } from '@headlessui/react';
import { useStudents, useStaff, useStudentStats, useStaffStats, useCreateStudent, useUpdateStudent, useDeleteStudent, useCreateStaff, useUpdateStaff, useDeleteStaff, useFeePayments, useCreateFeePayment, useUpdateFeePayment, useDeleteFeePayment, useExams, useCreateExam, useUpdateExam, useDeleteExam, useAttendance, useCreateAttendance, useUpdateAttendance, useDeleteAttendance, useHomework, useCreateHomework, useUpdateHomework, useDeleteHomework, useTimetables, useCreateTimetable, useUpdateTimetable, useDeleteTimetable, useBooks, useCreateBook, useUpdateBook, useDeleteBook, useVehicles, useCreateVehicle, useUpdateVehicle, useDeleteVehicle, useMessages, useCreateMessage, useUpdateMessage, useDeleteMessage } from '../../hooks/useApi';

export default function TeacherPortal() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const router = useRouter();

  // Modal states
  const [isAttendanceModalOpen, setAttendanceModalOpen] = useState(false);
  const [isAssignmentModalOpen, setAssignmentModalOpen] = useState(false);
  const [isMessageModalOpen, setMessageModalOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState<any>(null);
  const [formState, setFormState] = useState<any>({});
  const [formError, setFormError] = useState<string | null>(null);

  // API hooks
  const { data: studentsData, isLoading: studentsLoading, error: studentsError } = useStudents();
  const { data: attendanceData, isLoading: attendanceLoading, error: attendanceError } = useAttendance();
  const { data: homeworkData, isLoading: homeworkLoading, error: homeworkError } = useHomework();
  const { data: messageData, isLoading: messageLoading, error: messageError } = useMessages();
  const createAttendance = useCreateAttendance();
  const createHomework = useCreateHomework();
  const createMessage = useCreateMessage();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  // Action handlers
  const handleMarkAttendance = () => {
    setFormState({});
    setFormError(null);
    setSelectedItem(null);
    setAttendanceModalOpen(true);
  };

  const handleCreateAssignment = () => {
    setFormState({});
    setFormError(null);
    setSelectedItem(null);
    setAssignmentModalOpen(true);
  };

  const handleSendMessage = () => {
    setFormState({});
    setFormError(null);
    setSelectedItem(null);
    setMessageModalOpen(true);
  };

  const handleViewClassDetails = (className: string) => {
    // Navigate to class details or open modal
    console.log(`Viewing details for ${className}`);
  };

  const handleMarkClassAttendance = (className: string) => {
    setFormState({ className });
    setFormError(null);
    setSelectedItem(null);
    setAttendanceModalOpen(true);
  };

  const handleViewStudentDetails = (studentName: string) => {
    // Navigate to student details or open modal
    console.log(`Viewing details for student: ${studentName}`);
  };

  const handleMessageStudent = (studentName: string) => {
    setFormState({ to: studentName });
    setFormError(null);
    setSelectedItem(null);
    setMessageModalOpen(true);
  };

  const handleViewAssignmentSubmissions = (assignmentTitle: string) => {
    // Navigate to assignment submissions
    console.log(`Viewing submissions for assignment: ${assignmentTitle}`);
  };

  const handleGradeAssignment = (assignmentTitle: string) => {
    // Navigate to grading interface
    console.log(`Grading assignment: ${assignmentTitle}`);
  };

  const handleViewAttendanceRecord = (className: string) => {
    // Navigate to attendance records
    console.log(`Viewing attendance record for ${className}`);
  };

  const handleUpdateGrades = (className: string) => {
    // Navigate to grade update interface
    console.log(`Updating grades for ${className}`);
  };

  const handleSendClassMessage = (className: string) => {
    setFormState({ to: `${className} students` });
    setFormError(null);
    setSelectedItem(null);
    setMessageModalOpen(true);
  };

  const handleFormChange = (e: any) => {
    setFormState({ ...formState, [e.target.name]: e.target.value });
  };

  const handleAttendanceSubmit = async (e: any) => {
    e.preventDefault();
    setFormError(null);
    try {
      await createAttendance.mutateAsync(formState);
      setAttendanceModalOpen(false);
    } catch (err: any) {
      setFormError(err.message || 'Failed to mark attendance');
    }
  };

  const handleAssignmentSubmit = async (e: any) => {
    e.preventDefault();
    setFormError(null);
    try {
      await createHomework.mutateAsync(formState);
      setAssignmentModalOpen(false);
    } catch (err: any) {
      setFormError(err.message || 'Failed to create assignment');
    }
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
          <p className="text-gray-600">Please log in to access the teacher portal.</p>
        </div>
      </div>
    );
  }

  const stats = [
    { 
      title: 'My Classes', 
      value: studentsData?.total || '0', 
      change: '+1', 
      icon: GraduationCap,
      loading: studentsLoading 
    },
    { 
      title: 'Total Students', 
      value: studentsData?.students?.length || '0', 
      change: '+8', 
      icon: Users,
      loading: studentsLoading 
    },
    { 
      title: 'Assignments', 
      value: homeworkData?.homework?.length || '0', 
      change: '+2', 
      icon: FileText,
      loading: homeworkLoading 
    },
    { 
      title: 'Attendance Rate', 
      value: attendanceData?.attendance?.length ? '94%' : '0%', 
      change: '+2%', 
      icon: Clock,
      loading: attendanceLoading 
    },
  ];

  const serviceTabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'classes', label: 'My Classes', icon: GraduationCap },
    { id: 'students', label: 'Students', icon: Users },
    { id: 'assignments', label: 'Assignments', icon: FileText },
    { id: 'attendance', label: 'Attendance', icon: Clock },
    { id: 'grades', label: 'Grades', icon: BookOpen },
    { id: 'communication', label: 'Communication', icon: MessageSquare },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <TeacherRoute>
      <div className="flex h-screen bg-gray-50">
        {/* Sidebar */}
        <aside className="w-64 bg-white shadow-lg">
          <div className="p-6">
            <h1 className="text-2xl font-bold text-gray-900">AI SchoolOS</h1>
            <p className="text-sm text-gray-600">Teacher Portal</p>
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
                    Teacher Dashboard
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
                    <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-medium">T</span>
                    </div>
                    <span className="text-sm font-medium text-gray-700">Teacher</span>
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
                        ? 'bg-green-100 text-green-700'
                        : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
                    }`}
                  >
                    <tab.icon className="h-4 w-4" />
                    <span>{tab.label}</span>
                  </button>
                ))}
              </nav>

              {/* Tab Content */}
              {activeTab === 'dashboard' && (
                <div className="space-y-6">
                  {/* Stats Grid */}
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    {stats.map((stat, index) => (
                      <div key={index} className="bg-white rounded-lg shadow p-6">
                        <div className="flex items-center">
                          <div className="flex-shrink-0">
                            <stat.icon className="h-8 w-8 text-green-600" />
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
                                <div className="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                                  {stat.change}
                                </div>
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
                          onClick={handleMarkAttendance}
                          className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 transition-colors"
                        >
                          <Clock className="h-4 w-4 mr-2" />
                          Mark Attendance
                        </button>
                        <button 
                          onClick={handleCreateAssignment}
                          className="flex items-center justify-center px-4 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
                        >
                          <FileText className="h-4 w-4 mr-2" />
                          Create Assignment
                        </button>
                        <button 
                          onClick={handleSendMessage}
                          className="flex items-center justify-center px-4 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
                        >
                          <MessageSquare className="h-4 w-4 mr-2" />
                          Send Message
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
                        {attendanceLoading ? (
                          <div className="text-center text-gray-500">Loading activities...</div>
                        ) : (
                          <>
                            <div className="flex items-center space-x-4">
                              <div className="flex-shrink-0">
                                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                                  <Clock className="h-4 w-4 text-green-600" />
                                </div>
                              </div>
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900">
                                  Attendance marked for Class 10A
                                </p>
                                <p className="text-sm text-gray-500">
                                  {attendanceData?.attendance?.length || 0} students present • 2 hours ago
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center space-x-4">
                              <div className="flex-shrink-0">
                                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                                  <FileText className="h-4 w-4 text-blue-600" />
                                </div>
                              </div>
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900">
                                  Assignment created
                                </p>
                                <p className="text-sm text-gray-500">
                                  {homeworkData?.homework?.length || 0} assignments • 1 day ago
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
                                  Message sent to parents
                                </p>
                                <p className="text-sm text-gray-500">
                                  {messageData?.messages?.length || 0} messages • 2 days ago
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

              {/* Classes Tab */}
              {activeTab === 'classes' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-medium text-gray-900">My Classes</h3>
                    </div>
                    <div className="p-6">
                      {studentsLoading ? (
                        <div className="text-center text-gray-500">Loading classes...</div>
                      ) : studentsError ? (
                        <div className="text-center text-red-500">{(studentsError as any)?.message || 'Failed to load classes'}</div>
                      ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                          {(studentsData?.students || []).map((student: any, index: number) => (
                            <div key={index} className="border border-gray-200 rounded-lg p-4">
                              <h4 className="font-semibold text-gray-900 mb-2">{student.className || 'Class'}</h4>
                              <p className="text-sm text-gray-600 mb-2">{student.firstName} {student.lastName}</p>
                              <p className="text-sm text-gray-600 mb-2">Student</p>
                              <p className="text-sm text-gray-500">Active</p>
                              <div className="mt-3 flex space-x-2">
                                <button 
                                  onClick={() => handleViewClassDetails(student.className || 'Class')}
                                  className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded hover:bg-green-200"
                                >
                                  View Details
                                </button>
                                <button 
                                  onClick={() => handleMarkClassAttendance(student.className || 'Class')}
                                  className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded hover:bg-blue-200"
                                >
                                  Attendance
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

              {/* Students Tab */}
              {activeTab === 'students' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-medium text-gray-900">My Students</h3>
                    </div>
                    <div className="p-6">
                      {studentsLoading ? (
                        <div className="text-center text-gray-500">Loading students...</div>
                      ) : studentsError ? (
                        <div className="text-center text-red-500">{(studentsError as any)?.message || 'Failed to load students'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Class</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(studentsData?.students || []).map((student: any) => (
                                <tr key={student.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                    {student.firstName} {student.lastName}
                                  </td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{student.className || '-'}</td>
                                  <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${student.isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500'}`}>
                                      {student.isActive ? 'Active' : 'Inactive'}
                                    </span>
                                  </td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <button 
                                      onClick={() => handleViewStudentDetails(`${student.firstName} ${student.lastName}`)}
                                      className="text-blue-600 hover:text-blue-900 mr-3"
                                    >
                                      View
                                    </button>
                                    <button 
                                      onClick={() => handleMessageStudent(`${student.firstName} ${student.lastName}`)}
                                      className="text-green-600 hover:text-green-900"
                                    >
                                      Message
                                    </button>
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
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Assignments</h3>
                        <button 
                          onClick={handleCreateAssignment}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Create Assignment
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {homeworkLoading ? (
                        <div className="text-center text-gray-500">Loading assignments...</div>
                      ) : homeworkError ? (
                        <div className="text-center text-red-500">{(homeworkError as any)?.message || 'Failed to load assignments'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Subject</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(homeworkData?.homework || []).map((assignment: any) => (
                                <tr key={assignment.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{assignment.title}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{assignment.subject}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{assignment.dueDate}</td>
                                  <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                      assignment.status === 'active' ? 'bg-green-100 text-green-800' : 
                                      assignment.status === 'completed' ? 'bg-blue-100 text-blue-800' : 
                                      assignment.status === 'overdue' ? 'bg-red-100 text-red-800' : 
                                      'bg-gray-100 text-gray-500'
                                    }`}>
                                      {assignment.status}
                                    </span>
                                  </td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <button 
                                      onClick={() => handleViewAssignmentSubmissions(assignment.title)}
                                      className="text-blue-600 hover:text-blue-900 mr-3"
                                    >
                                      Submissions
                                    </button>
                                    <button 
                                      onClick={() => handleGradeAssignment(assignment.title)}
                                      className="text-green-600 hover:text-green-900"
                                    >
                                      Grade
                                    </button>
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

              {/* Attendance Tab */}
              {activeTab === 'attendance' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Attendance</h3>
                        <button 
                          onClick={handleMarkAttendance}
                          className="bg-green-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-green-700"
                        >
                          Mark Attendance
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {attendanceLoading ? (
                        <div className="text-center text-gray-500">Loading attendance...</div>
                      ) : attendanceError ? (
                        <div className="text-center text-red-500">{(attendanceError as any)?.message || 'Failed to load attendance'}</div>
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

              {/* Communication Tab */}
              {activeTab === 'communication' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Communication</h3>
                        <button 
                          onClick={handleSendMessage}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Send Message
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {messageLoading ? (
                        <div className="text-center text-gray-500">Loading messages...</div>
                      ) : messageError ? (
                        <div className="text-center text-red-500">{(messageError as any)?.message || 'Failed to load messages'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Subject</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">To</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(messageData?.messages || []).map((message: any) => (
                                <tr key={message.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{message.subject}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{message.to}</td>
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

              {/* Other tabs show placeholder */}
              {!['dashboard', 'classes', 'students', 'assignments', 'attendance', 'communication'].includes(activeTab) && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">{serviceTabs.find(tab => tab.id === activeTab)?.label}</h3>
                  <p className="text-gray-600">This feature is coming soon...</p>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>

      {/* Attendance Modal */}
      <Dialog open={isAttendanceModalOpen} onClose={() => setAttendanceModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
        <div className="flex items-center justify-center min-h-screen px-4">
          <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
            <Dialog.Title className="text-lg font-bold mb-4">Mark Attendance</Dialog.Title>
            <form onSubmit={handleAttendanceSubmit} className="space-y-4">
              <input type="text" name="studentId" value={formState.studentId || ''} onChange={handleFormChange} placeholder="Student ID" className="w-full border rounded px-3 py-2" required />
              <input type="date" name="date" value={formState.date || ''} onChange={handleFormChange} placeholder="Date" className="w-full border rounded px-3 py-2" required />
              <input type="time" name="time" value={formState.time || ''} onChange={handleFormChange} placeholder="Time" className="w-full border rounded px-3 py-2" />
              <select name="status" value={formState.status || ''} onChange={handleFormChange} className="w-full border rounded px-3 py-2">
                <option value="">Select Status</option>
                <option value="present">Present</option>
                <option value="absent">Absent</option>
                <option value="late">Late</option>
              </select>
              {formError && <div className="text-red-600 text-sm">{formError}</div>}
              <button type="submit" className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700">Mark Attendance</button>
              <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setAttendanceModalOpen(false)}>Close</button>
            </form>
          </div>
        </div>
      </Dialog>

      {/* Assignment Modal */}
      <Dialog open={isAssignmentModalOpen} onClose={() => setAssignmentModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
        <div className="flex items-center justify-center min-h-screen px-4">
          <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
            <Dialog.Title className="text-lg font-bold mb-4">Create Assignment</Dialog.Title>
            <form onSubmit={handleAssignmentSubmit} className="space-y-4">
              <input type="text" name="title" value={formState.title || ''} onChange={handleFormChange} placeholder="Assignment Title" className="w-full border rounded px-3 py-2" required />
              <input type="text" name="subject" value={formState.subject || ''} onChange={handleFormChange} placeholder="Subject" className="w-full border rounded px-3 py-2" required />
              <textarea name="description" value={formState.description || ''} onChange={handleFormChange} placeholder="Description" className="w-full border rounded px-3 py-2" rows={3} />
              <input type="date" name="dueDate" value={formState.dueDate || ''} onChange={handleFormChange} placeholder="Due Date" className="w-full border rounded px-3 py-2" />
              <select name="status" value={formState.status || ''} onChange={handleFormChange} className="w-full border rounded px-3 py-2">
                <option value="">Select Status</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
                <option value="overdue">Overdue</option>
              </select>
              {formError && <div className="text-red-600 text-sm">{formError}</div>}
              <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">Create Assignment</button>
              <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setAssignmentModalOpen(false)}>Close</button>
            </form>
          </div>
        </div>
      </Dialog>

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
              <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">Send Message</button>
              <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setMessageModalOpen(false)}>Close</button>
            </form>
          </div>
        </div>
      </Dialog>
    </TeacherRoute>
  );
} 