/**
 * User Settings component for viewing configuration (API keys, git repo, preferences).
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_URL } from '../config';

interface ConfigData {
  user_identity: {
    user_name: string;
    project_name: string;
  };
  api_keys: {
    openai_api_key?: string;
    anthropic_api_key?: string;
    langsmith_api_key?: string;
  };
  git_deployment: {
    github_repo_url: string;
    deployment_branch: string;
  };
  preferences: {
    use_prd_tool: boolean;
    auto_deploy: boolean;
    openai_model_preference: string;
    timezone: string;
  };
  setup_complete: boolean;
}

const UserSettings: React.FC = () => {
  const [config, setConfig] = useState<ConfigData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [copiedField, setCopiedField] = useState<string | null>(null);

  const loadConfig = async () => {
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.get(`${API_URL}/api/settings/config`);
      setConfig(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load configuration');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string, fieldName: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopiedField(fieldName);
      setTimeout(() => setCopiedField(null), 2000);
    });
  };

  useEffect(() => {
    loadConfig();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-500">Loading configuration...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-red-50 border border-red-200 text-red-700 p-6 rounded-lg max-w-md">
          <h2 className="font-bold mb-2">Error Loading Configuration</h2>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!config) return null;

  const CopyButton: React.FC<{ text: string; fieldName: string }> = ({ text, fieldName }) => (
    <button
      onClick={() => copyToClipboard(text, fieldName)}
      className="ml-2 px-3 py-1 text-xs bg-indigo-600 hover:bg-indigo-700 text-white rounded transition"
      title="Copy to clipboard"
    >
      {copiedField === fieldName ? '✓ Copied' : '📋 Copy'}
    </button>
  );

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-semibold text-gray-900">Configuration Settings</h1>
          <button
            onClick={loadConfig}
            className="px-4 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition border border-gray-200"
          >
            🔄 Refresh
          </button>
        </div>
        
        <div className="space-y-6">
          {/* Project Identity */}
          <div className="bg-white border border-gray-200 p-6 rounded-lg">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">👤 Project Identity</h2>
            <div className="space-y-3">
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-sm font-semibold text-gray-600">User Name:</span>
                <span className="text-sm text-gray-800">{config.user_identity.user_name}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm font-semibold text-gray-600">Project Name:</span>
                <span className="text-sm text-gray-800">{config.user_identity.project_name}</span>
              </div>
            </div>
          </div>

          {/* API Keys */}
          <div className="bg-white border border-gray-200 p-6 rounded-lg">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">🔑 API Keys</h2>
            <div className="space-y-4">
              {config.api_keys.openai_api_key && (
                <div>
                  <label className="block text-sm font-semibold text-gray-600 mb-1">OpenAI API Key</label>
                  <div className="flex items-center">
                    <code className="flex-1 px-4 py-2 bg-gray-50 border border-gray-200 rounded text-xs font-mono text-gray-700 overflow-x-auto">
                      {config.api_keys.openai_api_key}
                    </code>
                    <CopyButton text={config.api_keys.openai_api_key} fieldName="openai" />
                  </div>
                </div>
              )}
              
              {config.api_keys.anthropic_api_key && (
                <div>
                  <label className="block text-sm font-semibold text-gray-600 mb-1">Anthropic API Key</label>
                  <div className="flex items-center">
                    <code className="flex-1 px-4 py-2 bg-gray-50 border border-gray-200 rounded text-xs font-mono text-gray-700 overflow-x-auto">
                      {config.api_keys.anthropic_api_key}
                    </code>
                    <CopyButton text={config.api_keys.anthropic_api_key} fieldName="anthropic" />
                  </div>
                </div>
              )}
              
              {config.api_keys.langsmith_api_key && (
                <div>
                  <label className="block text-sm font-semibold text-gray-600 mb-1">LangSmith API Key</label>
                  <div className="flex items-center">
                    <code className="flex-1 px-4 py-2 bg-gray-50 border border-gray-200 rounded text-xs font-mono text-gray-700 overflow-x-auto">
                      {config.api_keys.langsmith_api_key}
                    </code>
                    <CopyButton text={config.api_keys.langsmith_api_key} fieldName="langsmith" />
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Git Deployment */}
          <div className="bg-white border border-gray-200 p-6 rounded-lg">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">🌿 Git Deployment</h2>
            <div className="space-y-3">
              <div>
                <label className="block text-sm font-semibold text-gray-600 mb-1">GitHub Repository URL</label>
                <div className="flex items-center">
                  <code className="flex-1 px-4 py-2 bg-gray-50 border border-gray-200 rounded text-xs font-mono text-gray-700 overflow-x-auto">
                    {config.git_deployment.github_repo_url}
                  </code>
                  <CopyButton text={config.git_deployment.github_repo_url} fieldName="github_url" />
                </div>
              </div>
              <div className="flex justify-between items-center pt-2 border-t">
                <span className="text-sm font-semibold text-gray-600">Deployment Branch:</span>
                <span className="text-sm text-gray-800">{config.git_deployment.deployment_branch}</span>
              </div>
            </div>
          </div>

          {/* Preferences */}
          <div className="bg-white border border-gray-200 p-6 rounded-lg">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">⚙️ Preferences</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-sm font-semibold text-gray-600">Use PRD Tool:</span>
                <span className="text-sm text-gray-800">{config.preferences.use_prd_tool ? 'Yes' : 'No'}</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-sm font-semibold text-gray-600">Auto Deploy:</span>
                <span className="text-sm text-gray-800">{config.preferences.auto_deploy ? 'Yes' : 'No'}</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-sm font-semibold text-gray-600">OpenAI Model:</span>
                <span className="text-sm text-gray-800">{config.preferences.openai_model_preference}</span>
              </div>
              <div className="flex justify-between items-center pb-2 border-b">
                <span className="text-sm font-semibold text-gray-600">Timezone:</span>
                <span className="text-sm text-gray-800">{config.preferences.timezone}</span>
              </div>
            </div>
          </div>

          {/* Info Notice */}
          <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg">
            <p className="text-sm text-blue-700">
              <strong>Note:</strong> These settings are read-only and loaded from <code className="bg-blue-100 px-1 py-0.5 rounded">user_config.json</code>. 
              To modify these values, update the configuration file directly or re-run the setup process.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserSettings;

