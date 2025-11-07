#!/bin/bash
# SaltAIr Welcome Script - Mac/Linux - FULLY AUTOMATED

set -e  # Exit on error

# Check for restart flag (temp file)
if [ -f "/tmp/saltair_restart.flag" ]; then
    rm -f /tmp/saltair_restart.flag
    echo ""
    echo "[OK] Shell restarted - PATH updated"
    echo ""
    # Skip to tool check after restart
    SKIP_PYTHON=1
fi

# Step 0: Check and auto-install Python if missing (only on first run)
if [ -z "$SKIP_PYTHON" ]; then
    echo ""
    echo "[CHECK] Checking Python installation..."
    
    if ! command -v python3 &> /dev/null; then
        echo "[INSTALL] Python not found - installing automatically..."
        echo ""
        
        # Check if Homebrew is installed
        if ! command -v brew &> /dev/null; then
            echo "[ERROR] Homebrew not installed"
            echo ""
            echo "Please install Homebrew first:"
            echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
            echo ""
            echo "After Homebrew is installed, run this script again."
            exit 1
        fi
        
        # Auto-install Python via brew
        brew install python@3.12
        
        if [ $? -ne 0 ]; then
            echo ""
            echo "[ERROR] Python installation failed"
            echo "Please install manually from: https://www.python.org/downloads/"
            exit 1
        fi
        
        echo ""
        echo "[OK] Python installed successfully"
        echo "[RESTART] Restarting shell to update PATH..."
        echo ""
        
        # Create restart flag
        touch /tmp/saltair_restart.flag
        
        # Restart this script in new shell
        exec bash "$0"
        exit
    else
        echo "[OK] Python found"
    fi
fi

# Step 1: Check and install required tools (Git, GitHub CLI, Azure CLI)
echo ""
echo "[CHECK] Checking required tools..."
echo ""
python3 install_tools.py
INSTALL_EXIT=$?

if [ $INSTALL_EXIT -eq 1 ]; then
    # Tools installed, restart needed
    echo ""
    echo "[OK] Tools installed successfully"
    echo "[RESTART] Restarting shell to update PATH..."
    echo ""
    
    # Create restart flag
    touch /tmp/saltair_restart.flag
    
    # Restart this script in new shell
    exec bash "$0"
    exit
fi

if [ $INSTALL_EXIT -eq 2 ]; then
    # Installation failed
    echo ""
    echo "[ERROR] Tool installation failed"
    echo "Please check the errors above and re-run this script"
    exit 1
fi

# If exit code is 0, all tools present - continue

# Check if config already exists
if [ -f "user_config.json" ]; then
    HAS_USER=$(python3 -c "import json; c=json.load(open('user_config.json')); print('yes' if c.get('user_identity',{}).get('user_name') else 'no')" 2>/dev/null || echo "no")
    
    if [ "$HAS_USER" == "yes" ] && grep -q '"setup_complete": true' user_config.json 2>/dev/null; then
        echo ""
        echo "=========================================="
        echo "  Setup already complete!"
        echo "=========================================="
        echo ""
        echo "Configuration loaded from user_config.json"
        echo ""
        echo "What would you like to do?"
        echo "  1. Start services (tell Cursor: 'Start backend' and 'Start frontend')"
        echo "  2. Build a PRD (tell Cursor: 'Help me build a PRD')"
        echo "  3. Build from existing PRD (tell Cursor: 'Build my PRD')"
        echo ""
        exit 0
    fi
fi

# Start setup server in foreground (visible output)
echo ""
echo "[START] Starting SaltAIr setup server..."
echo ""
echo "============================================================"
echo "  IMPORTANT: Keep this terminal window open"
echo "  You'll see all setup progress here in real-time"
echo "============================================================"
echo ""

# Open browser first
if command -v open &> /dev/null; then
    open http://localhost:8001/setup
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8001/setup
else
    echo "[INFO] Please open your browser to: http://localhost:8001/setup"
fi

# Wait a moment for browser to open
sleep 2

# Run server in foreground - all output visible
python3 setup_server.py
