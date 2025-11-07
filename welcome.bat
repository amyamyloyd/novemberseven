@echo off
REM SaltAIr Welcome Script - Windows - FULLY AUTOMATED

REM Check for restart flag (temp file)
if exist "%TEMP%\saltair_restart.flag" (
    del "%TEMP%\saltair_restart.flag"
    echo.
    echo [OK] Shell restarted - PATH updated
    echo.
    goto CHECK_TOOLS
)

REM Step -1: Find winget (may not be in PATH)
echo.
echo [CHECK] Locating winget...

REM Try winget in PATH first
winget --version >nul 2>&1
if %errorlevel% equ 0 (
    set "WINGET_CMD=winget"
    echo [OK] winget found in PATH
    goto CHECK_PYTHON
)

REM Not in PATH - search common locations
echo [WARN] winget not in PATH - searching common locations...

REM Check WindowsApps folder
set "WINGET_CMD=%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\winget.exe"
if exist "%WINGET_CMD%" (
    echo [OK] winget found at: %WINGET_CMD%
    goto CHECK_PYTHON
)

REM Check Program Files
for /d %%i in ("C:\Program Files\WindowsApps\Microsoft.DesktopAppInstaller_*") do (
    if exist "%%i\winget.exe" (
        set "WINGET_CMD=%%i\winget.exe"
        echo [OK] winget found at: %%i\winget.exe
        goto CHECK_PYTHON
    )
)

REM Winget not found - error
echo.
echo [ERROR] winget not found
echo.
echo Please install "App Installer" from Microsoft Store:
echo https://apps.microsoft.com/store/detail/app-installer/9NBLGGH4NNS1
echo.
echo Or update Windows to the latest version (winget comes pre-installed on Windows 10/11)
pause
exit /b 1

:CHECK_PYTHON

REM Step 0: Check and auto-install Python if missing
echo.
echo [CHECK] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INSTALL] Python not found - installing automatically...
    echo.
    echo [UAC] You may see a User Account Control prompt - please approve it
    echo.
    
    REM Auto-install Python via winget
    "%WINGET_CMD%" install -e --id Python.Python.3.12
    
    if %errorlevel% neq 0 (
        echo.
        echo [ERROR] Python installation failed
        echo Please install manually from: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    
    echo.
    echo [OK] Python installed successfully
    echo [RESTART] Restarting shell to update PATH...
    echo.
    
    REM Create restart flag
    echo 1 > "%TEMP%\saltair_restart.flag"
    
    REM Restart this script in new shell
    start "SaltAIr Setup" cmd /c "cd /d "%~dp0" && call "%~f0""
    exit
) else (
    echo [OK] Python found
)

:CHECK_TOOLS
REM Step 1: Check and install required tools (Git, GitHub CLI, Azure CLI)
echo.
echo [CHECK] Checking required tools...
echo.
python install_tools.py "%WINGET_CMD%"
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
    echo Please check the errors above and re-run this script
    pause
    exit /b 1
)

REM If exit code is 0, all tools present - continue

:START_SERVER
REM Check if setup server is already running
netstat -ano | findstr ":8001" | findstr "LISTENING" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] Setup server already running.
    goto OPEN_BROWSER
)

REM Start setup server in foreground (visible output)
echo.
echo [START] Starting SaltAIr setup server...
echo.
echo ============================================================
echo   IMPORTANT: Keep this terminal window open
echo   You'll see all setup progress here in real-time
echo ============================================================
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
echo [INFO] Browser should open automatically to the setup page.
echo [INFO] If not, visit: http://localhost:8001/setup
echo.

:END
