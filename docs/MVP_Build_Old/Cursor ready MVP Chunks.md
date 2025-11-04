Cursor ready Phase 1 Chunks

For Phase 1 (Foundation & Setup), here are the Cursor-ready PRD chunks:

## **Phase 1 PRDs (in build order):**

### **PRD 1.1: MongoDB Connection Layer**

* Replace SQLite with MongoDB in database.py  
* Connection pooling and retry logic  
* Basic CRUD operations  
* **Test:** Connect to Atlas, create/read/update/delete a user record

### **PRD 1.2: User Authentication with MongoDB**

* Update User model for MongoDB  
* Update auth endpoints (register, login)  
* JWT token generation/validation  
* **Test:** Register new user, login, access protected endpoint

### **PRD 1.3: Database Initialization Script**

* Create collections on first run  
* Seed default admin user  
* Verify schema/indexes  
* **Test:** Run script, confirm admin can login

### **PRD 1.4: Welcome Script \- Basic Setup**

* Bash script launches Flask server on localhost:8001  
* Simple HTML form for credentials  
* Script validates prerequisites (Python, Node, Git installed)  
* **Test:** Run welcome.sh, form opens in browser

### **PRD 1.5: Credential Collection Form**

* Form fields for all credentials (GitHub, Azure, MongoDB, OpenAI)  
* Client-side validation  
* Submit to backend endpoint  
* **Test:** Fill form with valid data, submit successfully

### **PRD 1.6: Credential Validation Backend**

* POST /setup/validate endpoint  
* Test GitHub API access  
* Test Azure CLI authentication  
* Test MongoDB connection  
* Test OpenAI API key  
* Return specific errors for each failure  
* **Test:** Submit invalid GitHub token, see clear error message

### **PRD 1.7: Credential Storage**

* Write validated credentials to .env  
* Write config to .saltair/config.json  
* Ensure .env not tracked by git  
* **Test:** Complete form, verify .env created, verify not in git status

### **PRD 1.8: Git Remote Configuration**

* Switch remote from boot\_lang to user's repo  
* Create dev and main branches  
* Initial commit of scaffold code  
* **Test:** Check git remote \-v, see user's repo; see both branches

### **PRD 1.9: GitHub Actions Setup**

* Copy workflow files for dev and main branches  
* Configure secrets in GitHub (via GitHub API)  
* Set up webhook for deployment tracking  
* **Test:** Make test commit, see workflow run in GitHub Actions

### **PRD 1.10: Azure Resource Creation**

* Azure CLI commands to create resource group  
* Create App Service plan  
* Create backend web app  
* Create staging slot  
* **Test:** Check Azure portal, all resources exist

### **PRD 1.11: Azure Configuration**

* Set environment variables in Azure  
* Configure CORS settings  
* Set up custom domains/URLs  
* **Test:** View environment variables in Azure portal

### **PRD 1.12: Code Deployment to Azure**

* Deploy scaffold code to production slot  
* Deploy scaffold code to staging slot  
* Configure deployment scripts  
* **Test:** Visit both URLs, see "deployment successful" page

### **PRD 1.13: Health Check Endpoint**

* Create /health endpoint in FastAPI  
* Return MongoDB status, uptime, version  
* Simple JSON response  
* **Test:** curl both Azure URLs /health, get 200 response

### **PRD 1.14: Deployment Verification**

* Automated health check after deployment  
* Test MongoDB connection from Azure  
* Test authentication from Azure  
* Display final URLs to user  
* **Test:** Complete full setup, see ✅ confirmation with working URLs

---

**Total PRDs for Phase 1: 14**

Each PRD is:

* \~2-4 hours of work  
* Has clear test criteria  
* User can verify it works before moving to next one  
* Failures are isolated to one small component

User becomes tester at each step \- if PRD 1.6 fails, they don't waste time on 1.7.

## **Phase 2 PRDs (Monitoring & Diagnostics \- in build order):**

### **PRD 2.1: Monitoring Database Schema**

* MongoDB schema for monitoring data (customers, health\_checks, deployments, setup\_logs)  
* Indexes for performance  
* Sample queries for dashboard  
* **Test:** Create collections, insert test data, query successfully

### **PRD 2.2: Customer Registration Endpoint**

* POST /api/monitor/register endpoint  
* Accept customer data (name, project, URLs, version, timestamp)  
* Generate unique customer ID and API key  
* Store in MongoDB  
* **Test:** POST valid data, get customer ID back, verify in database

### **PRD 2.3: Encryption for Sensitive Data**

* Encrypt MongoDB connection strings before storage  
* Decrypt for dashboard display (masked)  
* Encryption key management  
* **Test:** Register customer with connection string, verify encrypted in DB

### **PRD 2.4: Setup Verification Endpoint**

* POST /api/monitor/verify-setup endpoint  
* Accept checklist items (GitHub accessible, Azure responding, MongoDB connected, etc.)  
* Store pass/fail status with timestamps  
* Calculate overall setup status (complete/incomplete)  
* **Test:** POST checklist with mixed pass/fail, verify stored correctly

### **PRD 2.5: Health Monitoring Endpoint**

* POST /api/monitor/health endpoint  
* Accept health data (uptime, MongoDB status, error count, version)  
* Update customer's last health check timestamp  
* Store in time-series collection  
* **Test:** POST health ping, verify timestamp updated, verify historical data stored

### **PRD 2.6: Deployment Tracking Endpoint**

* POST /api/monitor/deployment endpoint  
* Accept deployment data (repo, branch, commit, status, duration, errors)  
* Calculate deployment success rate per customer  
* **Test:** POST successful deployment, verify appears in customer's deployment history

### **PRD 2.7: Update Check Endpoint**

* GET /api/monitor/updates/check endpoint  
* Accept current version as query param  
* Return latest version, changelog, update\_available flag  
* **Test:** GET with old version, verify returns update\_available:true

### **PRD 2.8: API Authentication Middleware**

* Validate customer API key on all requests  
* Return 401 for invalid/missing keys  
* Rate limiting (basic)  
* **Test:** Call endpoint without key (fail), with valid key (success), with invalid key (fail)

### **PRD 2.9: Alert Detection Logic**

* Background job to detect missed health pings (3+ consecutive)  
* Detect repeated deployment failures  
* Detect critically outdated versions  
* Log alerts (email integration deferred to V1)  
* **Test:** Simulate 3 missed pings, verify alert logged

### **PRD 2.10: Registration Integration in welcome.sh**

* Call registration endpoint after credentials validated  
* Store customer API key in .saltair/config.json  
* Handle registration failure gracefully  
* **Test:** Complete setup, verify registration called, verify API key stored

### **PRD 2.11: Setup Verification Integration**

* Call verify-setup endpoint after Azure deployment  
* Pass checklist results from setup process  
* Display verification status to user  
* **Test:** Complete setup, verify checklist sent to monitoring API

### **PRD 2.12: Health Ping Cron Job**

* Create health\_ping.py script  
* Gather health data (uptime, MongoDB status, error count)  
* POST to monitoring endpoint every 15 minutes  
* Add to system cron or use schedule library  
* **Test:** Wait 15 minutes, verify ping received in monitoring DB

### **PRD 2.13: GitHub Webhook Configuration**

* Configure webhook in user's GitHub repo during setup  
* Point to /api/monitor/deployment endpoint  
* Include authentication token  
* **Test:** Make deployment, verify webhook fires, verify data received

### **PRD 2.14: Webhook Handler for Deployments**

* Accept GitHub webhook payload  
* Parse deployment data (branch, commit, status)  
* Call deployment tracking endpoint  
* **Test:** Trigger webhook manually, verify parsed and stored correctly

### **PRD 2.15: Dashboard Authentication**

* Admin login page for dashboard  
* Simple password authentication (env variable)  
* Session management  
* **Test:** Access dashboard without login (redirect), login with password (success)

### **PRD 2.16: Customer List View (Dashboard)**

* React component showing all customers  
* Display: name, setup status, health status, version, last check  
* Color-coded status indicators (green/yellow/red)  
* **Test:** View dashboard with 3 test customers, verify all data shown

### **PRD 2.17: Customer Detail View (Dashboard)**

* React component for single customer detail  
* Display: full config, setup checklist, health history  
* Simple table for deployment history  
* Display error logs  
* **Test:** Click customer in list, see detail page with all data

### **PRD 2.18: System-Wide Metrics (Dashboard)**

* Calculate and display total active customers  
* Calculate setup success rate  
* Calculate deployment success rate  
* Calculate version adoption distribution  
* **Test:** View dashboard metrics, verify calculations correct

### **PRD 2.19: Real-Time Dashboard Updates**

* WebSocket or polling to refresh dashboard data  
* Update customer list every 30 seconds  
* Update health status in real-time  
* **Test:** Register new customer, verify appears in dashboard within 30 seconds

### **PRD 2.20: Error Log Display**

* Dashboard component to view error logs per customer  
* Filter by date range  
* Search/filter functionality  
* **Test:** View customer with errors, see logs displayed clearly

---

**Total PRDs for Phase 2: 20**

Each PRD is:

* \~2-4 hours of work  
* Has clear test criteria  
* User (developer working on Boot Lang) can verify before moving on  
* Builds incrementally on monitoring infrastructure

By PRD 2.20, complete monitoring system is operational.

