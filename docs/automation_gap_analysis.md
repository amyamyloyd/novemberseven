# Automation Gap Analysis & Implementation Plan

## What You Want vs What We Have

### ✅ What's Working:
1. Python detection/installation
2. OS detection (Mac/Windows) - welcome.sh / welcome.bat
3. CLI tool detection/installation (Git, GitHub CLI, Azure CLI)
4. Authentication (GitHub, Azure) via web-based device auth
5. Git setup (remote, branches dev/prod)
6. Virtual environment creation
7. Dependencies installation
8. Database initialization
9. Azure resource provisioning (resource group, web app, static web app)
10. GitHub workflows creation
11. Coming soon pages creation

### ❌ What's Missing:

#### 1. **Local Services Not Starting**
- **Frontend (port 3000)** - Not started after automation
- **Backend (port 8000)** - Not started after automation  
- **Admin Server (port 8080)** - Not started after automation
- **Terminal not activated in venv** - User has to manually activate

#### 2. **Azure Deployment Issues**
- **Switched from slots to separate apps** - You want deployment slots, not separate apps
- **Coming soon pages not deploying** - Pages created but not visible on Azure
- **GitHub Actions workflows broken** - Publish profile errors preventing deployment
- **No actual deployment happening** - Nothing visible on Azure URLs

#### 3. **Missing Automation Steps**
- **Frontend build/start** - `npm install` and `npm start` not run
- **Admin server start** - `admin_server.py` not started
- **Services in background** - Nothing running after automation completes
- **Platform-specific commands** - Mac vs Windows paths not handled (venv/bin vs venv/Scripts)

#### 4. **End State Not Achieved**
- User should see:
  - ✅ Terminal in venv (activated)
  - ❌ Frontend running on port 3000 (PRD builder visible)
  - ❌ Admin page on port 8080
  - ❌ Backend on port 8000
  - ❌ Azure dev site showing coming soon page
  - ❌ Azure prod site showing coming soon page

---

## Implementation Plan

### Phase 1: Fix Azure Deployment (Slots, Not Separate Apps)

**Revert to deployment slots:**
1. Change `provision_azure_resources()` back to creating slots (not separate apps)
2. Use Standard S1 SKU (supports slots)
3. Update workflows to deploy to slots
4. Fix publish profiles for slots

**Files to modify:**
- `automation_service.py` - `provision_azure_resources()` method
- `.github/workflows/deploy-dev.yml` - Add `slot-name: 'dev'`
- `.github/workflows/deploy-prod.yml` - Add `slot-name: 'prod'`

### Phase 2: Start Local Services

**Add methods to start services:**
1. `start_local_services()` - Starts backend, frontend, admin in background
2. Platform detection for paths (Mac: `venv/bin`, Windows: `venv/Scripts`)
3. Background process management

**Files to modify:**
- `automation_service.py` - Add `start_local_services()` method
- Update `run_automation()` to call it at the end

### Phase 3: Ensure Services Are Visible

**Frontend:**
- Run `npm install` in `frontend/` directory
- Run `npm start` in background (port 3000)
- Ensure PRD builder is accessible

**Backend:**
- Run `uvicorn app:app --host 0.0.0.0 --port 8000` in background
- Ensure API is accessible

**Admin:**
- Run `python admin_server.py` in background (port 8080)
- Ensure dashboard is accessible

### Phase 4: Platform-Specific Handling

**Mac:**
- Use `venv/bin/python`, `venv/bin/pip`
- Use `python3` commands
- Background processes: `&` or `nohup`

**Windows:**
- Use `venv\Scripts\python.exe`, `venv\Scripts\pip.exe`
- Use `python` commands
- Background processes: `Start-Process` or PowerShell jobs

### Phase 5: Terminal Activation

**After automation completes:**
- Print instructions to activate venv
- Or: Create a script that activates venv and shows status
- Show all running services and URLs

---

## Detailed Implementation Steps

### Step 1: Fix Azure Slots (Revert Separate Apps)

```python
# In provision_azure_resources():
# Change from:
dev_app_name = f"{app_service_name}-dev"
# Back to:
# Create dev slot (not separate app)
az webapp deployment slot create --slot dev
```

### Step 2: Add start_local_services() Method

```python
def start_local_services(self):
    """Start backend, frontend, and admin services."""
    # Detect platform
    # Start backend (port 8000)
    # Start frontend (port 3000) 
    # Start admin (port 8080)
    # All in background
    # Print URLs and status
```

### Step 3: Update run_automation() Flow

```python
# At the end, before success message:
self.start_local_services()
# Then show all URLs and running services
```

### Step 4: Fix GitHub Workflows

```yaml
# deploy-dev.yml
- name: Deploy to Azure Web App
  uses: azure/webapps-deploy@v2
  with:
    app-name: 'elevenseven-backend'
    slot-name: 'dev'  # Add this
    publish-profile: ${{ secrets.AZURE_DEV_PUBLISH_PROFILE }}
```

### Step 5: Ensure Coming Soon Pages Deploy

- Pages are in `templates/`
- Backend serves them at `/` route
- When code deploys, pages should be visible
- Verify deployment actually completes

---

## Success Criteria

After automation completes, user should see:

1. **Terminal:**
   - Venv activated (or clear instructions to activate)
   - All services running
   - URLs displayed

2. **Browser tabs open:**
   - http://localhost:3000 (Frontend with PRD builder)
   - http://localhost:8080 (Admin dashboard)
   - https://[app]-dev.azurewebsites.net (Dev coming soon)
   - https://[app]-prod.azurewebsites.net (Prod coming soon)

3. **Services running:**
   - Backend API responding on port 8000
   - Frontend dev server on port 3000
   - Admin server on port 8080

4. **Azure:**
   - Dev slot shows coming soon page
   - Prod slot shows coming soon page
   - GitHub Actions deployments successful

---

## Priority Order

1. **Fix Azure slots** (revert separate apps)
2. **Fix GitHub workflows** (add slot-name, fix publish profiles)
3. **Add start_local_services()** method
4. **Platform-specific handling** (Mac vs Windows)
5. **Test end-to-end** (verify all services start)

