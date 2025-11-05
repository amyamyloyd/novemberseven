@echo off
REM SaltAIr Welcome Script - Windows

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo.
    echo AGENT: Install Python using this command:
    echo winget install -e --id Python.Python.3.12
    echo.
    echo After installation completes, run this script again.
    pause
    exit /b 1
)

REM Check if setup server is already running
netstat -ano | findstr ":8001" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo Setup server already running.
    goto OPEN_BROWSER
)

REM Start setup server in background
echo Starting SaltAIr setup server...
start /B python setup_server.py

REM Wait for server to start
timeout /t 3 /nobreak >nul

:OPEN_BROWSER
REM Open browser automatically
start http://localhost:8001/setup

echo.
echo Browser should open automatically to the setup page.
echo If not, visit: http://localhost:8001/setup
echo.

