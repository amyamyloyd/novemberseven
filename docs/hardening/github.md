# Boot_Lang User Onboarding Process

## Goal

The goal of this process is to provide an easy, guided workflow for non-technical users to:
1. Download and configure Cursor IDE
2. Install necessary extensions (GitHub, Azure)
3. Complete initial setup and configuration
4. Test the deployment process to both staging and production environments
5. Verify successful connection to GitHub and Azure

This ensures users have a working development and deployment pipeline before building their first POC.

---

## Key Steps

### Email 1: Onboarding

Users receive initial setup instructions:

- **Link to download Cursor**
- **Instructions: Install GitHub + Azure extensions**
- **Instructions: Authenticate with GitHub + Azure in Cursor**
- **Instructions: Create new GitHub repo**
- **Instructions: Create Azure subscription/resource group**

### Email 2: Repo Access

Users receive access to the boot_lang scaffold:

- **Invite link to download boot_lang repo**
- **User copies repo URL**
- **User uses Cursor's clone function**

### After Clone

User runs the welcome script:

```bash
./welcome.sh
```

### Welcome Script Detects New User

The script launches setup backend (web form on localhost:8001) and collects:

- User info (name, project name)
- GitHub repo URL (their new repo)
- Azure credentials (app service, resource group, subscription)
- API keys (OpenAI, MongoDB Atlas connection string)

### User Clicks "Setup"

Automation begins:

- **Creates `dev` + `main` branches**
- **Builds simple welcome page + login**
- **Deploys to Azure:**
  - **Dev**: `https://myapp-staging.azurewebsites.net`
  - **Prod**: `https://myapp.azurewebsites.net`
- **Both branches include admin page with:**
  - Database viewer (tables + contents)
  - Stats dashboard
  - Links to MongoDB Atlas

### User Sees Success

Confirmation screen displays:

- "✅ Dev site: [URL]"
- "✅ Prod site: [URL]"
- "Next: Build your PRD → [localhost:3000/prd]"

---

## Update Process

### Scaffold Updates via Email

When new versions of boot_lang are released, users receive update notifications:

**Email: "Boot_Lang Update Available"**

Content includes:
- Version number
- Summary of changes (new features, bug fixes, improved rules)
- Simple update instruction: "Tell Cursor: 'Update scaffold'"

### Update Execution

User runs update script:

```bash
./update.sh
```

Or tells Cursor:
```
"Update scaffold"
```

**What happens:**
1. Script fetches latest version from boot_lang repo
2. Shows changelog and list of files to be updated
3. Asks user for confirmation
4. Updates scaffold files (.cursorrules, agent prompts, docs)
5. Preserves all user POCs and custom code
6. Updates version tracking file

**User receives confirmation:**
- "✅ Updated to v1.2.0"
- "✅ Cursor rules updated"
- "✅ Agent prompts updated"
- "Your POCs are safe and unchanged"

---

## Verification Points

This process verifies:

1. ✅ **Cursor installed and configured**
2. ✅ **GitHub extension working** (can clone, push, pull)
3. ✅ **Azure extension working** (can deploy, view logs)
4. ✅ **GitHub connection successful** (repo created, branches pushed)
5. ✅ **Azure deployment successful** (both staging and prod live)
6. ✅ **Database connection working** (MongoDB Atlas accessible)
7. ✅ **Authentication system working** (login page functional)
8. ✅ **Admin panel working** (can view database contents)

By completing this process, users confirm their entire development and deployment pipeline is operational before building their first POC application.