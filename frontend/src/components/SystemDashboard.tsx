/**
 * System Dashboard component for viewing deployment status, git info, database stats.
 * Replaces the Python HTTP server admin dashboard with React integration.
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_URL } from '../config';

interface SystemStatus {
  project: {
    name: string;
    user: string;
    environment: string;
  };
  git: {
    branch: string;
    commit_hash: string;
    commit_message: string;
    has_uncommitted_changes: boolean;
    status: string;
  };
  database: {
    exists: boolean;
    tables: Array<{ name: string; records: number | string }>;
    total_records: number;
    error?: string;
  };
  timestamp: string;
}

interface TableRecords {
  table_name: string;
  columns: string[];
  records: Array<Record<string, any>>;
  count: number;
}

const SystemDashboard: React.FC = () => {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedTable, setSelectedTable] = useState<string | null>(null);
  const [tableRecords, setTableRecords] = useState<TableRecords | null>(null);
  const [loadingRecords, setLoadingRecords] = useState(false);

  const loadStatus = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.get(`${API_URL}/api/system/status`);
      setStatus(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load system status');
    } finally {
      setLoading(false);
    }
  };

  const loadTableRecords = async (tableName: string) => {
    setLoadingRecords(true);
    setSelectedTable(tableName);
    setTableRecords(null);
    
    try {
      const response = await axios.get(`${API_URL}/api/system/table/${tableName}/records`);
      setTableRecords(response.data);
    } catch (err: any) {
      console.error('Error loading table records:', err);
      setTableRecords(null);
    } finally {
      setLoadingRecords(false);
    }
  };

  useEffect(() => {
    loadStatus();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-500">Loading system status...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-red-50 border border-red-200 text-red-700 p-6 rounded-lg max-w-md">
          <h2 className="font-bold mb-2">Error Loading Dashboard</h2>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!status) return null;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-semibold text-gray-900">System Dashboard</h1>
              <p className="text-gray-500 mt-1">{status.project.name} - {status.project.environment}</p>
            </div>
            <button
              onClick={loadStatus}
              className="px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition border border-gray-200"
            >
              🔄 Refresh
            </button>
          </div>
        </div>

        {/* Top Grid: Project Info and Git Status */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          
          {/* Project Info Card */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-base font-semibold text-gray-900 mb-4">📋 Project Info</h2>
            <div className="space-y-3">
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-sm font-semibold text-gray-600">Project Name:</span>
                <span className="text-sm text-gray-800">{status.project.name}</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-sm font-semibold text-gray-600">Owner:</span>
                <span className="text-sm text-gray-800">{status.project.user}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm font-semibold text-gray-600">Environment:</span>
                <span className="text-sm text-gray-800">{status.project.environment}</span>
              </div>
            </div>
          </div>

          {/* Git Status Card */}
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h2 className="text-base font-semibold text-gray-900 mb-4">🌿 Git Status</h2>
            <div className="space-y-3">
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-sm font-semibold text-gray-600">Branch:</span>
                <span className="text-sm text-gray-800">{status.git.branch}</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-sm font-semibold text-gray-600">Latest Commit:</span>
                <span className="text-sm text-gray-800" title={status.git.commit_message}>
                  {status.git.commit_hash}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm font-semibold text-gray-600">Status:</span>
                <span className="text-sm text-gray-800">{status.git.status}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Database Card (Full Width) */}
        <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
          <h2 className="text-base font-semibold text-gray-900 mb-4">🗄️ PRD Build Database</h2>
          {status.database.exists ? (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div className="flex justify-between items-center pb-2 border-b">
                  <span className="text-sm font-semibold text-gray-600">Total Tables:</span>
                  <span className="text-sm text-gray-800">{status.database.tables.length}</span>
                </div>
                <div className="flex justify-between items-center pb-2 border-b">
                  <span className="text-sm font-semibold text-gray-600">Total Records:</span>
                  <span className="text-sm text-gray-800">{status.database.total_records}</span>
                </div>
              </div>
              
              {/* Table List */}
              <div className="mb-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Tables (click to view records)</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                  {status.database.tables.map((table) => (
                    <button
                      key={table.name}
                      onClick={() => loadTableRecords(table.name)}
                      className={`flex justify-between items-center p-3 rounded-lg transition border ${
                        selectedTable === table.name
                          ? 'bg-indigo-50 border-indigo-500'
                          : 'bg-gray-50 border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      <span className="text-sm font-medium">{table.name}</span>
                      <span className="text-xs bg-indigo-600 text-white px-2 py-1 rounded-full">
                        {table.records}
                      </span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Table Records Display */}
              {loadingRecords && (
                <div className="text-center py-8 text-gray-500">
                  Loading table records...
                </div>
              )}

              {!loadingRecords && tableRecords && (
                <div className="mt-4">
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="text-sm font-semibold text-gray-700">
                      {tableRecords.table_name} - {tableRecords.count} records
                    </h3>
                    <button
                      onClick={() => setSelectedTable(null)}
                      className="text-sm text-gray-500 hover:text-gray-700"
                    >
                      ✕ Close
                    </button>
                  </div>
                  
                  {tableRecords.count === 0 ? (
                    <div className="text-center py-8 text-gray-500 italic">
                      No records in this table
                    </div>
                  ) : (
                    <div className="overflow-x-auto border border-gray-200 rounded-lg">
                      <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                          <tr>
                            {tableRecords.columns.map((column) => (
                              <th
                                key={column}
                                className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider"
                              >
                                {column}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                          {tableRecords.records.map((record, idx) => (
                            <tr key={idx} className="hover:bg-gray-50">
                              {tableRecords.columns.map((column) => (
                                <td
                                  key={column}
                                  className="px-4 py-3 text-sm text-gray-900 whitespace-nowrap"
                                >
                                  {record[column] !== null && record[column] !== undefined
                                    ? String(record[column])
                                    : '-'}
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
            </>
          ) : (
            <div className="text-center text-gray-500 italic py-4">
              Database not initialized yet
            </div>
          )}
        </div>

        {/* Quick Links Card */}
        <div className="bg-white border border-gray-200 rounded-lg p-6">
          <h2 className="text-base font-semibold text-gray-900 mb-4">🔗 Quick Links</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <a href="/" className="text-center p-4 border border-gray-200 rounded-lg hover:border-gray-300 transition">
              <div className="text-2xl mb-2">📝</div>
              <div className="font-medium text-gray-900">PRD Builder</div>
              <div className="text-sm text-gray-500">Create requirements</div>
            </a>
            
            <a href={`${API_URL}/docs`} target="_blank" rel="noopener noreferrer"
               className="text-center p-4 border border-gray-200 rounded-lg hover:border-gray-300 transition">
              <div className="text-2xl mb-2">📡</div>
              <div className="font-medium text-gray-900">API Docs</div>
              <div className="text-sm text-gray-500">FastAPI documentation</div>
            </a>
            
            <a href="/settings" className="text-center p-4 border border-gray-200 rounded-lg hover:border-gray-300 transition">
              <div className="text-2xl mb-2">⚙️</div>
              <div className="font-medium text-gray-900">Settings</div>
              <div className="text-sm text-gray-500">User preferences</div>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SystemDashboard;

