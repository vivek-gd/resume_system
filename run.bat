@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo    Starting Resume System
echo ============================================
echo.

:: Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call "venv\Scripts\activate.bat"
    echo [OK] Virtual environment activated
) else (
    echo [ERROR] Virtual environment not found
    pause
    exit /b 1
)

:: Start application
echo.
echo [INFO] Starting Flask application...
echo [INFO] Access URL: http://localhost:5000
echo [INFO] Press Ctrl+C to stop
echo.
python app.py

pause