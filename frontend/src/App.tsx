import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import POCBuilder from './components/POCBuilder';
import Login from './components/Login';
import Register from './components/Register';
import UserSettings from './components/UserSettings';
import AdminPanel from './components/AdminPanel';
import SystemDashboard from './components/SystemDashboard';

// Protected route wrapper
const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

// Navigation component - Left Sidebar
const Navigation: React.FC = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const [collapsed, setCollapsed] = React.useState(false);

  if (!isAuthenticated) return null;

  return (
    <div className={`${collapsed ? 'w-16' : 'w-64'} bg-white border-r border-gray-200 flex flex-col transition-all duration-300`}>
      {/* Logo & Collapse Button */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-gray-200">
        {!collapsed && (
          <Link to="/" className="text-lg font-semibold text-gray-900">
            SaltAIr
          </Link>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-2 text-gray-500 hover:bg-gray-50 rounded-lg transition"
          title={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? '→' : '←'}
        </button>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 p-3 space-y-1">
        <Link
          to="/"
          className="flex items-center px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition"
          title="PRD Builder"
        >
          <span className="text-lg">📝</span>
          {!collapsed && <span className="ml-3">PRD Builder</span>}
        </Link>
        
        <Link
          to="/dashboard"
          className="flex items-center px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition"
          title="System Dashboard"
        >
          <span className="text-lg">🎯</span>
          {!collapsed && <span className="ml-3">Dashboard</span>}
        </Link>
        
        <Link
          to="/settings"
          className="flex items-center px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition"
          title="Settings"
        >
          <span className="text-lg">⚙️</span>
          {!collapsed && <span className="ml-3">Settings</span>}
        </Link>
        
        {user?.is_admin && (
          <Link
            to="/admin"
            className="flex items-center px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition"
            title="Admin Panel"
          >
            <span className="text-lg">👤</span>
            {!collapsed && <span className="ml-3">Admin</span>}
          </Link>
        )}
      </nav>

      {/* User Info & Logout */}
      <div className="p-3 border-t border-gray-200">
        <div className="flex items-center justify-between px-3 py-2">
          {!collapsed && (
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">{user?.username}</p>
            </div>
          )}
          <button
            onClick={logout}
            className="p-2 text-gray-500 hover:bg-gray-50 rounded-lg transition"
            title="Logout"
          >
            {collapsed ? '→' : '↪'}
          </button>
        </div>
      </div>
    </div>
  );
};

// Main App component
const AppContent: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="h-screen bg-gray-50 flex overflow-hidden">
      {isAuthenticated && <Navigation />}
      <div className="flex-1 overflow-auto">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <POCBuilder />
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <SystemDashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/settings"
            element={
              <ProtectedRoute>
                <UserSettings />
              </ProtectedRoute>
            }
          />
          <Route
            path="/admin"
            element={
              <ProtectedRoute>
                <AdminPanel />
              </ProtectedRoute>
            }
          />
          <Route path="/tenant_1/poc_idea_1/*" element={<div>Tenant 1 POC 1 - Navigate to <a href="http://localhost:3001" target="_blank" rel="noopener noreferrer">http://localhost:3001</a></div>} />
        </Routes>
      </div>
    </div>
  );
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}

export default App;