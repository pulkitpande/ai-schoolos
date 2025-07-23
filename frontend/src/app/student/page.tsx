'use client';

import { useState } from 'react';
import { 
  BookOpen, 
  Calendar, 
  FileText, 
  Clock, 
  BarChart3, 
  Settings, 
  Bell,
  GraduationCap,
  MessageSquare,
  TrendingUp
} from 'lucide-react';
import { StudentRoute } from '../../components/ProtectedRoute';
import { useAuth } from '../../contexts/AuthContext';
import Navigation from '../../components/Navigation';
import { useRouter } from 'next/navigation';
import { Dialog } from '@headlessui/react';
import { useStudents, useStaff, useStudentStats, useStaffStats, useCreateStudent, useUpdateStudent, useDeleteStudent, useCreateStaff, useUpdateStaff, useDeleteStaff, useFeePayments, useCreateFeePayment, useUpdateFeePayment, useDeleteFeePayment, useExams, useCreateExam, useUpdateExam, useDeleteExam, useAttendance, useCreateAttendance, useUpdateAttendance, useDeleteAttendance, useHomework, useCreateHomework, useUpdateHomework, useDeleteHomework, useTimetables, useCreateTimetable, useUpdateTimetable, useDeleteTimetable, useBooks, useCreateBook, useUpdateBook, useDeleteBook, useVehicles, useCreateVehicle, useUpdateVehicle, useDeleteVehicle, useMessages, useCreateMessage, useUpdateMessage, useDeleteMessage } from '../../hooks/useApi';

export default function StudentPortal() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const router = useRouter();

  // Modal states
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
  const { data: timetableData, isLoading: timetableLoading, error: timetableError } = useTimetables();
  const { data: libraryData, isLoading: libraryLoading, error: libraryError } = useBooks();
  const createHomework = useCreateHomework();
  const createMessage = useCreateMessage();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  // Action handlers
  const handleSubmitAssignment = () => {
    setFormState({});
    setFormError(null);
    setSelectedItem(null);
    setAssignmentModalOpen(true);
  };

  const handleViewSchedule = () => {
    setActiveTab('timetable');
  };

  const handleContactTeacher = () => {
    setFormState({});
    setFormError(null);
    setSelectedItem(null);
    setMessageModalOpen(true);
  };

  const handleViewCourseDetails = (courseName: string) => {
    console.log(`Viewing details for ${courseName} course`);
  };

  const handleViewAssignmentDetails = (assignmentTitle: string) => {
    console.log(`Viewing details for assignment: ${assignmentTitle}`);
  };

  const handleEditAssignment = (assignmentTitle: string) => {
    console.log(`Editing assignment: ${assignmentTitle}`);
  };

  const handleDeleteAssignment = (assignmentTitle: string) => {
    if (confirm(`Are you sure you want to delete "${assignmentTitle}"?`)) {
      console.log(`Assignment "${assignmentTitle}" deleted successfully`);
    }
  };

  const handleViewGradeDetails = (subject: string) => {
    console.log(`Viewing detailed grades for ${subject}`);
  };

  const handleDownloadReport = () => {
    console.log('Downloading academic report...');
  };

  const handleViewAttendanceDetails = (date: string) => {
    console.log(`Viewing attendance details for ${date}`);
  };

  const handleContactParent = () => {
    console.log('Contacting parent...');
  };

  const handleViewLibrary = () => {
    setActiveTab('library');
  };

  const handleViewProgress = () => {
    setActiveTab('analytics');
  };

  const handleSettings = () => {
    setActiveTab('settings');
  };

  const handleFormChange = (e: any) => {
    setFormState({ ...formState, [e.target.name]: e.target.value });
  };

  const handleAssignmentSubmit = async (e: any) => {
    e.preventDefault();
    setFormError(null);
    try {
      await createHomework.mutateAsync(formState);
      setAssignmentModalOpen(false);
    } catch (err: any) {
      setFormError(err.message || 'Failed to submit assignment');
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
          <p className="text-gray-600">Please log in to access the student portal.</p>
        </div>
      </div>
    );
  }

  const stats = [
    { 
      title: 'My Courses', 
      value: studentsData?.students?.length || '0', 
      change: '+1', 
      icon: BookOpen,
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
      title: 'Attendance', 
      value: attendanceData?.attendance?.length ? '92%' : '0%', 
      change: '+3%', 
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
    { id: 'courses', label: 'My Courses', icon: BookOpen },
    { id: 'assignments', label: 'Assignments', icon: FileText },
    { id: 'grades', label: 'Grades', icon: BarChart3 },
    { id: 'attendance', label: 'Attendance', icon: Clock },
    { id: 'timetable', label: 'Timetable', icon: Calendar },
    { id: 'library', label: 'Library', icon: BookOpen },
    { id: 'communication', label: 'Messages', icon: MessageSquare },
    { id: 'analytics', label: 'Progress', icon: TrendingUp },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <StudentRoute>
      <div className="flex h-screen bg-gray-50">
        {/* Sidebar */}
        <aside className="w-64 bg-white shadow-lg">
          <div className="p-6">
            <h1 className="text-2xl font-bold text-gray-900">AI SchoolOS</h1>
            <p className="text-sm text-gray-600">Student Portal</p>
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
                    Student Dashboard
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
                    <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-medium">S</span>
                    </div>
                    <span className="text-sm font-medium text-gray-700">Student</span>
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
                        ? 'bg-purple-100 text-purple-700'
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
                            <stat.icon className="h-8 w-8 text-purple-600" />
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
                          onClick={handleSubmitAssignment}
                          className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-purple-600 hover:bg-purple-700 transition-colors"
                        >
                          <FileText className="h-4 w-4 mr-2" />
                          Submit Assignment
                        </button>
                        <button 
                          onClick={handleViewSchedule}
                          className="flex items-center justify-center px-4 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
                        >
                          <Calendar className="h-4 w-4 mr-2" />
                          View Schedule
                        </button>
                        <button 
                          onClick={handleContactTeacher}
                          className="flex items-center justify-center px-4 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
                        >
                          <MessageSquare className="h-4 w-4 mr-2" />
                          Contact Teacher
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
                        {homeworkLoading ? (
                          <div className="text-center text-gray-500">Loading activities...</div>
                        ) : (
                          <>
                            <div className="flex items-center space-x-4">
                              <div className="flex-shrink-0">
                                <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                                  <FileText className="h-4 w-4 text-green-600" />
                                </div>
                              </div>
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900">
                                  Assignment submitted
                                </p>
                                <p className="text-sm text-gray-500">
                                  {homeworkData?.homework?.length || 0} assignments • 2 hours ago
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center space-x-4">
                              <div className="flex-shrink-0">
                                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                                  <BarChart3 className="h-4 w-4 text-blue-600" />
                                </div>
                              </div>
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900">
                                  Grade received
                                </p>
                                <p className="text-sm text-gray-500">
                                  Science Test • 1 day ago
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

              {/* Courses Tab */}
              {activeTab === 'courses' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-medium text-gray-900">My Courses</h3>
                    </div>
                    <div className="p-6">
                      {studentsLoading ? (
                        <div className="text-center text-gray-500">Loading courses...</div>
                      ) : studentsError ? (
                        <div className="text-center text-red-500">{(studentsError as any)?.message || 'Failed to load courses'}</div>
                      ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                          {(studentsData?.students || []).map((student: any, index: number) => (
                            <div key={index} className="border border-gray-200 rounded-lg p-4">
                              <div className="flex justify-between items-start mb-2">
                                <h4 className="font-semibold text-gray-900">{student.className || 'Course'}</h4>
                                <button 
                                  onClick={() => handleViewCourseDetails(student.className || 'Course')}
                                  className="text-blue-600 hover:text-blue-900 text-sm font-medium"
                                >
                                  View Details
                                </button>
                              </div>
                              <p className="text-sm text-gray-600 mb-2">Student: {student.firstName} {student.lastName}</p>
                              <div className="flex justify-between items-center mb-2">
                                <span className="text-sm text-gray-600">Status: {student.isActive ? 'Active' : 'Inactive'}</span>
                                <span className="text-sm text-gray-600">100%</span>
                              </div>
                              <div className="w-full bg-gray-200 rounded-full h-2">
                                <div 
                                  className="bg-purple-600 h-2 rounded-full" 
                                  style={{ width: '100%' }}
                                ></div>
                              </div>
                            </div>
                          ))}
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
                        <div className="text-center text-red-500">{(homeworkError as any)?.message || 'Failed to load assignments'}</div>
                      ) : (
                        <div className="space-y-4">
                          {(homeworkData?.homework || []).map((assignment: any) => (
                            <div key={assignment.id} className="border border-gray-200 rounded-lg p-4">
                              <div className="flex justify-between items-start mb-2">
                                <h4 className="font-semibold text-gray-900">{assignment.title}</h4>
                                <div className="flex space-x-2">
                                  <button 
                                    onClick={() => handleViewAssignmentDetails(assignment.title)}
                                    className="text-blue-600 hover:text-blue-900 text-sm font-medium"
                                  >
                                    View
                                  </button>
                                  <button 
                                    onClick={() => handleEditAssignment(assignment.title)}
                                    className="text-green-600 hover:text-green-900 text-sm font-medium"
                                  >
                                    Edit
                                  </button>
                                  <button 
                                    onClick={() => handleDeleteAssignment(assignment.title)}
                                    className="text-red-600 hover:text-red-900 text-sm font-medium"
                                  >
                                    Delete
                                  </button>
                                </div>
                              </div>
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
                        <div className="text-center text-red-500">{(attendanceError as any)?.message || 'Failed to load attendance'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(attendanceData?.attendance || []).map((record: any) => (
                                <tr key={record.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{record.date}</td>
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
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <button 
                                      onClick={() => handleViewAttendanceDetails(record.date)}
                                      className="text-blue-600 hover:text-blue-900"
                                    >
                                      View Details
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

              {/* Timetable Tab */}
              {activeTab === 'timetable' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-medium text-gray-900">My Timetable</h3>
                    </div>
                    <div className="p-6">
                      {timetableLoading ? (
                        <div className="text-center text-gray-500">Loading timetable...</div>
                      ) : timetableError ? (
                        <div className="text-center text-red-500">{(timetableError as any)?.message || 'Failed to load timetable'}</div>
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

              {/* Library Tab */}
              {activeTab === 'library' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-medium text-gray-900">Library</h3>
                    </div>
                    <div className="p-6">
                      {libraryLoading ? (
                        <div className="text-center text-gray-500">Loading library...</div>
                      ) : libraryError ? (
                        <div className="text-center text-red-500">{(libraryError as any)?.message || 'Failed to load library'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Author</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(libraryData?.books || []).map((book: any) => (
                                <tr key={book.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{book.title}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{book.author}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{book.category}</td>
                                  <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                      book.status === 'available' ? 'bg-green-100 text-green-800' : 
                                      book.status === 'borrowed' ? 'bg-yellow-100 text-yellow-800' : 
                                      book.status === 'reserved' ? 'bg-blue-100 text-blue-800' : 
                                      'bg-gray-100 text-gray-500'
                                    }`}>
                                      {book.status}
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

              {/* Communication Tab */}
              {activeTab === 'communication' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Messages</h3>
                        <button 
                          onClick={handleContactTeacher}
                          className="bg-purple-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-purple-700"
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

              {/* Other tabs show placeholder */}
              {!['dashboard', 'courses', 'assignments', 'attendance', 'timetable', 'library', 'communication'].includes(activeTab) && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">{serviceTabs.find(tab => tab.id === activeTab)?.label}</h3>
                  <p className="text-gray-600">This feature is coming soon...</p>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>

      {/* Assignment Modal */}
      <Dialog open={isAssignmentModalOpen} onClose={() => setAssignmentModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
        <div className="flex items-center justify-center min-h-screen px-4">
          <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
            <Dialog.Title className="text-lg font-bold mb-4">Submit Assignment</Dialog.Title>
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
              <button type="submit" className="w-full bg-purple-600 text-white py-2 rounded hover:bg-purple-700">Submit Assignment</button>
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
              <button type="submit" className="w-full bg-purple-600 text-white py-2 rounded hover:bg-purple-700">Send Message</button>
              <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setMessageModalOpen(false)}>Close</button>
            </form>
          </div>
        </div>
      </Dialog>
    </StudentRoute>
  );
} 