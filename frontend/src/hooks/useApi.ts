import { useQuery, useMutation, useQueryClient, UseQueryOptions, UseMutationOptions } from '@tanstack/react-query';
import { studentService, Student, CreateStudentData, UpdateStudentData, StudentFilters, StudentListResponse } from '../services/student';
import { staffService, Staff, CreateStaffData, UpdateStaffData, StaffFilters, StaffListResponse } from '../services/staff';
import { authService, User, LoginCredentials, RegisterData } from '../services/auth';
import { feeService, FeeStructure, FeePayment, FeeDiscount, FinancialRecord, FeeFilters, FeeListResponse } from '../services/fee';
import { examService, Exam, ExamResult, ExamSchedule, Grade, ExamFilters, ExamListResponse } from '../services/exam';
import { attendanceService, Attendance, AttendanceReport, AttendanceStats, AttendanceFilters, AttendanceListResponse } from '../services/attendance';
import { homeworkService, Homework, HomeworkSubmission, HomeworkGrade, HomeworkFilters, HomeworkListResponse } from '../services/homework';
import { timetableService, Timetable, TimetableSlot, Room, Schedule, TimetableFilters, TimetableListResponse } from '../services/timetable';
import { libraryService, Book, BookBorrowing, LibraryMember, LibraryTransaction, LibraryFilters, LibraryListResponse } from '../services/library';
import { transportService, Vehicle, Route, RouteStop, TransportBooking, Driver, Conductor, TransportFilters, TransportListResponse } from '../services/transport';
import { communicationService, Message, Announcement, Notification as CommNotification, ChatRoom, ChatMessage, CommunicationFilters, CommunicationListResponse } from '../services/communication';
import { analyticsService, AnalyticsData, Dashboard, DashboardWidget, Report, PerformanceMetric, AnalyticsFilters, AnalyticsListResponse } from '../services/analytics';
import { notificationService, Notification, NotificationTemplate, NotificationChannel, NotificationPreference, NotificationSchedule, NotificationFilters, NotificationListResponse } from '../services/notification';

// Student Hooks
export const useStudents = (filters?: StudentFilters, options?: UseQueryOptions<StudentListResponse>) => {
  return useQuery({
    queryKey: ['students', filters],
    queryFn: () => studentService.getStudents(filters),
    ...options,
  });
};

export const useStudent = (id: string, options?: UseQueryOptions<Student>) => {
  return useQuery({
    queryKey: ['student', id],
    queryFn: () => studentService.getStudent(id),
    enabled: !!id,
    ...options,
  });
};

export const useCreateStudent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateStudentData) => studentService.createStudent(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['students'] });
    },
  });
};

export const useUpdateStudent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UpdateStudentData) => studentService.updateStudent(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['students'] });
      queryClient.invalidateQueries({ queryKey: ['student', data.id] });
    },
  });
};

export const useDeleteStudent = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => studentService.deleteStudent(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['students'] });
    },
  });
};

export const useStudentsBySchool = (schoolId: string, filters?: StudentFilters, options?: UseQueryOptions<StudentListResponse>) => {
  return useQuery({
    queryKey: ['students', 'school', schoolId, filters],
    queryFn: () => studentService.getStudentsBySchool(schoolId, filters),
    enabled: !!schoolId,
    ...options,
  });
};

export const useStudentsByClass = (classId: string, options?: UseQueryOptions<Student[]>) => {
  return useQuery({
    queryKey: ['students', 'class', classId],
    queryFn: () => studentService.getStudentsByClass(classId),
    enabled: !!classId,
    ...options,
  });
};

export const useStudentsByParent = (parentId: string, options?: UseQueryOptions<Student[]>) => {
  return useQuery({
    queryKey: ['students', 'parent', parentId],
    queryFn: () => studentService.getStudentsByParent(parentId),
    enabled: !!parentId,
    ...options,
  });
};

export const useStudentStats = (schoolId?: string, options?: UseQueryOptions<any>) => {
  return useQuery({
    queryKey: ['students', 'stats', schoolId],
    queryFn: () => studentService.getStudentStats(schoolId),
    ...options,
  });
};

// Staff Hooks
export const useStaff = (filters?: StaffFilters, options?: UseQueryOptions<StaffListResponse>) => {
  return useQuery({
    queryKey: ['staff', filters],
    queryFn: () => staffService.getStaff(filters),
    ...options,
  });
};

export const useStaffMember = (id: string, options?: UseQueryOptions<Staff>) => {
  return useQuery({
    queryKey: ['staff', id],
    queryFn: () => staffService.getStaffMember(id),
    enabled: !!id,
    ...options,
  });
};

export const useCreateStaff = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateStaffData) => staffService.createStaff(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['staff'] });
    },
  });
};

export const useUpdateStaff = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UpdateStaffData) => staffService.updateStaff(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['staff'] });
      queryClient.invalidateQueries({ queryKey: ['staff', data.id] });
    },
  });
};

export const useDeleteStaff = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => staffService.deleteStaff(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['staff'] });
    },
  });
};

export const useStaffBySchool = (schoolId: string, filters?: StaffFilters, options?: UseQueryOptions<StaffListResponse>) => {
  return useQuery({
    queryKey: ['staff', 'school', schoolId, filters],
    queryFn: () => staffService.getStaffBySchool(schoolId, filters),
    enabled: !!schoolId,
    ...options,
  });
};

export const useTeachers = (filters?: StaffFilters, options?: UseQueryOptions<StaffListResponse>) => {
  return useQuery({
    queryKey: ['staff', 'teachers', filters],
    queryFn: () => staffService.getTeachers(filters),
    ...options,
  });
};

export const useAdmins = (filters?: StaffFilters, options?: UseQueryOptions<StaffListResponse>) => {
  return useQuery({
    queryKey: ['staff', 'admins', filters],
    queryFn: () => staffService.getAdmins(filters),
    ...options,
  });
};

export const useStaffStats = (schoolId?: string, options?: UseQueryOptions<any>) => {
  return useQuery({
    queryKey: ['staff', 'stats', schoolId],
    queryFn: () => staffService.getStaffStats(schoolId),
    ...options,
  });
};

// Auth Hooks
export const useCurrentUser = (options?: UseQueryOptions<User>) => {
  return useQuery({
    queryKey: ['auth', 'me'],
    queryFn: () => authService.getCurrentUser(),
    enabled: authService.isAuthenticated(),
    ...options,
  });
};

export const useLogin = () => {
  return useMutation({
    mutationFn: (credentials: LoginCredentials) => authService.login(credentials),
  });
};

export const useRegister = () => {
  return useMutation({
    mutationFn: (data: RegisterData) => authService.register(data),
  });
};

export const useLogout = () => {
  return useMutation({
    mutationFn: () => authService.logout(),
  });
};

// Utility hooks
export const useAuthStatus = () => {
  return {
    isAuthenticated: authService.isAuthenticated(),
    isTokenExpired: authService.isTokenExpired(),
    userRole: authService.getUserRole(),
    storedUser: authService.getStoredUser(),
  };
};

export const useHasRole = (role: string) => {
  return authService.hasRole(role);
};

export const useHasAnyRole = (roles: string[]) => {
  return authService.hasAnyRole(roles);
};

// Fee Hooks
export const useFeeStructures = (schoolId?: string, options?: UseQueryOptions<FeeStructure[]>) => {
  return useQuery({
    queryKey: ['fee-structures', schoolId],
    queryFn: () => feeService.getFeeStructures(schoolId),
    ...options,
  });
};

export const useFeePayments = (filters?: FeeFilters, options?: UseQueryOptions<FeeListResponse>) => {
  return useQuery({
    queryKey: ['fee-payments', filters],
    queryFn: () => feeService.getFeePayments(filters),
    ...options,
  });
};

export const useFeePayment = (id: string, options?: UseQueryOptions<FeePayment>) => {
  return useQuery({
    queryKey: ['fee-payment', id],
    queryFn: () => feeService.getFeePayment(id),
    enabled: !!id,
    ...options,
  });
};

export const useCreateFeePayment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<FeePayment>) => feeService.createFeePayment(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['fee-payments'] });
    },
  });
};

export const useUpdateFeePayment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<FeePayment> }) => feeService.updateFeePayment(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['fee-payments'] });
      queryClient.invalidateQueries({ queryKey: ['fee-payment', id] });
    },
  });
};

export const useDeleteFeePayment = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => feeService.deleteFeePayment(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['fee-payments'] });
    },
  });
};

// Exam Hooks
export const useExams = (filters?: ExamFilters, options?: UseQueryOptions<ExamListResponse>) => {
  return useQuery({
    queryKey: ['exams', filters],
    queryFn: () => examService.getExams(filters),
    ...options,
  });
};

export const useExam = (id: string, options?: UseQueryOptions<Exam>) => {
  return useQuery({
    queryKey: ['exam', id],
    queryFn: () => examService.getExam(id),
    enabled: !!id,
    ...options,
  });
};

export const useCreateExam = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Exam>) => examService.createExam(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['exams'] });
    },
  });
};

export const useUpdateExam = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Exam> }) => examService.updateExam(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['exams'] });
      queryClient.invalidateQueries({ queryKey: ['exam', id] });
    },
  });
};

export const useDeleteExam = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => examService.deleteExam(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['exams'] });
    },
  });
};

// Attendance Hooks
export const useAttendance = (filters?: AttendanceFilters, options?: UseQueryOptions<AttendanceListResponse>) => {
  return useQuery({
    queryKey: ['attendance', filters],
    queryFn: () => attendanceService.getAttendance(filters),
    ...options,
  });
};

export const useAttendanceRecord = (id: string, options?: UseQueryOptions<Attendance>) => {
  return useQuery({
    queryKey: ['attendance-record', id],
    queryFn: () => attendanceService.getAttendanceRecord(id),
    enabled: !!id,
    ...options,
  });
};

export const useCreateAttendance = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Attendance>) => attendanceService.createAttendance(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['attendance'] });
    },
  });
};

export const useUpdateAttendance = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Attendance> }) => attendanceService.updateAttendance(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['attendance'] });
      queryClient.invalidateQueries({ queryKey: ['attendance-record', id] });
    },
  });
};

export const useDeleteAttendance = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => attendanceService.deleteAttendance(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['attendance'] });
    },
  });
};

// Homework Hooks
export const useHomework = (filters?: HomeworkFilters, options?: UseQueryOptions<HomeworkListResponse>) => {
  return useQuery({
    queryKey: ['homework', filters],
    queryFn: () => homeworkService.getHomeworkAssignments(filters),
    ...options,
  });
};

export const useHomeworkById = (id: string, options?: UseQueryOptions<Homework>) => {
  return useQuery({
    queryKey: ['homework', id],
    queryFn: () => homeworkService.getHomeworkAssignment(id),
    enabled: !!id,
    ...options,
  });
};

export const useCreateHomework = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Homework>) => homeworkService.createHomeworkAssignment(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['homework'] });
    },
  });
};

export const useUpdateHomework = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Homework> }) => homeworkService.updateHomeworkAssignment(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['homework'] });
      queryClient.invalidateQueries({ queryKey: ['homework', id] });
    },
  });
};

export const useDeleteHomework = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => homeworkService.deleteHomeworkAssignment(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['homework'] });
    },
  });
};

// Timetable Hooks
export const useTimetables = (filters?: TimetableFilters, options?: UseQueryOptions<TimetableListResponse>) => {
  return useQuery({
    queryKey: ['timetables', filters],
    queryFn: () => timetableService.getTimetables(filters),
    ...options,
  });
};

export const useTimetable = (id: string, options?: UseQueryOptions<Timetable>) => {
  return useQuery({
    queryKey: ['timetable', id],
    queryFn: () => timetableService.getTimetable(id),
    enabled: !!id,
    ...options,
  });
};

export const useCreateTimetable = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Timetable>) => timetableService.createTimetable(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['timetables'] });
    },
  });
};

export const useUpdateTimetable = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Timetable> }) => timetableService.updateTimetable(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['timetables'] });
      queryClient.invalidateQueries({ queryKey: ['timetable', id] });
    },
  });
};

export const useDeleteTimetable = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => timetableService.deleteTimetable(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['timetables'] });
    },
  });
};

// Library Hooks
export const useBooks = (filters?: LibraryFilters, options?: UseQueryOptions<LibraryListResponse>) => {
  return useQuery({
    queryKey: ['books', filters],
    queryFn: () => libraryService.getBooks(filters),
    ...options,
  });
};

export const useBook = (id: string, options?: UseQueryOptions<Book>) => {
  return useQuery({
    queryKey: ['book', id],
    queryFn: () => libraryService.getBook(id),
    enabled: !!id,
    ...options,
  });
};

export const useCreateBook = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Book>) => libraryService.createBook(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['books'] });
    },
  });
};

export const useUpdateBook = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Book> }) => libraryService.updateBook(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['books'] });
      queryClient.invalidateQueries({ queryKey: ['book', id] });
    },
  });
};

export const useDeleteBook = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => libraryService.deleteBook(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['books'] });
    },
  });
};

// Transport Hooks
export const useVehicles = (filters?: TransportFilters, options?: UseQueryOptions<TransportListResponse>) => {
  return useQuery({
    queryKey: ['vehicles', filters],
    queryFn: () => transportService.getVehicles(filters),
    ...options,
  });
};

export const useVehicle = (id: string, options?: UseQueryOptions<Vehicle>) => {
  return useQuery({
    queryKey: ['vehicle', id],
    queryFn: () => transportService.getVehicle(id),
    enabled: !!id,
    ...options,
  });
};

export const useCreateVehicle = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Vehicle>) => transportService.createVehicle(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vehicles'] });
    },
  });
};

export const useUpdateVehicle = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Vehicle> }) => transportService.updateVehicle(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['vehicles'] });
      queryClient.invalidateQueries({ queryKey: ['vehicle', id] });
    },
  });
};

export const useDeleteVehicle = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => transportService.deleteVehicle(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vehicles'] });
    },
  });
};

// Communication Hooks
export const useMessages = (filters?: CommunicationFilters, options?: UseQueryOptions<CommunicationListResponse>) => {
  return useQuery({
    queryKey: ['messages', filters],
    queryFn: () => communicationService.getMessages(filters),
    ...options,
  });
};

export const useMessage = (id: string, options?: UseQueryOptions<Message>) => {
  return useQuery({
    queryKey: ['message', id],
    queryFn: () => communicationService.getMessage(id),
    enabled: !!id,
    ...options,
  });
};

export const useCreateMessage = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Message>) => communicationService.createMessage(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['messages'] });
    },
  });
};

export const useUpdateMessage = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Message> }) => communicationService.updateMessage(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['messages'] });
      queryClient.invalidateQueries({ queryKey: ['message', id] });
    },
  });
};

export const useDeleteMessage = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => communicationService.deleteMessage(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['messages'] });
    },
  });
};

// Analytics Hooks
export const useAnalyticsData = (filters?: AnalyticsFilters, options?: UseQueryOptions<AnalyticsListResponse>) => {
  return useQuery({
    queryKey: ['analytics-data', filters],
    queryFn: () => analyticsService.getAnalyticsData(filters),
    ...options,
  });
};

export const useAnalyticsDataById = (id: string, options?: UseQueryOptions<AnalyticsData>) => {
  return useQuery({
    queryKey: ['analytics-data', id],
    queryFn: () => analyticsService.getAnalyticsDataById(id),
    enabled: !!id,
    ...options,
  });
};

export const useCreateAnalyticsData = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<AnalyticsData>) => analyticsService.createAnalyticsData(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['analytics-data'] });
    },
  });
};

export const useUpdateAnalyticsData = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<AnalyticsData> }) => analyticsService.updateAnalyticsData(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['analytics-data'] });
      queryClient.invalidateQueries({ queryKey: ['analytics-data', id] });
    },
  });
};

export const useDeleteAnalyticsData = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => analyticsService.deleteAnalyticsData(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['analytics-data'] });
    },
  });
};

// Notification Hooks
export const useNotifications = (filters?: NotificationFilters, options?: UseQueryOptions<NotificationListResponse>) => {
  return useQuery({
    queryKey: ['notifications', filters],
    queryFn: () => notificationService.getNotifications(filters),
    ...options,
  });
};

export const useNotification = (id: string, options?: UseQueryOptions<Notification>) => {
  return useQuery({
    queryKey: ['notification', id],
    queryFn: () => notificationService.getNotification(id),
    enabled: !!id,
    ...options,
  });
};

export const useCreateNotification = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<Notification>) => notificationService.createNotification(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
  });
};

export const useUpdateNotification = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Notification> }) => notificationService.updateNotification(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
      queryClient.invalidateQueries({ queryKey: ['notification', id] });
    },
  });
};

export const useDeleteNotification = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => notificationService.deleteNotification(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notifications'] });
    },
  });
}; 