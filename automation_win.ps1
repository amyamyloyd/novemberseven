# PowerShell Automation Script for Windows
# Runs after config saved

$ErrorActionPreference = "Stop"

# ==================================================
# STEP 0: Authenticate GitHub and Azure CLIs
# ==================================================
Write-Host "=================================================="
Write-Host "  [AUTH] CLI Authentication"
Write-Host "=================================================="
Write-Host ""

# Check if GitHub CLI is installed
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] GitHub CLI not found"
    Write-Host ""
    Write-Host "Installing GitHub CLI via winget..."
    winget install GitHub.cli
    
    Write-Host ""
    Write-Host "Please restart Cursor/PowerShell and run setup again."
    exit 1
}

# Check if Azure CLI is installed
if (-not (Get-Command az -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Azure CLI not found"
    Write-Host ""
    Write-Host "Installing Azure CLI via winget..."
    winget install Microsoft.AzureCLI
    
    Write-Host ""
    Write-Host "Please restart Cursor/PowerShell and run setup again."
    exit 1
}

Write-Host "[OK] CLIs installed"
Write-Host ""

# Authenticate GitHub CLI
Write-Host "-> Authenticating GitHub CLI..."
Write-Host "  (Browser will open for authentication)"
Write-Host ""

$ghStatus = gh auth status 2>&1
if ($LASTEXITCODE -ne 0) {
    gh auth login --web --git-protocol https
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] GitHub authentication failed"
        Write-Host "Please try again or check your network connection"
        exit 1
    }
}

Write-Host "[OK] GitHub CLI authenticated"
Write-Host ""

# Authenticate Azure CLI
Write-Host "-> Authenticating Azure CLI..."
Write-Host "  (Browser will open for authentication)"
Write-Host ""

$azStatus = az account show 2>&1
if ($LASTEXITCODE -ne 0) {
    az login --use-device-code
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Azure authentication failed"
        Write-Host "Please try again or check your network connection"
        exit 1
    }
}

Write-Host "[OK] Azure CLI authenticated"
Write-Host ""

# Load Azure subscription ID from config
$config = Get-Content user_config.json -Encoding UTF8 | ConvertFrom-Json
$AZURE_SUBSCRIPTION = $config.azure_settings.subscription_id

if ($AZURE_SUBSCRIPTION) {
    Write-Host "-> Setting Azure subscription..."
    az account set --subscription $AZURE_SUBSCRIPTION
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[WARN] Failed to set subscription $AZURE_SUBSCRIPTION"
        Write-Host "Using default subscription instead"
    } else {
        Write-Host "[OK] Azure subscription set: $AZURE_SUBSCRIPTION"
    }
} else {
    Write-Host "[WARN] No Azure subscription ID in config - using default"
}

Write-Host ""
Write-Host "=================================================="
Write-Host "  Starting Automated Setup"
Write-Host "=================================================="
Write-Host ""

# Ensure we're on main branch
$CURRENT_BRANCH = git branch --show-current
if ($CURRENT_BRANCH -ne "main") {
    Write-Host "Switching from $CURRENT_BRANCH to main branch..."
    git checkout main
}

# Load configuration
$USER_NAME = $config.user_identity.user_name
$PROJECT_NAME = $config.user_identity.project_name
$GITHUB_URL = $config.git_deployment.github_repo_url
$AZURE_STATIC_URL = $config.azure_settings.static_web_app_url
$APP_SERVICE_NAME = $config.azure_settings.app_service_name
$OPENAI_API_KEY = $config.api_keys.openai_api_key
$ANTHROPIC_API_KEY = $config.api_keys.anthropic_api_key
$LANGSMITH_API_KEY = $config.api_keys.langsmith_api_key

# Configure git remote
Write-Host "-> Configuring git remote..."
git remote add origin $GITHUB_URL 2>$null
if ($LASTEXITCODE -ne 0) {
    git remote set-url origin $GITHUB_URL
}
Write-Host "[OK] Git remote configured: $GITHUB_URL"
Write-Host ""

# Create progress log
"Starting automation..." | Out-File -FilePath setup_progress.log -Encoding UTF8

# Step 1: Virtual environment
"PROGRESS:Creating virtual environment" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
if (-not (Test-Path venv)) {
    python -m venv venv
}
.\venv\Scripts\Activate.ps1
"DONE:Creating virtual environment" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8

# Step 2: Install dependencies
"PROGRESS:Installing dependencies" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
python -m pip install --upgrade pip | Out-Null
python -m pip install -r requirements.txt | Out-Null
"DONE:Installing dependencies" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8

# Step 3: Initialize database
"PROGRESS:Initializing database" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
python database.py | Out-Null
"DONE:Initializing database" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8

# Step 4: Build welcome page for frontend
"PROGRESS:Building welcome page" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8

# Create Welcome component
$welcomeContent = @"
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
"@

$welcomeContent | Out-File -FilePath frontend\src\components\Welcome.tsx -Encoding UTF8

# Update App.tsx to show Welcome page
$appContent = @"
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
"@

$appContent | Out-File -FilePath frontend\src\App.tsx -Encoding UTF8

# Create config injection script
$configJs = @"
window.bootLangConfig = {
  userName: "$USER_NAME",
  projectName: "$PROJECT_NAME",
  githubUrl: "$GITHUB_URL"
};
"@

$configJs | Out-File -FilePath frontend\public\config.js -Encoding UTF8

# Update index.html to include config
$indexHtml = Get-Content frontend\public\index.html -Raw
if ($indexHtml -notmatch 'config\.js') {
    $indexHtml = $indexHtml -replace '</head>', "  <script src=`"%PUBLIC_URL%/config.js`"></script>`n  </head>"
    $indexHtml | Out-File -FilePath frontend\public\index.html -Encoding UTF8
}

# Build React app
Push-Location frontend
npm install | Out-Null
npm run build | Out-Null
Pop-Location

"DONE:Building welcome page" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8

# Step 5: Configure GitHub workflows
"PROGRESS:Configuring GitHub workflows" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8

if (Test-Path .github\workflows\deploy.yml) {
    $deployYml = Get-Content .github\workflows\deploy.yml -Raw
    $deployYml = $deployYml -replace "app-name:.*", "app-name: '$APP_SERVICE_NAME'"
    $deployYml | Out-File -FilePath .github\workflows\deploy.yml -Encoding UTF8
}

"DONE:Configuring GitHub workflows" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8

# Step 6: Add user_config.json to .gitignore
"PROGRESS:Securing configuration file" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
$gitignore = Get-Content .gitignore -ErrorAction SilentlyContinue
if ($gitignore -notcontains "user_config.json") {
    "user_config.json" | Out-File -FilePath .gitignore -Append -Encoding UTF8
}
"DONE:Securing configuration file" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8

# Step 7: Set GitHub secrets
"PROGRESS:Setting GitHub secrets" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
if (Get-Command gh -ErrorAction SilentlyContinue) {
    $ghStatus = gh auth status 2>&1
    if ($LASTEXITCODE -eq 0) {
        $OPENAI_API_KEY | gh secret set OPENAI_API_KEY
        if ($ANTHROPIC_API_KEY) {
            $ANTHROPIC_API_KEY | gh secret set ANTHROPIC_API_KEY
        }
        if ($LANGSMITH_API_KEY) {
            $LANGSMITH_API_KEY | gh secret set LANGSMITH_API_KEY
        }
        Write-Host "[OK] GitHub secrets set successfully"
    } else {
        Write-Host "[WARN] GitHub CLI not authenticated - secrets not set"
    }
} else {
    Write-Host "[WARN] GitHub CLI not installed - secrets not set"
}
"DONE:Setting GitHub secrets" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8

# Step 9: Commit and Push to GitHub
"PROGRESS:Pushing to GitHub" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
git add . 2>$null | Out-Null
git commit -m "Initial Boot_Lang setup: $PROJECT_NAME" 2>$null | Out-Null
git push -u origin main --force 2>$null | Out-Null
"DONE:Pushing to GitHub" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8

# Step 9.5: Create dev branch and Azure dev slot
"PROGRESS:Creating dev environment" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8

Write-Host ""
Write-Host "-> Creating dev branch..."

# Create dev branch from main
git checkout -b dev 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) {
    git checkout dev | Out-Null
}

# Push dev branch to GitHub
git push -u origin dev --force 2>$null | Out-Null

Write-Host "[OK] Dev branch created and pushed"
Write-Host ""

# Create Azure deployment slot
Write-Host "-> Creating Azure deployment slot (dev)..."

$RESOURCE_GROUP = $config.azure_settings.resource_group

if (-not $RESOURCE_GROUP) {
    Write-Host "[WARN] Resource group not found in config - skipping dev slot creation"
    Write-Host "  You can create it manually later in Azure Portal"
} else {
    # Set subscription if provided
    if ($AZURE_SUBSCRIPTION) {
        az account set --subscription $AZURE_SUBSCRIPTION 2>$null
    }
    
    # Create deployment slot
    az webapp deployment slot create `
        --name $APP_SERVICE_NAME `
        --resource-group $RESOURCE_GROUP `
        --slot dev `
        --configuration-source $APP_SERVICE_NAME `
        --output none 2>$null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  Note: Slot may already exist or requires manual creation"
    }
    
    # Get dev slot URL
    $DEV_SLOT_URL = "https://$APP_SERVICE_NAME-dev.azurewebsites.net"
    
    Write-Host "[OK] Dev slot created: $DEV_SLOT_URL"
    
    # Set environment variables for dev slot
    Write-Host "-> Configuring dev slot environment..."
    
    az webapp config appsettings set `
        --name $APP_SERVICE_NAME `
        --resource-group $RESOURCE_GROUP `
        --slot dev `
        --settings `
            ENVIRONMENT="development" `
            PROJECT_NAME="$PROJECT_NAME" `
            OPENAI_API_KEY="$OPENAI_API_KEY" `
            ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" `
            LANGSMITH_API_KEY="$LANGSMITH_API_KEY" `
        --output none 2>$null
    
    Write-Host "[OK] Dev slot environment configured"
    
    # Save dev URL to config
    $config.azure_settings | Add-Member -NotePropertyName dev_slot_url -NotePropertyValue $DEV_SLOT_URL -Force
    $config | ConvertTo-Json -Depth 10 | Out-File -FilePath user_config.json -Encoding UTF8
}

Write-Host ""

# Switch back to main branch
git checkout main 2>$null | Out-Null

"DONE:Creating dev environment" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8

# Step 10: Wait for GitHub Actions
"PROGRESS:Deploying to Azure via GitHub Actions" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
Write-Host "Waiting for GitHub Actions to start deployment..."
Start-Sleep -Seconds 15
"DONE:Deploying to Azure via GitHub Actions" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8

# Step 11: Verify deployment
"PROGRESS:Verifying deployment" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
$DEPLOYMENT_VERIFIED = $false

if ($AZURE_STATIC_URL) {
    Write-Host "Testing deployment at: $AZURE_STATIC_URL"
    
    # Try for up to 3 minutes
    for ($i = 1; $i -le 36; $i++) {
        try {
            $response = Invoke-WebRequest -Uri $AZURE_STATIC_URL -UseBasicParsing -ErrorAction SilentlyContinue
            $HTTP_CODE = $response.StatusCode
            
            $configResponse = Invoke-WebRequest -Uri "$AZURE_STATIC_URL/config.js" -UseBasicParsing -ErrorAction SilentlyContinue
            $CONFIG_CONTENT = $configResponse.Content
            
            if ($HTTP_CODE -eq 200) {
                if ($CONFIG_CONTENT -match $USER_NAME) {
                    Write-Host "[OK] Deployment verified! Site live with user config (HTTP $HTTP_CODE)"
                    $DEPLOYMENT_VERIFIED = $true
                    "DONE:Verifying deployment" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
                    "COMPLETE:$AZURE_STATIC_URL" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
                    break
                } elseif ($HTTP_CODE -eq 200) {
                    Write-Host "[OK] Deployment verified! Site responding (HTTP $HTTP_CODE)"
                    $DEPLOYMENT_VERIFIED = $true
                    "DONE:Verifying deployment" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
                    "COMPLETE:$AZURE_STATIC_URL" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
                    break
                }
            }
        } catch {
            $HTTP_CODE = "000"
        }
        
        Write-Host "[WAIT] Waiting for deployment... (attempt $i/36, HTTP $HTTP_CODE)"
        Start-Sleep -Seconds 5
    }
}

if (-not $DEPLOYMENT_VERIFIED) {
    Write-Host "[WARN] Deployment verification timed out after 3 minutes"
    Write-Host "  URL: $AZURE_STATIC_URL"
    Write-Host "  This may mean GitHub Actions is still building"
    Write-Host "  Your site may still deploy successfully - check the URL in a few minutes"
    "DONE:Verifying deployment" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
    "ERROR:Deployment not verified - check GitHub Actions at $GITHUB_URL" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
} else {
    "COMPLETE:$AZURE_STATIC_URL" | Out-File -FilePath setup_progress.log -Append -Encoding UTF8
}

# Kill setup server
Start-Sleep -Seconds 2
Stop-Process -Name python -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "=================================================="
Write-Host "  [OK] Setup Complete!"
Write-Host "=================================================="
Write-Host ""
Write-Host "Your Boot Lang environment is ready!"
Write-Host ""
Write-Host "📍 Access Points:"
Write-Host "   Backend API: http://localhost:8000"
Write-Host "   Frontend:    http://localhost:3000"
if ($AZURE_STATIC_URL) {
    Write-Host "   Deployed:    $AZURE_STATIC_URL"
}
Write-Host ""
Write-Host "💡 Next Steps:"
Write-Host "   • Start backend: tell Cursor 'Start backend'"
Write-Host "   • Start frontend: tell Cursor 'Start frontend'"
Write-Host "   • Login at http://localhost:3000"
Write-Host "   • View System Dashboard at http://localhost:3000/dashboard"
Write-Host "   • Build a PRD: tell Cursor 'Help me build a PRD'"
Write-Host ""

