@echo off
:: Quick start script - minimal checks
echo Starting Resume System...
echo.

:: Try to activate venv if exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

:: Install dependencies if needed
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

:: Start app
echo.
echo Running on http://localhost:5000
echo Press Ctrl+C to stop
echo.
python app.py

pause
