import { apiService, ApiResponse } from './api';

// Notification Types
export interface Notification {
  id: string;
  userId: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error' | 'reminder';
  category: 'academic' | 'financial' | 'attendance' | 'transport' | 'library' | 'general';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  status: 'unread' | 'read' | 'archived';
  readAt?: string;
  actionUrl?: string;
  metadata?: any;
  isActive: boolean;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface NotificationTemplate {
  id: string;
  name: string;
  description: string;
  title: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error' | 'reminder';
  category: 'academic' | 'financial' | 'attendance' | 'transport' | 'library' | 'general';
  variables: string[];
  isActive: boolean;
  schoolId: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}

export interface NotificationChannel {
  id: string;
  userId: string;
  channelType: 'email' | 'sms' | 'push' | 'in_app';
  channelValue: string;
  isActive: boolean;
  isVerified: boolean;
  verifiedAt?: string;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface NotificationPreference {
  id: string;
  userId: string;
  category: 'academic' | 'financial' | 'attendance' | 'transport' | 'library' | 'general';
  emailEnabled: boolean;
  smsEnabled: boolean;
  pushEnabled: boolean;
  inAppEnabled: boolean;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface NotificationSchedule {
  id: string;
  templateId: string;
  scheduleType: 'immediate' | 'scheduled' | 'recurring';
  scheduleTime?: string;
  recurrence?: string;
  targetAudience: 'all' | 'students' | 'teachers' | 'parents' | 'staff' | 'admin';
  filters?: any;
  status: 'draft' | 'scheduled' | 'sent' | 'cancelled';
  sentAt?: string;
  schoolId: string;
  createdBy: string;
  createdAt: string;
  updatedAt: string;
}

export interface NotificationFilters {
  userId?: string;
  type?: string;
  category?: string;
  priority?: string;
  status?: string;
  dateFrom?: string;
  dateTo?: string;
  schoolId?: string;
}

export interface NotificationListResponse {
  notifications: Notification[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Notification Service class
export class NotificationService {
  private readonly NOTIFICATION_ENDPOINTS = {
    NOTIFICATIONS: '/api/v1/notifications',
    TEMPLATES: '/api/v1/notifications/templates',
    CHANNELS: '/api/v1/notifications/channels',
    PREFERENCES: '/api/v1/notifications/preferences',
    SCHEDULES: '/api/v1/notifications/schedules',
    REPORTS: '/api/v1/notifications/reports',
  };

  // Get notifications
  async getNotifications(filters?: NotificationFilters): Promise<NotificationListResponse> {
    const response = await apiService.get<NotificationListResponse>(this.NOTIFICATION_ENDPOINTS.NOTIFICATIONS, filters);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch notifications');
  }

  // Get notification by ID
  async getNotification(id: string): Promise<Notification> {
    const response = await apiService.get<Notification>(`${this.NOTIFICATION_ENDPOINTS.NOTIFICATIONS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch notification');
  }

  // Create notification
  async createNotification(data: Partial<Notification>): Promise<Notification> {
    const response = await apiService.post<Notification>(this.NOTIFICATION_ENDPOINTS.NOTIFICATIONS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create notification');
  }

  // Update notification
  async updateNotification(id: string, data: Partial<Notification>): Promise<Notification> {
    const response = await apiService.put<Notification>(`${this.NOTIFICATION_ENDPOINTS.NOTIFICATIONS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update notification');
  }

  // Delete notification
  async deleteNotification(id: string): Promise<void> {
    const response = await apiService.delete(`${this.NOTIFICATION_ENDPOINTS.NOTIFICATIONS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete notification');
    }
  }

  // Get user notifications
  async getUserNotifications(userId: string, filters?: any): Promise<Notification[]> {
    const params = { ...filters, userId };
    const response = await apiService.get<Notification[]>(`${this.NOTIFICATION_ENDPOINTS.NOTIFICATIONS}/user/${userId}`, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch user notifications');
  }

  // Mark notification as read
  async markNotificationAsRead(id: string): Promise<Notification> {
    const response = await apiService.put<Notification>(`${this.NOTIFICATION_ENDPOINTS.NOTIFICATIONS}/${id}/read`, {});
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to mark notification as read');
  }

  // Mark all notifications as read
  async markAllNotificationsAsRead(userId: string): Promise<void> {
    const response = await apiService.put<void>(`${this.NOTIFICATION_ENDPOINTS.NOTIFICATIONS}/user/${userId}/read-all`, {});
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to mark all notifications as read');
    }
  }

  // Get notification templates
  async getNotificationTemplates(filters?: any): Promise<NotificationTemplate[]> {
    const response = await apiService.get<NotificationTemplate[]>(this.NOTIFICATION_ENDPOINTS.TEMPLATES, filters);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch notification templates');
  }

  // Get notification template by ID
  async getNotificationTemplate(id: string): Promise<NotificationTemplate> {
    const response = await apiService.get<NotificationTemplate>(`${this.NOTIFICATION_ENDPOINTS.TEMPLATES}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch notification template');
  }

  // Create notification template
  async createNotificationTemplate(data: Partial<NotificationTemplate>): Promise<NotificationTemplate> {
    const response = await apiService.post<NotificationTemplate>(this.NOTIFICATION_ENDPOINTS.TEMPLATES, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create notification template');
  }

  // Update notification template
  async updateNotificationTemplate(id: string, data: Partial<NotificationTemplate>): Promise<NotificationTemplate> {
    const response = await apiService.put<NotificationTemplate>(`${this.NOTIFICATION_ENDPOINTS.TEMPLATES}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update notification template');
  }

  // Delete notification template
  async deleteNotificationTemplate(id: string): Promise<void> {
    const response = await apiService.delete(`${this.NOTIFICATION_ENDPOINTS.TEMPLATES}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete notification template');
    }
  }

  // Get notification channels
  async getNotificationChannels(userId: string): Promise<NotificationChannel[]> {
    const response = await apiService.get<NotificationChannel[]>(`${this.NOTIFICATION_ENDPOINTS.CHANNELS}/user/${userId}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch notification channels');
  }

  // Get notification channel by ID
  async getNotificationChannel(id: string): Promise<NotificationChannel> {
    const response = await apiService.get<NotificationChannel>(`${this.NOTIFICATION_ENDPOINTS.CHANNELS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch notification channel');
  }

  // Create notification channel
  async createNotificationChannel(data: Partial<NotificationChannel>): Promise<NotificationChannel> {
    const response = await apiService.post<NotificationChannel>(this.NOTIFICATION_ENDPOINTS.CHANNELS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create notification channel');
  }

  // Update notification channel
  async updateNotificationChannel(id: string, data: Partial<NotificationChannel>): Promise<NotificationChannel> {
    const response = await apiService.put<NotificationChannel>(`${this.NOTIFICATION_ENDPOINTS.CHANNELS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update notification channel');
  }

  // Delete notification channel
  async deleteNotificationChannel(id: string): Promise<void> {
    const response = await apiService.delete(`${this.NOTIFICATION_ENDPOINTS.CHANNELS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete notification channel');
    }
  }

  // Verify notification channel
  async verifyNotificationChannel(id: string, verificationCode: string): Promise<NotificationChannel> {
    const response = await apiService.put<NotificationChannel>(`${this.NOTIFICATION_ENDPOINTS.CHANNELS}/${id}/verify`, { verificationCode });
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to verify notification channel');
  }

  // Get notification preferences
  async getNotificationPreferences(userId: string): Promise<NotificationPreference[]> {
    const response = await apiService.get<NotificationPreference[]>(`${this.NOTIFICATION_ENDPOINTS.PREFERENCES}/user/${userId}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch notification preferences');
  }

  // Update notification preferences
  async updateNotificationPreferences(userId: string, data: Partial<NotificationPreference>): Promise<NotificationPreference> {
    const response = await apiService.put<NotificationPreference>(`${this.NOTIFICATION_ENDPOINTS.PREFERENCES}/user/${userId}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update notification preferences');
  }

  // Get notification schedules
  async getNotificationSchedules(filters?: any): Promise<NotificationSchedule[]> {
    const response = await apiService.get<NotificationSchedule[]>(this.NOTIFICATION_ENDPOINTS.SCHEDULES, filters);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch notification schedules');
  }

  // Get notification schedule by ID
  async getNotificationSchedule(id: string): Promise<NotificationSchedule> {
    const response = await apiService.get<NotificationSchedule>(`${this.NOTIFICATION_ENDPOINTS.SCHEDULES}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch notification schedule');
  }

  // Create notification schedule
  async createNotificationSchedule(data: Partial<NotificationSchedule>): Promise<NotificationSchedule> {
    const response = await apiService.post<NotificationSchedule>(this.NOTIFICATION_ENDPOINTS.SCHEDULES, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create notification schedule');
  }

  // Update notification schedule
  async updateNotificationSchedule(id: string, data: Partial<NotificationSchedule>): Promise<NotificationSchedule> {
    const response = await apiService.put<NotificationSchedule>(`${this.NOTIFICATION_ENDPOINTS.SCHEDULES}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update notification schedule');
  }

  // Delete notification schedule
  async deleteNotificationSchedule(id: string): Promise<void> {
    const response = await apiService.delete(`${this.NOTIFICATION_ENDPOINTS.SCHEDULES}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete notification schedule');
    }
  }

  // Send immediate notification
  async sendImmediateNotification(data: { templateId: string; recipients: string[]; variables?: any }): Promise<any> {
    const response = await apiService.post<any>(`${this.NOTIFICATION_ENDPOINTS.NOTIFICATIONS}/send`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to send immediate notification');
  }

  // Get notification reports
  async getNotificationReports(schoolId?: string, dateFrom?: string, dateTo?: string): Promise<any> {
    const params = { schoolId, dateFrom, dateTo };
    const response = await apiService.get<any>(this.NOTIFICATION_ENDPOINTS.REPORTS, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch notification reports');
  }

  // Get notification statistics
  async getNotificationStats(schoolId?: string): Promise<any> {
    const params = schoolId ? { schoolId } : {};
    const response = await apiService.get<any>(`${this.NOTIFICATION_ENDPOINTS.REPORTS}/stats`, params);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch notification statistics');
  }
}

// Export singleton instance
export const notificationService = new NotificationService();
export default notificationService; 