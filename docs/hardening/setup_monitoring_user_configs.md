# Monitoring Endpoint - Business Requirements

## Purpose

Create a centralized monitoring system for SaltAIr to track all customer Boot_Lang deployments, verify successful setup, monitor ongoing health, and manage scaffold updates.

---

## Core Requirements

### 1. Registration Endpoint

**Purpose**: Capture initial customer configuration during welcome.sh setup

**Required Data**:
- Customer/company name
- Project name
- GitHub repository URL
- Azure backend URL (production)
- Azure backend URL (staging)
- Azure frontend URL
- MongoDB Atlas cluster connection string (encrypted/hashed)
- Scaffold version installed
- Setup timestamp

**Success Criteria**:
- Customer config stored in SaltAIr database
- Unique customer ID assigned
- Registration confirmation returned

---

### 2. Setup Verification Endpoint

**Purpose**: Track completion of setup checklist items

**Verification Checks**:
- GitHub repository accessible
- Azure production slot responding (curl health check)
- Azure staging slot responding (curl health check)
- MongoDB connection successful
- Default admin user created
- Authentication system functional
- Admin panel accessible

**Success Criteria**:
- Each checklist item marked pass/fail
- Overall setup status: Complete/Incomplete
- Timestamp for each verification step
- Failed items logged with error details

---

### 3. Health Monitoring Endpoint

**Purpose**: Receive periodic health pings from deployed customer applications

**Health Data**:
- Application uptime
- MongoDB connection status
- Azure endpoint response time
- Error count (if any)
- Last successful deployment timestamp
- Current scaffold version
- Timestamp of health check

**Success Criteria**:
- Health data updated every 15 minutes (or configurable interval)
- Missing health pings trigger alerts
- Historical health data retained for trend analysis

---

### 4. Deployment Tracking Endpoint

**Purpose**: Receive notifications via GitHub webhooks for deployment events

**Deployment Data**:
- Repository name
- Branch (dev or main)
- Commit hash
- Deployment status (success/failure)
- Deployment duration
- Error logs (if failed)
- Timestamp

**Success Criteria**:
- All deployments logged
- Failed deployments flagged for review
- Deployment success rate calculated per customer

---

### 5. Update Management Endpoint

**Purpose**: Manage scaffold version updates and notify customers

**Update Functions**:
- **Version Check**: Customer app queries for latest scaffold version
- **Update Notification**: Return available updates with changelog
- **Update Confirmation**: Log when customer successfully updates
- **Update Analytics**: Track adoption rate of new versions

**Success Criteria**:
- Customers can check for updates programmatically
- Update notifications sent via email when new version released
- Track which customers are on outdated versions
- Monitor update success/failure rates

---

## Dashboard Requirements

### Customer Overview Dashboard

**Display**:
- List of all customers
- Setup status (complete/incomplete)
- Current health status (healthy/warning/critical)
- Scaffold version
- Last health check timestamp
- Quick actions (view details, send notification)

### Customer Detail View

**Display**:
- Full configuration details
- Setup checklist with pass/fail status
- Health history graph
- Deployment history
- Error logs
- Update history

### System-Wide Metrics

**Display**:
- Total active customers
- Setup success rate
- Average deployment success rate
- Health check failure rate
- Version adoption distribution
- Common failure patterns

---

## Security & Privacy Requirements

1. **Data Encryption**: MongoDB connection strings must be encrypted at rest
2. **Access Control**: Dashboard requires SaltAIr admin authentication
3. **Customer Consent**: Customers must opt-in to monitoring during setup
4. **Data Retention**: Define retention policy for logs and health data
5. **API Authentication**: All endpoint calls require customer-specific API keys

---

## Opt-In/Opt-Out

- Customers can enable/disable monitoring during welcome.sh setup
- Customers can opt-out of telemetry while keeping update notifications
- Customers receive clear disclosure about what data is collected
- Opt-out customers still appear in dashboard with limited data

---

## Alert Requirements

**SaltAIr Admin Alerts**:
- Customer setup fails verification checks
- Customer health checks stop responding (missed 3+ consecutive pings)
- Customer deployment fails repeatedly
- Customer running critically outdated scaffold version

**Customer Alerts** (optional):
- Deployment failure notification
- Health check failure notification
- Update available notification

---

## API Endpoint Summary

1. `POST /api/monitor/register` - Initial customer registration
2. `POST /api/monitor/verify-setup` - Setup checklist verification
3. `POST /api/monitor/health` - Periodic health ping
4. `POST /api/monitor/deployment` - Deployment event notification
5. `GET /api/monitor/updates/check` - Check for scaffold updates
6. `POST /api/monitor/updates/confirm` - Confirm successful update

---

## Success Metrics

- 95%+ of customers complete setup successfully
- 90%+ health check success rate across all customers
- 85%+ deployment success rate
- 80%+ customers update within 30 days of release
- <5% customers experience repeated failures