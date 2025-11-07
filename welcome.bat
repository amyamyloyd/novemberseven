@echo off
REM SaltAIr Welcome Script - Windows

REM Check for restart flag (temp file)
if exist "%TEMP%\saltair_restart.flag" (
    del "%TEMP%\saltair_restart.flag"
    echo.
    echo [OK] Shell restarted - PATH updated
    echo.
    goto START_SERVER
)

REM Step 0: Check if Python is installed FIRST
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.11+ using:
    echo   winget install -e --id Python.Python.3.12
    echo.
    echo After installation completes, run this script again.
    pause
    exit /b 1
)

REM Step 1: Check and install required tools (Git, GitHub CLI, Azure CLI)
echo.
echo Checking required tools...
echo.
python install_tools.py
set INSTALL_EXIT=%errorlevel%

if %INSTALL_EXIT%==1 (
    REM Tools installed, restart needed
    echo.
    echo [OK] Tools installed successfully
    echo [RESTART] Restarting shell to update PATH...
    echo.
    
    REM Create restart flag
    echo 1 > "%TEMP%\saltair_restart.flag"
    
    REM Restart this script in new shell
    start "SaltAIr Setup" cmd /c "cd /d "%~dp0" && call "%~f0""
    exit
)

if %INSTALL_EXIT%==2 (
    REM Installation failed
    echo.
    echo [ERROR] Tool installation failed
    echo Please install missing tools manually and re-run this script
    pause
    exit /b 1
)

REM If exit code is 0, all tools present - continue

:START_SERVER
REM Check if setup server is already running
netstat -ano | findstr ":8001" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo Setup server already running.
    goto OPEN_BROWSER
)

REM Start setup server in foreground (visible output)
echo.
echo Starting SaltAIr setup server...
echo [IMPORTANT] Keep this terminal window open - you'll see all setup progress here
echo.

REM Open browser first
start http://localhost:8001/setup

REM Wait a moment for browser to open
timeout /t 2 /nobreak >nul

REM Run server in foreground - all output visible
python setup_server.py

goto END

:OPEN_BROWSER
REM Open browser if server already running
start http://localhost:8001/setup

echo.
echo Browser should open automatically to the setup page.
echo If not, visit: http://localhost:8001/setup
echo.

:END
