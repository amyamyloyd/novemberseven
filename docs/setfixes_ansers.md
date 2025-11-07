# Answers to Cursor's Questions

## Task 1: Azure Resource Provisioning

**1. Static Web App creation:**
- Source location: Not needed yet - we're just provisioning the resource
- Framework: Not needed - coming soon pages are plain HTML
- GitHub linking: NO - manual deployment for now, GitHub integration comes later
- Just create the empty Static Web App resource

**2. Resource existence:**
- **Resources should NOT exist** - this is brand new setup
- If resources exist, FAIL with clear error message telling user to delete them or use different names
- No checking/skipping - we want clean creation or failure

**3. Prod slot environment variables:**
- YES, same as dev but with `ENVIRONMENT=production`
- Full list: `ENVIRONMENT=production`, `PROJECT_NAME={project_name}`, `OPENAI_API_KEY={key}`

**4. Config values:**
- `OPENAI_API_KEY` from `self.config['api_keys']['openai_api_key']`
- `PROJECT_NAME` from `self.config['user_identity']['project_name']`
- `region` from `self.config['azure_settings']['region']`
- `resource_group` from `self.config['azure_settings']['resource_group']`
- `app_service_name` from `self.config['azure_settings']['app_service_name']`

---

## Task 2: GitHub Workflows

**5. Existing workflow:**
- **IGNORE the existing `configure_github_workflows()` method completely** - it's part of the broken code
- Create NEW workflows from scratch (deploy-dev.yml and deploy-prod.yml)
- We're replacing the broken system, not updating it

**6. Backend deployment:**
- Just install dependencies from requirements.txt
- No build steps needed - Python backend is ready to run after pip install

**7. Frontend deployment:**
- **Ignore frontend deployment for now** - coming soon pages are backend-served
- Static Web App will be manually deployed later
- Focus only on backend (Web App) deployment to dev and prod slots

---

## Task 3: Azure Publish Profiles

**8. Existing method:**
- **IGNORE `set_azure_secrets()` method** - it's part of the broken code
- Create NEW `set_azure_publish_profiles()` method from scratch
- We need TWO secrets: `AZURE_DEV_PUBLISH_PROFILE` and `AZURE_PROD_PUBLISH_PROFILE`

**9. Error handling:**
- If slots don't exist, FAIL with clear error
- This method runs AFTER `provision_azure_resources()` so slots MUST exist
- No retry - if provisioning failed, we should have already stopped

---

## Task 4: Coming Soon Pages

**10. Deployment target:**
- Backend App Service (Web App) to both dev and prod SLOTS
- NOT Static Web App
- These are temporary backend-served HTML pages

**11. Purpose:**
- **Temporary placeholders** for confidence building
- Show user that Azure deployment is working
- Will be replaced when real app deploys

---

## Task 5: run_automation() Flow

**12. Error handling:**
- If `provision_azure_resources()` fails, **STOP immediately**
- Do NOT continue - everything depends on Azure resources existing
- Use existing error handling pattern (try/except returns False)

**13. Method order:**
- **DELETE or IGNORE existing `set_azure_secrets()` call**
- Replace with `set_azure_publish_profiles()`
- New order: provision → workflows → profiles → pages → git → commit

---

## Task 6: create_dev_environment()

**14. Fallback:**
- **NO fallback** - dev slot MUST already exist from `provision_azure_resources()`
- This method should ONLY configure the existing slot
- If slot doesn't exist, something went wrong - fail clearly

**15. Prod slot:**
- This method should be renamed or split
- Configure BOTH dev and prod slots in `provision_azure_resources()`
- This method becomes redundant - consider removing it entirely or making it only do git branch operations

---

## Additional Critical Clarifications

### Coming Soon Page Deployment
The coming soon pages should be:
1. Created in `templates/` directory
2. Committed to git
3. Pushed to dev branch → triggers deploy-dev.yml → deploys to dev slot
4. Pushed to prod branch → triggers deploy-prod.yml → deploys to prod slot
5. Backend serves these as index pages

### Simplified Flow
```
1. provision_azure_resources()     → Creates ALL Azure infrastructure
2. create_github_workflows()       → Creates workflow YAML files
3. set_azure_publish_profiles()    → Gets profiles, sets GitHub secrets
4. create_coming_soon_pages()      → Creates HTML files in templates/
5. [existing git setup]            → Sets up remote
6. [existing commit/push]          → Pushes to both branches, triggers workflows
```

### What to IGNORE from existing code
- `configure_github_workflows()` method - broken/incomplete
- `set_azure_secrets()` method - wrong approach
- `create_dev_environment()` slot creation logic - redundant
- Any code that assumes resources exist

Tell Cursor: **"This is a clean slate implementation. Ignore existing Azure/workflow code that doesn't work. We're building the correct flow from scratch."**