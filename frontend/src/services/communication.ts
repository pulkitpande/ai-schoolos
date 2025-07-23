import { apiService, ApiResponse } from './api';

// Communication Types
export interface Message {
  id: string;
  senderId: string;
  recipientId: string;
  subject: string;
  content: string;
  messageType: 'internal' | 'announcement' | 'notification' | 'alert';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  status: 'sent' | 'delivered' | 'read' | 'archived';
  readAt?: string;
  attachments?: string[];
  isActive: boolean;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface Announcement {
  id: string;
  title: string;
  content: string;
  authorId: string;
  targetAudience: 'all' | 'students' | 'teachers' | 'parents' | 'staff' | 'admin';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  status: 'draft' | 'published' | 'archived';
  publishDate: string;
  expiryDate?: string;
  attachments?: string[];
  isActive: boolean;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

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
  isActive: boolean;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface ChatRoom {
  id: string;
  name: string;
  description?: string;
  roomType: 'private' | 'group' | 'class' | 'department';
  participants: string[];
  createdBy: string;
  isActive: boolean;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface ChatMessage {
  id: string;
  roomId: string;
  senderId: string;
  content: string;
  messageType: 'text' | 'file' | 'image' | 'audio' | 'video';
  attachments?: string[];
  status: 'sent' | 'delivered' | 'read';
  readBy: string[];
  isActive: boolean;
  schoolId: string;
  createdAt: string;
  updatedAt: string;
}

export interface CommunicationFilters {
  messageType?: string;
  priority?: string;
  status?: string;
  senderId?: string;
  recipientId?: string;
  dateFrom?: string;
  dateTo?: string;
  schoolId?: string;
}

export interface CommunicationListResponse {
  messages: Message[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Communication Service class
export class CommunicationService {
  private readonly COMMUNICATION_ENDPOINTS = {
    MESSAGES: '/api/v1/communications/messages',
    ANNOUNCEMENTS: '/api/v1/communications/announcements',
    NOTIFICATIONS: '/api/v1/communications/notifications',
    CHAT_ROOMS: '/api/v1/communications/chat-rooms',
    CHAT_MESSAGES: '/api/v1/communications/chat-messages',
    REPORTS: '/api/v1/communications/reports',
  };

  // Get messages
  async getMessages(filters?: CommunicationFilters): Promise<CommunicationListResponse> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<CommunicationListResponse>(
      `${this.COMMUNICATION_ENDPOINTS.MESSAGES}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch messages');
  }

  // Get message by ID
  async getMessage(id: string): Promise<Message> {
    const response = await apiService.get<Message>(`${this.COMMUNICATION_ENDPOINTS.MESSAGES}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch message');
  }

  // Create message
  async createMessage(data: Partial<Message>): Promise<Message> {
    const response = await apiService.post<Message>(this.COMMUNICATION_ENDPOINTS.MESSAGES, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create message');
  }

  // Update message
  async updateMessage(id: string, data: Partial<Message>): Promise<Message> {
    const response = await apiService.put<Message>(`${this.COMMUNICATION_ENDPOINTS.MESSAGES}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update message');
  }

  // Delete message
  async deleteMessage(id: string): Promise<void> {
    const response = await apiService.delete(`${this.COMMUNICATION_ENDPOINTS.MESSAGES}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete message');
    }
  }

  // Get user messages
  async getUserMessages(userId: string, filters?: any): Promise<Message[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<Message[]>(
      `${this.COMMUNICATION_ENDPOINTS.MESSAGES}/user/${userId}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch user messages');
  }

  // Mark message as read
  async markMessageAsRead(id: string): Promise<Message> {
    const response = await apiService.put<Message>(`${this.COMMUNICATION_ENDPOINTS.MESSAGES}/${id}/read`, {});
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to mark message as read');
  }

  // Get announcements
  async getAnnouncements(filters?: any): Promise<Announcement[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<Announcement[]>(
      `${this.COMMUNICATION_ENDPOINTS.ANNOUNCEMENTS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch announcements');
  }

  // Get announcement by ID
  async getAnnouncement(id: string): Promise<Announcement> {
    const response = await apiService.get<Announcement>(`${this.COMMUNICATION_ENDPOINTS.ANNOUNCEMENTS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch announcement');
  }

  // Create announcement
  async createAnnouncement(data: Partial<Announcement>): Promise<Announcement> {
    const response = await apiService.post<Announcement>(this.COMMUNICATION_ENDPOINTS.ANNOUNCEMENTS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create announcement');
  }

  // Update announcement
  async updateAnnouncement(id: string, data: Partial<Announcement>): Promise<Announcement> {
    const response = await apiService.put<Announcement>(`${this.COMMUNICATION_ENDPOINTS.ANNOUNCEMENTS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update announcement');
  }

  // Delete announcement
  async deleteAnnouncement(id: string): Promise<void> {
    const response = await apiService.delete(`${this.COMMUNICATION_ENDPOINTS.ANNOUNCEMENTS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete announcement');
    }
  }

  // Get notifications
  async getNotifications(userId?: string, filters?: any): Promise<Notification[]> {
    const params = new URLSearchParams();
    
    if (userId) {
      params.append('userId', userId);
    }
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<Notification[]>(
      `${this.COMMUNICATION_ENDPOINTS.NOTIFICATIONS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch notifications');
  }

  // Get notification by ID
  async getNotification(id: string): Promise<Notification> {
    const response = await apiService.get<Notification>(`${this.COMMUNICATION_ENDPOINTS.NOTIFICATIONS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch notification');
  }

  // Create notification
  async createNotification(data: Partial<Notification>): Promise<Notification> {
    const response = await apiService.post<Notification>(this.COMMUNICATION_ENDPOINTS.NOTIFICATIONS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create notification');
  }

  // Update notification
  async updateNotification(id: string, data: Partial<Notification>): Promise<Notification> {
    const response = await apiService.put<Notification>(`${this.COMMUNICATION_ENDPOINTS.NOTIFICATIONS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update notification');
  }

  // Delete notification
  async deleteNotification(id: string): Promise<void> {
    const response = await apiService.delete(`${this.COMMUNICATION_ENDPOINTS.NOTIFICATIONS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete notification');
    }
  }

  // Mark notification as read
  async markNotificationAsRead(id: string): Promise<Notification> {
    const response = await apiService.put<Notification>(`${this.COMMUNICATION_ENDPOINTS.NOTIFICATIONS}/${id}/read`, {});
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to mark notification as read');
  }

  // Get chat rooms
  async getChatRooms(userId?: string): Promise<ChatRoom[]> {
    const params = new URLSearchParams();
    
    if (userId) {
      params.append('userId', userId);
    }

    const response = await apiService.get<ChatRoom[]>(
      `${this.COMMUNICATION_ENDPOINTS.CHAT_ROOMS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch chat rooms');
  }

  // Get chat room by ID
  async getChatRoom(id: string): Promise<ChatRoom> {
    const response = await apiService.get<ChatRoom>(`${this.COMMUNICATION_ENDPOINTS.CHAT_ROOMS}/${id}`);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch chat room');
  }

  // Create chat room
  async createChatRoom(data: Partial<ChatRoom>): Promise<ChatRoom> {
    const response = await apiService.post<ChatRoom>(this.COMMUNICATION_ENDPOINTS.CHAT_ROOMS, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create chat room');
  }

  // Update chat room
  async updateChatRoom(id: string, data: Partial<ChatRoom>): Promise<ChatRoom> {
    const response = await apiService.put<ChatRoom>(`${this.COMMUNICATION_ENDPOINTS.CHAT_ROOMS}/${id}`, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to update chat room');
  }

  // Delete chat room
  async deleteChatRoom(id: string): Promise<void> {
    const response = await apiService.delete(`${this.COMMUNICATION_ENDPOINTS.CHAT_ROOMS}/${id}`);
    
    if (!response.success) {
      throw new Error(response.message || 'Failed to delete chat room');
    }
  }

  // Get chat messages
  async getChatMessages(roomId: string, filters?: any): Promise<ChatMessage[]> {
    const params = new URLSearchParams();
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          params.append(key, value.toString());
        }
      });
    }

    const response = await apiService.get<ChatMessage[]>(
      `${this.COMMUNICATION_ENDPOINTS.CHAT_MESSAGES}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch chat messages');
  }

  // Create chat message
  async createChatMessage(data: Partial<ChatMessage>): Promise<ChatMessage> {
    const response = await apiService.post<ChatMessage>(this.COMMUNICATION_ENDPOINTS.CHAT_MESSAGES, data);
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to create chat message');
  }

  // Mark chat message as read
  async markChatMessageAsRead(messageId: string, userId: string): Promise<ChatMessage> {
    const response = await apiService.put<ChatMessage>(`${this.COMMUNICATION_ENDPOINTS.CHAT_MESSAGES}/${messageId}/read`, { userId });
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to mark chat message as read');
  }

  // Get communication reports
  async getCommunicationReports(schoolId?: string, dateFrom?: string, dateTo?: string): Promise<any> {
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
      `${this.COMMUNICATION_ENDPOINTS.REPORTS}?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch communication reports');
  }

  // Get communication stats
  async getCommunicationStats(schoolId?: string): Promise<any> {
    const params = new URLSearchParams();
    
    if (schoolId) {
      params.append('schoolId', schoolId);
    }

    const response = await apiService.get<any>(
      `${this.COMMUNICATION_ENDPOINTS.REPORTS}/stats?${params.toString()}`
    );
    
    if (response.success && response.data) {
      return response.data;
    }
    
    throw new Error(response.message || 'Failed to fetch communication stats');
  }
}

// Export singleton instance
export const communicationService = new CommunicationService();
export default communicationService; 