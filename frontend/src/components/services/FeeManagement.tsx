'use client';

import React, { useState } from 'react';
import { useFeeStructures, useFeePayments, useCreateFeePayment, useUpdateFeePayment, useDeleteFeePayment } from '../../hooks/useApi';
import { FeeStructure, FeePayment, FeeDiscount, FinancialRecord } from '../../services/fee';
import { Plus, Edit, Trash2, DollarSign, CreditCard, FileText, Calendar, Users, TrendingUp, AlertCircle } from 'lucide-react';

interface FeeManagementProps {
  schoolId?: string;
}

export default function FeeManagement({ schoolId }: FeeManagementProps) {
  const [activeTab, setActiveTab] = useState<'payments' | 'structures' | 'discounts' | 'records'>('payments');
  const [selectedPayment, setSelectedPayment] = useState<FeePayment | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState<'create' | 'edit'>('create');

  const { data: feeStructures, isLoading: loadingStructures } = useFeeStructures(schoolId);
  const { data: feePayments, isLoading: loadingPayments } = useFeePayments();
  const createPayment = useCreateFeePayment();
  const updatePayment = useUpdateFeePayment();
  const deletePayment = useDeleteFeePayment();

  const handleCreatePayment = () => {
    setModalType('create');
    setSelectedPayment(null);
    setShowModal(true);
  };

  const handleEditPayment = (payment: FeePayment) => {
    setModalType('edit');
    setSelectedPayment(payment);
    setShowModal(true);
  };

  const handleDeletePayment = async (id: string) => {
    if (confirm('Are you sure you want to delete this payment?')) {
      await deletePayment.mutateAsync(id);
    }
  };

  const handleSubmitPayment = async (data: Partial<FeePayment>) => {
    try {
      if (modalType === 'create') {
        await createPayment.mutateAsync(data as any);
      } else {
        await updatePayment.mutateAsync({ id: selectedPayment!.id, ...data } as any);
      }
      setShowModal(false);
    } catch (error) {
      console.error('Error saving payment:', error);
    }
  };

  const tabs = [
    { id: 'payments', label: 'Fee Payments', icon: CreditCard },
    { id: 'structures', label: 'Fee Structures', icon: FileText },
    { id: 'discounts', label: 'Discounts', icon: TrendingUp },
    { id: 'records', label: 'Financial Records', icon: DollarSign },
  ];

  const mockStats = {
    totalRevenue: 125000,
    pendingPayments: 15000,
    totalStudents: 450,
    monthlyGrowth: 12.5,
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Fee Management</h1>
          <p className="text-gray-600">Manage fee structures, payments, and financial records</p>
        </div>
        <button
          onClick={handleCreatePayment}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
        >
          <Plus className="w-4 h-4" />
          New Payment
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Revenue</p>
              <p className="text-2xl font-bold text-gray-900">₹{mockStats.totalRevenue.toLocaleString()}</p>
            </div>
            <DollarSign className="w-8 h-8 text-green-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Pending Payments</p>
              <p className="text-2xl font-bold text-orange-600">₹{mockStats.pendingPayments.toLocaleString()}</p>
            </div>
            <AlertCircle className="w-8 h-8 text-orange-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Students</p>
              <p className="text-2xl font-bold text-gray-900">{mockStats.totalStudents}</p>
            </div>
            <Users className="w-8 h-8 text-blue-500" />
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Monthly Growth</p>
              <p className="text-2xl font-bold text-green-600">+{mockStats.monthlyGrowth}%</p>
            </div>
            <TrendingUp className="w-8 h-8 text-green-500" />
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
          {activeTab === 'payments' && (
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900">Fee Payments</h3>
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Search payments..."
                    className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>

              {loadingPayments ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Student
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Fee Type
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Amount
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
                      {feePayments?.payments?.map((payment) => (
                        <tr key={payment.id} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center">
                              <div className="flex-shrink-0 h-10 w-10">
                                <div className="h-10 w-10 rounded-full bg-blue-100 flex items-center justify-center">
                                  <span className="text-sm font-medium text-blue-600">
                                    {payment.student_name?.charAt(0)}
                                  </span>
                                </div>
                              </div>
                              <div className="ml-4">
                                <div className="text-sm font-medium text-gray-900">{payment.student_name}</div>
                                <div className="text-sm text-gray-500">{payment.student_id}</div>
                              </div>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {payment.fee_type}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                            ₹{payment.amount?.toLocaleString()}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <span
                              className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${
                                payment.status === 'paid'
                                  ? 'bg-green-100 text-green-800'
                                  : payment.status === 'pending'
                                  ? 'bg-yellow-100 text-yellow-800'
                                  : 'bg-red-100 text-red-800'
                              }`}
                            >
                              {payment.status}
                            </span>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {new Date(payment.payment_date || '').toLocaleDateString()}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                            <div className="flex gap-2">
                              <button
                                onClick={() => handleEditPayment(payment)}
                                className="text-blue-600 hover:text-blue-900"
                              >
                                <Edit className="w-4 h-4" />
                              </button>
                              <button
                                onClick={() => handleDeletePayment(payment.id)}
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

          {activeTab === 'structures' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Fee Structures</h3>
              {loadingStructures ? (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {feeStructures?.map((structure) => (
                    <div key={structure.id} className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="font-semibold text-gray-900">{structure.name}</h4>
                      <p className="text-sm text-gray-600">{structure.description}</p>
                      <div className="mt-2">
                        <span className="text-lg font-bold text-blue-600">₹{structure.amount?.toLocaleString()}</span>
                        <span className="text-sm text-gray-500 ml-2">per {structure.frequency}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === 'discounts' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Fee Discounts</h3>
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <p className="text-yellow-800">Discount management features coming soon...</p>
              </div>
            </div>
          )}

          {activeTab === 'records' && (
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Financial Records</h3>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-blue-800">Financial records and reporting features coming soon...</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Payment Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {modalType === 'create' ? 'Create Payment' : 'Edit Payment'}
            </h3>
            <form onSubmit={(e) => { e.preventDefault(); handleSubmitPayment({}); }} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Student</label>
                <input
                  type="text"
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Select student"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Fee Type</label>
                <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option>Tuition Fee</option>
                  <option>Transport Fee</option>
                  <option>Library Fee</option>
                  <option>Other</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Amount</label>
                <input
                  type="number"
                  className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter amount"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Status</label>
                <select className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                  <option>paid</option>
                  <option>pending</option>
                  <option>overdue</option>
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