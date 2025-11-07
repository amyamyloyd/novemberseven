# app.py
import os
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables FIRST before any other imports
load_dotenv()

# Import database initialization
from database import init_db

# Import routers
from auth import router as auth_router
from user_management import router as user_router
from admin import router as admin_router
from poc_api import router as poc_router
from tenant.tenant_1.poc_idea_1.backend.routes import router as t1_poc1_router

app = FastAPI(title="Boot_Lang Platform")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on application startup."""
    init_db()
    print("✓ Application started, database initialized")

# CORS - pre-configured for deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://proud-smoke-02a8bab0f.1.azurestaticapps.net",  # Azure Static Web App
        "https://boot-lang-gscvbveeg3dvgefh.eastus2-01.azurewebsites.net",  # Azure App Service
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(poc_router)
app.include_router(t1_poc1_router, prefix="/api/tenant_1/poc_idea_1", tags=["tenant_1"])

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    token: Optional[str] = None
    error: Optional[str] = None

class POCRequest(BaseModel):
    description: str
    user_id: str

class POCResponse(BaseModel):
    success: bool
    poc_id: Optional[str] = None
    poc_structure: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

# Root endpoint - serves coming soon page
@app.get("/")
async def root():
    """Serve coming soon page."""
    from fastapi.responses import HTMLResponse
    import os
    
    template_path = os.path.join("templates", "coming-soon-prod.html")
    
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    else:
        # Fallback if template doesn't exist
        return {
            "message": "Boot_Lang Platform",
            "status": "running",
            "version": "1.0.0"
        }

# Config endpoint - serves user configuration for splash page
@app.get("/api/config")
async def get_config():
    """
    Get user configuration for splash page display.
    
    Returns non-sensitive config data.
    """
    import json
    import os
    
    config_path = "user_config.json"
    
    if not os.path.exists(config_path):
        return {
            "user_name": "User",
            "project_name": "Boot_Lang Project",
            "setup_complete": False
        }
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        return {
            "user_name": config.get("user_identity", {}).get("user_name", "User"),
            "project_name": config.get("user_identity", {}).get("project_name", "Project"),
            "github_url": config.get("git_deployment", {}).get("github_repo_url", ""),
            "setup_complete": config.get("setup_complete", False)
        }
    except Exception as e:
        return {
            "user_name": "User",
            "project_name": "Boot_Lang Project",
            "setup_complete": False,
            "error": str(e)
        }


# System status endpoint for admin dashboard
@app.get("/api/system/status")
async def get_system_status():
    """
    Get system status for admin dashboard.
    
    Returns git status, Azure URLs, database info, project info.
    """
    import json
    import subprocess
    import sqlite3
    
    status = {
        "project": {},
        "git": {},
        "azure": {},
        "database": {},
        "timestamp": datetime.now().isoformat()
    }
    
    # Project info
    try:
        with open('user_config.json', 'r') as f:
            config = json.load(f)
        
        status["project"] = {
            "name": config.get('user_identity', {}).get('project_name', 'Unknown'),
            "user": config.get('user_identity', {}).get('user_name', 'Unknown'),
            "environment": os.getenv('ENVIRONMENT', 'development')
        }
    except:
        status["project"] = {
            "name": "Unknown",
            "user": "Unknown",
            "environment": "development"
        }
    
    # Git status
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
        
        status_output = subprocess.check_output(
            ['git', 'status', '--porcelain'],
            text=True,
            stderr=subprocess.DEVNULL
        ).strip()
        
        has_changes = bool(status_output)
        
        status["git"] = {
            "branch": branch,
            "commit_hash": commit_hash,
            "commit_message": commit_msg,
            "has_uncommitted_changes": has_changes,
            "status": "⚠️ Uncommitted changes" if has_changes else "✅ Clean"
        }
    except:
        status["git"] = {
            "branch": "unknown",
            "commit_hash": "N/A",
            "commit_message": "N/A",
            "has_uncommitted_changes": False,
            "status": "⚠️ Git info unavailable"
        }
    
    # Azure info
    try:
        with open('user_config.json', 'r') as f:
            config = json.load(f)
        
        azure = config.get('azure_settings', {})
        app_service = azure.get('app_service_name', '')
        static_url = azure.get('static_web_app_url', 'Not deployed yet')
        dev_url = azure.get('dev_slot_url', 'Not created yet')
        resource_group = azure.get('resource_group', 'N/A')
        
        prod_url = f"https://{app_service}.azurewebsites.net" if app_service else "Not configured"
        
        status["azure"] = {
            "resource_group": resource_group,
            "backend_prod": prod_url,
            "backend_dev": dev_url,
            "frontend": static_url
        }
    except:
        status["azure"] = {
            "resource_group": "N/A",
            "backend_prod": "Not configured",
            "backend_dev": "Not configured",
            "frontend": "Not configured"
        }
    
    # Database info
    db_path = 'boot_lang.db'
    
    if not os.path.exists(db_path):
        status["database"] = {
            "exists": False,
            "tables": [],
            "total_records": 0
        }
    else:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
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
            
            status["database"] = {
                "exists": True,
                "tables": table_info,
                "total_records": total_records
            }
        except Exception as e:
            status["database"] = {
                "exists": True,
                "tables": [],
                "total_records": 0,
                "error": str(e)
            }
    
    return status

# Login endpoint
@app.post("/api/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Simple auth endpoint - expand with real JWT/bcrypt later
    """
    # TODO: Replace with real auth
    if request.username and request.password:
        return LoginResponse(
            success=True,
            token="dummy_token_for_now"
        )
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

# POC Agent endpoint
@app.post("/api/poc/create", response_model=POCResponse)
async def create_poc(request: POCRequest):
    """
    POC Agent: Takes user description, generates POC structure
    """
    try:
        from agents.poc_agent import POCAgent
        
        agent = POCAgent()
        result = agent.create_poc(request.description, request.user_id)
        
        return POCResponse(
            success=True,
            poc_id=result["poc_id"],
            poc_structure=result["structure"]
        )
    
    except Exception as e:
        return POCResponse(
            success=False,
            error=str(e)
        )

# List POCs
@app.get("/api/poc/list")
async def list_pocs(user_id: str):
    """
    List all POCs for a user
    """
    # TODO: Implement with database
    return {"pocs": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)