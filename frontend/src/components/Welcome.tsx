import React from 'react';

interface WelcomeProps {
  userName: string;
  projectName: string;
  githubUrl: string;
}

const Welcome: React.FC<WelcomeProps> = ({ userName, projectName, githubUrl }) => {
  // Detect environment
  const environment = window.location.hostname.includes('-dev') || 
                      window.location.hostname.includes('localhost') 
                      ? 'Development' 
                      : 'Production';
  
  const envColor = environment === 'Development' ? 'bg-indigo-50 text-indigo-700 border-indigo-200' : 'bg-green-50 text-green-700 border-green-200';
  const envIcon = environment === 'Development' ? '🧪' : '🚀';

  return (
    <div className="min-h-screen bg-white flex items-center justify-center p-6">
      <div className="max-w-4xl w-full">
        
        {/* Environment Indicator */}
        <div className="flex justify-center mb-6">
          <span className={`${envColor} border px-4 py-2 rounded-full font-medium text-sm`}>
            {envIcon} {environment}
          </span>
        </div>
        
        <div className="text-center mb-12">
          <h1 className="text-4xl font-semibold text-gray-900 mb-3">
            Setup Complete
          </h1>
          <p className="text-gray-500">Your Boot_Lang environment is ready</p>
        </div>
        
        <div className="space-y-4 mb-8">
          {/* Configuration */}
          <div className="bg-gray-50 border border-gray-200 p-6 rounded-lg">
            <h3 className="font-medium text-gray-900 mb-4">Configuration</h3>
            <dl className="space-y-3 text-sm">
              <div className="flex justify-between">
                <dt className="text-gray-500">User</dt>
                <dd className="text-gray-900 font-medium">{userName}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Project</dt>
                <dd className="text-gray-900 font-medium">{projectName}</dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-gray-500">Repository</dt>
                <dd>
                  <a href={githubUrl} target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:text-indigo-700 font-medium">
                    View on GitHub →
                  </a>
                </dd>
              </div>
            </dl>
          </div>
          
          {/* Tech Stack */}
          <div className="grid grid-cols-3 gap-3 text-sm">
            <div className="bg-gray-50 border border-gray-200 p-4 rounded-lg text-center">
              <div className="font-medium text-gray-900">React 19</div>
              <div className="text-gray-500 text-xs mt-1">Frontend</div>
            </div>
            <div className="bg-gray-50 border border-gray-200 p-4 rounded-lg text-center">
              <div className="font-medium text-gray-900">FastAPI</div>
              <div className="text-gray-500 text-xs mt-1">Backend</div>
            </div>
            <div className="bg-gray-50 border border-gray-200 p-4 rounded-lg text-center">
              <div className="font-medium text-gray-900">SQLite</div>
              <div className="text-gray-500 text-xs mt-1">Database</div>
            </div>
          </div>
          
          {/* Quick Actions */}
          <div className="grid grid-cols-2 gap-4 pt-4">
            <a 
              href="http://localhost:3000" 
              className="text-center p-6 border border-gray-200 rounded-lg hover:border-indigo-300 hover:bg-indigo-50 transition group"
            >
              <div className="text-3xl mb-2">📝</div>
              <div className="font-medium text-gray-900 group-hover:text-indigo-600">PRD Builder</div>
              <div className="text-sm text-gray-500 mt-1">Create requirements</div>
            </a>
            
            <a 
              href="http://localhost:3000/dashboard" 
              className="text-center p-6 border border-gray-200 rounded-lg hover:border-indigo-300 hover:bg-indigo-50 transition group"
            >
              <div className="text-3xl mb-2">🎯</div>
              <div className="font-medium text-gray-900 group-hover:text-indigo-600">System Dashboard</div>
              <div className="text-sm text-gray-500 mt-1">View status</div>
            </a>
          </div>
        </div>
        
        <div className="text-center text-gray-400 text-sm">
          Boot_Lang v1.0 · Powered by Cursor AI
        </div>
      </div>
    </div>
  );
};

export default Welcome;
