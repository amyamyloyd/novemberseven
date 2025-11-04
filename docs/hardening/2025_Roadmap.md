# Boot_Lang Scaffolding - Updated Requirements Checklist
## (Integrated with ChatGPT Deep Dive Features)

---

## **1. Project Structure & Initialization**

### **Existing**
* [x] Root directory structure (frontend/backend separation)
* [x] README with quick start guide
* [x] `.gitignore` properly configured for Python/React/Azure

### **MVP (New)**
* [ ] `.env.example` template with all required environment variables (MongoDB, Azure, GitHub, API keys)
* [ ] `welcome.sh` script that collects credentials and configures environment - in progress
* [ ] Setup server (localhost:8001) for credential collection form
* [ ] Automated git remote switching (boot_lang → user's repo)
* [ ] Initial push to user's GitHub repo (dev + main branches)
* [ ] **Lloyd agent integration during setup** (conversational wizard to guide user through configuration)
* [ ] **Two-path setup**: New users (guided signup + repo creation via GitHub API) vs Existing users (inline form with direct credentials)
* [ ] **Writes `.env` and `.saltair/config.json`** after setup completion
* [ ] **Installation diagnostics** - verify installations, connectivity, API validation
* [ ] **Post-setup confirmation screen** showing dev/prod URLs and next steps

### **V1**
* [ ] `update.sh` script for pulling scaffold updates
* [ ] Version tracking file (`.scaffold_version`)
* [ ] Automated dependency installation (pip, npm)
* [ ] **Interactive CLI wizard** (alternative to web form)
* [ ] **"Lloyd" conversational agent** for advanced setup with agents handling most configuration

### **V2**
* [ ] Validation of all credentials before proceeding
* [ ] Rollback mechanism if setup fails
* [ ] **Recovery script (`recover.sh`)** - re-authenticates GitHub, MongoDB, Azure if tokens expire
* [ ] **"Check All" command** - restarts all local services, re-validates environment
* [ ] **Auto-logging** (browser + local logs folder)
* [ ] **Daily heartbeat**: check system health, prompt password renewal

---

## **2. Backend (Python/FastAPI) Foundation**

### **Existing**
* [x] FastAPI app structure with proper routing
* [x] Environment configuration management (python-dotenv)
* [x] CORS configuration for local dev
* [x] Health check/status endpoints

### **MVP (Migration Required)**
* [ ] **MongoDB connection** (replace SQLite/SQLAlchemy)
* [ ] **PyMongo/Motor setup** for async MongoDB operations
* [ ] Database connection management & session handling (MongoDB)
* [ ] Common MongoDB models (User, metadata)
* [ ] Database initialization in welcome.sh (create collections, seed admin)
* [ ] **API routes to interact with installed CLIs** (`az`, `gh`, `mongosh`)

### **V1**
* [ ] Database migration utilities (if schema changes)
* [ ] Connection pooling configuration
* [ ] Retry logic for MongoDB connections

### **V2**
* [ ] Performance monitoring (query timing)
* [ ] Database backup/restore utilities
* [ ] Multi-database support (dev/test/prod databases)

---

## **3. Authentication System (Pre-built)**

### **Existing**
* [x] User registration endpoint
* [x] Login endpoint (JWT token generation)
* [x] Password hashing (bcrypt/passlib)
* [x] JWT token validation middleware
* [x] Protected route decorators/dependencies
* [x] Frontend auth context/hooks

### **MVP (Migration Required)**
* [ ] **Update all auth to use MongoDB** (replace SQLAlchemy User model)
* [ ] Token refresh mechanism
* [ ] Password reset functionality
* [ ] **Password-protected admin portal** (set on install; forced reset in 23 hours)
* [ ] **Default admin user created during setup**

### **V1**
* [ ] Email verification
* [ ] Rate limiting on login attempts
* [ ] Session management
* [ ] **Optional OAuth via GitHub for admin portal**

### **V2**
* [ ] OAuth integration (Google, GitHub)
* [ ] 2FA support
* [ ] Role-based permissions (beyond admin/user)

---

## **4. LangChain Integration**

### **Existing**
* [x] LangChain setup & configuration
* [x] OpenAI API key management
* [x] POC Agent implementation
* [x] Common prompt templates (poc_agent_prompts.json)
* [x] Memory/conversation management
* [x] Vector store integration (FAISS)

### **MVP (Improvements Needed)**
* [ ] **PRD Agent reads existing scaffold code** (auth.py, database.py, etc.)
* [ ] **Update agent to reference MongoDB** (not SQLite)
* [ ] **Generate test suites** in implementation plans
* [ ] **Generate user/technical documentation** in POC package
* [ ] **Complexity validation** ("Is this really a POC?")
* [ ] Save PRD to standardized location Cursor can find
* [ ] **Agent must be opinionated**: Push back on complexity, enforce stack, validate integration
* [ ] **Agent must enforce phased approach**: Forces incremental builds with testing between phases
* [ ] **PRD Agent creates 3 phase files**: `phase_1_frontend.md`, `phase_2_backend.md`, `phase_3_database.md`
* [ ] **Generates README with POC structure**
* [ ] **Packages everything as ZIP download**

### **V1**
* [ ] **Lloyd/Help agents integrated to the admin tools AND cursor directly**
* [ ] Agent suggests integrations with existing POCs
* [ ] Agent can update existing PRDs
* [ ] Context-aware suggestions based on project history
* [ ] **LangGraph implementation for dynamic agent switching** (Lloyd ⇄ Help ⇄ specialized agents)
* [ ] **Shared state management** across agents (session state, environment, credentials, active project)

### **V2**
* [ ] Multi-agent collaboration (separate agents for frontend/backend/database)
* [ ] Agent learns from successful POC patterns
* [ ] Custom agent training per user/company
* [ ] **Advanced specialized agents**: MongoDBSetupAgent, AzureAgent, GitHubAgent
* [ ] **PRD Builder flows that persist** across conversations and phases

---

## **5. Langflow Integration**

### **Existing**
* [x] Documentation on Langflow usage

### **MVP**
* [ ] Remove or deprecate (not critical for scaffold MVP)

### **V1**
* [ ] Langflow installation as optional add-on
* [ ] Example flows for common patterns

### **V2**
* [ ] Visual flow builder integration in PRD tool
* [ ] Pre-built flows for authentication, CRUD, etc.

---

## **6. Frontend (React/Tailwind)**

### **Existing**
* [x] Vite/Create React App setup
* [x] Tailwind configured & working
* [x] Authentication UI (login/register forms)
* [x] Protected route wrapper components
* [x] API client/service layer
* [x] Loading states & error handling patterns
* [x] Environment variable handling

### **MVP (New)**
* [ ] **Welcome page** with user info and quick links (GitHub, Azure, MongoDB dashboards)
* [ ] **Admin page/Admin Portal (localhost dashboard)** with:
  * [ ] **Service Overview cards** (GitHub, Azure, MongoDB, ChatGPT, Claude) - connection status, last action
  * [ ] **System Controls** - Start/Stop local services, rebuild venv, re-run diagnostics
  * [ ] **GitHub Section** - List repos, branches, last commits, PRs, pushes
  * [ ] **MongoDB Section** - View tables/collections, sample data, CRUD via CLI links
  * [ ] **Azure Section** - Show deployments, logs, monitors (if configured)
  * [ ] **Usage Stats** - Cursor tokens used, API activity, system health
  * [ ] **Chat & Help** - Embedded chatbot ("Lloyd") for Q&A, tutorials, contextual help
  * [ ] **Video Guides** - Quick access to how-to videos and best practices
  * [ ] Links to services and database viewer
  * [ ] Should incorporate high-level stats/dashboard stats via API to vendors
* [ ] **PRD Builder UI** (chat interface + file upload)
* [ ] Bookmarkable dev/prod URLs displayed after setup
* [ ] **Bootstrap/React frontend** (AdminLTE or custom CSS)

### **V1**
* [ ] **Database viewer component** (browse MongoDB collections)
* [ ] **Advanced agents to build monitoring/healthcheck dashboards**
* [ ] Deployment status dashboard
* [ ] Health check visualizations
* [ ] **Optional integration with SaltAIr central telemetry** (logins, activity)

### **V2**
* [ ] Visual query builder for MongoDB
* [ ] Log viewer
* [ ] Performance metrics dashboard

---

## **7. Common Utilities & Helpers**

### **Existing**
* [x] API response formatters
* [x] Error handling utilities
* [x] Logging setup
* [x] Input validation schemas (Pydantic)

### **MVP (Migration Required)**
* [ ] **MongoDB CRUD helper functions** (replace SQLAlchemy helpers)
* [ ] Date/time utilities
* [ ] File upload handling
* [ ] **SQLite or JSON for local persistence** (admin portal)

### **V1**
* [ ] Bulk operations utilities
* [ ] Data import/export helpers
* [ ] Query builders for common patterns

### **V2**
* [ ] Caching layer
* [ ] Background job utilities
* [ ] Email/notification helpers

---

## **8. Azure Deployment Automation**

### **Existing**
* [x] GitHub Actions workflow templates
* [x] Basic deployment documentation

### **MVP (Critical New Work)**
* [ ] **Azure CLI scripts to create all resources**:
  * [ ] Resource group
  * [ ] App Service plan
  * [ ] Backend web app
  * [ ] Staging slot
  * [ ] Static Web App (frontend)
* [ ] **Configure GitHub deployment** for both branches (dev → staging, main → prod)
* [ ] **Set environment variables** in Azure (MongoDB, API keys)
* [ ] **CORS configuration** for Azure
* [ ] **Deploy initial scaffold code** to both slots during welcome.sh
* [ ] **Health check verification** (curl test) after deployment
* [ ] **Report deployment URLs** to user
* [ ] **Confirmation screen displays**: "✅ Dev site: [URL]", "✅ Prod site: [URL]", "Next: Build your PRD → [localhost:3000/prd]"

### **V1**
* [ ] Azure cost estimation tool
* [ ] One-click slot swap (staging → production)
* [ ] Automated SSL certificate setup
* [ ] Custom domain configuration

### **V2**
* [ ] Multi-region deployment
* [ ] Auto-scaling configuration
* [ ] CDN setup for frontend
* [ ] Backup and disaster recovery

---

## **9. Git Workflow Automation**

### **Existing**
* [x] Branch naming conventions documented

### **MVP (New)**
* [ ] **Automated branch creation** (dev + main) in welcome.sh
* [ ] **Git remote switching** (boot_lang → user repo)
* [ ] **Initial commit and push** to user's repo
* [ ] **GitHub Actions setup** for both branches
* [ ] **PRD Agent guides branch creation** (`dev`, `main`, optional `feature`)

### **V1**
* [ ] Pre-commit hooks (linting, formatting)
* [ ] Commit message templates
* [ ] PR templates
* [ ] Automated version bumping

### **V2**
* [ ] Automated changelog generation
* [ ] Release notes generation
* [ ] Tag-based deployments

---

## **10. Cursor Rules & AI Instructions**

### **Existing**
* [x] `.cursorrules` file with code standards
* [x] Cursor instructions for common tasks

### **MVP (Updates Required)**
* [ ] **Update rules to reference MongoDB** (not SQLite)
* [ ] **Add instructions for finding/executing PRDs**
* [ ] **Add instructions for running update.sh**
* [ ] **Add instructions for Azure deployment**
* [ ] Add test suite execution instructions
* [ ] **Cursor configuration to expose Lloyd and Help agents** in dropdown
* [ ] **Routing configuration**: Lloyd → `python agents/lloyd_helper.py --mode=lloyd`, Help → `python agents/lloyd_helper.py --mode=help`

### **V1**
* [ ] Context-specific rules (different rules per project type)
* [ ] Auto-generated rules based on PRD
* [ ] Rules for common integration patterns

### **V2**
* [ ] Learning rules (adapt based on user patterns)
* [ ] Team-specific rule customization
* [ ] Rule validation and linting

---

## **11. Documentation**

### **Existing**
* [x] Architecture overview
* [x] API documentation (FastAPI auto-generated)
* [x] Authentication documentation
* [x] Database documentation (needs MongoDB update)
* [x] Admin panel documentation
* [x] POC Agent usage guide

### **MVP (Updates Required)**
* [ ] **Update all docs to reference MongoDB** (not SQLite)
* [ ] **Quick Start guide** (5 minutes: setup → deployed)
* [ ] **Deployment troubleshooting guide**
* [ ] **Update management documentation**
* [ ] **PRD Agent documentation**: Requirements gathering, file analysis (wireframes via GPT-4 Vision, PDF/TXT/MD via FAISS), semantic search

### **V1**
* [ ] Video tutorials
* [ ] Example PRD templates (various app types)
* [ ] Tutorial: PRD → working app
* [ ] FAQ section

### **V2**
* [ ] Interactive documentation
* [ ] Community-contributed examples
* [ ] Best practices library

---

## **12. Example/Template Code**

### **Existing**
* [x] Example authenticated page
* [x] Example LangChain agent usage (POC Agent)

### **MVP (New)**
* [ ] **Example MongoDB CRUD operations** (frontend + backend)
* [ ] Example form with validation
* [ ] Example file upload
* [ ] Simple welcome page template

### **V1**
* [ ] Example data visualization (charts, graphs)
* [ ] Example real-time features (WebSockets)
* [ ] Example third-party API integration

### **V2**
* [ ] Template library (common app patterns)
* [ ] Drag-and-drop component builder
* [ ] Pre-built feature modules

---

## **13. Testing Setup**

### **Existing**
* [ ] None

### **MVP (Critical)**
* [ ] **Backend test framework** (pytest)
* [ ] **Frontend test framework** (Vitest/Jest)
* [ ] **Example tests for auth system**
* [ ] **Test database setup** (separate MongoDB database)
* [ ] **PRD Agent generates test suite** for each POC
* [ ] **Cursor instructions for running tests**
* [ ] **All PRDs must contain**: Testing requirements (pytest/Jest), "Pause and test" checkpoints

### **V1**
* [ ] Integration tests
* [ ] E2E tests (Playwright/Cypress)
* [ ] Test coverage reporting
* [ ] Automated regression testing

### **V2**
* [ ] Performance testing
* [ ] Load testing
* [ ] Security testing (OWASP compliance)

---

## **14. Developer Experience**

### **Existing**
* [x] Hot reload configured (frontend & backend)
* [x] Clear error messages
* [x] Logging configured

### **MVP (New)**
* [ ] **Development vs Production environment switching**
* [ ] **Database seeding script** (sample admin user, test data)
* [ ] **Health check endpoint** with detailed status
* [ ] **Installation of system tools**: Azure CLI, GitHub CLI, MongoDB Shell, VSCode extensions
* [ ] **Verify installations and run post-install diagnostics**
* [ ] **Register installation with SaltAIr's service registry**

### **V1**
* [ ] VSCode/Cursor debugging configuration
* [ ] Performance profiling tools
* [ ] Local development Docker setup

### **V2**
* [ ] AI-powered error suggestions
* [ ] Automated code review
* [ ] Performance optimization suggestions

---

## **15. Monitoring System (NEW SECTION)**

### **MVP (Critical New Work)**

#### **Central Monitoring Endpoint at SaltAIr**

* [ ] **Registration endpoint** (`POST /api/monitor/register`)
  * Captures: company name, project name, GitHub repo URL, Azure backend URLs (prod/staging), Azure frontend URL, MongoDB connection string (encrypted), scaffold version, setup timestamp
  * Assigns unique customer ID
  * Returns registration confirmation

* [ ] **Setup verification endpoint** (`POST /api/monitor/verify-setup`)
  * Verifies: GitHub repo accessible, Azure prod slot responding (curl), Azure staging slot responding (curl), MongoDB connected, default admin user created, auth system functional, admin panel accessible
  * Tracks: Each checklist item (pass/fail), overall setup status (complete/incomplete), timestamp for each step, failed items with error details

* [ ] **Health monitoring endpoint** (`POST /api/monitor/health`)
  * Receives: application uptime, MongoDB connection status, Azure endpoint response time, error count, last deployment timestamp, current scaffold version, health check timestamp
  * Frequency: Every 15 minutes (configurable)
  * Missing health pings trigger alerts
  * Historical health data retained for trend analysis

* [ ] **Deployment tracking endpoint** (`POST /api/monitor/deployment`)
  * Via GitHub webhooks
  * Tracks: repository name, branch (dev/main), commit hash, deployment status (success/failure), deployment duration, error logs (if failed), timestamp
  * Calculates deployment success rate per customer

* [ ] **Update management endpoint** (`GET /api/monitor/updates/check`)
  * Returns: latest scaffold version, changelog, update available flag
  * Tracks which customers are on outdated versions
  * Monitor update success/failure rates

* [ ] **Update confirmation endpoint** (`POST /api/monitor/updates/confirm`)
  * Logs successful updates
  * Tracks update adoption rate

#### **Dashboard (MVP)**

* [ ] **Customer overview dashboard**
  * List all customers
  * Setup status (complete/incomplete)
  * Health status (healthy/warning/critical)
  * Scaffold version
  * Last health check timestamp
  * Quick actions (view details, send notification)

* [ ] **Customer detail view**
  * Full configuration details
  * Setup checklist with pass/fail status
  * Health history graph
  * Deployment history
  * Error logs
  * Update history

* [ ] **System-wide metrics**
  * Total active customers
  * Setup success rate (target: 95%+)
  * Average deployment success rate (target: 85%+)
  * Health check failure rate
  * Version adoption distribution (target: 80%+ update within 30 days)
  * Common failure patterns
  * Target: <5% customers experience repeated failures

#### **Integration (MVP)**

* [ ] **welcome.sh calls registration endpoint** after successful setup
* [ ] **welcome.sh calls verification endpoint** after deployment
* [ ] **Deployed apps ping health endpoint** every 15 minutes
* [ ] **GitHub webhooks configured** to call deployment endpoint
* [ ] **update.sh calls update confirmation endpoint**

#### **Security & Privacy**

* [ ] **Data encryption**: MongoDB connection strings encrypted at rest
* [ ] **Access control**: Dashboard requires SaltAIr admin authentication
* [ ] **Customer consent**: Customers opt-in to monitoring during setup
* [ ] **Data retention**: Define retention policy for logs and health data
* [ ] **API authentication**: All endpoint calls require customer-specific API keys
* [ ] **Opt-in/opt-out**: Customers can enable/disable monitoring, opt-out of telemetry while keeping update notifications

#### **Alert Requirements**

* [ ] **SaltAIr Admin Alerts**:
  * Customer setup fails verification checks
  * Customer health checks stop responding (missed 3+ consecutive pings)
  * Customer deployment fails repeatedly
  * Customer running critically outdated scaffold version

* [ ] **Customer Alerts** (optional):
  * Deployment failure notification
  * Health check failure notification
  * Update available notification

### **V1**
* [ ] Email alerts for failed setups/deployments
* [ ] Opt-in/opt-out for monitoring
* [ ] Customer-facing health dashboard
* [ ] Automated issue detection and recommendations

### **V2**
* [ ] Predictive failure detection
* [ ] Automated remediation for common issues
* [ ] Performance benchmarking across customers
* [ ] Cost optimization recommendations

---

## **16. Update Management (NEW SECTION)**

### **MVP**

* [ ] **update.sh script**
  * Fetches latest from boot_lang repo
  * Shows changelog and list of files to be updated
  * Prompts for confirmation
  * Updates: .cursorrules, poc_agent_prompts.json, docs/, requirements.txt, agent scripts
  * Preserves: user POCs, user_config.json, .env, all user code
  * Updates .scaffold_version file
  * Confirmation: "✅ Updated to v1.2.0", "✅ Cursor rules updated", "✅ Agent prompts updated", "Your POCs are safe and unchanged"

* [ ] **Cursor integration** ("update scaffold" command runs update.sh)
* [ ] **Version checking** on PRD builder startup
* [ ] **Email notifications**: "Boot_Lang Update Available" with version number, summary of changes, simple update instruction

### **V1**
* [ ] Email notifications when updates available
* [ ] Automated update scheduling (user chooses frequency)
* [ ] Update rollback mechanism
* [ ] Selective updates (choose which components to update)

### **V2**
* [ ] Beta channel for early adopters
* [ ] Automated testing before applying updates
* [ ] Update impact analysis

---

## **17. Lloyd & Help Agents (NEW SECTION - CORE IP)**

### **MVP**

* [ ] **Lloyd Agent** (Confident mentor mode)
  * Teach, explain features, guide setup
  * Reinforce best practices
  * Integration into Cursor dropdown
  * Invokes: `python agents/lloyd_helper.py --mode=lloyd`

* [ ] **Help Agent** (Calming triage mode)
  * Reassure frustrated users
  * Offer immediate recovery steps
  * De-escalate problems
  * Invokes: `python agents/lloyd_helper.py --mode=help`

* [ ] **Shared backend agent process** with persona framing for tone
* [ ] **One-way routing**: Send messages to Cursor's main agent, never supervise or override
* [ ] **Integration with PRD Builder**: Generate, explain, and step through project documentation
* [ ] **Integration with SaltAIr Rules Engine**: Enforce workflow standards, formatting, safety prompts

### **V1**
* [ ] **Secure deployment** (hidden local agents under `~/.saltair/agents/`)
* [ ] **Packaged distribution** (freeze with pyinstaller/shiv/pkg)
* [ ] **Automatic `.cursor/config.json` editing** during installation
* [ ] **Tone detection** (auto-switch to help mode on frustration indicators)
* [ ] **Session context storage** (small text log, emotional state tracking)

### **V2**
* [ ] **Training & continuous improvement** system
* [ ] **Knowledge feeds** from PRD Builder, rules, sample project metadata
* [ ] **Modular intents** (setup → deployment → testing → troubleshooting)
* [ ] **Log anonymized interactions** for fine-tuning
* [ ] **Rule sync** from SaltAIr cloud or local policy repository

---

## **18. PRD Builder / Pre-Builder Agent (NEW SECTION)**

### **MVP**

* [ ] **Conversational requirements gathering** ("What do you want to build?")
* [ ] **Generates PRD structure**:
  * `/prds/<project>_start/` directory
  * Phase breakdown (Phase 0 → Phase n)
  * Implementation plan (stepwise, testable, with checkpoints)
  * Testing requirements (pytest/Jest)
  * Deployment rules (Azure/AppService)
  * Logging strategy
  * Documentation & guides
  * "Pause and test" checkpoints

* [ ] **File analysis**:
  * Wireframes (PNG/JPG) → GPT-4 Vision analysis
  * Documents (PDF/TXT/MD) → chunked and stored in FAISS vector store
  * Semantic search on uploaded docs for context

* [ ] **POC generation**:
  * Creates `poc_name` folder
  * Generates 3 phase markdown files (frontend, backend, database)
  * Creates README
  * Packages as ZIP download

* [ ] **API endpoints**:
  * `/chat` - conversational interaction
  * `/upload` - file upload
  * `/generate` - trigger POC generation
  * `/download/{poc_name}` - download ZIP

* [ ] **Guides branch creation** (`dev`, `main`, optional `feature`)
* [ ] **Encourages best practices**: CORS handling, branch discipline, commit timing

### **V1**
* [ ] **PRD templates** (YAML/JSON driven or Markdown-based)
* [ ] **LLM integration** for drafting PRDs
* [ ] **Agent suggests integrations** with existing POCs
* [ ] **Agent can update existing PRDs**

### **V2**
* [ ] **Visual PRD builder** integration
* [ ] **Template library** for different project types
* [ ] **Community-contributed templates**

---

## **Summary: MVP Priority Order**

### **Phase 1: Infrastructure (Weeks 1-2)**
1. MongoDB migration (replace all SQLite/SQLAlchemy)
2. Azure deployment automation in welcome.sh
3. Git workflow automation (branch creation, remote switching)
4. Monitoring endpoints and registration
5. Lloyd agent conversational wizard integration

### **Phase 2: Core Features (Weeks 3-4)**
6. Update management (update.sh + version tracking)
7. PRD Agent improvements (read scaffold code, MongoDB references, test generation)
8. Welcome/Admin pages with service links and embedded Lloyd chatbot
9. Basic testing framework
10. Lloyd & Help agents in Cursor dropdown

### **Phase 3: Documentation & Polish (Week 5)**
11. Update all docs for MongoDB
12. Quick start guide
13. Troubleshooting guide
14. Example code for MongoDB CRUD
15. Video tutorials for setup process

### **Phase 4: Monitoring Dashboard (Week 6)**
16. Customer overview dashboard
17. Health monitoring integration
18. Deployment tracking integration
19. Alert system configuration

### **Phase 5: Agent Ecosystem (Week 7)**
20. LangGraph implementation for dynamic agent routing
21. Shared state management across agents
22. Specialized agents (MongoDB, Azure, GitHub)
23. PRD Builder flow persistence

---

## **Changes from Original Roadmap**

**New sections added:**
- Section 17: Lloyd & Help Agents (Core IP)
- Section 18: PRD Builder / Pre-Builder Agent

**Major feature additions:**
- Lloyd conversational wizard during setup
- Admin Portal with comprehensive dashboard
- Lloyd & Help agents integrated into Cursor
- LangGraph for dynamic agent orchestration
- Recovery and maintenance scripts
- Enhanced PRD Agent capabilities (file analysis, semantic search)
- Comprehensive monitoring with health checks, deployment tracking
- Two-path setup (new vs existing users)
- Email notifications for updates
- Opt-in/opt-out monitoring with customer consent

**Enhanced existing sections:**
- Authentication: Added password-protected admin portal with forced reset
- Frontend: Detailed admin portal specification with service cards
- LangChain: Added agent orchestration, phased approach enforcement
- Monitoring: Expanded with complete API specification, security, alerts
- Testing: Added PRD-generated test suites requirement
- Developer Experience: Added system tool installation and diagnostics