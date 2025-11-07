# Cursor-Ready Implementation Plan

## File Structure
```
/automation_service.py          [MODIFY - Add 4 new methods]
/.github/workflows/             [CREATE - New directory]
/.github/workflows/deploy-dev.yml    [CREATE]
/.github/workflows/deploy-prod.yml   [CREATE]
/templates/                     [CREATE - New directory]
/templates/coming-soon-dev.html [CREATE]
/templates/coming-soon-prod.html [CREATE]
```

---

## Task 1: Add Azure Resource Provisioning Method

**File:** `automation_service.py`

**Location:** After `setup_azure_subscription()` method (around line 380)

**Instruction to Cursor:**
```
Add a new method called provision_azure_resources() that:
1. Creates Azure resource group using az group create
2. Creates App Service plan (Linux, B1 SKU, Python 3.11)
3. Creates Web App for backend
4. Creates deployment slot named "dev"
5. Creates deployment slot named "prod"
6. Creates Static Web App for frontend
7. Configures environment variables for dev slot (ENVIRONMENT=development, PROJECT_NAME, OPENAI_API_KEY)
8. Configures environment variables for prod slot (ENVIRONMENT=production, PROJECT_NAME, OPENAI_API_KEY)
9. Saves all URLs to config: backend_dev_url, backend_prod_url, backend_main_url, static_web_app_url
10. Uses self._log() for console output and self._log_progress() for status tracking
11. Uses self._run_command() for all az CLI commands with --output none flag
12. All resource names should use self.config['azure_settings'] values
```

---

## Task 2: Add GitHub Workflows Creation Method

**File:** `automation_service.py`

**Location:** After `provision_azure_resources()` method

**Instruction to Cursor:**
```
Add a new method called create_github_workflows() that:
1. Creates directory .github/workflows using Path().mkdir(parents=True, exist_ok=True)
2. Creates deploy-dev.yml workflow that:
   - Triggers on push to dev branch
   - Uses ubuntu-latest runner
   - Checks out code
   - Sets up Python 3.11
   - Installs dependencies from requirements.txt
   - Deploys to Azure Web App dev slot using azure/webapps-deploy@v2
   - Uses secret AZURE_DEV_PUBLISH_PROFILE
   - App name from self.config['azure_settings']['app_service_name']
3. Creates deploy-prod.yml workflow that:
   - Triggers on push to prod branch  
   - Same steps as dev but deploys to prod slot
   - Uses secret AZURE_PROD_PUBLISH_PROFILE
4. Stages workflow files with git add .github/workflows/
5. Uses self._log() for output and self._log_progress() for tracking
```

---

## Task 3: Add Azure Publish Profiles Secret Setup Method

**File:** `automation_service.py`

**Location:** After `create_github_workflows()` method

**Instruction to Cursor:**
```
Add a new method called set_azure_publish_profiles() that:
1. Gets app_name and resource_group from self.config['azure_settings']
2. Gets GitHub CLI path using self._find_gh_command()
3. Gets dev slot publish profile using az webapp deployment list-publishing-profiles with --slot dev --xml flags
4. Gets prod slot publish profile using az webapp deployment list-publishing-profiles with --slot prod --xml flags
5. Sets GitHub secret AZURE_DEV_PUBLISH_PROFILE using gh secret set command with dev profile
6. Sets GitHub secret AZURE_PROD_PUBLISH_PROFILE using gh secret set command with prod profile
7. Uses self._run_command() with capture_output=True to get XML profiles
8. Uses self._log() for console output and self._log_progress() for tracking
```

---

## Task 4: Add Coming Soon Pages Creation Method

**File:** `automation_service.py`

**Location:** After `set_azure_publish_profiles()` method

**Instruction to Cursor:**
```
Add a new method called create_coming_soon_pages() that:
1. Creates templates/ directory using Path('templates').mkdir(exist_ok=True)
2. Creates coming-soon-dev.html with:
   - Simple HTML page with title "Dev Environment - Coming Soon"
   - Styled with centered layout, gradient background using Tailwind colors
   - Shows "🚧 Development Environment" heading
   - Shows project name from self.config['user_identity']['project_name']
   - Shows "Your app is being built..." message
3. Creates coming-soon-prod.html with:
   - Simple HTML page with title "Production - Coming Soon"
   - Different gradient background
   - Shows "🚀 Coming Soon" heading
   - Shows project name
   - Shows "Your production app will be here soon!" message
4. Uses Path().write_text() to write files
5. Stages files with git add templates/
6. Uses self._log() for output and self._log_progress() for tracking
```

---

## Task 5: Update run_automation() Method Flow

**File:** `automation_service.py`

**Location:** `run_automation()` method (around line 737)

**Instruction to Cursor:**
```
Modify the run_automation() method to call new methods in this order:
1. After setup_azure_subscription() - add call to provision_azure_resources()
2. After provision_azure_resources() - add call to create_github_workflows()
3. After create_github_workflows() - add call to set_azure_publish_profiles()
4. After set_azure_publish_profiles() - add call to create_coming_soon_pages()
5. Keep all existing method calls in their current positions
6. The flow should be: authenticate Azure → provision resources → create workflows → set secrets → create pages → setup git → build welcome page → commit/push

Do not modify any other parts of run_automation(), only add these 4 method calls in the specified sequence.
```

---

## Task 6: Fix create_dev_environment() Method

**File:** `automation_service.py`

**Location:** `create_dev_environment()` method (around line 573)

**Instruction to Cursor:**
```
The create_dev_environment() method tries to create a dev slot that should already exist from provision_azure_resources(). 

Modify this method to:
1. Remove the az webapp deployment slot create commands (lines that create dev slot)
2. Keep only the configuration steps that set environment variables for the dev slot
3. Keep the part that saves dev_slot_url to config
4. Keep the git checkout dev and git push commands at the end
5. Update log messages to say "Configuring dev environment" instead of "Creating dev environment"
```

---

## Testing Checklist for Cursor

After implementing all changes, verify:

```
☐ automation_service.py has 4 new methods added
☐ .github/workflows/deploy-dev.yml exists and references correct app name
☐ .github/workflows/deploy-prod.yml exists and references correct app name  
☐ templates/coming-soon-dev.html exists with proper HTML structure
☐ templates/coming-soon-prod.html exists with proper HTML structure
☐ run_automation() calls new methods in correct order
☐ create_dev_environment() no longer tries to create dev slot
☐ All new methods use self._log() and self._log_progress()
☐ All new methods use self._run_command() for shell commands
☐ No syntax errors in Python code
```

---

## Execution Order for Cursor

1. **Start with Task 1** - Add provision_azure_resources() method
2. **Then Task 2** - Add create_github_workflows() method  
3. **Then Task 3** - Add set_azure_publish_profiles() method
4. **Then Task 4** - Add create_coming_soon_pages() method
5. **Then Task 5** - Update run_automation() to call all new methods
6. **Finally Task 6** - Fix create_dev_environment() to avoid duplicate slot creation

Each task is independent except Task 5 which integrates everything.