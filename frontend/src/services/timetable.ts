import { apiService, ApiResponse } from './api';

// Timetable Types
export interface Timetable {
  id: string;
  name: string;
  description: string;
  classId: string;
  academicYear: string;
  semester?: string;
  isActive: boolean;
  schoolId: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}

export interface TimetableSlot {
  id: string;
  timetableId: string;
  dayOfWeek: number; // 1-7 (Monday-Sunday)
  startTime: string;
  endTime: string;
  subjectId: string;
  teacherId: string;
  roomId?: string;
  slotType: 'lecture' | 'lab' | 'break' | 'lunch' | 'assembly';
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Room {
  id: string;
  name: string;
  roomNumber: string;
  capacity: number;
  roomType: 'classroom' | 'laboratory' | 'auditorium' | 'library' | 'office';
  building: string;
  floor: string;
  isActive: boolean;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface Schedule {
  id: string;
  timetableId: string;
  classId: string;
  subjectId: string;
  teacherId: string;
  roomId?: string;
  dayOfWeek: number;
  startTime: string;
  endTime: string;
  date?: string; // For specific dates
  isRecurring: boolean;
  status: 'scheduled' | 'cancelled' | 'rescheduled';
  notes?: string;
  createdAt: string;
  updatedAt: string;
}

export interface TimetableFilters {
  classId?: string;
  teacherId?: string;
  subjectId?: string;
  dayOfWeek?: number;
  schoolId?: string;
  isActive?: boolean;
}

export interface TimetableListResponse {
  timetables: Timetable[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Timetable Service class
export class TimetableService {
  private readonly TIMETABLE_ENDPOINTS = {
    TIMETABLES: '/api/v1/timetables',
    SLOTS: '/api/v1/timetables/slots',
    ROOMS: '/api/v1/timetables/rooms',
    SCHEDULES: '/api/v1/timetables/schedules',
    CLASS_TIMETABLES: '/api/v1/timetables/classes',
    TEACHER_TIMETABLES: '/api/v1/timetables/teachers',
    CONFLICTS: '/api/v1/timetables/conflicts',
    REPORTS: '/api/v1/timetables/reports',
  };

  // Get timetables
  async getTimetables(filters?: TimetableFilters): Promise<TimetableListResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<TimetableListResponse>(
      `${this.TIMETABLE_ENDPOINTS.TIMETABLES}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch timetables');
  }

  // Get timetable by ID
  async getTimetable(id: string): Promise<Timetable> {
    const response = await apiService.get<Timetable>(`${this.TIMETABLE_ENDPOINTS.TIMETABLES}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch timetable');
  }

  // Create timetable
  async createTimetable(data: Partial<Timetable>): Promise<Timetable> {
    const response = await apiService.post<Timetable>(this.TIMETABLE_ENDPOINTS.TIMETABLES, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create timetable');
  }

  // Update timetable
  async updateTimetable(id: string, data: Partial<Timetable>): Promise<Timetable> {
    const response = await apiService.put<Timetable>(`${this.TIMETABLE_ENDPOINTS.TIMETABLES}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update timetable');
  }

  // Delete timetable
  async deleteTimetable(id: string): Promise<void> {
    const response = await apiService.delete(`${this.TIMETABLE_ENDPOINTS.TIMETABLES}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete timetable');
    }
  }

  // Get timetable slots
  async getTimetableSlots(filters?: any): Promise<TimetableSlot[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<TimetableSlot[]>(
      `${this.TIMETABLE_ENDPOINTS.SLOTS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch timetable slots');
  }

  // Get timetable slot by ID
  async getTimetableSlot(id: string): Promise<TimetableSlot> {
    const response = await apiService.get<TimetableSlot>(`${this.TIMETABLE_ENDPOINTS.SLOTS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch timetable slot');
  }

  // Create timetable slot
  async createTimetableSlot(data: Partial<TimetableSlot>): Promise<TimetableSlot> {
    const response = await apiService.post<TimetableSlot>(this.TIMETABLE_ENDPOINTS.SLOTS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create timetable slot');
  }

  // Update timetable slot
  async updateTimetableSlot(id: string, data: Partial<TimetableSlot>): Promise<TimetableSlot> {
    const response = await apiService.put<TimetableSlot>(`${this.TIMETABLE_ENDPOINTS.SLOTS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update timetable slot');
  }

  // Delete timetable slot
  async deleteTimetableSlot(id: string): Promise<void> {
    const response = await apiService.delete(`${this.TIMETABLE_ENDPOINTS.SLOTS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete timetable slot');
    }
  }

  // Get rooms
  async getRooms(schoolId?: string, filters?: any): Promise<Room[]> {
    const params = new URLSearchParams();
    
    if (schoolId) {
      params.append('schoolId', schoolId);
    }
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<Room[]>(
      `${this.TIMETABLE_ENDPOINTS.ROOMS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch rooms');
  }

  // Get room by ID
  async getRoom(id: string): Promise<Room> {
    const response = await apiService.get<Room>(`${this.TIMETABLE_ENDPOINTS.ROOMS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch room');
  }

  // Create room
  async createRoom(data: Partial<Room>): Promise<Room> {
    const response = await apiService.post<Room>(this.TIMETABLE_ENDPOINTS.ROOMS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create room');
  }

  // Update room
  async updateRoom(id: string, data: Partial<Room>): Promise<Room> {
    const response = await apiService.put<Room>(`${this.TIMETABLE_ENDPOINTS.ROOMS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update room');
  }

  // Delete room
  async deleteRoom(id: string): Promise<void> {
    const response = await apiService.delete(`${this.TIMETABLE_ENDPOINTS.ROOMS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete room');
    }
  }

  // Get schedules
  async getSchedules(filters?: any): Promise<Schedule[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<Schedule[]>(
      `${this.TIMETABLE_ENDPOINTS.SCHEDULES}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch schedules');
  }

  // Get schedule by ID
  async getSchedule(id: string): Promise<Schedule> {
    const response = await apiService.get<Schedule>(`${this.TIMETABLE_ENDPOINTS.SCHEDULES}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch schedule');
  }

  // Create schedule
  async createSchedule(data: Partial<Schedule>): Promise<Schedule> {
    const response = await apiService.post<Schedule>(this.TIMETABLE_ENDPOINTS.SCHEDULES, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create schedule');
  }

  // Update schedule
  async updateSchedule(id: string, data: Partial<Schedule>): Promise<Schedule> {
    const response = await apiService.put<Schedule>(`${this.TIMETABLE_ENDPOINTS.SCHEDULES}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update schedule');
  }

  // Delete schedule
  async deleteSchedule(id: string): Promise<void> {
    const response = await apiService.delete(`${this.TIMETABLE_ENDPOINTS.SCHEDULES}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete schedule');
    }
  }

  // Get class timetables
  async getClassTimetables(classId: string): Promise<Timetable[]> {
    const response = await apiService.get<Timetable[]>(`${this.TIMETABLE_ENDPOINTS.CLASS_TIMETABLES}/${classId}/timetables`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch class timetables');
  }

  // Get teacher timetables
  async getTeacherTimetables(teacherId: string): Promise<Timetable[]> {
    const response = await apiService.get<Timetable[]>(`${this.TIMETABLE_ENDPOINTS.TEACHER_TIMETABLES}/${teacherId}/timetables`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch teacher timetables');
  }

  // Get timetable reports
  async getTimetableReports(schoolId?: string, dateFrom?: string, dateTo?: string): Promise<any> {
    const params = new URLSearchParams();
    
    if (schoolId) {
      params.append('schoolId', schoolId);
    }
    
    if (dateFrom) {
      params.append('dateFrom', dateFrom);
    }
    
    if (dateTo) {
      params.append('dateTo', dateTo);
    }

    const response = await apiService.get<any>(
      `${this.TIMETABLE_ENDPOINTS.REPORTS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch timetable reports');
  }

  // Get timetable stats
  async getTimetableStats(schoolId?: string): Promise<any> {
    const params = new URLSearchParams();
    
    if (schoolId) {
      params.append('schoolId', schoolId);
    }

    const response = await apiService.get<any>(
      `${this.TIMETABLE_ENDPOINTS.REPORTS}/stats?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch timetable stats');
  }
}

// Export singleton instance
export const timetableService = new TimetableService();
export default timetableService; 