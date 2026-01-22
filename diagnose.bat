@echo off
chcp 65001 >nul 2>&1
cls
echo ============================================
echo    Resume System - Diagnostic Tool
echo ============================================
echo.

echo [1] Checking Python...
where python >nul 2>&1
if errorlevel 1 (
    echo [X] Python not found in PATH
    echo.
    echo Please install Python first:
    echo 1. Visit: https://www.python.org/downloads/
    echo 2. Download Python 3.9 or higher
    echo 3. IMPORTANT: Check "Add Python to PATH" during installation
    echo 4. After installation, restart this diagnostic
    echo.
    goto :end
) else (
    echo [OK] Python found
    python --version
    echo.
)

echo [2] Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [X] pip not found
    echo.
    goto :end
) else (
    echo [OK] pip found
    pip --version
    echo.
)

echo [3] Checking virtual environment...
if exist "venv\Scripts\activate.bat" (
    echo [OK] Virtual environment exists
    call venv\Scripts\activate.bat
    echo     Activated
) else (
    echo [INFO] No virtual environment found
    echo     Creating one now...
    python -m venv venv
    if errorlevel 1 (
        echo [X] Failed to create virtual environment
        goto :end
    ) else (
        echo [OK] Virtual environment created
        call venv\Scripts\activate.bat
    )
    echo.
)

echo [4] Checking dependencies...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo [INFO] Flask not installed, installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [X] Failed to install dependencies
        echo.
        echo Try manually: pip install -r requirements.txt
        goto :end
    ) else (
        echo [OK] Dependencies installed
    )
) else (
    echo [OK] Flask already installed
    pip show Flask | findstr Version
)
echo.

echo [5] Checking app.py...
if not exist "app.py" (
    echo [X] app.py not found!
) else (
    echo [OK] app.py exists
)
echo.

echo [6] Checking wkhtmltopdf (for PDF export)...
if exist "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" (
    echo [OK] wkhtmltopdf found (64-bit)
) else if exist "C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe" (
    echo [OK] wkhtmltopdf found (32-bit)
) else (
    echo [WARNING] wkhtmltopdf not found
    echo     PDF export will be unavailable
    echo     Download: https://wkhtmltopdf.org/downloads.html
    echo     (This is optional, the app will still work)
)
echo.

echo ============================================
echo    All checks complete!
echo ============================================
echo.
echo You can now run: start-quick.bat
echo.

:end
pause
