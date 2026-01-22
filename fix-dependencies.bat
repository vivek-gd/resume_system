@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo    Fixing Dependencies
echo ============================================
echo.

:: Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] Virtual environment not found
    pause
    exit /b 1
)

:: Remove old packages
echo [1] Removing incompatible packages...
pip uninstall -y Flask-Uploads

:: Install compatible versions
echo.
echo [2] Installing compatible packages...
pip install Werkzeug==2.3.8
pip install Flask-Reuploaded==1.4.0

:: Reinstall all dependencies
echo.
echo [3] Reinstalling all dependencies...
pip install -r requirements.txt

echo.
echo ============================================
echo    Fix Complete!
echo ============================================
echo.
echo Now run: start-quick.bat
echo.
pause
