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
  Shield,
  Database,
  Activity,
  MessageSquare,
  TrendingUp
} from 'lucide-react';
import { SuperAdminRoute } from '../../components/ProtectedRoute';
import { useAuth } from '../../contexts/AuthContext';
import Navigation from '../../components/Navigation';
import { useRouter } from 'next/navigation';
import { Dialog } from '@headlessui/react';
import { useStudents, useStaff, useStudentStats, useStaffStats, useCreateStudent, useUpdateStudent, useDeleteStudent, useCreateStaff, useUpdateStaff, useDeleteStaff, useFeePayments, useCreateFeePayment, useUpdateFeePayment, useDeleteFeePayment, useExams, useCreateExam, useUpdateExam, useDeleteExam, useAttendance, useCreateAttendance, useUpdateAttendance, useDeleteAttendance, useHomework, useCreateHomework, useUpdateHomework, useDeleteHomework, useTimetables, useCreateTimetable, useUpdateTimetable, useDeleteTimetable, useBooks, useCreateBook, useUpdateBook, useDeleteBook, useVehicles, useCreateVehicle, useUpdateVehicle, useDeleteVehicle, useMessages, useCreateMessage, useUpdateMessage, useDeleteMessage } from '../../hooks/useApi';

export default function SuperAdminPortal() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const router = useRouter();

  // Modal states
  const [isSchoolModalOpen, setSchoolModalOpen] = useState(false);
  const [isUserModalOpen, setUserModalOpen] = useState(false);
  const [isMessageModalOpen, setMessageModalOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState<any>(null);
  const [formState, setFormState] = useState<any>({});
  const [formError, setFormError] = useState<string | null>(null);

  // API hooks
  const { data: studentsData, isLoading: studentsLoading, error: studentsError } = useStudents();
  const { data: staffData, isLoading: staffLoading, error: staffError } = useStaff();
  const { data: messageData, isLoading: messageLoading, error: messageError } = useMessages();
  const { data: feeData, isLoading: feeLoading, error: feeError } = useFeePayments();
  const { data: attendanceData, isLoading: attendanceLoading, error: attendanceError } = useAttendance();
  const { data: homeworkData, isLoading: homeworkLoading, error: homeworkError } = useHomework();
  const createStudent = useCreateStudent();
  const createStaff = useCreateStaff();
  const createMessage = useCreateMessage();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  const handleAddSchool = () => {
    setFormState({});
    setFormError(null);
    setSelectedItem(null);
    setSchoolModalOpen(true);
  };

  const handleManageUsers = () => {
    setActiveTab('users');
  };

  const handleSystemMonitor = () => {
    setActiveTab('system');
  };

  const handleAddUser = () => {
    setFormState({});
    setFormError(null);
    setSelectedItem(null);
    setUserModalOpen(true);
  };

  const handleSendMessage = () => {
    setFormState({});
    setFormError(null);
    setSelectedItem(null);
    setMessageModalOpen(true);
  };

  const handleFormChange = (e: any) => {
    setFormState({ ...formState, [e.target.name]: e.target.value });
  };

  const handleSchoolSubmit = async (e: any) => {
    e.preventDefault();
    setFormError(null);
    try {
      await createStudent.mutateAsync(formState);
      setSchoolModalOpen(false);
    } catch (err: any) {
      setFormError(err.message || 'Failed to add school');
    }
  };

  const handleUserSubmit = async (e: any) => {
    e.preventDefault();
    setFormError(null);
    try {
      await createStaff.mutateAsync(formState);
      setUserModalOpen(false);
    } catch (err: any) {
      setFormError(err.message || 'Failed to add user');
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
          <p className="text-gray-600">Please log in to access the super admin portal.</p>
        </div>
      </div>
    );
  }

  const stats = [
    { 
      title: 'Total Schools', 
      value: studentsData?.total || '0', 
      change: '+3', 
      icon: Shield,
      loading: studentsLoading 
    },
    { 
      title: 'Total Users', 
      value: staffData?.total || '0', 
      change: '+156', 
      icon: Users,
      loading: staffLoading 
    },
    { 
      title: 'System Health', 
      value: '98%', 
      change: '+2%', 
      icon: Activity,
      loading: false 
    },
    { 
      title: 'Revenue', 
      value: feeData?.total ? `$${feeData.total}` : '$0', 
      change: '+12%', 
      icon: DollarSign,
      loading: feeLoading 
    },
  ];

  const serviceTabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'schools', label: 'Schools', icon: Shield },
    { id: 'users', label: 'Users', icon: Users },
    { id: 'system', label: 'System', icon: Database },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp },
    { id: 'communication', label: 'Communication', icon: MessageSquare },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <SuperAdminRoute>
      <div className="flex h-screen bg-gray-50">
        {/* Sidebar */}
        <aside className="w-64 bg-white shadow-lg">
          <div className="p-6">
            <h1 className="text-2xl font-bold text-gray-900">AI SchoolOS</h1>
            <p className="text-sm text-gray-600">Super Admin Portal</p>
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
                    Super Admin Dashboard
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
                    <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-medium">S</span>
                    </div>
                    <span className="text-sm font-medium text-gray-700">Super Admin</span>
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
                        ? 'bg-red-100 text-red-700'
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
                            <stat.icon className="h-8 w-8 text-red-600" />
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
                          onClick={handleAddSchool}
                          className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 transition-colors"
                        >
                          <Shield className="h-4 w-4 mr-2" />
                          Add New School
                        </button>
                        <button 
                          onClick={handleManageUsers}
                          className="flex items-center justify-center px-4 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
                        >
                          <Users className="h-4 w-4 mr-2" />
                          Manage Users
                        </button>
                        <button 
                          onClick={handleSystemMonitor}
                          className="flex items-center justify-center px-4 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
                        >
                          <Database className="h-4 w-4 mr-2" />
                          System Monitor
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
                                  <Shield className="h-4 w-4 text-green-600" />
                                </div>
                              </div>
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900">
                                  New school registered
                                </p>
                                <p className="text-sm text-gray-500">
                                  {studentsData?.students?.length || 0} schools • 2 hours ago
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center space-x-4">
                              <div className="flex-shrink-0">
                                <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                                  <Activity className="h-4 w-4 text-blue-600" />
                                </div>
                              </div>
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900">
                                  System backup completed
                                </p>
                                <p className="text-sm text-gray-500">
                                  Database backup • 4 hours ago
                                </p>
                              </div>
                            </div>
                            <div className="flex items-center space-x-4">
                              <div className="flex-shrink-0">
                                <div className="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                                  <Users className="h-4 w-4 text-yellow-600" />
                                </div>
                              </div>
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900">
                                  User account created
                                </p>
                                <p className="text-sm text-gray-500">
                                  {staffData?.staff?.length || 0} users • 6 hours ago
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

              {/* Schools Tab */}
              {activeTab === 'schools' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Schools</h3>
                        <button 
                          onClick={handleAddSchool}
                          className="bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700"
                        >
                          Add School
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {studentsLoading ? (
                        <div className="text-center text-gray-500">Loading schools...</div>
                      ) : studentsError ? (
                        <div className="text-center text-red-500">{studentsError.message || 'Failed to load schools'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">School Name</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Location</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Students</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(studentsData?.students || []).map((student: any) => (
                                <tr key={student.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{student.firstName} {student.lastName}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{student.className || 'N/A'}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">-</td>
                                  <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${student.isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500'}`}>
                                      {student.isActive ? 'Active' : 'Inactive'}
                                    </span>
                                  </td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <button className="text-blue-600 hover:text-blue-900 mr-3">Edit</button>
                                    <button className="text-red-600 hover:text-red-900">Delete</button>
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

              {/* Users Tab */}
              {activeTab === 'users' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Users</h3>
                        <button 
                          onClick={handleAddUser}
                          className="bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700"
                        >
                          Add User
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {staffLoading ? (
                        <div className="text-center text-gray-500">Loading users...</div>
                      ) : staffError ? (
                        <div className="text-center text-red-500">{staffError.message || 'Failed to load users'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Role</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(staffData?.staff || []).map((staff: any) => (
                                <tr key={staff.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{staff.firstName} {staff.lastName}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{staff.email}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{staff.role || 'Staff'}</td>
                                  <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${staff.isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500'}`}>
                                      {staff.isActive ? 'Active' : 'Inactive'}
                                    </span>
                                  </td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <button className="text-blue-600 hover:text-blue-900 mr-3">Edit</button>
                                    <button className="text-red-600 hover:text-red-900">Delete</button>
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

              {/* System Tab */}
              {activeTab === 'system' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <h3 className="text-lg font-medium text-gray-900">System Status</h3>
                    </div>
                    <div className="p-6">
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        <div className="bg-green-50 p-4 rounded-lg">
                          <h4 className="text-sm font-medium text-green-600">Database</h4>
                          <p className="text-2xl font-bold text-green-900">Online</p>
                        </div>
                        <div className="bg-blue-50 p-4 rounded-lg">
                          <h4 className="text-sm font-medium text-blue-600">API Services</h4>
                          <p className="text-2xl font-bold text-blue-900">Healthy</p>
                        </div>
                        <div className="bg-yellow-50 p-4 rounded-lg">
                          <h4 className="text-sm font-medium text-yellow-600">Storage</h4>
                          <p className="text-2xl font-bold text-yellow-900">75%</p>
                        </div>
                        <div className="bg-purple-50 p-4 rounded-lg">
                          <h4 className="text-sm font-medium text-purple-600">Uptime</h4>
                          <p className="text-2xl font-bold text-purple-900">99.9%</p>
                        </div>
                      </div>
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
                          className="bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-red-700"
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
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">To</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(messageData?.messages || []).map((message: any) => (
                                <tr key={message.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{message.subject}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{message.from}</td>
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
              {!['dashboard', 'schools', 'users', 'system', 'communication'].includes(activeTab) && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">{serviceTabs.find(tab => tab.id === activeTab)?.label}</h3>
                  <p className="text-gray-600">This feature is coming soon...</p>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>

      {/* School Modal */}
      <Dialog open={isSchoolModalOpen} onClose={() => setSchoolModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
        <div className="flex items-center justify-center min-h-screen px-4">
          <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
            <Dialog.Title className="text-lg font-bold mb-4">Add School</Dialog.Title>
            <form onSubmit={handleSchoolSubmit} className="space-y-4">
              <input type="text" name="firstName" value={formState.firstName || ''} onChange={handleFormChange} placeholder="School Name" className="w-full border rounded px-3 py-2" required />
              <input type="text" name="lastName" value={formState.lastName || ''} onChange={handleFormChange} placeholder="Location" className="w-full border rounded px-3 py-2" required />
              <input type="email" name="email" value={formState.email || ''} onChange={handleFormChange} placeholder="Email" className="w-full border rounded px-3 py-2" required />
              <input type="text" name="className" value={formState.className || ''} onChange={handleFormChange} placeholder="Address" className="w-full border rounded px-3 py-2" />
              <select name="isActive" value={formState.isActive || ''} onChange={handleFormChange} className="w-full border rounded px-3 py-2">
                <option value="">Select Status</option>
                <option value="true">Active</option>
                <option value="false">Inactive</option>
              </select>
              {formError && <div className="text-red-600 text-sm">{formError}</div>}
              <button type="submit" className="w-full bg-red-600 text-white py-2 rounded hover:bg-red-700">Add School</button>
              <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setSchoolModalOpen(false)}>Close</button>
            </form>
          </div>
        </div>
      </Dialog>

      {/* User Modal */}
      <Dialog open={isUserModalOpen} onClose={() => setUserModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
        <div className="flex items-center justify-center min-h-screen px-4">
          <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
            <Dialog.Title className="text-lg font-bold mb-4">Add User</Dialog.Title>
            <form onSubmit={handleUserSubmit} className="space-y-4">
              <input type="text" name="firstName" value={formState.firstName || ''} onChange={handleFormChange} placeholder="First Name" className="w-full border rounded px-3 py-2" required />
              <input type="text" name="lastName" value={formState.lastName || ''} onChange={handleFormChange} placeholder="Last Name" className="w-full border rounded px-3 py-2" required />
              <input type="email" name="email" value={formState.email || ''} onChange={handleFormChange} placeholder="Email" className="w-full border rounded px-3 py-2" required />
              <input type="text" name="role" value={formState.role || ''} onChange={handleFormChange} placeholder="Role" className="w-full border rounded px-3 py-2" />
              <select name="isActive" value={formState.isActive || ''} onChange={handleFormChange} className="w-full border rounded px-3 py-2">
                <option value="">Select Status</option>
                <option value="true">Active</option>
                <option value="false">Inactive</option>
              </select>
              {formError && <div className="text-red-600 text-sm">{formError}</div>}
              <button type="submit" className="w-full bg-red-600 text-white py-2 rounded hover:bg-red-700">Add User</button>
              <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setUserModalOpen(false)}>Close</button>
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
              <input type="text" name="from" value={formState.from || ''} onChange={handleFormChange} placeholder="From" className="w-full border rounded px-3 py-2" required />
              <input type="text" name="to" value={formState.to || ''} onChange={handleFormChange} placeholder="To" className="w-full border rounded px-3 py-2" required />
              <textarea name="message" value={formState.message || ''} onChange={handleFormChange} placeholder="Message" className="w-full border rounded px-3 py-2" rows={4} />
              <select name="type" value={formState.type || ''} onChange={handleFormChange} className="w-full border rounded px-3 py-2">
                <option value="">Select Type</option>
                <option value="email">Email</option>
                <option value="sms">SMS</option>
                <option value="notification">Notification</option>
              </select>
              {formError && <div className="text-red-600 text-sm">{formError}</div>}
              <button type="submit" className="w-full bg-red-600 text-white py-2 rounded hover:bg-red-700">Send Message</button>
              <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setMessageModalOpen(false)}>Close</button>
            </form>
          </div>
        </div>
      </Dialog>
    </SuperAdminRoute>
  );
} 