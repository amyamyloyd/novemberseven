# SaltAIr Setup Success Checklist

Complete checklist of a successful setup from start to finish.

---

## Pre-Setup Requirements

- [ ] Python 3.11+ installed and in PATH
- [ ] Git installed (for cloning repo)
- [ ] Windows: Running in CMD (not PowerShell)
- [ ] User has accounts: GitHub, Azure, OpenAI

---

## Step 1: Clone Repository

- [ ] Repository cloned successfully
- [ ] Can see files: `welcome.bat`, `setup_server.py`, `automation_service.py`, etc.
- [ ] Navigate to repository root directory

---

## Step 2: Run Welcome Script

**Command:** `cmd /c welcome.bat` (Windows) or `./welcome.sh` (Mac/Linux)

- [ ] Python version check passes (3.11+)
- [ ] Message: "Starting SaltAIr setup server..."
- [ ] `setup_server.py` starts on port 8001
- [ ] Browser opens automatically to `http://localhost:8001/setup`
- [ ] Setup form displays correctly with 4 tabs (Identity, Git, API Keys, Azure)

---

## Step 3: Fill Setup Form

### Identity Tab
- [ ] Enter User Name
- [ ] Enter Project Name

### Git Tab
- [ ] Enter GitHub Repository URL (format: `https://github.com/username/repo-name.git`)

### API Keys Tab
- [ ] Enter OpenAI API Key (required)
- [ ] Enter Anthropic API Key (optional)
- [ ] Enter LangSmith API Key (optional)

### Azure Tab
- [ ] Enter Azure Subscription ID (GUID format)
- [ ] Note: Resource Group, App Service Name, and Region are auto-generated

### Progress Checklist
- [ ] All required fields filled (5 total: user_name, project_name, github_repo_url, openai_api_key, subscription_id)
- [ ] Green checkmarks show for completed fields
- [ ] "Save & Complete Setup" button enabled

---

## Step 4: Submit Form & Automation Begins

**Click "Save & Complete Setup"**

### Expected Automation Steps:

#### 1. CLI Tools Installation
- [ ] Message: "[SETUP] Installing CLI Tools"
- [ ] Azure extension installed: `ms-vscode.azurecli`
- [ ] GitHub CLI check: "GitHub CLI not found, installing..."
- [ ] **Windows:** `winget install GitHub.cli` prompt appears
  - [ ] User clicks "Accept" on winget prompt
  - [ ] Installation progress streams to terminal
  - [ ] Message: "[OK] GitHub CLI installed successfully"
- [ ] **Mac:** `brew install gh` runs automatically
- [ ] Verification: "[OK] GitHub CLI available"
- [ ] Verification: "[OK] Azure CLI available"

#### 2. GitHub Authentication
- [ ] Message: "-> Authenticating GitHub CLI..."
- [ ] Browser opens for GitHub authentication
- [ ] User signs in to GitHub
- [ ] Message: "[OK] GitHub CLI authenticated"

#### 3. Azure Authentication
- [ ] Message: "-> Authenticating Azure CLI..."
- [ ] Browser/device code prompt for Azure authentication
- [ ] User signs in to Azure
- [ ] Message: "[OK] Azure CLI authenticated"
- [ ] Azure subscription set successfully

#### 4. Git Remote Configuration
- [ ] Message: "-> Configuring git remote..."
- [ ] Git remote added/updated with GitHub URL
- [ ] Message: "[OK] Git remote configured: [GitHub URL]"

#### 5. Virtual Environment Setup
- [ ] Message: "-> Creating virtual environment..."
- [ ] `venv` folder created in project root
- [ ] Virtual environment activated
- [ ] Message: "[OK] Virtual environment ready"
- [ ] Progress log: "DONE:Creating virtual environment"

#### 6. Install Dependencies
- [ ] Message: "-> Installing dependencies..."
- [ ] Pip upgraded
- [ ] All packages from `requirements.txt` installed
- [ ] Message: "[OK] Dependencies installed"
- [ ] Progress log: "DONE:Installing dependencies"

#### 7. Initialize Database
- [ ] Message: "-> Initializing database..."
- [ ] `boot_lang.db` file created
- [ ] SQLite tables created (users, poc_conversations, etc.)
- [ ] Message: "[OK] Database initialized"
- [ ] Progress log: "DONE:Initializing database"

#### 8. Build Welcome Page
- [ ] Message: "-> Building welcome page..."
- [ ] `config.js` created with user info
- [ ] `index.html` updated with config script
- [ ] `npm install` runs in frontend directory
- [ ] `npm run build` creates production build
- [ ] Message: "[OK] Welcome page built"
- [ ] Progress log: "DONE:Building welcome page"

#### 9. Configure GitHub Workflows
- [ ] Message: "-> Configuring GitHub workflows..."
- [ ] `.github/workflows/deploy.yml` updated with app service name
- [ ] Message: "[OK] GitHub workflows configured"
- [ ] Progress log: "DONE:Configuring GitHub workflows"

#### 10. Secure Configuration
- [ ] `user_config.json` added to `.gitignore`
- [ ] Progress log: "DONE:Securing configuration file"

#### 11. Set GitHub Secrets
- [ ] Message: "-> Setting GitHub secrets..."
- [ ] `OPENAI_API_KEY` secret set in GitHub repo
- [ ] `ANTHROPIC_API_KEY` secret set (if provided)
- [ ] `LANGSMITH_API_KEY` secret set (if provided)
- [ ] Message: "[OK] GitHub secrets set"
- [ ] Progress log: "DONE:Setting GitHub secrets"

#### 12. Commit and Push to GitHub
- [ ] Message: "-> Committing and pushing to GitHub..."
- [ ] All files staged with `git add .`
- [ ] Initial commit created: "Initial Boot_Lang setup: [Project Name]"
- [ ] Pushed to `main` branch
- [ ] Message: "[OK] Pushed to GitHub"
- [ ] Progress log: "DONE:Pushing to GitHub"

#### 13. Create Dev Environment
- [ ] Message: "-> Creating dev branch..."
- [ ] `dev` branch created from `main`
- [ ] Pushed to GitHub
- [ ] Message: "[OK] Dev branch created and pushed"
- [ ] Message: "-> Creating Azure deployment slot (dev)..."
- [ ] Azure dev slot created: `[app-service-name]-dev.azurewebsites.net`
- [ ] Dev slot environment variables configured
- [ ] Message: "[OK] Dev slot created: [dev URL]"
- [ ] Message: "[OK] Dev slot environment configured"
- [ ] Switched back to `main` branch
- [ ] Progress log: "DONE:Creating dev environment"

#### 14. Wait for GitHub Actions
- [ ] Message: "Waiting for GitHub Actions to start deployment..."
- [ ] 15-second wait
- [ ] Progress log: "DONE:Deploying to Azure via GitHub Actions"

#### 15. Verify Deployment
- [ ] Message: "-> Testing deployment at: [Azure URL]"
- [ ] Polling Azure URL (up to 3 minutes, 36 attempts)
- [ ] HTTP 200 response received
- [ ] Message: "[OK] Deployment verified! Site responding (HTTP 200)"
- [ ] Progress log: "DONE:Verifying deployment"
- [ ] Progress log: "COMPLETE:[Azure URL]"

---

## Step 5: Setup Complete

### Success Messages
- [ ] Message: "=================================================="
- [ ] Message: "  [OK] Setup Complete!"
- [ ] Message: "=================================================="
- [ ] Message: "Your Boot Lang environment is ready!"

### Access Points Displayed
- [ ] Backend API: `http://localhost:8000`
- [ ] Frontend: `http://localhost:3000`
- [ ] Deployed: `[Azure Static Web App URL]`

### Next Steps Shown
- [ ] Start backend: tell Cursor 'Start backend'
- [ ] Start frontend: tell Cursor 'Start frontend'
- [ ] Login at `http://localhost:3000`
- [ ] View System Dashboard at `http://localhost:3000/dashboard`
- [ ] Build a PRD: tell Cursor 'Help me build a PRD'

---

## Step 6: Verify Deployment

### GitHub Verification
- [ ] Navigate to GitHub repository
- [ ] `main` branch exists with all project files
- [ ] `dev` branch exists
- [ ] GitHub Actions workflow completed successfully
- [ ] Secrets visible in Settings → Secrets and variables → Actions:
  - [ ] `OPENAI_API_KEY`
  - [ ] `ANTHROPIC_API_KEY` (if provided)
  - [ ] `LANGSMITH_API_KEY` (if provided)

### Azure Verification
- [ ] Log in to Azure Portal
- [ ] Resource Group exists: `[project-name]-rg`
- [ ] App Service exists: `[project-name]-backend`
- [ ] Production slot URL works: `https://[project-name]-backend.azurewebsites.net`
- [ ] Dev slot exists: `https://[project-name]-backend-dev.azurewebsites.net`
- [ ] Static Web App deployed and accessible
- [ ] Welcome page displays with correct user info

### Local Verification
- [ ] Files in project root:
  - [ ] `user_config.json` (ignored by git)
  - [ ] `setup_progress.log`
  - [ ] `boot_lang.db`
  - [ ] `venv/` directory
  - [ ] `frontend/build/` directory
- [ ] Can start backend: `venv/Scripts/python main.py` (Windows) or `venv/bin/python main.py` (Mac)
- [ ] Can start frontend: `cd frontend && npm start`
- [ ] Login page accessible at `http://localhost:3000`

---

## Troubleshooting Completed Setup

### If Setup Completes but Deployment Fails
- [ ] Check GitHub Actions at `https://github.com/[username]/[repo]/actions`
- [ ] Review workflow logs for errors
- [ ] Verify Azure subscription has credits/is active
- [ ] Manually trigger GitHub Actions workflow

### If Local Services Won't Start
- [ ] Verify venv activated
- [ ] Check `boot_lang.db` exists and has tables
- [ ] Check ports 8000 and 3000 are available
- [ ] Review `setup_progress.log` for errors

### If Authentication Failed
- [ ] Manually authenticate GitHub CLI: `gh auth login`
- [ ] Manually authenticate Azure CLI: `az login`
- [ ] Re-run automation: `python automation_service.py`

---

## Success Indicators

✅ **Full Success:**
- All 15 automation steps completed
- GitHub repo populated
- Azure resources created
- Deployment verified (HTTP 200)
- Welcome page shows user info

✅ **Partial Success (Deployment Pending):**
- Automation completed
- GitHub Actions still running
- Can manually verify later

❌ **Failure Indicators:**
- Progress stuck/frozen
- Error messages in terminal
- GitHub Actions failed
- Azure resources not created

---

## Total Expected Time

- **Form submission to automation start:** < 5 seconds
- **CLI tool installation:** 30-60 seconds
- **Authentication:** 1-2 minutes (user interaction)
- **Automation steps:** 5-10 minutes
- **GitHub Actions deployment:** 5-10 minutes
- **Total:** 15-25 minutes

---

## Files Created During Setup

### Project Root
- `user_config.json` - User configuration (gitignored)
- `setup_progress.log` - Automation progress log
- `boot_lang.db` - SQLite database
- `venv/` - Python virtual environment

### Frontend
- `frontend/public/config.js` - User config for React
- `frontend/build/` - Production build

### Git
- `.gitignore` - Updated with `user_config.json`
- Remote configured to GitHub URL

---

## Post-Setup Next Steps

1. **Start Local Development:**
   ```bash
   # Backend
   venv/Scripts/activate  # Windows
   python main.py
   
   # Frontend
   cd frontend
   npm start
   ```

2. **Access Application:**
   - Local: `http://localhost:3000`
   - Deployed: Check Azure URL from setup

3. **Build a PRD:**
   - Login to local app
   - Navigate to PRD Builder
   - Start conversation with agent

4. **Monitor Deployment:**
   - GitHub Actions: `https://github.com/[username]/[repo]/actions`
   - Azure Portal: `https://portal.azure.com`

---

## Support

If setup fails at any step, check:
1. `setup_progress.log` - Last successful step
2. Terminal output - Error messages
3. GitHub Actions logs - Deployment errors
4. Azure Portal - Resource creation status

---

*Last Updated: 2025-01-05*

