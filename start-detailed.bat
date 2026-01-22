@echo off
chcp 65001 >nul 2>&1
cls
echo ============================================
echo    Resume System - Detailed Startup
echo ============================================
echo.

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run diagnose.bat first
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

:: Check Python
python --version
if errorlevel 1 (
    echo [ERROR] Python failed to start
    pause
    exit /b 1
)
echo.

:: Check Flask is installed
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Flask not installed
    echo Installing Flask now...
    pip install Flask
    if errorlevel 1 (
        echo [ERROR] Failed to install Flask
        pause
        exit /b 1
    )
)

:: Check Flask-Reuploaded is installed
pip show Flask-Reuploaded >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Flask-Reuploaded not installed
    echo Installing Flask-Reuploaded now...
    pip install Flask-Reuploaded
    if errorlevel 1 (
        echo [ERROR] Failed to install Flask-Reuploaded
        pause
        exit /b 1
    )
)

echo [OK] Dependencies verified
echo.

:: Check app.py exists
if not exist "app.py" (
    echo [ERROR] app.py not found!
    pause
    exit /b 1
)
echo [OK] app.py found
echo.

echo ============================================
echo    Starting Application
echo ============================================
echo.
echo Access URL: http://localhost:5000
echo Login URL:  http://localhost:5000/login
echo Username: admin
echo Password: your_new_password (change in app.py)
echo.
echo Press Ctrl+C to stop the server
echo.

:: Start app with error display
python app.py

if errorlevel 1 (
    echo.
    echo ============================================
    echo    Application Failed to Start!
    echo ============================================
    echo.
    echo Please check the error message above
)

echo.
echo Server stopped. Press any key to exit...
pause
