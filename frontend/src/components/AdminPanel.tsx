/**
 * Admin Panel component for user management (admin only).
 * 40/60 layout: Left panel for actions, Right panel for user list and messages.
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { getAuthHeader } from '../utils/auth';
import { useNavigate } from 'react-router-dom';
import { API_URL } from '../config';

interface User {
  id: number;
  username: string;
  email: string | null;
  is_admin: boolean;
  created_at: string;
  updated_at: string;
}

const AdminPanel: React.FC = () => {
  const { isAdmin } = useAuth();
  const navigate = useNavigate();
  
  // Redirect if not admin
  useEffect(() => {
    if (!isAdmin) {
      navigate('/');
    }
  }, [isAdmin, navigate]);

  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Add user form state
  const [newUsername, setNewUsername] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [newEmail, setNewEmail] = useState('');
  const [newIsAdmin, setNewIsAdmin] = useState(false);
  const [addLoading, setAddLoading] = useState(false);

  // Reset password state
  const [resetUserId, setResetUserId] = useState<number | null>(null);
  const [resetPassword, setResetPassword] = useState('');
  const [resetLoading, setResetLoading] = useState(false);

  // Load users on mount
  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get(`${API_URL}/api/admin/users`, {
        headers: getAuthHeader(),
      });
      if (response.data.success) {
        setUsers(response.data.users);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  const handleAddUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (newPassword.length < 4) {
      setError('Password must be at least 4 characters long');
      return;
    }

    setAddLoading(true);

    try {
      const response = await axios.post(
        `${API_URL}/api/admin/users`,
        {
          username: newUsername,
          password: newPassword,
          email: newEmail || null,
          is_admin: newIsAdmin,
        },
        { headers: getAuthHeader() }
      );

      if (response.data.success) {
        setSuccess(`User '${newUsername}' created successfully`);
        setNewUsername('');
        setNewPassword('');
        setNewEmail('');
        setNewIsAdmin(false);
        loadUsers();
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create user');
    } finally {
      setAddLoading(false);
    }
  };

  const handleDeleteUser = async (userId: number, username: string) => {
    if (!window.confirm(`Are you sure you want to delete user '${username}'?`)) {
      return;
    }

    setError('');
    setSuccess('');

    try {
      const response = await axios.delete(`${API_URL}/api/admin/users/${userId}`, {
        headers: getAuthHeader(),
      });

      if (response.data.success) {
        setSuccess(response.data.message);
        loadUsers();
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete user');
    }
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!resetUserId) return;

    setError('');
    setSuccess('');

    if (resetPassword.length < 4) {
      setError('Password must be at least 4 characters long');
      return;
    }

    setResetLoading(true);

    try {
      const response = await axios.put(
        `${API_URL}/api/admin/users/${resetUserId}/reset-password`,
        { new_password: resetPassword },
        { headers: getAuthHeader() }
      );

      if (response.data.success) {
        setSuccess(response.data.message);
        setResetUserId(null);
        setResetPassword('');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to reset password');
    } finally {
      setResetLoading(false);
    }
  };

  if (!isAdmin) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-6">
        <h1 className="text-2xl font-semibold text-gray-900 mb-8">Admin Panel</h1>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
          {/* Left Panel - 40% (2/5) - Actions */}
          <div className="md:col-span-2 space-y-6">
            {/* Add User Form */}
            <div className="bg-white border border-gray-200 p-6 rounded-lg">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Add New User</h2>
              <form onSubmit={handleAddUser} className="space-y-4">
                <div>
                  <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
                    Username
                  </label>
                  <input
                    id="username"
                    type="text"
                    required
                    minLength={3}
                    maxLength={50}
                    value={newUsername}
                    onChange={(e) => setNewUsername(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                    placeholder="Enter username"
                  />
                </div>

                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                    Password
                  </label>
                  <input
                    id="password"
                    type="password"
                    required
                    minLength={4}
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                    placeholder="Minimum 4 characters"
                  />
                </div>

                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                    Email <span className="text-gray-400 font-normal">(optional)</span>
                  </label>
                  <input
                    id="email"
                    type="email"
                    value={newEmail}
                    onChange={(e) => setNewEmail(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                    placeholder="user@example.com"
                  />
                </div>

                <div className="flex items-center pt-2">
                  <input
                    id="isAdmin"
                    type="checkbox"
                    checked={newIsAdmin}
                    onChange={(e) => setNewIsAdmin(e.target.checked)}
                    className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <label htmlFor="isAdmin" className="ml-2 text-sm text-gray-700">
                    Grant admin privileges
                  </label>
                </div>

                <button
                  type="submit"
                  disabled={addLoading}
                  className="w-full py-3 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition disabled:opacity-50"
                >
                  {addLoading ? 'Adding...' : 'Add User'}
                </button>
              </form>
            </div>

            {/* Reset Password Form */}
            {resetUserId && (
              <div className="bg-white border border-gray-200 p-6 rounded-lg">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Reset Password</h2>
                <form onSubmit={handleResetPassword} className="space-y-4">
                  <div>
                    <label htmlFor="resetPassword" className="block text-sm font-medium text-gray-700 mb-1">
                      New Password
                    </label>
                    <input
                      id="resetPassword"
                      type="password"
                      required
                      minLength={4}
                      value={resetPassword}
                      onChange={(e) => setResetPassword(e.target.value)}
                      className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                      placeholder="Minimum 4 characters"
                    />
                  </div>

                  <div className="flex space-x-3">
                    <button
                      type="submit"
                      disabled={resetLoading}
                      className="flex-1 py-3 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition disabled:opacity-50"
                    >
                      {resetLoading ? 'Resetting...' : 'Reset Password'}
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setResetUserId(null);
                        setResetPassword('');
                      }}
                      className="flex-1 py-3 px-4 border border-gray-200 text-gray-700 hover:bg-gray-50 rounded-lg transition"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            )}
          </div>

          {/* Right Panel - 60% (3/5) - User List */}
          <div className="md:col-span-3">
            <div className="bg-white border border-gray-200 p-6 rounded-lg">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Users</h2>
                <button
                  onClick={loadUsers}
                  className="px-4 py-2 text-gray-700 hover:bg-gray-50 border border-gray-200 rounded-lg transition text-sm"
                >
                  Refresh
                </button>
              </div>

              {error && (
                <div className="mb-4 bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg text-sm">
                  {error}
                </div>
              )}

              {success && (
                <div className="mb-4 bg-green-50 border border-green-200 text-green-600 px-4 py-3 rounded-lg text-sm">
                  {success}
                </div>
              )}

              {loading ? (
                <div className="text-center py-8 text-gray-500">Loading users...</div>
              ) : users.length === 0 ? (
                <div className="text-center py-8 text-gray-500">No users found</div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          ID
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Username
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Email
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Role
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Created
                        </th>
                        <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {users.map((user) => (
                        <tr key={user.id} className="hover:bg-gray-50">
                          <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">
                            {user.id}
                          </td>
                          <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                            {user.username}
                          </td>
                          <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                            {user.email || '-'}
                          </td>
                          <td className="px-4 py-3 whitespace-nowrap text-sm">
                            {user.is_admin ? (
                              <span className="px-2 py-1 text-xs font-medium rounded-full bg-indigo-50 text-indigo-700">
                                Admin
                              </span>
                            ) : (
                              <span className="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-700">
                                User
                              </span>
                            )}
                          </td>
                          <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">
                            {new Date(user.created_at).toLocaleDateString()}
                          </td>
                          <td className="px-4 py-3 whitespace-nowrap text-sm space-x-3">
                            <button
                              onClick={() => setResetUserId(user.id)}
                              className="text-indigo-600 hover:text-indigo-700 font-medium"
                            >
                              Reset
                            </button>
                            <button
                              onClick={() => handleDeleteUser(user.id, user.username)}
                              className="text-red-600 hover:text-red-700 font-medium"
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
        </div>
      </div>
    </div>
  );
};

export default AdminPanel;

