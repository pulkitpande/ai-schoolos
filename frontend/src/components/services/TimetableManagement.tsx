'use client';

import React, { useState } from 'react';
import { useTimetables, useCreateTimetable, useUpdateTimetable, useDeleteTimetable } from '../../hooks/useApi';
import { Timetable, TimetableSlot, Room, Schedule } from '../../services/timetable';
import { Plus, Edit, Trash2, Calendar, Clock, MapPin, Users, BookOpen, BarChart3 } from 'lucide-react';

interface TimetableManagementProps {
  schoolId?: string;
}

export default function TimetableManagement({ schoolId }: TimetableManagementProps) {
  const [activeTab, setActiveTab] = useState<'schedule' | 'rooms' | 'classes' | 'conflicts'>('schedule');
  const [selectedTimetable, setSelectedTimetable] = useState<Timetable | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState<'create' | 'edit'>('create');

  const { data: timetables, isLoading: loadingTimetables } = useTimetables();
  const createTimetable = useCreateTimetable();
  const updateTimetable = useUpdateTimetable();
  const deleteTimetable = useDeleteTimetable();

  const handleCreateTimetable = () => {
    setModalType('create');
    setSelectedTimetable(null);
    setShowModal(true);
  };

  const handleEditTimetable = (timetable: Timetable) => {
    setModalType('edit');
    setSelectedTimetable(timetable);
    setShowModal(true);
  };

  const handleDeleteTimetable = async (id: string) => {
    if (confirm('Are you sure you want to delete this timetable?')) {
      await deleteTimetable.mutateAsync(id);
    }
  };

  const handleSubmitTimetable = async (data: Partial<Timetable>) => {
    try {
      if (modalType === 'create') {
        await createTimetable.mutateAsync(data as any);
      } else {
        await updateTimetable.mutateAsync({ id: selectedTimetable!.id, ...data } as any);
      }
      setShowModal(false);
    } catch (error) {
      console.error('Error saving timetable:', error);
    }
  };

  const tabs = [
    { id: 'schedule', label: 'Schedule', icon: Calendar },
    { id: 'rooms', label: 'Rooms', icon: MapPin },
    { id: 'classes', label: 'Classes', icon: Users },
    { id: 'conflicts', label: 'Conflicts', icon: BarChart3 },
  ];

  const mockStats = {
    totalClasses: 24,
    totalRooms: 12,
    totalTeachers: 35,
    conflicts: 2,
  };

  const timeSlots = [
    '8:00 AM - 9:00 AM',
    '9:00 AM - 10:00 AM',
    '10:00 AM - 11:00 AM',
    '11:00 AM - 12:00 PM',
    '12:00 PM - 1:00 PM',
    '1:00 PM - 2:00 PM',
    '2:00 PM - 3:00 PM',
    '3:00 PM - 4:00 PM',
  ];

  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Timetable Management</h1>
          <p className="text-gray-600">Manage class schedules, room allocation, and timetables</p>
        </div>
        <button
          onClick={handleCreateTimetable}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          New Schedule
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Classes</p>
              <p className="text-2xl font-bold text-gray-900">{mockStats.totalClasses}</p>
            </div>
            <BookOpen className="w-8 h-8 text-blue-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Rooms</p>
              <p className="text-2xl font-bold text-green-600">{mockStats.totalRooms}</p>
            </div>
            <MapPin className="w-8 h-8 text-green-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Teachers</p>
              <p className="text-2xl font-bold text-purple-600">{mockStats.totalTeachers}</p>
            </div>
            <Users className="w-8 h-8 text-purple-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Conflicts</p>
              <p className="text-2xl font-bold text-red-600">{mockStats.conflicts}</p>
            </div>
            <BarChart3 className="w-8 h-8 text-red-500" />
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
          {activeTab === 'schedule' && (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900">Class Schedule</h3>
                <div className="flex gap-2">
                  <select className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option>All Classes</option>
                    <option>Class 10A</option>
                    <option>Class 10B</option>
                    <option>Class 11A</option>
                  </select>
                </div>
              </div>

              {loadingTimetables ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Time
                        </th>
                        {days.map((day) => (
                          <th key={day} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            {day}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {timeSlots.map((timeSlot, index) => (
                        <tr key={index} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            {timeSlot}
                          </td>
                          {days.map((day) => (
                            <td key={day} className="px-6 py-4 whitespace-nowrap">
                              <div className="bg-blue-50 border border-blue-200 rounded p-2">
                                <div className="text-sm font-medium text-blue-900">Mathematics</div>
                                <div className="text-xs text-blue-600">Room 101 - Mr. Smith</div>
                              </div>
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {activeTab === 'rooms' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Room Management</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Array.from({ length: 12 }, (_, i) => (
                  <div key={i} className="bg-gray-50 p-4 rounded-lg border">
                    <div className="flex items-center justify-between">
                      <div>
                        <h4 className="font-semibold text-gray-900">Room {i + 101}</h4>
                        <p className="text-sm text-gray-600">Capacity: 30 students</p>
                      </div>
                      <div className="text-right">
                        <span className="inline-flex px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                          Available
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'classes' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Class Timetables</h3>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-blue-800">Class-specific timetable views coming soon...</p>
              </div>
            </div>
          )}

          {activeTab === 'conflicts' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Schedule Conflicts</h3>
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-800">Conflict detection and resolution features coming soon...</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Timetable Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {modalType === 'create' ? 'Create Schedule' : 'Edit Schedule'}
            </h3>
            <form onSubmit={(e) => { e.preventDefault(); handleSubmitTimetable({}); }} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Class</label>
                <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option>Class 10A</option>
                  <option>Class 10B</option>
                  <option>Class 11A</option>
                  <option>Class 11B</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Subject</label>
                <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option>Mathematics</option>
                  <option>Science</option>
                  <option>English</option>
                  <option>History</option>
                  <option>Geography</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Teacher</label>
                <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option>Mr. Smith</option>
                  <option>Ms. Johnson</option>
                  <option>Mr. Davis</option>
                  <option>Ms. Wilson</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Room</label>
                <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option>Room 101</option>
                  <option>Room 102</option>
                  <option>Room 103</option>
                  <option>Room 104</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Time Slot</label>
                <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  {timeSlots.map((slot) => (
                    <option key={slot}>{slot}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Day</label>
                <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  {days.map((day) => (
                    <option key={day}>{day}</option>
                  ))}
                </select>
              </div>
              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
                >
                  {modalType === 'create' ? 'Create' : 'Update'}
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