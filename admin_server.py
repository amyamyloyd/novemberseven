"""
Local Admin Dashboard Server

Runs on localhost:8080 and provides a web interface for:
- Viewing git status
- Viewing Azure deployment URLs
- Viewing database tables and records
- Quick links to resources
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import subprocess
import sqlite3
from datetime import datetime

class AdminHandler(BaseHTTPRequestHandler):
    """Handle admin dashboard requests."""
    
    def do_GET(self):
        """Serve admin dashboard or API endpoints."""
        
        if self.path == '/' or self.path == '/index.html':
            # Serve main dashboard page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = self.generate_dashboard_html()
            self.wfile.write(html.encode())
            
        elif self.path == '/api/status':
            # Serve status JSON for dashboard refresh
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status = self.get_system_status()
            self.wfile.write(json.dumps(status).encode())
            
        else:
            self.send_error(404)
    
    def get_system_status(self):
        """Gather system status information."""
        status = {
            "project": self.get_project_info(),
            "git": self.get_git_status(),
            "azure": self.get_azure_info(),
            "database": self.get_database_info(),
            "timestamp": datetime.now().isoformat()
        }
        return status
    
    def get_project_info(self):
        """Get project information from config."""
        try:
            with open('user_config.json', 'r') as f:
                config = json.load(f)
            
            return {
                "name": config.get('user_identity', {}).get('project_name', 'Unknown'),
                "user": config.get('user_identity', {}).get('user_name', 'Unknown'),
                "environment": os.getenv('ENVIRONMENT', 'development')
            }
        except:
            return {
                "name": "Unknown",
                "user": "Unknown",
                "environment": "development"
            }
    
    def get_git_status(self):
        """Get current git branch and commit info."""
        try:
            branch = subprocess.check_output(
                ['git', 'branch', '--show-current'],
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
            
            commit_hash = subprocess.check_output(
                ['git', 'rev-parse', '--short', 'HEAD'],
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
            
            commit_msg = subprocess.check_output(
                ['git', 'log', '-1', '--pretty=%B'],
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
            
            # Check if there are uncommitted changes
            status_output = subprocess.check_output(
                ['git', 'status', '--porcelain'],
                text=True,
                stderr=subprocess.DEVNULL
            ).strip()
            
            has_changes = bool(status_output)
            
            return {
                "branch": branch,
                "commit_hash": commit_hash,
                "commit_message": commit_msg,
                "has_uncommitted_changes": has_changes,
                "status": "⚠️ Uncommitted changes" if has_changes else "✅ Clean"
            }
        except:
            return {
                "branch": "unknown",
                "commit_hash": "N/A",
                "commit_message": "N/A",
                "has_uncommitted_changes": False,
                "status": "⚠️ Git info unavailable"
            }
    
    def get_azure_info(self):
        """Get Azure deployment URLs from config."""
        try:
            with open('user_config.json', 'r') as f:
                config = json.load(f)
            
            azure = config.get('azure_settings', {})
            app_service = azure.get('app_service_name', '')
            static_url = azure.get('static_web_app_url', 'Not deployed yet')
            dev_url = azure.get('dev_slot_url', 'Not created yet')
            resource_group = azure.get('resource_group', 'N/A')
            
            prod_url = f"https://{app_service}.azurewebsites.net" if app_service else "Not configured"
            
            return {
                "resource_group": resource_group,
                "backend_prod": prod_url,
                "backend_dev": dev_url,
                "frontend": static_url
            }
        except:
            return {
                "resource_group": "N/A",
                "backend_prod": "Not configured",
                "backend_dev": "Not configured",
                "frontend": "Not configured"
            }
    
    def get_database_info(self):
        """Get SQLite database information."""
        db_path = 'boot_lang.db'
        
        if not os.path.exists(db_path):
            return {
                "exists": False,
                "tables": [],
                "total_records": 0
            }
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get list of tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = cursor.fetchall()
            
            table_info = []
            total_records = 0
            
            for (table_name,) in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    total_records += count
                    table_info.append({
                        "name": table_name,
                        "records": count
                    })
                except:
                    table_info.append({
                        "name": table_name,
                        "records": "Error"
                    })
            
            conn.close()
            
            return {
                "exists": True,
                "tables": table_info,
                "total_records": total_records
            }
        except Exception as e:
            return {
                "exists": True,
                "tables": [],
                "total_records": 0,
                "error": str(e)
            }
    
    def generate_dashboard_html(self):
        """Generate the admin dashboard HTML."""
        status = self.get_system_status()
        
        # Build tables HTML
        tables_html = ""
        if status['database']['exists'] and status['database']['tables']:
            for table in status['database']['tables']:
                tables_html += f'<div class="table-item"><span class="table-name">{table["name"]}</span><span class="table-count">{table["records"]} records</span></div>'
        else:
            tables_html = "<div class='empty-state'>Database not initialized yet</div>"
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Boot Lang Admin Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: #f7fafc;
            color: #2d3748;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 28px;
            margin-bottom: 8px;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 14px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px;
        }}
        
        .refresh-button {{
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            margin-bottom: 20px;
        }}
        
        .refresh-button:hover {{
            background: #5568d3;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }}
        
        .card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .card h2 {{
            font-size: 18px;
            margin-bottom: 16px;
            color: #667eea;
        }}
        
        .info-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .info-row:last-child {{
            border-bottom: none;
        }}
        
        .label {{
            font-weight: 600;
            color: #4a5568;
            font-size: 14px;
        }}
        
        .value {{
            color: #2d3748;
            font-size: 14px;
            text-align: right;
            word-break: break-word;
            max-width: 60%;
        }}
        
        .link {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .link:hover {{
            text-decoration: underline;
        }}
        
        .table-list {{
            margin-top: 12px;
        }}
        
        .table-item {{
            background: #f7fafc;
            padding: 8px 12px;
            margin-bottom: 8px;
            border-radius: 6px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .table-name {{
            font-weight: 600;
            font-size: 14px;
        }}
        
        .table-count {{
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
        }}
        
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .status-success {{
            background: #c6f6d5;
            color: #22543d;
        }}
        
        .status-warning {{
            background: #feebc8;
            color: #7c2d12;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 20px;
            color: #718096;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1>🎯 Boot Lang Admin Dashboard</h1>
                <p>{status['project']['name']} - {status['project']['environment']}</p>
            </div>
            <a href="http://localhost:3000" 
               target="prd_builder"
               style="background: rgba(255,255,255,0.2); color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: 600; backdrop-filter: blur(10px);">
                📝 PRD Builder →
            </a>
        </div>
    </div>
    
    <div class="container">
        <button class="refresh-button" onclick="location.reload()">🔄 Refresh</button>
        
        <div class="grid">
            <!-- Project Info Card -->
            <div class="card">
                <h2>📋 Project Info</h2>
                <div class="info-row">
                    <span class="label">Project Name:</span>
                    <span class="value">{status['project']['name']}</span>
                </div>
                <div class="info-row">
                    <span class="label">Owner:</span>
                    <span class="value">{status['project']['user']}</span>
                </div>
                <div class="info-row">
                    <span class="label">Environment:</span>
                    <span class="value">{status['project']['environment']}</span>
                </div>
            </div>
            
            <!-- Git Status Card -->
            <div class="card">
                <h2>🌿 Git Status</h2>
                <div class="info-row">
                    <span class="label">Branch:</span>
                    <span class="value">{status['git']['branch']}</span>
                </div>
                <div class="info-row">
                    <span class="label">Latest Commit:</span>
                    <span class="value" title="{status['git']['commit_message']}">{status['git']['commit_hash']}</span>
                </div>
                <div class="info-row">
                    <span class="label">Status:</span>
                    <span class="value">{status['git']['status']}</span>
                </div>
            </div>
            
            <!-- Database Card -->
            <div class="card">
                <h2>🗄️ Database</h2>
                {f'''
                <div class="info-row">
                    <span class="label">Total Tables:</span>
                    <span class="value">{len(status['database']['tables'])}</span>
                </div>
                <div class="info-row">
                    <span class="label">Total Records:</span>
                    <span class="value">{status['database']['total_records']}</span>
                </div>
                <div class="table-list">
                    {tables_html}
                </div>
                ''' if status['database']['exists'] else '<div class="empty-state">Database not initialized yet</div>'}
            </div>
        </div>
        
        <!-- Azure Deployments Card (Full Width) -->
        <div class="card">
            <h2>☁️ Azure Deployments</h2>
            <div class="info-row">
                <span class="label">Resource Group:</span>
                <span class="value">{status['azure']['resource_group']}</span>
            </div>
            <div class="info-row">
                <span class="label">Backend (Production):</span>
                <span class="value"><a href="{status['azure']['backend_prod']}" class="link" target="_blank">{status['azure']['backend_prod']}</a></span>
            </div>
            <div class="info-row">
                <span class="label">Backend (Development):</span>
                <span class="value"><a href="{status['azure']['backend_dev']}" class="link" target="_blank">{status['azure']['backend_dev']}</a></span>
            </div>
            <div class="info-row">
                <span class="label">Frontend (Static Web App):</span>
                <span class="value"><a href="{status['azure']['frontend']}" class="link" target="_blank">{status['azure']['frontend']}</a></span>
            </div>
        </div>
        
        <!-- Quick Links Card -->
        <div class="card">
            <h2>🔗 Quick Links</h2>
            <div class="info-row">
                <span class="label">PRD Builder:</span>
                <span class="value"><a href="http://localhost:3000" class="link" target="prd_builder">Open PRD Builder</a></span>
            </div>
            <div class="info-row">
                <span class="label">Backend API Docs:</span>
                <span class="value"><a href="http://localhost:8000/docs" class="link" target="api_docs">FastAPI Docs</a></span>
            </div>
            <div class="info-row">
                <span class="label">GitHub Repo:</span>
                <span class="value"><a href="https://github.com" class="link" target="github">View on GitHub</a></span>
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        return html
    
    def log_message(self, format, *args):
        """Suppress log messages."""
        pass


if __name__ == "__main__":
    print("=" * 60)
    print("🎯 Boot Lang Admin Dashboard")
    print("=" * 60)
    print("\nAccess at: http://localhost:8080")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)
    print()
    
    server = HTTPServer(('127.0.0.1', 8080), AdminHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n✅ Admin dashboard stopped")
        server.shutdown()

