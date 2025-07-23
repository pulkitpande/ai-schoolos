'use client';

import React, { useState } from 'react';
import { useMessages, useCreateMessage, useUpdateMessage, useDeleteMessage } from '../../hooks/useApi';
import { Message, Announcement, Notification as CommNotification, ChatRoom, ChatMessage } from '../../services/communication';
import { Plus, Edit, Trash2, MessageSquare, Bell, Users, Send, FileText, Mail } from 'lucide-react';

interface CommunicationManagementProps {
  schoolId?: string;
}

export default function CommunicationManagement({ schoolId }: CommunicationManagementProps) {
  const [activeTab, setActiveTab] = useState<'messages' | 'announcements' | 'notifications' | 'chat'>('messages');
  const [selectedMessage, setSelectedMessage] = useState<Message | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState<'create' | 'edit'>('create');

  const { data: messages, isLoading: loadingMessages } = useMessages();
  const createMessage = useCreateMessage();
  const updateMessage = useUpdateMessage();
  const deleteMessage = useDeleteMessage();

  const handleCreateMessage = () => {
    setModalType('create');
    setSelectedMessage(null);
    setShowModal(true);
  };

  const handleEditMessage = (message: Message) => {
    setModalType('edit');
    setSelectedMessage(message);
    setShowModal(true);
  };

  const handleDeleteMessage = async (id: string) => {
    if (confirm('Are you sure you want to delete this message?')) {
      await deleteMessage.mutateAsync(id);
    }
  };

  const handleSubmitMessage = async (data: Partial<Message>) => {
    try {
      if (modalType === 'create') {
        await createMessage.mutateAsync(data as any);
      } else {
        await updateMessage.mutateAsync({ id: selectedMessage!.id, ...data } as any);
      }
      setShowModal(false);
    } catch (error) {
      console.error('Error saving message:', error);
    }
  };

  const tabs = [
    { id: 'messages', label: 'Messages', icon: MessageSquare },
    { id: 'announcements', label: 'Announcements', icon: Bell },
    { id: 'notifications', label: 'Notifications', icon: Mail },
    { id: 'chat', label: 'Chat Rooms', icon: Users },
  ];

  const mockStats = {
    totalMessages: 156,
    unreadMessages: 23,
    totalAnnouncements: 45,
    activeChats: 8,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Communication Management</h1>
          <p className="text-gray-600">Manage messages, announcements, and notifications</p>
        </div>
        <button
          onClick={handleCreateMessage}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          New Message
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Messages</p>
              <p className="text-2xl font-bold text-gray-900">{mockStats.totalMessages}</p>
            </div>
            <MessageSquare className="w-8 h-8 text-blue-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Unread Messages</p>
              <p className="text-2xl font-bold text-orange-600">{mockStats.unreadMessages}</p>
            </div>
            <Bell className="w-8 h-8 text-orange-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Announcements</p>
              <p className="text-2xl font-bold text-green-600">{mockStats.totalAnnouncements}</p>
            </div>
            <FileText className="w-8 h-8 text-green-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Active Chats</p>
              <p className="text-2xl font-bold text-purple-600">{mockStats.activeChats}</p>
            </div>
            <Users className="w-8 h-8 text-purple-500" />
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </button>
              );
            })}
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'messages' && (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900">Messages</h3>
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Search messages..."
                    className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              {loadingMessages ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Sender
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Recipient
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Subject
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Status
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Date
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {messages?.messages?.map((message) => (
                        <tr key={message.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center">
                              <div className="flex-shrink-0 h-10 w-10">
                                <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                                  <span className="text-sm font-medium text-blue-600">
                                    {message.senderId?.charAt(0)}
                                  </span>
                                </div>
                              </div>
                              <div className="ml-4">
                                <div className="text-sm font-medium text-gray-900">{message.senderId}</div>
                                <div className="text-sm text-gray-500">Sender</div>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm text-gray-900">{message.recipientId}</div>
                            <div className="text-sm text-gray-500">Recipient</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="text-sm font-medium text-gray-900">{message.subject}</div>
                            <div className="text-sm text-gray-500 truncate max-w-xs">{message.content}</div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span
                              className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                message.status === 'delivered'
                                  ? 'bg-green-100 text-green-800'
                                  : message.status === 'sent'
                                  ? 'bg-yellow-100 text-yellow-800'
                                  : 'bg-gray-100 text-gray-800'
                              }`}
                            >
                              {message.status}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {new Date(message.createdAt || '').toLocaleDateString()}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <div className="flex gap-2">
                              <button
                                onClick={() => handleEditMessage(message)}
                                className="text-blue-600 hover:text-blue-900"
                              >
                                <Edit className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleDeleteMessage(message.id)}
                                className="text-red-600 hover:text-red-900"
                              >
                                <Trash2 className="w-4 h-4" />
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {activeTab === 'announcements' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Announcements</h3>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-blue-800">Announcement management and broadcasting features coming soon...</p>
              </div>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Notifications</h3>
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <p className="text-green-800">Notification system and alert management features coming soon...</p>
              </div>
            </div>
          )}

          {activeTab === 'chat' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Chat Rooms</h3>
              <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <p className="text-purple-800">Real-time chat and messaging features coming soon...</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Message Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {modalType === 'create' ? 'Send Message' : 'Edit Message'}
            </h3>
            <form onSubmit={(e) => { e.preventDefault(); handleSubmitMessage({}); }} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Recipient</label>
                <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option>Select recipient</option>
                  <option>All Teachers</option>
                  <option>All Students</option>
                  <option>All Parents</option>
                  <option>Specific User</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Subject</label>
                <input
                  type="text"
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter message subject"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Message</label>
                <textarea
                  rows={4}
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter your message"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Priority</label>
                <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option>Normal</option>
                  <option>High</option>
                  <option>Urgent</option>
                </select>
              </div>
              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 flex items-center justify-center gap-2"
                >
                  <Send className="w-4 h-4" />
                  {modalType === 'create' ? 'Send' : 'Update'}
                </button>
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 bg-gray-300 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
} 