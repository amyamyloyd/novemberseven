"""
SaltAIr Helper Tools Dashboard
Simple landing page with links to PRD Builder and Admin Panel
Port: 9000
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class DashboardHandler(BaseHTTPRequestHandler):
    """Dashboard with links to helper tools."""
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        try:
            with open('user_config.json', 'r') as f:
                config = json.load(f)
            project_name = config.get('user_identity', {}).get('project_name', 'Unknown')
        except:
            project_name = 'Unknown'
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SaltAIr Helper Tools</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <div class="min-h-screen flex items-center justify-center p-8">
        <div class="max-w-4xl w-full">
            <div class="text-center mb-12">
                <h1 class="text-5xl font-bold text-gray-900 mb-4">🚀 SaltAIr Helper Tools</h1>
                <p class="text-xl text-gray-600">Project: {project_name}</p>
            </div>
            
            <div class="grid grid-cols-2 gap-6">
                <a href="http://localhost:9001" target="_blank" 
                   class="block p-8 bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow border-2 border-transparent hover:border-indigo-500">
                    <div class="text-6xl mb-4">📝</div>
                    <h2 class="text-2xl font-bold text-gray-900 mb-2">PRD Builder</h2>
                    <p class="text-gray-600">Create and manage Product Requirements Documents</p>
                    <p class="text-sm text-indigo-600 mt-4 font-mono">localhost:9001</p>
                </a>
                
                <a href="http://localhost:9002" target="_blank"
                   class="block p-8 bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow border-2 border-transparent hover:border-purple-500">
                    <div class="text-6xl mb-4">⚙️</div>
                    <h2 class="text-2xl font-bold text-gray-900 mb-2">Admin Panel</h2>
                    <p class="text-gray-600">View project status, git info, and database</p>
                    <p class="text-sm text-purple-600 mt-4 font-mono">localhost:9002</p>
                </a>
            </div>
            
            <div class="bg-white rounded-xl shadow-lg p-6 mt-8">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">🔌 Port Usage</h3>
                <div class="grid grid-cols-2 gap-4 text-sm">
                    <div>
                        <p class="text-gray-500 font-semibold mb-2">Helper Tools (High Ports)</p>
                        <p class="font-mono text-xs">9000 - Dashboard</p>
                        <p class="font-mono text-xs">9001 - PRD Builder</p>
                        <p class="font-mono text-xs">9002 - Admin Panel</p>
                    </div>
                    <div>
                        <p class="text-gray-500 font-semibold mb-2">Your App (Available)</p>
                        <p class="font-mono text-xs">3000 - Frontend</p>
                        <p class="font-mono text-xs">8000 - Backend</p>
                        <p class="font-mono text-xs">8001 - API/Services</p>
                    </div>
                </div>
            </div>
            
            <div class="text-center mt-6 text-sm text-gray-500">
                <p>Helper tools won't interfere with your development ports</p>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    PORT = 9000
    print("=" * 60)
    print("SaltAIr Helper Tools Dashboard")
    print("=" * 60)
    print(f"\nDashboard: http://localhost:{PORT}")
    print("\nHelper Tools:")
    print("  PRD Builder: http://localhost:9001")
    print("  Admin Panel: http://localhost:9002")
    print("\nYour app ports (3000, 8000, 8001) are available")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)
    print()
    
    server = HTTPServer(('localhost', PORT), DashboardHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n[OK] Dashboard stopped")
        server.shutdown()

