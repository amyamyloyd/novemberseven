# Boot_Lang Local Development Guide

## Port Structure

- **9000**: React PRD Builder UI (Dashboard, PRDs, chat, etc.)
- **9002**: Admin Panel (project status, git, database, no Azure)
- **8000**: FastAPI backend/API

## Getting Started (Mac/Linux)

1. Create the virtual environment and install deps:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Start FastAPI backend:
   ```bash
   python3 app.py
   # or
   uvicorn app:app --reload --port 8000
   ```
3. Start React frontend on port 9000:
   ```bash
   cd frontend
   PORT=9000 npm start
   ```
4. Start the admin panel:
   ```bash
   python3 admin_server.py
   # Now open http://localhost:9002
   ```

## Quick Start (Windows)

Follow the welcome.bat script as before. See the docs for full automation.

## What Changed

- **Azure**: Provisioning, CLI, config, and deployment REMOVED (local-only)
- **Setup**: Only requires project, OpenAI API key, GitHub URL. Simpler onboarding.
- **Admin**: Local-only dashboard, shows git, db, and local status (no cloud/Azure)
- **React App**: Fully local, no auth required in dev, runs on 9000

## Typical Workflows

- **Build a PRD**: Open http://localhost:9000 and use the builder/chat/prd tabs
- **Monitor Project Status**: Open http://localhost:9002 (admin panel)
- **Backend API**: Docs available at http://localhost:8000/docs

---

- Azure scripts, fields, and cloud deployment have been fully REMOVED for local-only environments.
