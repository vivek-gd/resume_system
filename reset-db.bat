@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo    Reset Database
echo ============================================
echo.
echo [WARNING] This will delete all data!
echo.
set /p confirm="Are you sure? (y/n): "
if /i not "%confirm%"=="y" (
    echo Operation cancelled.
    pause
    exit /b 0
)

echo.
echo [1/3] Stopping any running instances...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 >nul

echo [2/3] Removing old database...
if exist "resume.db" (
    del resume.db
    echo Database removed.
)

echo [3/3] Done!
echo.
echo The database will be recreated when you start the application.
echo.
pause
