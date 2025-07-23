'use client';

import React, { useState } from 'react';
import { useAnalyticsData, useCreateAnalyticsData, useUpdateAnalyticsData, useDeleteAnalyticsData } from '../../hooks/useApi';
import { AnalyticsData, Dashboard, DashboardWidget, Report, PerformanceMetric } from '../../services/analytics';
import { Plus, Edit, Trash2, BarChart3, TrendingUp, PieChart, Activity, FileText } from 'lucide-react';

interface AnalyticsManagementProps {
  schoolId?: string;
}

export default function AnalyticsManagement({ schoolId }: AnalyticsManagementProps) {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'reports' | 'metrics' | 'widgets'>('dashboard');
  const [selectedAnalytics, setSelectedAnalytics] = useState<AnalyticsData | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState<'create' | 'edit'>('create');

  const { data: analytics, isLoading: loadingAnalytics } = useAnalyticsData();
  const createAnalytics = useCreateAnalyticsData();
  const updateAnalytics = useUpdateAnalyticsData();
  const deleteAnalytics = useDeleteAnalyticsData();

  const handleCreateAnalytics = () => {
    setModalType('create');
    setSelectedAnalytics(null);
    setShowModal(true);
  };

  const handleEditAnalytics = (analytics: AnalyticsData) => {
    setModalType('edit');
    setSelectedAnalytics(analytics);
    setShowModal(true);
  };

  const handleDeleteAnalytics = async (id: string) => {
    if (confirm('Are you sure you want to delete this analytics data?')) {
      await deleteAnalytics.mutateAsync(id);
    }
  };

  const handleSubmitAnalytics = async (data: Partial<AnalyticsData>) => {
    try {
      if (modalType === 'create') {
        await createAnalytics.mutateAsync(data as any);
      } else {
        await updateAnalytics.mutateAsync({ id: selectedAnalytics!.id, ...data } as any);
      }
      setShowModal(false);
    } catch (error) {
      console.error('Error saving analytics:', error);
    }
  };

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'reports', label: 'Reports', icon: FileText },
    { id: 'metrics', label: 'Metrics', icon: TrendingUp },
    { id: 'widgets', label: 'Widgets', icon: PieChart },
  ];

  const mockStats = {
    totalStudents: 1250,
    averageAttendance: 94.5,
    totalRevenue: 2500000,
    performanceIndex: 87.2,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analytics Management</h1>
          <p className="text-gray-600">Data analytics, reporting, and performance insights</p>
        </div>
        <button
          onClick={handleCreateAnalytics}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          New Report
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Students</p>
              <p className="text-2xl font-bold text-gray-900">{mockStats.totalStudents}</p>
            </div>
            <BarChart3 className="w-8 h-8 text-blue-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Avg Attendance</p>
              <p className="text-2xl font-bold text-green-600">{mockStats.averageAttendance}%</p>
            </div>
            <TrendingUp className="w-8 h-8 text-green-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Revenue</p>
              <p className="text-2xl font-bold text-purple-600">₹{mockStats.totalRevenue.toLocaleString()}</p>
            </div>
            <Activity className="w-8 h-8 text-purple-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Performance Index</p>
              <p className="text-2xl font-bold text-orange-600">{mockStats.performanceIndex}%</p>
            </div>
            <PieChart className="w-8 h-8 text-orange-500" />
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
          {activeTab === 'dashboard' && (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900">Analytics Dashboard</h3>
                <div className="flex gap-2">
                  <select className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option>Last 30 Days</option>
                    <option>Last 3 Months</option>
                    <option>Last 6 Months</option>
                    <option>Last Year</option>
                  </select>
                </div>
              </div>

              {loadingAnalytics ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {/* Chart Placeholders */}
                  <div className="bg-gray-50 p-6 rounded-lg border">
                    <h4 className="font-semibold text-gray-900 mb-4">Student Performance</h4>
                    <div className="h-48 bg-white rounded border flex items-center justify-center">
                      <p className="text-gray-500">Chart coming soon...</p>
                    </div>
                  </div>
                  <div className="bg-gray-50 p-6 rounded-lg border">
                    <h4 className="font-semibold text-gray-900 mb-4">Attendance Trends</h4>
                    <div className="h-48 bg-white rounded border flex items-center justify-center">
                      <p className="text-gray-500">Chart coming soon...</p>
                    </div>
                  </div>
                  <div className="bg-gray-50 p-6 rounded-lg border">
                    <h4 className="font-semibold text-gray-900 mb-4">Revenue Analysis</h4>
                    <div className="h-48 bg-white rounded border flex items-center justify-center">
                      <p className="text-gray-500">Chart coming soon...</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'reports' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Analytics Reports</h3>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-blue-800">Comprehensive reporting and analytics features coming soon...</p>
              </div>
            </div>
          )}

          {activeTab === 'metrics' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Performance Metrics</h3>
              <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                <p className="text-green-800">Performance metrics and KPI tracking features coming soon...</p>
              </div>
            </div>
          )}

          {activeTab === 'widgets' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Dashboard Widgets</h3>
              <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                <p className="text-purple-800">Customizable dashboard widgets and charts coming soon...</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Analytics Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {modalType === 'create' ? 'Create Report' : 'Edit Report'}
            </h3>
            <form onSubmit={(e) => { e.preventDefault(); handleSubmitAnalytics({}); }} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Report Name</label>
                <input
                  type="text"
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter report name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Report Type</label>
                <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option>Performance Report</option>
                  <option>Attendance Report</option>
                  <option>Financial Report</option>
                  <option>Academic Report</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Date Range</label>
                <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option>Last 30 Days</option>
                  <option>Last 3 Months</option>
                  <option>Last 6 Months</option>
                  <option>Last Year</option>
                  <option>Custom Range</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Format</label>
                <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option>PDF</option>
                  <option>Excel</option>
                  <option>CSV</option>
                  <option>JSON</option>
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