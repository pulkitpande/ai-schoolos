'use client';

import { useState, useEffect } from 'react';
import { 
  Users, 
  GraduationCap, 
  Calendar, 
  BookOpen, 
  DollarSign, 
  BarChart3, 
  Settings, 
  Bell,
  Search,
  Plus,
  Filter,
  FileText,
  Clock,
  MapPin,
  Truck,
  MessageSquare,
  TrendingUp
} from 'lucide-react';
import { AdminRoute } from '../../components/ProtectedRoute';
import { useStudents, useStaff, useStudentStats, useStaffStats, useCreateStudent, useUpdateStudent, useDeleteStudent, useCreateStaff, useUpdateStaff, useDeleteStaff, useFeePayments, useCreateFeePayment, useUpdateFeePayment, useDeleteFeePayment, useExams, useCreateExam, useUpdateExam, useDeleteExam, useAttendance, useCreateAttendance, useUpdateAttendance, useDeleteAttendance, useHomework, useCreateHomework, useUpdateHomework, useDeleteHomework, useTimetables, useCreateTimetable, useUpdateTimetable, useDeleteTimetable, useBooks, useCreateBook, useUpdateBook, useDeleteBook, useVehicles, useCreateVehicle, useUpdateVehicle, useDeleteVehicle, useMessages, useCreateMessage, useUpdateMessage, useDeleteMessage } from '../../hooks/useApi';
import { useAuth } from '../../contexts/AuthContext';
import Navigation from '../../components/Navigation';
import { useRouter } from 'next/navigation';
import {
  FeeManagement,
  ExamManagement,
  AttendanceManagement,
  HomeworkManagement,
  TimetableManagement,
  LibraryManagement,
  TransportManagement,
  CommunicationManagement,
  AnalyticsManagement,
  NotificationManagement
} from '../../components/services';
import { Dialog } from '@headlessui/react';

export default function AdminPortal() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const router = useRouter();

  // Modal state
  const [isStudentModalOpen, setStudentModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState<'add' | 'edit' | 'view'>('add');
  const [selectedStudent, setSelectedStudent] = useState<any>(null);
  const [formState, setFormState] = useState<any>({});
  const [formError, setFormError] = useState<string | null>(null);

  // Staff modal state
  const [isStaffModalOpen, setStaffModalOpen] = useState(false);
  const [staffModalMode, setStaffModalMode] = useState<'add' | 'edit' | 'view'>('add');
  const [selectedStaff, setSelectedStaff] = useState<any>(null);
  const [staffFormState, setStaffFormState] = useState<any>({});
  const [staffFormError, setStaffFormError] = useState<string | null>(null);

  // Fees modal state
  const [isFeeModalOpen, setFeeModalOpen] = useState(false);
  const [feeModalMode, setFeeModalMode] = useState<'add' | 'edit' | 'view'>('add');
  const [selectedFee, setSelectedFee] = useState<any>(null);
  const [feeFormState, setFeeFormState] = useState<any>({});
  const [feeFormError, setFeeFormError] = useState<string | null>(null);

  // Exams modal state
  const [isExamModalOpen, setExamModalOpen] = useState(false);
  const [examModalMode, setExamModalMode] = useState<'add' | 'edit' | 'view'>('add');
  const [selectedExam, setSelectedExam] = useState<any>(null);
  const [examFormState, setExamFormState] = useState<any>({});
  const [examFormError, setExamFormError] = useState<string | null>(null);

  // Attendance modal state
  const [isAttendanceModalOpen, setAttendanceModalOpen] = useState(false);
  const [attendanceModalMode, setAttendanceModalMode] = useState<'add' | 'edit' | 'view'>('add');
  const [selectedAttendance, setSelectedAttendance] = useState<any>(null);
  const [attendanceFormState, setAttendanceFormState] = useState<any>({});
  const [attendanceFormError, setAttendanceFormError] = useState<string | null>(null);

  // Homework modal state
  const [isHomeworkModalOpen, setHomeworkModalOpen] = useState(false);
  const [homeworkModalMode, setHomeworkModalMode] = useState<'add' | 'edit' | 'view'>('add');
  const [selectedHomework, setSelectedHomework] = useState<any>(null);
  const [homeworkFormState, setHomeworkFormState] = useState<any>({});
  const [homeworkFormError, setHomeworkFormError] = useState<string | null>(null);

  // Timetable modal state
  const [isTimetableModalOpen, setTimetableModalOpen] = useState(false);
  const [timetableModalMode, setTimetableModalMode] = useState<'add' | 'edit' | 'view'>('add');
  const [selectedTimetable, setSelectedTimetable] = useState<any>(null);
  const [timetableFormState, setTimetableFormState] = useState<any>({});
  const [timetableFormError, setTimetableFormError] = useState<string | null>(null);

  // Library modal state
  const [isLibraryModalOpen, setLibraryModalOpen] = useState(false);
  const [libraryModalMode, setLibraryModalMode] = useState<'add' | 'edit' | 'view'>('add');
  const [selectedLibrary, setSelectedLibrary] = useState<any>(null);
  const [libraryFormState, setLibraryFormState] = useState<any>({});
  const [libraryFormError, setLibraryFormError] = useState<string | null>(null);

  // Transport modal state
  const [isTransportModalOpen, setTransportModalOpen] = useState(false);
  const [transportModalMode, setTransportModalMode] = useState<'add' | 'edit' | 'view'>('add');
  const [selectedTransport, setSelectedTransport] = useState<any>(null);
  const [transportFormState, setTransportFormState] = useState<any>({});
  const [transportFormError, setTransportFormError] = useState<string | null>(null);

  // Communication modal state
  const [isCommunicationModalOpen, setCommunicationModalOpen] = useState(false);
  const [communicationModalMode, setCommunicationModalMode] = useState<'add' | 'edit' | 'view'>('add');
  const [selectedCommunication, setSelectedCommunication] = useState<any>(null);
  const [communicationFormState, setCommunicationFormState] = useState<any>({});
  const [communicationFormError, setCommunicationFormError] = useState<string | null>(null);

  // API hooks
  const { data: studentsData, isLoading: studentsLoading, error: studentsError, refetch: refetchStudents } = useStudents();
  const createStudent = useCreateStudent();
  const updateStudent = useUpdateStudent();
  const deleteStudent = useDeleteStudent();
  const { data: staffData, isLoading: staffLoading, error: staffError, refetch: refetchStaff } = useStaff();
  const createStaff = useCreateStaff();
  const updateStaff = useUpdateStaff();
  const deleteStaff = useDeleteStaff();
  const { data: feeData, isLoading: feeLoading, error: feeError, refetch: refetchFees } = useFeePayments();
  const createFee = useCreateFeePayment();
  const updateFee = useUpdateFeePayment();
  const deleteFee = useDeleteFeePayment();
  const { data: examData, isLoading: examLoading, error: examError, refetch: refetchExams } = useExams();
  const createExam = useCreateExam();
  const updateExam = useUpdateExam();
  const deleteExam = useDeleteExam();
  const { data: attendanceData, isLoading: attendanceLoading, error: attendanceError, refetch: refetchAttendance } = useAttendance();
  const createAttendance = useCreateAttendance();
  const updateAttendance = useUpdateAttendance();
  const deleteAttendance = useDeleteAttendance();
  const { data: homeworkData, isLoading: homeworkLoading, error: homeworkError, refetch: refetchHomework } = useHomework();
  const createHomework = useCreateHomework();
  const updateHomework = useUpdateHomework();
  const deleteHomework = useDeleteHomework();
  const { data: timetableData, isLoading: timetableLoading, error: timetableError, refetch: refetchTimetables } = useTimetables();
  const createTimetable = useCreateTimetable();
  const updateTimetable = useUpdateTimetable();
  const deleteTimetable = useDeleteTimetable();
  const { data: libraryData, isLoading: libraryLoading, error: libraryError, refetch: refetchLibrary } = useBooks();
  const createLibrary = useCreateBook();
  const updateLibrary = useUpdateBook();
  const deleteLibrary = useDeleteBook();
  const { data: transportData, isLoading: transportLoading, error: transportError, refetch: refetchTransport } = useVehicles();
  const createTransport = useCreateVehicle();
  const updateTransport = useUpdateVehicle();
  const deleteTransport = useDeleteVehicle();
  const { data: communicationData, isLoading: communicationLoading, error: communicationError, refetch: refetchCommunications } = useMessages();
  const createCommunication = useCreateMessage();
  const updateCommunication = useUpdateMessage();
  const deleteCommunication = useDeleteMessage();

  const handleLogout = () => {
    logout();
    router.push('/login');
  };

  // Action handlers
  const handleAddStudent = () => {
    setModalMode('add');
    setFormState({});
    setFormError(null);
    setSelectedStudent(null);
    setStudentModalOpen(true);
  };
  const handleEditStudent = (student: any) => {
    setModalMode('edit');
    setFormState(student);
    setFormError(null);
    setSelectedStudent(student);
    setStudentModalOpen(true);
  };
  const handleViewStudent = (student: any) => {
    setModalMode('view');
    setFormState(student);
    setFormError(null);
    setSelectedStudent(student);
    setStudentModalOpen(true);
  };
  const handleDeleteStudent = async (student: any) => {
    if (confirm(`Are you sure you want to delete student "${student.firstName} ${student.lastName}"?`)) {
      try {
        await deleteStudent.mutateAsync(student.id);
        refetchStudents();
      } catch (err: any) {
        alert(err.message || 'Failed to delete student');
      }
    }
  };
  const handleStudentFormChange = (e: any) => {
    setFormState({ ...formState, [e.target.name]: e.target.value });
  };
  const handleStudentFormSubmit = async (e: any) => {
    e.preventDefault();
    setFormError(null);
    try {
      if (modalMode === 'add') {
        await createStudent.mutateAsync(formState);
      } else if (modalMode === 'edit') {
        await updateStudent.mutateAsync({ ...formState, id: selectedStudent.id });
      }
      setStudentModalOpen(false);
      refetchStudents();
    } catch (err: any) {
      setFormError(err.message || 'Failed to save student');
    }
  };

  // Staff handlers
  const handleAddStaff = () => {
    setStaffModalMode('add');
    setStaffFormState({});
    setStaffFormError(null);
    setSelectedStaff(null);
    setStaffModalOpen(true);
  };
  const handleEditStaff = (staff: any) => {
    setStaffModalMode('edit');
    setStaffFormState(staff);
    setStaffFormError(null);
    setSelectedStaff(staff);
    setStaffModalOpen(true);
  };
  const handleViewStaff = (staff: any) => {
    setStaffModalMode('view');
    setStaffFormState(staff);
    setStaffFormError(null);
    setSelectedStaff(staff);
    setStaffModalOpen(true);
  };
  const handleDeleteStaff = async (staff: any) => {
    if (confirm(`Are you sure you want to delete staff member "${staff.firstName} ${staff.lastName}"?`)) {
      try {
        await deleteStaff.mutateAsync(staff.id);
        refetchStaff();
      } catch (err: any) {
        alert(err.message || 'Failed to delete staff member');
      }
    }
  };
  const handleStaffFormChange = (e: any) => {
    setStaffFormState({ ...staffFormState, [e.target.name]: e.target.value });
  };
  const handleStaffFormSubmit = async (e: any) => {
    e.preventDefault();
    setStaffFormError(null);
    try {
      if (staffModalMode === 'add') {
        await createStaff.mutateAsync(staffFormState);
      } else if (staffModalMode === 'edit') {
        await updateStaff.mutateAsync({ ...staffFormState, id: selectedStaff.id });
      }
      setStaffModalOpen(false);
      refetchStaff();
    } catch (err: any) {
      setStaffFormError(err.message || 'Failed to save staff member');
    }
  };

  // Fees handlers
  const handleAddFee = () => {
    setFeeModalMode('add');
    setFeeFormState({});
    setFeeFormError(null);
    setSelectedFee(null);
    setFeeModalOpen(true);
  };
  const handleEditFee = (fee: any) => {
    setFeeModalMode('edit');
    setFeeFormState(fee);
    setFeeFormError(null);
    setSelectedFee(fee);
    setFeeModalOpen(true);
  };
  const handleViewFee = (fee: any) => {
    setFeeModalMode('view');
    setFeeFormState(fee);
    setFeeFormError(null);
    setSelectedFee(fee);
    setFeeModalOpen(true);
  };
  const handleDeleteFee = async (fee: any) => {
    if (confirm(`Are you sure you want to delete this fee payment?`)) {
      try {
        await deleteFee.mutateAsync(fee.id);
        refetchFees();
      } catch (err: any) {
        alert(err.message || 'Failed to delete fee payment');
      }
    }
  };
  const handleFeeFormChange = (e: any) => {
    setFeeFormState({ ...feeFormState, [e.target.name]: e.target.value });
  };
  const handleFeeFormSubmit = async (e: any) => {
    e.preventDefault();
    setFeeFormError(null);
    try {
      if (feeModalMode === 'add') {
        await createFee.mutateAsync(feeFormState);
      } else if (feeModalMode === 'edit') {
        await updateFee.mutateAsync({ ...feeFormState, id: selectedFee.id });
      }
      setFeeModalOpen(false);
      refetchFees();
    } catch (err: any) {
      setFeeFormError(err.message || 'Failed to save fee payment');
    }
  };

  // Exams handlers
  const handleAddExam = () => {
    setExamModalMode('add');
    setExamFormState({});
    setExamFormError(null);
    setSelectedExam(null);
    setExamModalOpen(true);
  };
  const handleEditExam = (exam: any) => {
    setExamModalMode('edit');
    setExamFormState(exam);
    setExamFormError(null);
    setSelectedExam(exam);
    setExamModalOpen(true);
  };
  const handleViewExam = (exam: any) => {
    setExamModalMode('view');
    setExamFormState(exam);
    setExamFormError(null);
    setSelectedExam(exam);
    setExamModalOpen(true);
  };
  const handleDeleteExam = async (exam: any) => {
    if (confirm(`Are you sure you want to delete exam "${exam.title}"?`)) {
      try {
        await deleteExam.mutateAsync(exam.id);
        refetchExams();
      } catch (err: any) {
        alert(err.message || 'Failed to delete exam');
      }
    }
  };
  const handleExamFormChange = (e: any) => {
    setExamFormState({ ...examFormState, [e.target.name]: e.target.value });
  };
  const handleExamFormSubmit = async (e: any) => {
    e.preventDefault();
    setExamFormError(null);
    try {
      if (examModalMode === 'add') {
        await createExam.mutateAsync(examFormState);
      } else if (examModalMode === 'edit') {
        await updateExam.mutateAsync({ ...examFormState, id: selectedExam.id });
      }
      setExamModalOpen(false);
      refetchExams();
    } catch (err: any) {
      setExamFormError(err.message || 'Failed to save exam');
    }
  };

  // Attendance handlers
  const handleAddAttendance = () => {
    setAttendanceModalMode('add');
    setAttendanceFormState({});
    setAttendanceFormError(null);
    setSelectedAttendance(null);
    setAttendanceModalOpen(true);
  };
  const handleEditAttendance = (attendance: any) => {
    setAttendanceModalMode('edit');
    setAttendanceFormState(attendance);
    setAttendanceFormError(null);
    setSelectedAttendance(attendance);
    setAttendanceModalOpen(true);
  };
  const handleViewAttendance = (attendance: any) => {
    setAttendanceModalMode('view');
    setAttendanceFormState(attendance);
    setAttendanceFormError(null);
    setSelectedAttendance(attendance);
    setAttendanceModalOpen(true);
  };
  const handleDeleteAttendance = async (attendance: any) => {
    if (confirm(`Are you sure you want to delete this attendance record?`)) {
      try {
        await deleteAttendance.mutateAsync(attendance.id);
        refetchAttendance();
      } catch (err: any) {
        alert(err.message || 'Failed to delete attendance record');
      }
    }
  };
  const handleAttendanceFormChange = (e: any) => {
    setAttendanceFormState({ ...attendanceFormState, [e.target.name]: e.target.value });
  };
  const handleAttendanceFormSubmit = async (e: any) => {
    e.preventDefault();
    setAttendanceFormError(null);
    try {
      if (attendanceModalMode === 'add') {
        await createAttendance.mutateAsync(attendanceFormState);
      } else if (attendanceModalMode === 'edit') {
        await updateAttendance.mutateAsync({ ...attendanceFormState, id: selectedAttendance.id });
      }
      setAttendanceModalOpen(false);
      refetchAttendance();
    } catch (err: any) {
      setAttendanceFormError(err.message || 'Failed to save attendance record');
    }
  };

  // Homework handlers
  const handleAddHomework = () => {
    setHomeworkModalMode('add');
    setHomeworkFormState({});
    setHomeworkFormError(null);
    setSelectedHomework(null);
    setHomeworkModalOpen(true);
  };
  const handleEditHomework = (homework: any) => {
    setHomeworkModalMode('edit');
    setHomeworkFormState(homework);
    setHomeworkFormError(null);
    setSelectedHomework(homework);
    setHomeworkModalOpen(true);
  };
  const handleViewHomework = (homework: any) => {
    setHomeworkModalMode('view');
    setHomeworkFormState(homework);
    setHomeworkFormError(null);
    setSelectedHomework(homework);
    setHomeworkModalOpen(true);
  };
  const handleDeleteHomework = async (homework: any) => {
    if (confirm(`Are you sure you want to delete homework "${homework.title}"?`)) {
      try {
        await deleteHomework.mutateAsync(homework.id);
        refetchHomework();
      } catch (err: any) {
        alert(err.message || 'Failed to delete homework');
      }
    }
  };
  const handleHomeworkFormChange = (e: any) => {
    setHomeworkFormState({ ...homeworkFormState, [e.target.name]: e.target.value });
  };
  const handleHomeworkFormSubmit = async (e: any) => {
    e.preventDefault();
    setHomeworkFormError(null);
    try {
      if (homeworkModalMode === 'add') {
        await createHomework.mutateAsync(homeworkFormState);
      } else if (homeworkModalMode === 'edit') {
        await updateHomework.mutateAsync({ ...homeworkFormState, id: selectedHomework.id });
      }
      setHomeworkModalOpen(false);
      refetchHomework();
    } catch (err: any) {
      setHomeworkFormError(err.message || 'Failed to save homework');
    }
  };

  // Timetable handlers
  const handleAddTimetable = () => {
    setTimetableModalMode('add');
    setTimetableFormState({});
    setTimetableFormError(null);
    setSelectedTimetable(null);
    setTimetableModalOpen(true);
  };
  const handleEditTimetable = (timetable: any) => {
    setTimetableModalMode('edit');
    setTimetableFormState(timetable);
    setTimetableFormError(null);
    setSelectedTimetable(timetable);
    setTimetableModalOpen(true);
  };
  const handleViewTimetable = (timetable: any) => {
    setTimetableModalMode('view');
    setTimetableFormState(timetable);
    setTimetableFormError(null);
    setSelectedTimetable(timetable);
    setTimetableModalOpen(true);
  };
  const handleDeleteTimetable = async (timetable: any) => {
    if (confirm(`Are you sure you want to delete timetable "${timetable.title}"?`)) {
      try {
        await deleteTimetable.mutateAsync(timetable.id);
        refetchTimetables();
      } catch (err: any) {
        alert(err.message || 'Failed to delete timetable');
      }
    }
  };
  const handleTimetableFormChange = (e: any) => {
    setTimetableFormState({ ...timetableFormState, [e.target.name]: e.target.value });
  };
  const handleTimetableFormSubmit = async (e: any) => {
    e.preventDefault();
    setTimetableFormError(null);
    try {
      if (timetableModalMode === 'add') {
        await createTimetable.mutateAsync(timetableFormState);
      } else if (timetableModalMode === 'edit') {
        await updateTimetable.mutateAsync({ ...timetableFormState, id: selectedTimetable.id });
      }
      setTimetableModalOpen(false);
      refetchTimetables();
    } catch (err: any) {
      setTimetableFormError(err.message || 'Failed to save timetable');
    }
  };

  const handleViewPayment = (studentName: string) => {
    alert(`Viewing payment details for ${studentName}`);
  };

  const handleProcessPayment = (studentName: string) => {
    alert(`Processing payment for ${studentName}`);
  };

  const handleGenerateReport = () => {
    alert('Generating financial report...');
  };

  const handleViewAnalytics = () => {
    setActiveTab('analytics');
  };

  const handleManageSettings = () => {
    setActiveTab('settings');
  };

  // API hooks with error handling
  const { data: studentStats, isLoading: studentStatsLoading, error: studentStatsError } = useStudentStats();
  const { data: staffStats, isLoading: staffStatsLoading, error: staffStatsError } = useStaffStats();

  // Debug information
  console.log('Admin Portal Debug:', { 
    user, 
    isAuthenticated, 
    isLoading,
    studentsData,
    staffData,
    studentStats,
    staffStats
  });

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
          <p className="text-gray-600">Please log in to access the admin portal.</p>
        </div>
      </div>
    );
  }

  const stats = [
    { 
      title: 'Total Students', 
      value: studentStats?.total || studentsData?.total || '0', 
      change: '+12%', 
      icon: Users,
      loading: studentStatsLoading || studentsLoading,
      error: studentStatsError || studentsError
    },
    { 
      title: 'Total Staff', 
      value: staffStats?.total || staffData?.total || '0', 
      change: '+5%', 
      icon: GraduationCap,
      loading: staffStatsLoading || staffLoading,
      error: staffStatsError || staffError
    },
    { 
      title: 'Active Classes', 
      value: '45', 
      change: '+3%', 
      icon: Calendar,
      loading: false 
    },
    { 
      title: 'Revenue', 
      value: '$2.4M', 
      change: '+18%', 
      icon: DollarSign,
      loading: false 
    },
  ];

  const recentActivities = [
    { id: 1, type: 'student', action: 'New student enrolled', time: '2 hours ago', user: 'Sarah Johnson' },
    { id: 2, type: 'fee', action: 'Fee payment received', time: '4 hours ago', user: 'Mike Chen' },
    { id: 3, type: 'exam', action: 'Exam results published', time: '6 hours ago', user: 'Dr. Williams' },
    { id: 4, type: 'attendance', action: 'Attendance marked', time: '8 hours ago', user: 'Mrs. Davis' },
  ];

  const serviceTabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'students', label: 'Students', icon: Users },
    { id: 'staff', label: 'Staff', icon: GraduationCap },
    { id: 'fees', label: 'Fees', icon: DollarSign },
    { id: 'exams', label: 'Exams', icon: FileText },
    { id: 'attendance', label: 'Attendance', icon: Clock },
    { id: 'homework', label: 'Homework', icon: BookOpen },
    { id: 'timetable', label: 'Timetable', icon: Calendar },
    { id: 'library', label: 'Library', icon: BookOpen },
    { id: 'transport', label: 'Transport', icon: Truck },
    { id: 'communication', label: 'Communication', icon: MessageSquare },
    { id: 'analytics', label: 'Analytics', icon: TrendingUp },
    { id: 'notifications', label: 'Notifications', icon: Bell },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  const renderServiceComponent = () => {
    switch (activeTab) {
      case 'fees':
        return <FeeManagement schoolId={user?.schoolId} />;
      case 'exams':
        return <ExamManagement schoolId={user?.schoolId} />;
      case 'attendance':
        return <AttendanceManagement schoolId={user?.schoolId} />;
      case 'homework':
        return <HomeworkManagement schoolId={user?.schoolId} />;
      case 'timetable':
        return <TimetableManagement schoolId={user?.schoolId} />;
      case 'library':
        return <LibraryManagement schoolId={user?.schoolId} />;
      case 'transport':
        return <TransportManagement schoolId={user?.schoolId} />;
      case 'communication':
        return <CommunicationManagement schoolId={user?.schoolId} />;
      case 'analytics':
        return <AnalyticsManagement schoolId={user?.schoolId} />;
      case 'notifications':
        return <NotificationManagement schoolId={user?.schoolId} />;
      default:
        return null;
    }
  };

  // Transport handlers
  const handleAddTransport = () => {
    setTransportModalMode('add');
    setTransportFormState({});
    setTransportFormError(null);
    setSelectedTransport(null);
    setTransportModalOpen(true);
  };
  const handleEditTransport = (transport: any) => {
    setTransportModalMode('edit');
    setTransportFormState(transport);
    setTransportFormError(null);
    setSelectedTransport(transport);
    setTransportModalOpen(true);
  };
  const handleViewTransport = (transport: any) => {
    setTransportModalMode('view');
    setTransportFormState(transport);
    setTransportFormError(null);
    setSelectedTransport(transport);
    setTransportModalOpen(true);
  };
  const handleDeleteTransport = async (transport: any) => {
    if (confirm(`Are you sure you want to delete transport "${transport.vehicleNumber}"?`)) {
      try {
        await deleteTransport.mutateAsync(transport.id);
        refetchTransport();
      } catch (err: any) {
        alert(err.message || 'Failed to delete transport');
      }
    }
  };
  const handleTransportFormChange = (e: any) => {
    setTransportFormState({ ...transportFormState, [e.target.name]: e.target.value });
  };
  const handleTransportFormSubmit = async (e: any) => {
    e.preventDefault();
    setTransportFormError(null);
    try {
      if (transportModalMode === 'add') {
        await createTransport.mutateAsync(transportFormState);
      } else if (transportModalMode === 'edit') {
        await updateTransport.mutateAsync({ ...transportFormState, id: selectedTransport.id });
      }
      setTransportModalOpen(false);
      refetchTransport();
    } catch (err: any) {
      setTransportFormError(err.message || 'Failed to save transport');
    }
  };

  // Library handlers
  const handleAddLibrary = () => {
    setLibraryModalMode('add');
    setLibraryFormState({});
    setLibraryFormError(null);
    setSelectedLibrary(null);
    setLibraryModalOpen(true);
  };
  const handleEditLibrary = (library: any) => {
    setLibraryModalMode('edit');
    setLibraryFormState(library);
    setLibraryFormError(null);
    setSelectedLibrary(library);
    setLibraryModalOpen(true);
  };
  const handleViewLibrary = (library: any) => {
    setLibraryModalMode('view');
    setLibraryFormState(library);
    setLibraryFormError(null);
    setSelectedLibrary(library);
    setLibraryModalOpen(true);
  };
  const handleDeleteLibrary = async (library: any) => {
    if (confirm(`Are you sure you want to delete book "${library.title}"?`)) {
      try {
        await deleteLibrary.mutateAsync(library.id);
        refetchLibrary();
      } catch (err: any) {
        alert(err.message || 'Failed to delete book');
      }
    }
  };
  const handleLibraryFormChange = (e: any) => {
    setLibraryFormState({ ...libraryFormState, [e.target.name]: e.target.value });
  };
  const handleLibraryFormSubmit = async (e: any) => {
    e.preventDefault();
    setLibraryFormError(null);
    try {
      if (libraryModalMode === 'add') {
        await createLibrary.mutateAsync(libraryFormState);
      } else if (libraryModalMode === 'edit') {
        await updateLibrary.mutateAsync({ ...libraryFormState, id: selectedLibrary.id });
      }
      setLibraryModalOpen(false);
      refetchLibrary();
    } catch (err: any) {
      setLibraryFormError(err.message || 'Failed to save book');
    }
  };

  // Communication handlers
  const handleAddCommunication = () => {
    setCommunicationModalMode('add');
    setCommunicationFormState({});
    setCommunicationFormError(null);
    setSelectedCommunication(null);
    setCommunicationModalOpen(true);
  };
  const handleEditCommunication = (communication: any) => {
    setCommunicationModalMode('edit');
    setCommunicationFormState(communication);
    setCommunicationFormError(null);
    setSelectedCommunication(communication);
    setCommunicationModalOpen(true);
  };
  const handleViewCommunication = (communication: any) => {
    setCommunicationModalMode('view');
    setCommunicationFormState(communication);
    setCommunicationFormError(null);
    setSelectedCommunication(communication);
    setCommunicationModalOpen(true);
  };
  const handleDeleteCommunication = async (communication: any) => {
    if (confirm(`Are you sure you want to delete message "${communication.subject}"?`)) {
      try {
        await deleteCommunication.mutateAsync(communication.id);
        refetchCommunications();
      } catch (err: any) {
        alert(err.message || 'Failed to delete message');
      }
    }
  };
  const handleCommunicationFormChange = (e: any) => {
    setCommunicationFormState({ ...communicationFormState, [e.target.name]: e.target.value });
  };
  const handleCommunicationFormSubmit = async (e: any) => {
    e.preventDefault();
    setCommunicationFormError(null);
    try {
      if (communicationModalMode === 'add') {
        await createCommunication.mutateAsync(communicationFormState);
      } else if (communicationModalMode === 'edit') {
        await updateCommunication.mutateAsync({ ...communicationFormState, id: selectedCommunication.id });
      }
      setCommunicationModalOpen(false);
      refetchCommunications();
    } catch (err: any) {
      setCommunicationFormError(err.message || 'Failed to save message');
    }
  };

  return (
    <AdminRoute>
      <div className="flex h-screen bg-gray-50">
        {/* Sidebar */}
        <aside className="w-64 bg-white shadow-lg">
          <div className="p-6">
            <h1 className="text-2xl font-bold text-gray-900">AI SchoolOS</h1>
            <p className="text-sm text-gray-600">Admin Portal</p>
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
                    Admin Dashboard
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
                    <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                      <span className="text-white text-sm font-medium">A</span>
                    </div>
                    <span className="text-sm font-medium text-gray-700">Admin</span>
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
                        ? 'bg-blue-100 text-blue-700'
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
                            <stat.icon className="h-8 w-8 text-blue-600" />
                          </div>
                          <div className="ml-5 w-0 flex-1">
                            <dl>
                              <dt className="text-sm font-medium text-gray-500 truncate">
                                {stat.title}
                              </dt>
                              <dd className="flex items-baseline">
                                <div className="text-2xl font-semibold text-gray-900">
                                  {stat.value}
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
                        <button className="flex items-center justify-center px-4 py-3 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors">
                          <Users className="h-4 w-4 mr-2" />
                          Add Student
                        </button>
                        <button 
                          onClick={handleAddStaff}
                          className="flex items-center justify-center px-4 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
                        >
                          <GraduationCap className="h-4 w-4 mr-2" />
                          Add Staff
                        </button>
                        <button className="flex items-center justify-center px-4 py-3 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors">
                          <DollarSign className="h-4 w-4 mr-2" />
                          Manage Fees
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
                        <div className="flex items-center space-x-4">
                          <div className="flex-shrink-0">
                            <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                              <Users className="h-4 w-4 text-green-600" />
                            </div>
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-gray-900">
                              New student enrolled
                            </p>
                            <p className="text-sm text-gray-500">
                              Sarah Johnson • 2 hours ago
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
                              Fee payment received
                            </p>
                            <p className="text-sm text-gray-500">
                              Mike Chen • 4 hours ago
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-4">
                          <div className="flex-shrink-0">
                            <div className="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                              <GraduationCap className="h-4 w-4 text-yellow-600" />
                            </div>
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className="text-sm font-medium text-gray-900">
                              New teacher hired
                            </p>
                            <p className="text-sm text-gray-500">
                              Mrs. Williams • 1 day ago
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Students Tab */}
              {activeTab === 'students' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Student Management</h3>
                        <button 
                          onClick={handleAddStudent}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Add Student
                        </button>
                      </div>
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
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Parent</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(studentsData?.students || []).map((student: any) => (
                                <tr key={student.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{student.firstName} {student.lastName}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{student.className || '-'}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{student.parentName || '-'}</td>
                                  <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${student.isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500'}`}>{student.isActive ? 'Active' : 'Inactive'}</span>
                                  </td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <button 
                                      onClick={() => handleEditStudent(student)}
                                      className="text-blue-600 hover:text-blue-900 mr-3"
                                    >
                                      Edit
                                    </button>
                                    <button 
                                      onClick={() => handleViewStudent(student)}
                                      className="text-green-600 hover:text-green-900 mr-3"
                                    >
                                      View
                                    </button>
                                    <button 
                                      onClick={() => handleDeleteStudent(student)}
                                      className="text-red-600 hover:text-red-900"
                                    >
                                      Delete
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
                  {/* Student Modal */}
                  <Dialog open={isStudentModalOpen} onClose={() => setStudentModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
                    <div className="flex items-center justify-center min-h-screen px-4">
                      <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
                      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
                        <Dialog.Title className="text-lg font-bold mb-4">
                          {modalMode === 'add' ? 'Add Student' : modalMode === 'edit' ? 'Edit Student' : 'View Student'}
                        </Dialog.Title>
                        <form onSubmit={handleStudentFormSubmit} className="space-y-4">
                          <input type="text" name="firstName" value={formState.firstName || ''} onChange={handleStudentFormChange} placeholder="First Name" className="w-full border rounded px-3 py-2" disabled={modalMode === 'view'} required />
                          <input type="text" name="lastName" value={formState.lastName || ''} onChange={handleStudentFormChange} placeholder="Last Name" className="w-full border rounded px-3 py-2" disabled={modalMode === 'view'} required />
                          <input type="text" name="className" value={formState.className || ''} onChange={handleStudentFormChange} placeholder="Class" className="w-full border rounded px-3 py-2" disabled={modalMode === 'view'} />
                          <input type="text" name="parentName" value={formState.parentName || ''} onChange={handleStudentFormChange} placeholder="Parent Name" className="w-full border rounded px-3 py-2" disabled={modalMode === 'view'} />
                          <label className="flex items-center space-x-2">
                            <input type="checkbox" name="isActive" checked={!!formState.isActive} onChange={e => setFormState({ ...formState, isActive: e.target.checked })} disabled={modalMode === 'view'} />
                            <span>Active</span>
                          </label>
                          {formError && <div className="text-red-600 text-sm">{formError}</div>}
                          {modalMode !== 'view' && (
                            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">{modalMode === 'add' ? 'Add' : 'Save'}</button>
                          )}
                          <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setStudentModalOpen(false)}>Close</button>
                        </form>
                      </div>
                    </div>
                  </Dialog>
                </div>
              )}

              {/* Staff Tab */}
              {activeTab === 'staff' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Staff Management</h3>
                        <button 
                          onClick={handleAddStaff}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Add Staff
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {staffLoading ? (
                        <div className="text-center text-gray-500">Loading staff...</div>
                      ) : staffError ? (
                        <div className="text-center text-red-500">{(staffError as any)?.message || 'Failed to load staff'}</div>
                      ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                          {(staffData?.staff || []).map((staff: any) => (
                            <div key={staff.id} className="border border-gray-200 rounded-lg p-4">
                              <h4 className="font-semibold text-gray-900 mb-2">{staff.firstName} {staff.lastName}</h4>
                              <p className="text-sm text-gray-600 mb-2">{staff.role || staff.department}</p>
                              <p className="text-sm text-gray-500 mb-3">{staff.email}</p>
                              <div className="flex justify-between items-center">
                                <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${staff.isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-500'}`}>
                                  {staff.isActive ? 'Active' : 'Inactive'}
                                </span>
                                <div className="flex space-x-2">
                                  <button 
                                    onClick={() => handleEditStaff(staff)}
                                    className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded hover:bg-blue-200"
                                  >
                                    Edit
                                  </button>
                                  <button 
                                    onClick={() => handleViewStaff(staff)}
                                    className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded hover:bg-green-200"
                                  >
                                    View
                                  </button>
                                  <button 
                                    onClick={() => handleDeleteStaff(staff)}
                                    className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded hover:bg-red-200"
                                  >
                                    Delete
                                  </button>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                  {/* Staff Modal */}
                  <Dialog open={isStaffModalOpen} onClose={() => setStaffModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
                    <div className="flex items-center justify-center min-h-screen px-4">
                      <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
                      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
                        <Dialog.Title className="text-lg font-bold mb-4">
                          {staffModalMode === 'add' ? 'Add Staff Member' : staffModalMode === 'edit' ? 'Edit Staff Member' : 'View Staff Member'}
                        </Dialog.Title>
                        <form onSubmit={handleStaffFormSubmit} className="space-y-4">
                          <input type="text" name="firstName" value={staffFormState.firstName || ''} onChange={handleStaffFormChange} placeholder="First Name" className="w-full border rounded px-3 py-2" disabled={staffModalMode === 'view'} required />
                          <input type="text" name="lastName" value={staffFormState.lastName || ''} onChange={handleStaffFormChange} placeholder="Last Name" className="w-full border rounded px-3 py-2" disabled={staffModalMode === 'view'} required />
                          <input type="email" name="email" value={staffFormState.email || ''} onChange={handleStaffFormChange} placeholder="Email" className="w-full border rounded px-3 py-2" disabled={staffModalMode === 'view'} required />
                          <input type="text" name="role" value={staffFormState.role || ''} onChange={handleStaffFormChange} placeholder="Role/Position" className="w-full border rounded px-3 py-2" disabled={staffModalMode === 'view'} />
                          <input type="text" name="department" value={staffFormState.department || ''} onChange={handleStaffFormChange} placeholder="Department" className="w-full border rounded px-3 py-2" disabled={staffModalMode === 'view'} />
                          <label className="flex items-center space-x-2">
                            <input type="checkbox" name="isActive" checked={!!staffFormState.isActive} onChange={e => setStaffFormState({ ...staffFormState, isActive: e.target.checked })} disabled={staffModalMode === 'view'} />
                            <span>Active</span>
                          </label>
                          {staffFormError && <div className="text-red-600 text-sm">{staffFormError}</div>}
                          {staffModalMode !== 'view' && (
                            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">{staffModalMode === 'add' ? 'Add' : 'Save'}</button>
                          )}
                          <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setStaffModalOpen(false)}>Close</button>
                        </form>
                      </div>
                    </div>
                  </Dialog>
                </div>
              )}

              {/* Financial Tab */}
              {activeTab === 'fees' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Fee Management</h3>
                        <button 
                          onClick={handleAddFee}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Add Fee Payment
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {feeLoading ? (
                        <div className="text-center text-gray-500">Loading fees...</div>
                      ) : feeError ? (
                        <div className="text-center text-red-500">{(feeError as any)?.message || 'Failed to load fees'}</div>
                      ) : (
                        <div className="space-y-6">
                          {/* Fee Summary */}
                          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                            <div className="bg-blue-50 p-4 rounded-lg">
                              <h4 className="text-sm font-medium text-blue-600">Total Payments</h4>
                              <p className="text-2xl font-bold text-blue-900">{feeData?.total || 0}</p>
                            </div>
                            <div className="bg-green-50 p-4 rounded-lg">
                              <h4 className="text-sm font-medium text-green-600">Paid Fees</h4>
                              <p className="text-2xl font-bold text-green-900">{(feeData?.payments || []).filter((p: any) => p.paymentStatus === 'paid').length}</p>
                            </div>
                            <div className="bg-red-50 p-4 rounded-lg">
                              <h4 className="text-sm font-medium text-red-600">Pending Fees</h4>
                              <p className="text-2xl font-bold text-red-900">{(feeData?.payments || []).filter((p: any) => p.paymentStatus === 'pending').length}</p>
                            </div>
                            <div className="bg-purple-50 p-4 rounded-lg">
                              <h4 className="text-sm font-medium text-purple-600">Collection Rate</h4>
                              <p className="text-2xl font-bold text-purple-900">
                                {feeData?.total ? Math.round(((feeData.payments || []).filter((p: any) => p.paymentStatus === 'paid').length / feeData.total) * 100) : 0}%
                              </p>
                            </div>
                          </div>

                          {/* Fee Payments Table */}
                          <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200">
                              <thead className="bg-gray-50">
                                <tr>
                                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Student</th>
                                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amount</th>
                                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
                                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                                </tr>
                              </thead>
                              <tbody className="bg-white divide-y divide-gray-200">
                                {(feeData?.payments || []).map((fee: any) => (
                                  <tr key={fee.id}>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{fee.studentId}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${fee.amount}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{fee.dueDate}</td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                      <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                        fee.paymentStatus === 'paid' ? 'bg-green-100 text-green-800' : 
                                        fee.paymentStatus === 'pending' ? 'bg-yellow-100 text-yellow-800' : 
                                        fee.paymentStatus === 'overdue' ? 'bg-red-100 text-red-800' :
                                        'bg-gray-100 text-gray-500'
                                      }`}>
                                        {fee.paymentStatus}
                                      </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                      <button 
                                        onClick={() => handleEditFee(fee)}
                                        className="text-blue-600 hover:text-blue-900 mr-3"
                                      >
                                        Edit
                                      </button>
                                      <button 
                                        onClick={() => handleViewFee(fee)}
                                        className="text-green-600 hover:text-green-900 mr-3"
                                      >
                                        View
                                      </button>
                                      <button 
                                        onClick={() => handleDeleteFee(fee)}
                                        className="text-red-600 hover:text-red-900"
                                      >
                                        Delete
                                      </button>
                                    </td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                  {/* Fee Modal */}
                  <Dialog open={isFeeModalOpen} onClose={() => setFeeModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
                    <div className="flex items-center justify-center min-h-screen px-4">
                      <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
                      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
                        <Dialog.Title className="text-lg font-bold mb-4">
                          {feeModalMode === 'add' ? 'Add Fee Payment' : feeModalMode === 'edit' ? 'Edit Fee Payment' : 'View Fee Payment'}
                        </Dialog.Title>
                        <form onSubmit={handleFeeFormSubmit} className="space-y-4">
                          <input type="text" name="studentName" value={feeFormState.studentName || ''} onChange={handleFeeFormChange} placeholder="Student Name" className="w-full border rounded px-3 py-2" disabled={feeModalMode === 'view'} required />
                          <input type="number" name="amount" value={feeFormState.amount || ''} onChange={handleFeeFormChange} placeholder="Amount" className="w-full border rounded px-3 py-2" disabled={feeModalMode === 'view'} required />
                          <input type="date" name="dueDate" value={feeFormState.dueDate || ''} onChange={handleFeeFormChange} placeholder="Due Date" className="w-full border rounded px-3 py-2" disabled={feeModalMode === 'view'} />
                          <select name="status" value={feeFormState.status || ''} onChange={handleFeeFormChange} className="w-full border rounded px-3 py-2" disabled={feeModalMode === 'view'}>
                            <option value="">Select Status</option>
                            <option value="Paid">Paid</option>
                            <option value="Pending">Pending</option>
                            <option value="Overdue">Overdue</option>
                          </select>
                          {feeFormError && <div className="text-red-600 text-sm">{feeFormError}</div>}
                          {feeModalMode !== 'view' && (
                            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">{feeModalMode === 'add' ? 'Add' : 'Save'}</button>
                          )}
                          <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setFeeModalOpen(false)}>Close</button>
                        </form>
                      </div>
                    </div>
                  </Dialog>
                </div>
              )}

              {/* Exams Tab */}
              {activeTab === 'exams' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Exam Management</h3>
                        <button 
                          onClick={handleAddExam}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Add Exam
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {examLoading ? (
                        <div className="text-center text-gray-500">Loading exams...</div>
                      ) : examError ? (
                        <div className="text-center text-red-500">{(examError as any)?.message || 'Failed to load exams'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Subject</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Date</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Duration</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(examData?.exams || []).map((exam: any) => (
                                <tr key={exam.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{exam.title}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{exam.subject}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{exam.examDate}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{exam.duration} mins</td>
                                  <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                      exam.status === 'Scheduled' ? 'bg-blue-100 text-blue-800' : 
                                      exam.status === 'In Progress' ? 'bg-yellow-100 text-yellow-800' : 
                                      exam.status === 'Completed' ? 'bg-green-100 text-green-800' : 
                                      'bg-gray-100 text-gray-500'
                                    }`}>
                                      {exam.status}
                                    </span>
                                  </td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <button 
                                      onClick={() => handleEditExam(exam)}
                                      className="text-blue-600 hover:text-blue-900 mr-3"
                                    >
                                      Edit
                                    </button>
                                    <button 
                                      onClick={() => handleViewExam(exam)}
                                      className="text-green-600 hover:text-green-900 mr-3"
                                    >
                                      View
                                    </button>
                                    <button 
                                      onClick={() => handleDeleteExam(exam)}
                                      className="text-red-600 hover:text-red-900"
                                    >
                                      Delete
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
                  {/* Exam Modal */}
                  <Dialog open={isExamModalOpen} onClose={() => setExamModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
                    <div className="flex items-center justify-center min-h-screen px-4">
                      <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
                      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
                        <Dialog.Title className="text-lg font-bold mb-4">
                          {examModalMode === 'add' ? 'Add Exam' : examModalMode === 'edit' ? 'Edit Exam' : 'View Exam'}
                        </Dialog.Title>
                        <form onSubmit={handleExamFormSubmit} className="space-y-4">
                          <input type="text" name="title" value={examFormState.title || ''} onChange={handleExamFormChange} placeholder="Exam Title" className="w-full border rounded px-3 py-2" disabled={examModalMode === 'view'} required />
                          <input type="text" name="subject" value={examFormState.subject || ''} onChange={handleExamFormChange} placeholder="Subject" className="w-full border rounded px-3 py-2" disabled={examModalMode === 'view'} required />
                          <input type="date" name="examDate" value={examFormState.examDate || ''} onChange={handleExamFormChange} placeholder="Exam Date" className="w-full border rounded px-3 py-2" disabled={examModalMode === 'view'} />
                          <input type="number" name="duration" value={examFormState.duration || ''} onChange={handleExamFormChange} placeholder="Duration (minutes)" className="w-full border rounded px-3 py-2" disabled={examModalMode === 'view'} />
                          <select name="status" value={examFormState.status || ''} onChange={handleExamFormChange} className="w-full border rounded px-3 py-2" disabled={examModalMode === 'view'}>
                            <option value="">Select Status</option>
                            <option value="Scheduled">Scheduled</option>
                            <option value="In Progress">In Progress</option>
                            <option value="Completed">Completed</option>
                          </select>
                          {examFormError && <div className="text-red-600 text-sm">{examFormError}</div>}
                          {examModalMode !== 'view' && (
                            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">{examModalMode === 'add' ? 'Add' : 'Save'}</button>
                          )}
                          <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setExamModalOpen(false)}>Close</button>
                        </form>
                      </div>
                    </div>
                  </Dialog>
                </div>
              )}

              {/* Attendance Tab */}
              {activeTab === 'attendance' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Attendance Management</h3>
                        <button 
                          onClick={handleAddAttendance}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Add Attendance
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
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(attendanceData?.attendance || []).map((attendance: any) => (
                                <tr key={attendance.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{attendance.studentId}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{attendance.date}</td>
                                  <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                      attendance.status === 'present' ? 'bg-green-100 text-green-800' : 
                                      attendance.status === 'absent' ? 'bg-red-100 text-red-800' : 
                                      attendance.status === 'late' ? 'bg-yellow-100 text-yellow-800' : 
                                      'bg-gray-100 text-gray-500'
                                    }`}>
                                      {attendance.status}
                                    </span>
                                  </td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{attendance.time}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <button 
                                      onClick={() => handleEditAttendance(attendance)}
                                      className="text-blue-600 hover:text-blue-900 mr-3"
                                    >
                                      Edit
                                    </button>
                                    <button 
                                      onClick={() => handleViewAttendance(attendance)}
                                      className="text-green-600 hover:text-green-900 mr-3"
                                    >
                                      View
                                    </button>
                                    <button 
                                      onClick={() => handleDeleteAttendance(attendance)}
                                      className="text-red-600 hover:text-red-900"
                                    >
                                      Delete
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
                  {/* Attendance Modal */}
                  <Dialog open={isAttendanceModalOpen} onClose={() => setAttendanceModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
                    <div className="flex items-center justify-center min-h-screen px-4">
                      <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
                      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
                        <Dialog.Title className="text-lg font-bold mb-4">
                          {attendanceModalMode === 'add' ? 'Add Attendance' : attendanceModalMode === 'edit' ? 'Edit Attendance' : 'View Attendance'}
                        </Dialog.Title>
                        <form onSubmit={handleAttendanceFormSubmit} className="space-y-4">
                          <input type="text" name="studentId" value={attendanceFormState.studentId || ''} onChange={handleAttendanceFormChange} placeholder="Student ID" className="w-full border rounded px-3 py-2" disabled={attendanceModalMode === 'view'} required />
                          <input type="date" name="date" value={attendanceFormState.date || ''} onChange={handleAttendanceFormChange} placeholder="Date" className="w-full border rounded px-3 py-2" disabled={attendanceModalMode === 'view'} required />
                          <input type="time" name="time" value={attendanceFormState.time || ''} onChange={handleAttendanceFormChange} placeholder="Time" className="w-full border rounded px-3 py-2" disabled={attendanceModalMode === 'view'} />
                          <select name="status" value={attendanceFormState.status || ''} onChange={handleAttendanceFormChange} className="w-full border rounded px-3 py-2" disabled={attendanceModalMode === 'view'}>
                            <option value="">Select Status</option>
                            <option value="present">Present</option>
                            <option value="absent">Absent</option>
                            <option value="late">Late</option>
                          </select>
                          {attendanceFormError && <div className="text-red-600 text-sm">{attendanceFormError}</div>}
                          {attendanceModalMode !== 'view' && (
                            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">{attendanceModalMode === 'add' ? 'Add' : 'Save'}</button>
                          )}
                          <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setAttendanceModalOpen(false)}>Close</button>
                        </form>
                      </div>
                    </div>
                  </Dialog>
                </div>
              )}

              {/* Homework Tab */}
              {activeTab === 'homework' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Homework Management</h3>
                        <button 
                          onClick={handleAddHomework}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Add Homework
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {homeworkLoading ? (
                        <div className="text-center text-gray-500">Loading homework...</div>
                      ) : homeworkError ? (
                        <div className="text-center text-red-500">{(homeworkError as any)?.message || 'Failed to load homework'}</div>
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
                              {(homeworkData?.homework || []).map((homework: any) => (
                                <tr key={homework.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{homework.title}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{homework.subject}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{homework.dueDate}</td>
                                  <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                      homework.status === 'active' ? 'bg-green-100 text-green-800' : 
                                      homework.status === 'completed' ? 'bg-blue-100 text-blue-800' : 
                                      homework.status === 'overdue' ? 'bg-red-100 text-red-800' : 
                                      'bg-gray-100 text-gray-500'
                                    }`}>
                                      {homework.status}
                                    </span>
                                  </td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <button 
                                      onClick={() => handleEditHomework(homework)}
                                      className="text-blue-600 hover:text-blue-900 mr-3"
                                    >
                                      Edit
                                    </button>
                                    <button 
                                      onClick={() => handleViewHomework(homework)}
                                      className="text-green-600 hover:text-green-900 mr-3"
                                    >
                                      View
                                    </button>
                                    <button 
                                      onClick={() => handleDeleteHomework(homework)}
                                      className="text-red-600 hover:text-red-900"
                                    >
                                      Delete
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
                  {/* Homework Modal */}
                  <Dialog open={isHomeworkModalOpen} onClose={() => setHomeworkModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
                    <div className="flex items-center justify-center min-h-screen px-4">
                      <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
                      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
                        <Dialog.Title className="text-lg font-bold mb-4">
                          {homeworkModalMode === 'add' ? 'Add Homework' : homeworkModalMode === 'edit' ? 'Edit Homework' : 'View Homework'}
                        </Dialog.Title>
                        <form onSubmit={handleHomeworkFormSubmit} className="space-y-4">
                          <input type="text" name="title" value={homeworkFormState.title || ''} onChange={handleHomeworkFormChange} placeholder="Homework Title" className="w-full border rounded px-3 py-2" disabled={homeworkModalMode === 'view'} required />
                          <input type="text" name="subject" value={homeworkFormState.subject || ''} onChange={handleHomeworkFormChange} placeholder="Subject" className="w-full border rounded px-3 py-2" disabled={homeworkModalMode === 'view'} required />
                          <textarea name="description" value={homeworkFormState.description || ''} onChange={handleHomeworkFormChange} placeholder="Description" className="w-full border rounded px-3 py-2" disabled={homeworkModalMode === 'view'} rows={3} />
                          <input type="date" name="dueDate" value={homeworkFormState.dueDate || ''} onChange={handleHomeworkFormChange} placeholder="Due Date" className="w-full border rounded px-3 py-2" disabled={homeworkModalMode === 'view'} />
                          <select name="status" value={homeworkFormState.status || ''} onChange={handleHomeworkFormChange} className="w-full border rounded px-3 py-2" disabled={homeworkModalMode === 'view'}>
                            <option value="">Select Status</option>
                            <option value="active">Active</option>
                            <option value="completed">Completed</option>
                            <option value="overdue">Overdue</option>
                          </select>
                          {homeworkFormError && <div className="text-red-600 text-sm">{homeworkFormError}</div>}
                          {homeworkModalMode !== 'view' && (
                            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">{homeworkModalMode === 'add' ? 'Add' : 'Save'}</button>
                          )}
                          <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setHomeworkModalOpen(false)}>Close</button>
                        </form>
                      </div>
                    </div>
                  </Dialog>
                </div>
              )}

              {/* Timetable Tab */}
              {activeTab === 'timetable' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Timetable Management</h3>
                        <button 
                          onClick={handleAddTimetable}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Add Timetable
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {timetableLoading ? (
                        <div className="text-center text-gray-500">Loading timetables...</div>
                      ) : timetableError ? (
                        <div className="text-center text-red-500">{(timetableError as any)?.message || 'Failed to load timetables'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Class</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Day</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Time</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Subject</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(timetableData?.timetables || []).map((timetable: any) => (
                                <tr key={timetable.id}>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{timetable.title}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{timetable.className}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{timetable.day}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{timetable.startTime} - {timetable.endTime}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{timetable.subject}</td>
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <button 
                                      onClick={() => handleEditTimetable(timetable)}
                                      className="text-blue-600 hover:text-blue-900 mr-3"
                                    >
                                      Edit
                                    </button>
                                    <button 
                                      onClick={() => handleViewTimetable(timetable)}
                                      className="text-green-600 hover:text-green-900 mr-3"
                                    >
                                      View
                                    </button>
                                    <button 
                                      onClick={() => handleDeleteTimetable(timetable)}
                                      className="text-red-600 hover:text-red-900"
                                    >
                                      Delete
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
                  {/* Timetable Modal */}
                  <Dialog open={isTimetableModalOpen} onClose={() => setTimetableModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
                    <div className="flex items-center justify-center min-h-screen px-4">
                      <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
                      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
                        <Dialog.Title className="text-lg font-bold mb-4">
                          {timetableModalMode === 'add' ? 'Add Timetable' : timetableModalMode === 'edit' ? 'Edit Timetable' : 'View Timetable'}
                        </Dialog.Title>
                        <form onSubmit={handleTimetableFormSubmit} className="space-y-4">
                          <input type="text" name="title" value={timetableFormState.title || ''} onChange={handleTimetableFormChange} placeholder="Timetable Title" className="w-full border rounded px-3 py-2" disabled={timetableModalMode === 'view'} required />
                          <input type="text" name="className" value={timetableFormState.className || ''} onChange={handleTimetableFormChange} placeholder="Class" className="w-full border rounded px-3 py-2" disabled={timetableModalMode === 'view'} required />
                          <select name="day" value={timetableFormState.day || ''} onChange={handleTimetableFormChange} className="w-full border rounded px-3 py-2" disabled={timetableModalMode === 'view'}>
                            <option value="">Select Day</option>
                            <option value="Monday">Monday</option>
                            <option value="Tuesday">Tuesday</option>
                            <option value="Wednesday">Wednesday</option>
                            <option value="Thursday">Thursday</option>
                            <option value="Friday">Friday</option>
                            <option value="Saturday">Saturday</option>
                            <option value="Sunday">Sunday</option>
                          </select>
                          <input type="time" name="startTime" value={timetableFormState.startTime || ''} onChange={handleTimetableFormChange} placeholder="Start Time" className="w-full border rounded px-3 py-2" disabled={timetableModalMode === 'view'} />
                          <input type="time" name="endTime" value={timetableFormState.endTime || ''} onChange={handleTimetableFormChange} placeholder="End Time" className="w-full border rounded px-3 py-2" disabled={timetableModalMode === 'view'} />
                          <input type="text" name="subject" value={timetableFormState.subject || ''} onChange={handleTimetableFormChange} placeholder="Subject" className="w-full border rounded px-3 py-2" disabled={timetableModalMode === 'view'} />
                          {timetableFormError && <div className="text-red-600 text-sm">{timetableFormError}</div>}
                          {timetableModalMode !== 'view' && (
                            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">{timetableModalMode === 'add' ? 'Add' : 'Save'}</button>
                          )}
                          <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setTimetableModalOpen(false)}>Close</button>
                        </form>
                      </div>
                    </div>
                  </Dialog>
                </div>
              )}

              {/* Library Tab */}
              {activeTab === 'library' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Library Management</h3>
                        <button 
                          onClick={handleAddLibrary}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Add Book
                        </button>
                      </div>
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
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
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
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <button 
                                      onClick={() => handleEditLibrary(book)}
                                      className="text-blue-600 hover:text-blue-900 mr-3"
                                    >
                                      Edit
                                    </button>
                                    <button 
                                      onClick={() => handleViewLibrary(book)}
                                      className="text-green-600 hover:text-green-900 mr-3"
                                    >
                                      View
                                    </button>
                                    <button 
                                      onClick={() => handleDeleteLibrary(book)}
                                      className="text-red-600 hover:text-red-900"
                                    >
                                      Delete
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
                  {/* Library Modal */}
                  <Dialog open={isLibraryModalOpen} onClose={() => setLibraryModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
                    <div className="flex items-center justify-center min-h-screen px-4">
                      <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
                      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
                        <Dialog.Title className="text-lg font-bold mb-4">
                          {libraryModalMode === 'add' ? 'Add Book' : libraryModalMode === 'edit' ? 'Edit Book' : 'View Book'}
                        </Dialog.Title>
                        <form onSubmit={handleLibraryFormSubmit} className="space-y-4">
                          <input type="text" name="title" value={libraryFormState.title || ''} onChange={handleLibraryFormChange} placeholder="Book Title" className="w-full border rounded px-3 py-2" disabled={libraryModalMode === 'view'} required />
                          <input type="text" name="author" value={libraryFormState.author || ''} onChange={handleLibraryFormChange} placeholder="Author" className="w-full border rounded px-3 py-2" disabled={libraryModalMode === 'view'} required />
                          <input type="text" name="isbn" value={libraryFormState.isbn || ''} onChange={handleLibraryFormChange} placeholder="ISBN" className="w-full border rounded px-3 py-2" disabled={libraryModalMode === 'view'} />
                          <select name="category" value={libraryFormState.category || ''} onChange={handleLibraryFormChange} className="w-full border rounded px-3 py-2" disabled={libraryModalMode === 'view'}>
                            <option value="">Select Category</option>
                            <option value="Fiction">Fiction</option>
                            <option value="Non-Fiction">Non-Fiction</option>
                            <option value="Science">Science</option>
                            <option value="Mathematics">Mathematics</option>
                            <option value="Literature">Literature</option>
                            <option value="History">History</option>
                            <option value="Geography">Geography</option>
                            <option value="Reference">Reference</option>
                          </select>
                          <select name="status" value={libraryFormState.status || ''} onChange={handleLibraryFormChange} className="w-full border rounded px-3 py-2" disabled={libraryModalMode === 'view'}>
                            <option value="">Select Status</option>
                            <option value="available">Available</option>
                            <option value="borrowed">Borrowed</option>
                            <option value="reserved">Reserved</option>
                          </select>
                          {libraryFormError && <div className="text-red-600 text-sm">{libraryFormError}</div>}
                          {libraryModalMode !== 'view' && (
                            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">{libraryModalMode === 'add' ? 'Add' : 'Save'}</button>
                          )}
                          <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setLibraryModalOpen(false)}>Close</button>
                        </form>
                      </div>
                    </div>
                  </Dialog>
                </div>
              )}

              {/* Transport Tab */}
              {activeTab === 'transport' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Transport Management</h3>
                        <button 
                          onClick={handleAddTransport}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Add Transport
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {transportLoading ? (
                        <div className="text-center text-gray-500">Loading transport...</div>
                      ) : transportError ? (
                        <div className="text-center text-red-500">{(transportError as any)?.message || 'Failed to load transport'}</div>
                      ) : (
                        <div className="overflow-x-auto">
                          <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vehicle Number</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Driver</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Route</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
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
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <button 
                                      onClick={() => handleEditTransport(vehicle)}
                                      className="text-blue-600 hover:text-blue-900 mr-3"
                                    >
                                      Edit
                                    </button>
                                    <button 
                                      onClick={() => handleViewTransport(vehicle)}
                                      className="text-green-600 hover:text-green-900 mr-3"
                                    >
                                      View
                                    </button>
                                    <button 
                                      onClick={() => handleDeleteTransport(vehicle)}
                                      className="text-red-600 hover:text-red-900"
                                    >
                                      Delete
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
                  {/* Transport Modal */}
                  <Dialog open={isTransportModalOpen} onClose={() => setTransportModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
                    <div className="flex items-center justify-center min-h-screen px-4">
                      <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
                      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
                        <Dialog.Title className="text-lg font-bold mb-4">
                          {transportModalMode === 'add' ? 'Add Transport' : transportModalMode === 'edit' ? 'Edit Transport' : 'View Transport'}
                        </Dialog.Title>
                        <form onSubmit={handleTransportFormSubmit} className="space-y-4">
                          <input type="text" name="vehicleNumber" value={transportFormState.vehicleNumber || ''} onChange={handleTransportFormChange} placeholder="Vehicle Number" className="w-full border rounded px-3 py-2" disabled={transportModalMode === 'view'} required />
                          <input type="text" name="driverName" value={transportFormState.driverName || ''} onChange={handleTransportFormChange} placeholder="Driver Name" className="w-full border rounded px-3 py-2" disabled={transportModalMode === 'view'} required />
                          <input type="text" name="route" value={transportFormState.route || ''} onChange={handleTransportFormChange} placeholder="Route" className="w-full border rounded px-3 py-2" disabled={transportModalMode === 'view'} />
                          <input type="text" name="capacity" value={transportFormState.capacity || ''} onChange={handleTransportFormChange} placeholder="Capacity" className="w-full border rounded px-3 py-2" disabled={transportModalMode === 'view'} />
                          <select name="status" value={transportFormState.status || ''} onChange={handleTransportFormChange} className="w-full border rounded px-3 py-2" disabled={transportModalMode === 'view'}>
                            <option value="">Select Status</option>
                            <option value="active">Active</option>
                            <option value="maintenance">Maintenance</option>
                            <option value="inactive">Inactive</option>
                          </select>
                          {transportFormError && <div className="text-red-600 text-sm">{transportFormError}</div>}
                          {transportModalMode !== 'view' && (
                            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">{transportModalMode === 'add' ? 'Add' : 'Save'}</button>
                          )}
                          <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setTransportModalOpen(false)}>Close</button>
                        </form>
                      </div>
                    </div>
                  </Dialog>
                </div>
              )}

              {/* Communication Tab */}
              {activeTab === 'communication' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Communication Management</h3>
                        <button 
                          onClick={handleAddCommunication}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Send Message
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {communicationLoading ? (
                        <div className="text-center text-gray-500">Loading messages...</div>
                      ) : communicationError ? (
                        <div className="text-center text-red-500">{(communicationError as any)?.message || 'Failed to load messages'}</div>
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
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                              </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                              {(communicationData?.messages || []).map((message: any) => (
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
                                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <button 
                                      onClick={() => handleEditCommunication(message)}
                                      className="text-blue-600 hover:text-blue-900 mr-3"
                                    >
                                      Edit
                                    </button>
                                    <button 
                                      onClick={() => handleViewCommunication(message)}
                                      className="text-green-600 hover:text-green-900 mr-3"
                                    >
                                      View
                                    </button>
                                    <button 
                                      onClick={() => handleDeleteCommunication(message)}
                                      className="text-red-600 hover:text-red-900"
                                    >
                                      Delete
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
                  {/* Communication Modal */}
                  <Dialog open={isCommunicationModalOpen} onClose={() => setCommunicationModalOpen(false)} className="fixed z-50 inset-0 overflow-y-auto">
                    <div className="flex items-center justify-center min-h-screen px-4">
                      <Dialog.Overlay className="fixed inset-0 bg-black opacity-30" />
                      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-auto z-50 p-6 relative">
                        <Dialog.Title className="text-lg font-bold mb-4">
                          {communicationModalMode === 'add' ? 'Send Message' : communicationModalMode === 'edit' ? 'Edit Message' : 'View Message'}
                        </Dialog.Title>
                        <form onSubmit={handleCommunicationFormSubmit} className="space-y-4">
                          <input type="text" name="subject" value={communicationFormState.subject || ''} onChange={handleCommunicationFormChange} placeholder="Subject" className="w-full border rounded px-3 py-2" disabled={communicationModalMode === 'view'} required />
                          <input type="text" name="from" value={communicationFormState.from || ''} onChange={handleCommunicationFormChange} placeholder="From" className="w-full border rounded px-3 py-2" disabled={communicationModalMode === 'view'} required />
                          <input type="text" name="to" value={communicationFormState.to || ''} onChange={handleCommunicationFormChange} placeholder="To" className="w-full border rounded px-3 py-2" disabled={communicationModalMode === 'view'} required />
                          <textarea name="message" value={communicationFormState.message || ''} onChange={handleCommunicationFormChange} placeholder="Message" className="w-full border rounded px-3 py-2" disabled={communicationModalMode === 'view'} rows={4} />
                          <select name="type" value={communicationFormState.type || ''} onChange={handleCommunicationFormChange} className="w-full border rounded px-3 py-2" disabled={communicationModalMode === 'view'}>
                            <option value="">Select Type</option>
                            <option value="email">Email</option>
                            <option value="sms">SMS</option>
                            <option value="notification">Notification</option>
                          </select>
                          {communicationFormError && <div className="text-red-600 text-sm">{communicationFormError}</div>}
                          {communicationModalMode !== 'view' && (
                            <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700">{communicationModalMode === 'add' ? 'Send' : 'Save'}</button>
                          )}
                          <button type="button" className="w-full mt-2 border py-2 rounded" onClick={() => setCommunicationModalOpen(false)}>Close</button>
                        </form>
                      </div>
                    </div>
                  </Dialog>
                </div>
              )}

              {/* Analytics Tab */}
              {activeTab === 'analytics' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Analytics Management</h3>
                        <button 
                          onClick={handleGenerateReport}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Generate Report
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {/* Add analytics content here */}
                    </div>
                  </div>
                </div>
              )}

              {/* Notifications Tab */}
              {activeTab === 'notifications' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Notification Management</h3>
                        <button 
                          onClick={handleManageSettings}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Manage Settings
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {/* Add notification content here */}
                    </div>
                  </div>
                </div>
              )}

              {/* Settings Tab */}
              {activeTab === 'settings' && (
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow">
                    <div className="px-6 py-4 border-b border-gray-200">
                      <div className="flex justify-between items-center">
                        <h3 className="text-lg font-medium text-gray-900">Settings</h3>
                        <button 
                          onClick={handleManageSettings}
                          className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
                        >
                          Manage Settings
                        </button>
                      </div>
                    </div>
                    <div className="p-6">
                      {/* Add settings content here */}
                    </div>
                  </div>
                </div>
              )}

              {/* Other tabs show placeholder */}
              {!['dashboard', 'students', 'staff', 'fees', 'exams', 'attendance', 'homework', 'timetable'].includes(activeTab) && (
                <div className="bg-white rounded-lg shadow p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">{serviceTabs.find(tab => tab.id === activeTab)?.label}</h3>
                  <p className="text-gray-600">This feature is coming soon...</p>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </AdminRoute>
  );
} 