# SaltAIr Boot_Lang

Local development helper tools for rapid application development.

## Prerequisites

1. **Cursor IDE**: https://cursor.sh
2. **Cursor Extensions**: Python, Git

## Quick Start

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd saltair-bootlang
```

### 2. Open in Cursor
```bash
cursor .
```

### 3. Run Setup

**Windows:**
```bash
welcome.bat
```

**Mac/Linux:**
```bash
bash welcome.sh
```

Browser opens to http://localhost:8001/setup

### 4. Fill Setup Form

Provide:
- Your name
- Project name
- GitHub repo URL (create empty repo first)
- OpenAI API key (required)
- Anthropic API key (optional)
- LangSmith API key (optional)

### 5. Wait for Setup

Setup automatically:
- ✅ Creates virtual environment
- ✅ Connects to your GitHub repo
- ✅ Creates .env with API keys
- ✅ Installs dependencies
- ✅ Initializes SQLite database
- ✅ Commits and pushes
- ✅ Starts helper tools

### 6. Start Building!

Browser opens to **http://localhost:9000**

## Helper Tools

**Three servers on high ports:**

- 🏠 **Dashboard** - http://localhost:9000
- 📝 **PRD Builder** - http://localhost:9001
- ⚙️ **Admin Panel** - http://localhost:9002

### Restart Helper Tools

```bash
python helper_server.py
python prd_builder.py
python admin_server.py
```

## Your App Development

**Use any common ports:**

- ✅ Port 3000 - Your frontend
- ✅ Port 8000 - Your backend
- ✅ Port 8001 - Your API/services

Helper tools (9000+) won't interfere.

## Project Structure

```
/
├── helper_server.py      # Dashboard (port 9000)
├── prd_builder.py        # PRD Builder (port 9001)
├── admin_server.py       # Admin Panel (port 9002)
├── automation_service.py # Setup automation
├── setup_server.py       # Setup form server
├── install_tools.py      # Tool checker/installer
├── welcome.bat           # Windows launcher
├── welcome.sh            # Mac/Linux launcher
├── user_config.json      # Your configuration
├── .env                  # API keys (auto-generated)
├── boot_lang.db          # SQLite database
└── venv/                 # Virtual environment
```

## What You Get

✅ **Clean local environment**
- Virtual environment
- Git connected to your repo
- API keys configured
- Database initialized

✅ **Helper tools**
- PRD Builder for planning
- Admin panel for monitoring
- Dashboard for quick access

✅ **Port strategy**
- Helper tools: 9000-9002
- Your app: 3000, 8000, 8001, etc.
- No conflicts

## Need Help?

Cursor agent commands in welcome.md

---

Built by SaltAIr

