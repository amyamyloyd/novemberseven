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
  
  // Skip authentication on localhost for development
  const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
  
  if (isLocalhost) {
    return <>{children}</>;
  }
  
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

// Navigation component - Left Sidebar
const Navigation: React.FC = () => {
  // Always show navigation (dev mode)
  return (
    <div className={`w-64 bg-white border-r border-gray-200 flex flex-col transition-all duration-300`}>
      {/* Logo & Collapse Button */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-gray-200">
        <Link to="/" className="text-lg font-semibold text-gray-900">
          SaltAIr
        </Link>
      </div>
      {/* Navigation Links */}
      <nav className="flex-1 p-3 space-y-1">
        <Link to="/" className="flex items-center px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition" title="PRD Builder">
          <span className="text-lg">📝</span>
          <span className="ml-3">PRD Builder</span>
        </Link>
        <Link to="/dashboard" className="flex items-center px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition" title="System Dashboard">
          <span className="text-lg">🎯</span>
          <span className="ml-3">Dashboard</span>
        </Link>
        <Link to="/settings" className="flex items-center px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition" title="Settings">
          <span className="text-lg">⚙️</span>
          <span className="ml-3">Settings</span>
        </Link>
        <Link to="/admin" className="flex items-center px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition" title="Admin Panel">
          <span className="text-lg">👤</span>
          <span className="ml-3">Admin</span>
        </Link>
      </nav>
    </div>
  );
};

// Main App component
const AppContent: React.FC = () => {
  // Always show navigation and all pages for dev (localhost)
  return (
    <div className="h-screen bg-gray-50 flex overflow-hidden">
      <Navigation />
      <div className="flex-1 overflow-auto">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<POCBuilder />} />
          <Route path="/dashboard" element={<SystemDashboard />} />
          <Route path="/settings" element={<UserSettings />} />
          <Route path="/admin" element={<AdminPanel />} />
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