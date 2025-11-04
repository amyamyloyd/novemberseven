# **Boot Lang MVP \- Business Requirements Document**

## **SaltAIr Development Scaffold Platform**

**Version:** 1.0 MVP  
 **Date:** November 2, 2025  
 **Status:** Requirements Definition

---

## **Executive Summary**

Boot Lang is a scaffolding platform that enables non-technical users to rapidly deploy production-ready web applications. The platform provides:

* Automated environment setup and credential management  
* Pre-built authentication and database infrastructure  
* AI-assisted project requirements gathering (PRD Builder)  
* Conversational guidance through development (Lloyd & Help agents)  
* Automated deployment to Azure with staging and production environments  
* Centralized monitoring and health tracking

**MVP Goal:** Deliver a complete setup-to-deployment experience in under 30 minutes, with users having working dev and production environments ready to build their first POC application.

---

## **Target Users**

### **Primary User**

**Non-technical entrepreneur or business analyst** who:

* Has an idea for a web application  
* Limited or no coding experience  
* Willing to use Cursor IDE with AI assistance  
* Comfortable following guided setup instructions  
* Has budget for cloud services (Azure, MongoDB Atlas)

### **Secondary User**

**Junior developer** who:

* Wants to accelerate project setup  
* Needs deployment pipeline automation  
* Benefits from best-practice scaffolding  
* Requires guidance on integrating services

---

## **Success Criteria (MVP)**

| Metric | Target | Measurement |
| ----- | ----- | ----- |
| **Setup Success Rate** | 95%+ | Percentage of users who complete initial setup without errors |
| **Time to Deployment** | \<30 minutes | From repo download to live dev/prod sites |
| **Health Check Success** | 90%+ | Percentage of deployed apps responding to health checks |
| **User Satisfaction** | 4.0/5.0 | Post-setup survey rating |
| **Deployment Success** | 85%+ | Percentage of successful GitHub → Azure deployments |

---

## **Core User Journey (MVP)**

### **Phase 1: Onboarding (5 minutes)**

1. User receives email with instructions  
2. User downloads Cursor IDE  
3. User creates GitHub account (if needed)  
4. User creates Azure subscription (if needed)  
5. User creates MongoDB Atlas account (if needed)

### **Phase 2: Setup (10-15 minutes)**

1. User clones boot\_lang repository in Cursor  
2. User runs `./welcome.sh` script  
3. Lloyd agent launches in browser (localhost:8001)  
4. Lloyd guides user through credential collection:  
   * GitHub repository URL (or helps create new repo)  
   * Azure credentials (subscription, resource group)  
   * MongoDB Atlas connection string  
   * OpenAI API key  
5. System validates all credentials  
6. System creates dev and main branches  
7. System deploys to Azure (staging and production slots)  
8. System confirms deployment with URLs

### **Phase 3: Verification (5 minutes)**

1. User visits both deployed URLs (dev and prod)  
2. User logs into admin panel  
3. User verifies database connection  
4. User sees confirmation: "✅ Setup Complete"

### **Phase 4: PRD Building (Variable time)**

1. User accesses PRD Builder (localhost:3000/prd)  
2. Lloyd agent asks about project requirements  
3. User describes what they want to build  
4. Lloyd validates scope (is this truly a POC?)  
5. User can upload wireframes or documents  
6. Lloyd generates:  
   * Product Requirements Document  
   * 3-phase implementation plan (frontend, backend, database)  
   * Test requirements  
   * Deployment checklist  
7. Files saved locally for Cursor to access

### **Phase 5: Development (User-paced)**

1. User opens Cursor  
2. User has access to Lloyd and Help agents in dropdown  
3. User follows phase-by-phase implementation plan  
4. Lloyd provides guidance and best practices  
5. Help provides troubleshooting when needed  
6. User commits to dev branch → auto-deploys to staging  
7. User merges to main → auto-deploys to production

---

## **Feature Requirements (MVP)**

### **1\. Automated Setup Wizard**

**Business Need:** Non-technical users cannot manually configure multiple cloud services and development environments.

**Requirements:**

* BR-1.1: System shall launch a local web server (localhost:8001) when user runs welcome.sh  
* BR-1.2: System shall present a conversational interface (Lloyd) to guide credential collection  
* BR-1.3: System shall support two paths: new users (guided account creation) and existing users (credential entry)  
* BR-1.4: System shall validate all credentials before proceeding with deployment  
* BR-1.5: System shall store credentials securely in `.env` and `.saltair/config.json`  
* BR-1.6: System shall NOT proceed if any credential validation fails  
* BR-1.7: System shall provide clear error messages for failed validations with remediation steps

**Success Criteria:**

* 95% of users complete credential collection without support  
* Average time: 5-7 minutes  
* Zero credential exposure in logs or version control

---

### **2\. Automated Git Configuration**

**Business Need:** Users need their own GitHub repository without understanding Git workflows.

**Requirements:**

* BR-2.1: System shall create or link to user's GitHub repository  
* BR-2.2: System shall create `dev` and `main` branches automatically  
* BR-2.3: System shall configure GitHub Actions for both branches  
* BR-2.4: System shall switch git remote from boot\_lang to user's repository  
* BR-2.5: System shall perform initial commit and push  
* BR-2.6: System shall configure webhooks for deployment tracking

**Success Criteria:**

* 100% of setups result in functioning GitHub repository  
* User never needs to run manual git commands during setup  
* All GitHub Actions workflows execute successfully on first commit

---

### **3\. Automated Azure Deployment**

**Business Need:** Manual Azure configuration is complex and error-prone for non-technical users.

**Requirements:**

* BR-3.1: System shall create Azure resource group (if not exists)  
* BR-3.2: System shall create App Service plan  
* BR-3.3: System shall create backend web app with staging slot  
* BR-3.4: System shall create Static Web App for frontend  
* BR-3.5: System shall configure all environment variables in Azure  
* BR-3.6: System shall configure CORS for dev and prod  
* BR-3.7: System shall deploy initial scaffold code to both slots  
* BR-3.8: System shall perform health check verification after deployment  
* BR-3.9: System shall display both URLs to user upon completion

**Success Criteria:**

* 90% of deployments succeed without manual intervention  
* Both staging and production environments are accessible within 15 minutes  
* Health checks pass on both environments

---

### **4\. MongoDB Integration**

**Business Need:** Users need a production-ready database without database administration expertise.

**Requirements:**

* BR-4.1: System shall connect to MongoDB Atlas using provided connection string  
* BR-4.2: System shall create initial database collections (users, metadata)  
* BR-4.3: System shall create default admin user with secure password  
* BR-4.4: System shall verify database connectivity during setup  
* BR-4.5: System shall provide database viewer in admin portal

**Success Criteria:**

* 100% of setups have functioning database connection  
* Admin user can log in immediately after setup  
* Database viewer shows collections and sample data

---

### **5\. Admin Portal (Localhost Dashboard)**

**Business Need:** Users need a central place to monitor services, view data, and access help.

**Requirements:**

* BR-5.1: System shall run local admin portal (localhost with user-defined port)  
* BR-5.2: Admin portal shall be password-protected (set during install)  
* BR-5.3: Admin portal shall force password reset after 23 hours  
* BR-5.4: Admin portal shall display service status cards:  
  * GitHub (connection status, last commit, repository link)  
  * Azure (deployment status, URLs to staging/prod, logs link)  
  * MongoDB (connection status, collection count, Atlas dashboard link)  
  * API Keys (masked values, validity status)  
* BR-5.5: Admin portal shall provide system controls:  
  * Start/stop local services  
  * Re-run diagnostics  
  * Rebuild virtual environment  
  * Access logs  
* BR-5.6: Admin portal shall embed Lloyd chatbot for help and Q\&A  
* BR-5.7: Admin portal shall link to video guides and tutorials

**Success Criteria:**

* Portal loads within 2 seconds  
* All service status cards show accurate real-time data  
* Lloyd chatbot responds to queries within 3 seconds  
* Users rate portal usefulness 4.0/5.0 or higher

---

### **6\. PRD Builder Agent**

**Business Need:** Users need help defining project requirements in a structured, POC-appropriate format.

**Requirements:**

* BR-6.1: System shall provide conversational interface for requirements gathering  
* BR-6.2: Agent shall ask clarifying questions about:  
  * Project purpose and goals  
  * Target users  
  * Key features and functionality  
  * Data models needed  
  * Success criteria  
* BR-6.3: Agent shall validate scope ("Is this really a POC?")  
* BR-6.4: Agent shall push back on overly complex requirements  
* BR-6.5: Agent shall enforce technology stack (React, FastAPI, MongoDB)  
* BR-6.6: Agent shall accept file uploads:  
  * Wireframes (PNG/JPG) \- analyzed via GPT-4 Vision  
  * Documents (PDF/TXT/MD) \- stored in vector database for context  
* BR-6.7: Agent shall generate:  
  * Product Requirements Document (PRD)  
  * Phase 1: Frontend implementation plan  
  * Phase 2: Backend implementation plan  
  * Phase 3: Database implementation plan  
  * README with project overview  
  * Test requirements and checkpoints  
* BR-6.8: Agent shall save all outputs to `/prds/{project_name}/` directory  
* BR-6.9: Agent shall package outputs as downloadable ZIP  
* BR-6.10: Agent shall read existing scaffold code (auth.py, database.py) to suggest integrations

**Success Criteria:**

* 85% of generated PRDs result in successful POC builds  
* Users report PRD clarity rating of 4.0/5.0 or higher  
* 90% of PRDs include all required phases and checkpoints  
* PRD generation time: under 15 minutes for typical POC

---

### **7\. Lloyd & Help Agents (Cursor Integration)**

**Business Need:** Users need contextual help and guidance while building in Cursor, with different support for learning vs troubleshooting.

**Requirements:**

#### **Lloyd Agent (Mentor Mode)**

* BR-7.1: Lloyd shall appear in Cursor agent dropdown  
* BR-7.2: Lloyd shall use confident, encouraging tone  
* BR-7.3: Lloyd shall explain scaffold features and best practices  
* BR-7.4: Lloyd shall guide users through implementation phases  
* BR-7.5: Lloyd shall reference PRD and phase documents  
* BR-7.6: Lloyd shall teach "why" behind decisions

#### **Help Agent (Triage Mode)**

* BR-7.7: Help shall appear in Cursor agent dropdown  
* BR-7.8: Help shall use calming, empathetic tone  
* BR-7.9: Help shall focus on immediate problem resolution  
* BR-7.10: Help shall provide step-by-step recovery instructions  
* BR-7.11: Help shall detect common error patterns  
* BR-7.12: Help shall escalate to support if needed

#### **Shared Capabilities**

* BR-7.13: Both agents shall access same backend process  
* BR-7.14: Both agents shall have read access to:  
  * Current PRD  
  * Scaffold documentation  
  * User's project files  
  * Error logs  
* BR-7.15: Agents shall NOT modify user code without explicit request  
* BR-7.16: Agents shall provide code examples when helpful  
* BR-7.17: Agents shall route messages to Cursor's native agent when appropriate

**Success Criteria:**

* 80% of user questions answered without external support  
* Average response time: under 5 seconds  
* User satisfaction with agent help: 4.0/5.0 or higher  
* 70% reduction in support ticket volume

---

### **8\. Centralized Monitoring System**

**Business Need:** SaltAIr needs visibility into customer deployments for support, updates, and product improvement.

**Requirements:**

#### **Registration**

* BR-8.1: System shall register each customer setup with SaltAIr monitoring endpoint  
* BR-8.2: Registration shall include:  
  * Company/project name  
  * GitHub repository URL  
  * Azure backend URLs (staging and prod)  
  * Azure frontend URL  
  * Scaffold version installed  
  * Setup timestamp  
* BR-8.3: MongoDB connection string shall be encrypted before transmission  
* BR-8.4: Customer shall receive unique monitoring ID

#### **Setup Verification**

* BR-8.5: System shall verify setup checklist items:  
  * GitHub repository accessible  
  * Azure production slot responding  
  * Azure staging slot responding  
  * MongoDB connection successful  
  * Admin user created  
  * Authentication system functional  
  * Admin panel accessible  
* BR-8.6: Each verification item shall be logged as pass/fail with timestamp  
* BR-8.7: Failed items shall include error details

#### **Health Monitoring**

* BR-8.8: Deployed applications shall ping SaltAIr health endpoint every 15 minutes  
* BR-8.9: Health ping shall include:  
  * Application uptime  
  * MongoDB connection status  
  * Error count since last ping  
  * Current scaffold version  
* BR-8.10: Missed health pings (3+ consecutive) shall trigger alerts  
* BR-8.11: Health history shall be retained for 90 days

#### **Deployment Tracking**

* BR-8.12: GitHub webhooks shall notify SaltAIr of all deployments  
* BR-8.13: Deployment notification shall include:  
  * Repository name  
  * Branch (dev or main)  
  * Commit hash  
  * Deployment status (success/failure)  
  * Deployment duration  
  * Error logs (if failed)

#### **Update Management**

* BR-8.14: Customers shall check for scaffold updates via monitoring endpoint  
* BR-8.15: Endpoint shall return:  
  * Latest scaffold version  
  * Changelog summary  
  * Update availability flag  
* BR-8.16: System shall track which customers are on outdated versions  
* BR-8.17: Update notifications shall be sent via email when new version released

#### **Dashboard**

* BR-8.18: SaltAIr admin dashboard shall display:  
  * List of all customers  
  * Setup status per customer  
  * Health status (healthy/warning/critical)  
  * Current scaffold version  
  * Last health check timestamp  
* BR-8.19: Dashboard shall provide customer detail view with:  
  * Full configuration  
  * Setup checklist results  
  * Health history graph  
  * Deployment history  
  * Error logs  
* BR-8.20: Dashboard shall show system-wide metrics:  
  * Total active customers  
  * Setup success rate  
  * Deployment success rate  
  * Version adoption distribution

#### **Privacy & Security**

* BR-8.21: Customers shall opt-in to monitoring during setup  
* BR-8.22: Customers can opt-out of telemetry while keeping update notifications  
* BR-8.23: All API calls shall require customer-specific authentication  
* BR-8.24: Sensitive data shall be encrypted at rest  
* BR-8.25: Dashboard shall require SaltAIr admin authentication

**Success Criteria:**

* 95% of customers opt-in to monitoring  
* 90% health check success rate across all customers  
* Alert response time: under 15 minutes for critical issues  
* Dashboard loads all customer data within 3 seconds

---

### **9\. Update Management System**

**Business Need:** Scaffold improvements must reach customers without breaking their existing projects.

**Requirements:**

* BR-9.1: System shall provide `update.sh` script  
* BR-9.2: Script shall fetch latest version from boot\_lang repository  
* BR-9.3: Script shall display changelog before updating  
* BR-9.4: Script shall require user confirmation before proceeding  
* BR-9.5: Script shall update:  
  * `.cursorrules` file  
  * `poc_agent_prompts.json`  
  * Documentation files  
  * `requirements.txt`  
  * Agent scripts  
* BR-9.6: Script shall preserve:  
  * All user POC projects  
  * `.env` file  
  * `user_config.json`  
  * All user-generated code  
* BR-9.7: Script shall update `.scaffold_version` file  
* BR-9.8: Script shall confirm successful update to user  
* BR-9.9: Cursor shall support "update scaffold" command  
* BR-9.10: PRD Builder shall check for updates on startup  
* BR-9.11: Email notifications shall be sent when updates available

**Success Criteria:**

* 80% of customers update within 30 days of release  
* Zero data loss or project corruption from updates  
* Update process completes in under 5 minutes  
* Rollback available if update fails

---

## **Out of Scope (MVP)**

The following features are explicitly excluded from MVP:

### **Deferred to V1**

* OAuth authentication (GitHub, Google)  
* 2FA support  
* Visual query builder for MongoDB  
* Advanced agent collaboration (specialized agents for MongoDB, Azure, etc.)  
* Performance monitoring and optimization suggestions  
* Email verification for user accounts  
* Custom domain configuration for Azure  
* Automated SSL certificate setup  
* Multi-region deployments  
* Video tutorials (will link to external resources)

### **Deferred to V2**

* Multi-tenant architecture (one project per scaffold instance for MVP)  
* Role-based permissions beyond admin/user  
* Visual PRD builder interface  
* Community-contributed templates  
* Predictive failure detection  
* Automated remediation  
* Performance benchmarking across customers  
* Beta channel for updates

---

## **Dependencies & Prerequisites**

### **User Prerequisites**

* Computer with terminal access (Mac, Linux, or Windows with WSL)  
* Internet connection  
* Email address  
* Credit card for cloud service subscriptions

### **Required Accounts (User Responsibility)**

* GitHub account (free tier acceptable)  
* Azure subscription ($200 free credit for new accounts)  
* MongoDB Atlas account (free tier M0 cluster acceptable)  
* OpenAI API account with billing enabled

### **Technical Dependencies**

* Python 3.11+  
* Node.js 18+  
* Git CLI  
* Azure CLI  
* Cursor IDE

### **SaltAIr Infrastructure**

* Monitoring API endpoints (cloud-hosted)  
* Admin dashboard (cloud-hosted)  
* Documentation website  
* Support email system

---

## **Risks & Mitigations**

| Risk | Impact | Probability | Mitigation |
| ----- | ----- | ----- | ----- |
| **User credential errors** | High \- blocks setup | High | Extensive validation, clear error messages, Lloyd guidance |
| **Azure deployment failures** | High \- no production environment | Medium | Retry logic, fallback configurations, detailed error logging |
| **MongoDB connection issues** | High \- no database | Medium | Connection testing, firewall detection, alternative connection strings |
| **Cursor AI limitations** | Medium \- degraded experience | Medium | Lloyd/Help provide additional guidance, documentation as backup |
| **Cost overruns for users** | Medium \- user dissatisfaction | Medium | Clear cost estimates upfront, Azure free tier guidance |
| **Security vulnerabilities** | Critical \- data breach | Low | Security review, credential encryption, regular dependency updates |
| **Poor PRD quality** | Medium \- wasted development time | Medium | Agent validation, scope enforcement, iterative refinement |

---

## **Compliance & Security Requirements**

### **Data Protection**

* BR-10.1: System shall NOT store user passwords in plain text  
* BR-10.2: System shall NOT log sensitive credentials  
* BR-10.3: System shall encrypt MongoDB connection strings before transmission  
* BR-10.4: System shall use environment variables for all secrets  
* BR-10.5: System shall NOT commit `.env` files to version control

### **Access Control**

* BR-10.6: Admin portal shall require authentication  
* BR-10.7: Admin portal passwords shall expire after 23 hours  
* BR-10.8: Monitoring API shall require customer-specific API keys  
* BR-10.9: SaltAIr dashboard shall require admin authentication

### **Privacy**

* BR-10.10: System shall obtain user consent for monitoring  
* BR-10.11: System shall allow opt-out of telemetry  
* BR-10.12: System shall not collect personally identifiable information beyond email  
* BR-10.13: System shall provide data retention policy disclosure

---

## **Acceptance Criteria (MVP Release)**

The MVP is considered complete when:

1. ✅ **Setup Success**: 20 beta users complete setup with 95%+ success rate  
2. ✅ **Deployment Success**: All beta users have functioning dev and prod environments  
3. ✅ **PRD Generation**: 85% of generated PRDs result in buildable POCs  
4. ✅ **Agent Functionality**: Lloyd and Help agents successfully answer 80% of user queries  
5. ✅ **Monitoring Operational**: Dashboard shows real-time data for all beta users  
6. ✅ **Update Process**: At least one update successfully deployed to all beta users  
7. ✅ **Documentation Complete**: Quick start guide, troubleshooting guide, and video tutorials available  
8. ✅ **Support Load**: Support ticket volume under 10% of user count per week  
9. ✅ **Performance**: Average setup time under 30 minutes  
10. ✅ **User Satisfaction**: Post-setup survey shows 4.0/5.0 or higher satisfaction

---

## **Open Questions**

1. **Pricing Model**: How will SaltAIr charge for the scaffold? One-time fee, subscription, or usage-based?  
2. **Support Model**: What support channels will be available? Email only, or chat/phone?  
3. **Azure Cost Responsibility**: Who pays for Azure resources \- user or SaltAIr initially?  
4. **LLM Cost Management**: How to handle high OpenAI API costs from heavy agent usage?  
5. **Multi-language Support**: MVP is English only \- when to add other languages?  
6. **Offline Mode**: Should any functionality work without internet connection?  
7. **Team Accounts**: How to handle multiple users working on same project?  
8. **White Labeling**: Will partners be able to rebrand the scaffold?

---

## **Next Steps**

1. **Technical Architecture Review** \- Validate technical feasibility of all requirements  
2. **Cost Analysis** \- Calculate infrastructure costs for SaltAIr and typical user  
3. **UI/UX Design** \- Create mockups for admin portal and PRD builder  
4. **Agent Prompt Engineering** \- Develop and test Lloyd and Help personalities  
5. **Security Audit** \- Review credential handling and data protection measures  
6. **Beta User Recruitment** \- Identify 20 users for MVP testing  
7. **Documentation Creation** \- Write all guides, tutorials, and help content  
8. **Monitoring Infrastructure** \- Build and deploy SaltAIr cloud services

---

## **Document History**

| Version | Date | Author | Changes |
| ----- | ----- | ----- | ----- |
| 1.0 | 2025-11-02 | Claude | Initial MVP requirements document |

---

## **Approval**

This document requires approval from:

* \[ \] Product Owner  
* \[ \] Technical Lead  
* \[ \] Security Lead  
* \[ \] Legal/Compliance

