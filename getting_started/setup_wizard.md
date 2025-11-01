# Setup Wizard Guide

## Overview
The Boot_Lang setup wizard configures your development environment and connects it to your GitHub repository and Azure deployment.

---

## Quick Start

```bash
./welcome.sh
```

Opens browser to `http://localhost:8001/setup`

---

## What It Does

### Phase 1: Configuration Collection (Web Form)

**User Identity:**
- Your name
- Project name

**Git Configuration:**
- Your GitHub repository URL (create empty repo first)
- Click "Configure Git Remote" to connect

**API Keys:**
- OpenAI API key (required)
- Anthropic API key (optional)
- LangSmith API key (optional)

**Azure Configuration:**
- App Service name
- Static Web App URL
- Resource group
- Subscription ID
- Region

**Preferences:**
- Use PRD tool (default: true)
- Auto-deploy (default: false)
- OpenAI model preference
- Timezone

### Phase 2: Automation (Runs After "Save & Complete Setup")

**Automated steps:**

1. **Create virtual environment** - Python 3.11 venv
2. **Install dependencies** - From requirements.txt
3. **Initialize database** - SQLite with User table
4. **Build welcome page** - React component with your info
5. **Configure GitHub workflows** - Update with your app service name
6. **Secure configuration** - Add user_config.json to .gitignore
7. **Set GitHub secrets** - API keys (requires `gh` CLI authenticated)
8. **Push to GitHub** - Initial commit to your repo (force push)
9. **Deploy to Azure** - Via GitHub Actions
10. **Verify deployment** - Poll Azure URL for up to 3 minutes
11. **Show results** - Success page with live URL

---

## Git Remote Switching

**Before wizard:**
- Remote: `https://github.com/amyamyloyd/boot_lang.git` (scaffold)

**After wizard:**
- Remote: Your GitHub repo
- All future commits push to YOUR repo
- Deploys to YOUR Azure

---

## Requirements

### Before Running Wizard:

1. **Create empty GitHub repository**
   - Go to github.com/new
   - Name it (e.g., "my-app")
   - Don't add README, .gitignore, or license
   - Copy the URL

2. **Set up Azure deployment**
   
   **For App Service (Backend):**
   - Create App Service in Azure Portal
   - Deployment Center → GitHub → Select your repo
   - Choose authentication type (User-assigned identity recommended)
   - Azure creates workflow and secrets automatically
   
   **For Static Web App (Frontend):**
   - Create Static Web App in Azure Portal
   - Copy deployment token
   - Add to GitHub: Secrets → `AZURE_STATIC_WEB_APPS_API_TOKEN`

3. **Optional: Authenticate GitHub CLI**
   ```bash
   gh auth login
   ```
   Allows wizard to auto-set API key secrets

---

## During Wizard

**Step 1: Fill User Identity**
- Name and project name

**Step 2: Configure Git**
- Paste your GitHub repo URL
- Click "Configure Git Remote"
- Wait for green checkmark

**Step 3: Fill API Keys**
- OpenAI key (required for PRD tool)
- Others optional

**Step 4: Fill Azure Settings**
- App service name (from Azure Portal)
- Static Web App URL (from Azure Portal)
- Resource group
- Region

**Step 5: Set Preferences**
- Leave defaults unless you have specific needs

**Step 6: Complete Setup**
- Click "Save & Complete Setup"
- Watch progress in real-time
- Wait for deployment verification (3 minutes max)

---

## Success Indicators

✅ **Setup Complete:**
- Green card: "🎉 Setup Complete!"
- Live Azure URL shown
- All tasks marked DONE
- Ready to build

⚠️ **Setup Incomplete:**
- Yellow card: "⚠️ Setup Incomplete"
- Link to GitHub Actions to check deployment
- Environment ready but deployment still building

---

## After Setup

Your environment is ready:

```bash
# Start backend
venv/bin/python app.py

# Start frontend
cd frontend && npm start

# Start PRD builder
# Opens automatically at localhost:3000
```

**Tell Cursor:**
- "Start backend"
- "Start frontend"
- "Build my PRD"
- "Help me build a PRD"

---

## Troubleshooting

### Wizard Already Complete
If you see:
```
✓ Setup already complete!
```

The wizard detected existing `user_config.json` with `setup_complete: true`.

**To re-run:**
```bash
rm user_config.json
./welcome.sh
```

### Git Remote Not Switching
Check:
- GitHub repo URL is correct (https://github.com/username/repo)
- Repo exists and is accessible
- You have push permissions

### Deployment Fails
Check:
- Azure Deployment Center configured for your repo
- GitHub secrets exist (AZURE_STATIC_WEB_APPS_API_TOKEN, etc.)
- GitHub Actions tab shows errors
- Azure App Service is running

### GitHub Secrets Not Set
If `gh` CLI not authenticated:
1. Run `gh auth login`
2. Or manually add secrets at: github.com/yourrepo/settings/secrets/actions

**Required secrets:**
- `OPENAI_API_KEY` - From user_config.json
- `ANTHROPIC_API_KEY` - Optional
- `LANGSMITH_API_KEY` - Optional
- `AZURE_STATIC_WEB_APPS_API_TOKEN` - From Azure Portal
- Azure auth secrets (auto-created by Azure Deployment Center)

---

## Files Created

**Configuration:**
- `user_config.json` - Your settings (NOT committed to git)

**Frontend:**
- `frontend/src/components/Welcome.tsx` - Welcome page with your info
- `frontend/public/config.js` - Runtime config (deleted before push)

**Logs:**
- `setup_progress.log` - Automation progress (NOT committed)

**Updated:**
- `.gitignore` - Excludes user_config.json
- `.github/workflows/deploy.yml` - Your app service name
- Git remote - Points to your repo

---

## Testing Setup (For Developers)

To test wizard without affecting boot_lang development:

**Before testing:**
```bash
# Already done - restore script exists
./restore_bootlang.sh  # Restore back to boot_lang after test
```

**Test:**
1. Create test GitHub repo
2. Create test Azure resources
3. Run `./welcome.sh`
4. Complete wizard with test data

**After testing:**
```bash
./restore_bootlang.sh  # Switches back to boot_lang repo
```

---

## Next Steps

After successful setup:
1. Review `getting_started/` documentation
2. Build a PRD (Tool or manual)
3. Tell Cursor: "Build my PRD"
4. Start developing!

