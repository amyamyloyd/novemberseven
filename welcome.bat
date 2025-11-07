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

REM Step 1: Check and install required tools
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

REM Start setup server
echo.
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
