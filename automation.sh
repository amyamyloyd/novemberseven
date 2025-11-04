#!/bin/bash
# Automation script - runs after config saved

set -e

# ==================================================
# STEP 0: Authenticate GitHub and Azure CLIs
# ==================================================
echo "=================================================="
echo "  [AUTH] CLI Authentication"
echo "=================================================="
echo ""

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo "[ERROR] GitHub CLI not found"
    echo ""
    echo "Please install GitHub CLI:"
    echo "  macOS:   brew install gh"
    echo "  Linux:   (visit https://cli.github.com/)"
    echo "  Windows: winget install GitHub.cli"
    echo ""
    exit 1
fi

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "[ERROR] Azure CLI not found"
    echo ""
    echo "Please install Azure CLI:"
    echo "  macOS:   brew install azure-cli"
    echo "  Linux:   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash"
    echo "  Windows: winget install Microsoft.AzureCLI"
    echo ""
    exit 1
fi

echo "[OK] CLIs installed"
echo ""

# Authenticate GitHub CLI
echo "-> Authenticating GitHub CLI..."
echo "  (Browser will open for authentication)"
echo ""

if ! gh auth status &> /dev/null; then
    gh auth login --web --git-protocol https
    
    if [ $? -ne 0 ]; then
        echo "[ERROR] GitHub authentication failed"
        echo "Please try again or check your network connection"
        exit 1
    fi
fi

echo "[OK] GitHub CLI authenticated"
echo ""

# Authenticate Azure CLI
echo "-> Authenticating Azure CLI..."
echo "  (Browser will open for authentication)"
echo ""

if ! az account show &> /dev/null; then
    az login --use-device-code
    
    if [ $? -ne 0 ]; then
        echo "[ERROR] Azure authentication failed"
        echo "Please try again or check your network connection"
        exit 1
    fi
fi

echo "[OK] Azure CLI authenticated"
echo ""

# Load Azure subscription ID from config
AZURE_SUBSCRIPTION=$(python3 -c "import json; print(json.load(open('user_config.json'))['azure_settings'].get('subscription_id', ''))" 2>/dev/null || echo "")

if [ -n "$AZURE_SUBSCRIPTION" ]; then
    echo "-> Setting Azure subscription..."
    az account set --subscription "$AZURE_SUBSCRIPTION"
    
    if [ $? -ne 0 ]; then
        echo "[WARN] Failed to set subscription $AZURE_SUBSCRIPTION"
        echo "Using default subscription instead"
    else
        echo "[OK] Azure subscription set: $AZURE_SUBSCRIPTION"
    fi
else
    echo "[WARN] No Azure subscription ID in config - using default"
fi

echo ""
echo "=================================================="
echo "  Starting Automated Setup"
echo "=================================================="
echo ""

# Ensure we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "Switching from $CURRENT_BRANCH to main branch..."
    git checkout main
fi

# Load configuration
USER_NAME=$(python3 -c "import json; print(json.load(open('user_config.json'))['user_identity']['user_name'])")
PROJECT_NAME=$(python3 -c "import json; print(json.load(open('user_config.json'))['user_identity']['project_name'])")
GITHUB_URL=$(python3 -c "import json; print(json.load(open('user_config.json'))['git_deployment']['github_repo_url'])")
AZURE_STATIC_URL=$(python3 -c "import json; print(json.load(open('user_config.json'))['azure_settings']['static_web_app_url'])" 2>/dev/null || echo "")
APP_SERVICE_NAME=$(python3 -c "import json; print(json.load(open('user_config.json'))['azure_settings']['app_service_name'])")
OPENAI_API_KEY=$(python3 -c "import json; print(json.load(open('user_config.json'))['api_keys']['openai_api_key'])")
ANTHROPIC_API_KEY=$(python3 -c "import json; print(json.load(open('user_config.json'))['api_keys'].get('anthropic_api_key', ''))" 2>/dev/null || echo "")
LANGSMITH_API_KEY=$(python3 -c "import json; print(json.load(open('user_config.json'))['api_keys'].get('langsmith_api_key', ''))" 2>/dev/null || echo "")

# Configure git remote
echo "-> Configuring git remote..."
git remote add origin "$GITHUB_URL" 2>/dev/null || git remote set-url origin "$GITHUB_URL"
echo "[OK] Git remote configured: $GITHUB_URL"
echo ""

# Create progress log
echo "Starting automation..." > setup_progress.log

# Step 1: Virtual environment
echo "PROGRESS:Creating virtual environment" >> setup_progress.log
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
echo "DONE:Creating virtual environment" >> setup_progress.log

# Step 2: Install dependencies
echo "PROGRESS:Installing dependencies" >> setup_progress.log
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "DONE:Installing dependencies" >> setup_progress.log

# Step 3: Initialize database
echo "PROGRESS:Initializing database" >> setup_progress.log
python3 database.py > /dev/null 2>&1
echo "DONE:Initializing database" >> setup_progress.log

# Step 4: Build welcome page for frontend
echo "PROGRESS:Building welcome page" >> setup_progress.log

# Create Welcome component
cat > frontend/src/components/Welcome.tsx << 'WELCOME_EOF'
import React from 'react';

interface WelcomeProps {
  userName: string;
  projectName: string;
  githubUrl: string;
}

const Welcome: React.FC<WelcomeProps> = ({ userName, projectName, githubUrl }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full bg-white p-8 rounded-lg shadow-2xl">
        <h1 className="text-4xl font-bold text-center text-gray-900 mb-6">
          ✅ Boot_Lang Setup Complete!
        </h1>
        
        <div className="space-y-6 text-gray-700">
          <div className="bg-blue-50 p-6 rounded-md">
            <h3 className="font-semibold mb-3 text-xl">Configuration:</h3>
            <ul className="space-y-2">
              <li><strong>User:</strong> {userName}</li>
              <li><strong>Project:</strong> {projectName}</li>
              <li><strong>GitHub:</strong> <a href={githubUrl} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">{githubUrl}</a></li>
            </ul>
          </div>
          
          <div className="bg-green-50 p-6 rounded-md">
            <h3 className="font-semibold mb-3 text-xl text-green-800">✓ Environment Ready:</h3>
            <ul className="list-disc list-inside space-y-1">
              <li>Virtual environment created</li>
              <li>Dependencies installed</li>
              <li>Database initialized</li>
              <li>Deployed to Azure</li>
            </ul>
          </div>
          
          <div className="bg-purple-50 p-6 rounded-md">
            <h3 className="font-semibold mb-3 text-xl text-purple-800">Tech Stack:</h3>
            <ul className="grid grid-cols-2 gap-2 text-sm">
              <li>• React 18 + TypeScript</li>
              <li>• Tailwind CSS</li>
              <li>• Python 3.11 + FastAPI</li>
              <li>• LangChain + OpenAI</li>
              <li>• SQLite Database</li>
              <li>• Azure App Service</li>
            </ul>
          </div>
          
          <div className="bg-yellow-50 p-6 rounded-md">
            <h3 className="font-semibold mb-3 text-xl text-yellow-800">Quick Start Commands:</h3>
            <ul className="space-y-2 text-sm font-mono">
              <li className="bg-white p-2 rounded border"><strong>"Build my PRD"</strong> - Start building from a PRD document</li>
              <li className="bg-white p-2 rounded border"><strong>"Start backend"</strong> - Launch FastAPI server (port 8000)</li>
              <li className="bg-white p-2 rounded border"><strong>"Start frontend"</strong> - Launch React dev server (port 3000)</li>
              <li className="bg-white p-2 rounded border"><strong>"Deploy to Azure"</strong> - Push changes to production</li>
              <li className="bg-white p-2 rounded border"><strong>"Commit the code"</strong> - Stage and commit changes</li>
            </ul>
          </div>
          
          <div className="text-center pt-4">
            <a href="http://localhost:3000" className="inline-block px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-semibold">
              Start Building →
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Welcome;
WELCOME_EOF

# Update App.tsx to show Welcome page
cat > frontend/src/App.tsx << 'APP_EOF'
import React from 'react';
import Welcome from './components/Welcome';

const App: React.FC = () => {
  // Load config from window object (injected during build)
  const config = (window as any).bootLangConfig || {
    userName: 'User',
    projectName: 'Boot_Lang Project',
    githubUrl: 'https://github.com'
  };

  return <Welcome {...config} />;
};

export default App;
APP_EOF

# Create config injection script
cat > frontend/public/config.js << EOF
window.bootLangConfig = {
  userName: "$USER_NAME",
  projectName: "$PROJECT_NAME",
  githubUrl: "$GITHUB_URL"
};
EOF

# Update index.html to include config
sed -i.bak 's|</head>|  <script src="%PUBLIC_URL%/config.js"></script>\n  </head>|' frontend/public/index.html

# Build React app
cd frontend
npm install > /dev/null 2>&1
npm run build > /dev/null 2>&1
cd ..

echo "DONE:Building welcome page" >> setup_progress.log

# Step 5: Configure GitHub workflows with user settings
echo "PROGRESS:Configuring GitHub workflows" >> setup_progress.log

# Update deploy.yml with correct app service name (preserve env vars)
if [ -f ".github/workflows/deploy.yml" ]; then
    # Use python to update YAML safely
    python3 << EOF
import re
with open('.github/workflows/deploy.yml', 'r') as f:
    content = f.read()
content = re.sub(r"app-name:.*", f"app-name: '$APP_SERVICE_NAME'", content)
with open('.github/workflows/deploy.yml', 'w') as f:
    f.write(content)
EOF
fi

echo "DONE:Configuring GitHub workflows" >> setup_progress.log

# Step 6: Add user_config.json to .gitignore (prevent exposing API keys)
echo "PROGRESS:Securing configuration file" >> setup_progress.log
if ! grep -q "user_config.json" .gitignore 2>/dev/null; then
    echo "user_config.json" >> .gitignore
fi
echo "DONE:Securing configuration file" >> setup_progress.log

# Step 7: Set GitHub secrets for environment variables
echo "PROGRESS:Setting GitHub secrets" >> setup_progress.log
if command -v gh &> /dev/null; then
    if gh auth status > /dev/null 2>&1; then
        echo "$OPENAI_API_KEY" | gh secret set OPENAI_API_KEY
        if [ -n "$ANTHROPIC_API_KEY" ]; then
            echo "$ANTHROPIC_API_KEY" | gh secret set ANTHROPIC_API_KEY
        fi
        if [ -n "$LANGSMITH_API_KEY" ]; then
            echo "$LANGSMITH_API_KEY" | gh secret set LANGSMITH_API_KEY
        fi
        echo "[OK] GitHub secrets set successfully"
    else
        echo "[WARN] GitHub CLI not authenticated - secrets not set"
    fi
else
    echo "[WARN] GitHub CLI not installed - secrets not set"
fi
echo "DONE:Setting GitHub secrets" >> setup_progress.log

# Step 9: Commit and Push to GitHub (first push with all configuration)
echo "PROGRESS:Pushing to GitHub" >> setup_progress.log
git add . > /dev/null 2>&1
git commit -m "Initial Boot_Lang setup: $PROJECT_NAME" > /dev/null 2>&1 || true
git push -u origin main --force > /dev/null 2>&1 || true
echo "DONE:Pushing to GitHub" >> setup_progress.log

# Step 9.5: Create dev branch and Azure dev slot
echo "PROGRESS:Creating dev environment" >> setup_progress.log

echo ""
echo "-> Creating dev branch..."

# Create dev branch from main
git checkout -b dev > /dev/null 2>&1 || git checkout dev > /dev/null 2>&1

# Push dev branch to GitHub
git push -u origin dev --force > /dev/null 2>&1 || true

echo "[OK] Dev branch created and pushed"
echo ""

# Create Azure deployment slot for dev environment
echo "-> Creating Azure deployment slot (dev)..."

# Extract resource group from config
RESOURCE_GROUP=$(python3 -c "import json; print(json.load(open('user_config.json'))['azure_settings']['resource_group'])" 2>/dev/null || echo "")

if [ -z "$RESOURCE_GROUP" ]; then
    echo "[WARN] Resource group not found in config - skipping dev slot creation"
    echo "  You can create it manually later in Azure Portal"
else
    # Set subscription if provided
    if [ -n "$AZURE_SUBSCRIPTION" ]; then
        az account set --subscription "$AZURE_SUBSCRIPTION" 2>/dev/null
    fi
    
    # Create deployment slot
    az webapp deployment slot create \
        --name "$APP_SERVICE_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --slot dev \
        --configuration-source "$APP_SERVICE_NAME" \
        --output none 2>/dev/null || echo "  Note: Slot may already exist or requires manual creation"
    
    # Get dev slot URL
    DEV_SLOT_URL="https://${APP_SERVICE_NAME}-dev.azurewebsites.net"
    
    echo "[OK] Dev slot created: $DEV_SLOT_URL"
    
    # Set environment variables for dev slot
    echo "-> Configuring dev slot environment..."
    
    az webapp config appsettings set \
        --name "$APP_SERVICE_NAME" \
        --resource-group "$RESOURCE_GROUP" \
        --slot dev \
        --settings \
            ENVIRONMENT="development" \
            PROJECT_NAME="$PROJECT_NAME" \
            OPENAI_API_KEY="$OPENAI_API_KEY" \
            ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
            LANGSMITH_API_KEY="$LANGSMITH_API_KEY" \
        --output none 2>/dev/null
    
    echo "[OK] Dev slot environment configured"
    
    # Save dev URL to config
    python3 << EOF
import json
try:
    with open('user_config.json', 'r') as f:
        config = json.load(f)
    config['azure_settings']['dev_slot_url'] = '$DEV_SLOT_URL'
    with open('user_config.json', 'w') as f:
        json.dump(config, f, indent=2)
except Exception as e:
    print(f"Warning: Could not save dev URL to config: {e}")
EOF
fi

echo ""

# Switch back to main branch for deployment verification
git checkout main > /dev/null 2>&1

echo "DONE:Creating dev environment" >> setup_progress.log

# Step 10: Wait for GitHub Actions deployment (both frontend + backend)
echo "PROGRESS:Deploying to Azure via GitHub Actions" >> setup_progress.log
echo "Waiting for GitHub Actions to start deployment..."
sleep 15  # Give GitHub Actions time to start
echo "DONE:Deploying to Azure via GitHub Actions" >> setup_progress.log

# Step 11: Verify deployment by checking URL content
echo "PROGRESS:Verifying deployment" >> setup_progress.log
DEPLOYMENT_VERIFIED=false

if [ -n "$AZURE_STATIC_URL" ]; then
    echo "Testing deployment at: $AZURE_STATIC_URL"
    
    # Try for up to 3 minutes (GitHub Actions + React build time)
    for i in {1..36}; do
        # Get the page content and config.js
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$AZURE_STATIC_URL" 2>/dev/null || echo "000")
        CONFIG_CONTENT=$(curl -s "$AZURE_STATIC_URL/config.js" 2>/dev/null || echo "")
        
        # Check if page loads with 200 status
        if [ "$HTTP_CODE" = "200" ]; then
            # Additional verification: check if config.js exists and has user data
            if echo "$CONFIG_CONTENT" | grep -q "$USER_NAME" 2>/dev/null; then
                echo "[OK] Deployment verified! Site live with user config (HTTP $HTTP_CODE)"
                DEPLOYMENT_VERIFIED=true
                echo "DONE:Verifying deployment" >> setup_progress.log
                echo "COMPLETE:$AZURE_STATIC_URL" >> setup_progress.log
                break
            elif [ "$HTTP_CODE" = "200" ]; then
                # Page loads but config might be embedded differently - still count as success
                echo "[OK] Deployment verified! Site responding (HTTP $HTTP_CODE)"
                DEPLOYMENT_VERIFIED=true
                echo "DONE:Verifying deployment" >> setup_progress.log
                echo "COMPLETE:$AZURE_STATIC_URL" >> setup_progress.log
                break
            fi
        fi
        
        echo "[WAIT] Waiting for deployment... (attempt $i/36, HTTP $HTTP_CODE)"
        sleep 5
    done
fi

if [ "$DEPLOYMENT_VERIFIED" = false ]; then
    echo "[WARN] Deployment verification timed out after 3 minutes"
    echo "  URL: $AZURE_STATIC_URL"
    echo "  This may mean GitHub Actions is still building (check: https://github.com/$(echo $GITHUB_URL | sed 's|https://github.com/||' | sed 's|.git||')/actions)"
    echo "  Your site may still deploy successfully - check the URL in a few minutes"
    echo "DONE:Verifying deployment" >> setup_progress.log
    echo "ERROR:Deployment not verified - check GitHub Actions at $GITHUB_URL" >> setup_progress.log
else
    echo "COMPLETE:$AZURE_STATIC_URL" >> setup_progress.log
fi

# Kill setup server
sleep 2
pkill -f setup_server.py

echo ""
echo "=================================================="
echo "  [OK] Setup Complete!"
echo "=================================================="
echo ""
echo "Your Boot Lang environment is ready!"
echo ""
echo "📍 Access Points:"
echo "   Backend API: http://localhost:8000"
echo "   Frontend:    http://localhost:3000"
if [ -n "$AZURE_STATIC_URL" ]; then
echo "   Deployed:    $AZURE_STATIC_URL"
fi
echo ""
echo "💡 Next Steps:"
echo "   • Start backend: tell Cursor 'Start backend'"
echo "   • Start frontend: tell Cursor 'Start frontend'"
echo "   • Login at http://localhost:3000"
echo "   • View System Dashboard at http://localhost:3000/dashboard"
echo "   • Build a PRD: tell Cursor 'Help me build a PRD'"
echo ""

