@echo off
REM Full reset for clean testing - removes ALL artifacts

echo ========================================
echo FULL RESET - Clean Test Environment
echo ========================================
echo.

echo [1/10] Stopping setup server...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8001" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo [2/10] Logging out of GitHub CLI...
"C:\Program Files\GitHub CLI\gh.exe" auth logout --hostname github.com 2>nul
if errorlevel 1 (
    echo GitHub CLI not authenticated or not found
)

echo [3/10] Uninstalling GitHub CLI...
winget uninstall GitHub.cli --silent >nul 2>&1

echo [4/10] Logging out of Azure CLI...
"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd" logout 2>nul
if errorlevel 1 (
    echo Azure CLI not authenticated or not found
)

echo [5/10] Uninstalling Azure CLI...
winget uninstall Microsoft.AzureCLI --silent >nul 2>&1

echo [6/10] Removing virtual environment...
if exist venv (
    rmdir /S /Q venv
    echo   Removed venv/
) else (
    echo   No venv found
)

echo [7/10] Removing database file...
if exist boot_lang.db (
    del boot_lang.db
    echo   Removed boot_lang.db
) else (
    echo   No database file found
)

echo [8/10] Removing GitHub workflows...
if exist .github\workflows (
    rmdir /S /Q .github\workflows
    echo   Removed .github/workflows/
) else (
    echo   No workflows found
)

echo [9/10] Removing logs...
if exist setup_progress.log (
    del setup_progress.log
    echo   Removed setup_progress.log
)
if exist user_config.json (
    del user_config.json
    echo   Removed user_config.json
)

echo [10/10] Resetting Git state...
git reset --hard HEAD >nul 2>&1
git clean -fd >nul 2>&1
echo   Git workspace reset

echo.
echo ========================================
echo [OK] Full reset complete!
echo ========================================
echo.
echo Ready for clean test. Run welcome.bat to start.
echo.
pause

