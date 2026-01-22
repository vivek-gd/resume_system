@echo off
chcp 65001 >nul 2>&1
cls
echo ============================================
echo    Installing All Dependencies
echo ============================================
echo.

:: Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
) else (
    echo [ERROR] Virtual environment not found
    pause
    exit /b 1
)

:: Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip not available
    pause
    exit /b 1
)
echo [OK] pip ready
echo.

:: Upgrade pip
echo [1/7] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip upgraded
echo.

:: Install Flask
echo [2/7] Installing Flask...
pip install Flask --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install Flask
    pause
    exit /b 1
)
echo [OK] Flask installed
echo.

:: Install Flask-SQLAlchemy
echo [3/7] Installing Flask-SQLAlchemy...
pip install Flask-SQLAlchemy --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install Flask-SQLAlchemy
    pause
    exit /b 1
)
echo [OK] Flask-SQLAlchemy installed
echo.

:: Install Flask-Reuploaded
echo [4/7] Installing Flask-Reuploaded...
pip install Flask-Reuploaded --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install Flask-Reuploaded
    pause
    exit /b 1
)
echo [OK] Flask-Reuploaded installed
echo.

:: Install PyPDF2
echo [5/7] Installing PyPDF2...
pip install PyPDF2 --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install PyPDF2
    pause
    exit /b 1
)
echo [OK] PyPDF2 installed
echo.

:: Install python-docx
echo [6/7] Installing python-docx...
pip install python-docx --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install python-docx
    pause
    exit /b 1
)
echo [OK] python-docx installed
echo.

:: Install pdfkit
echo [7/7] Installing pdfkit...
pip install pdfkit --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install pdfkit
    pause
    exit /b 1
)
echo [OK] pdfkit installed
echo.

echo ============================================
echo    All Dependencies Installed!
echo ============================================
echo.
echo Verifying installation...
pip show Flask-Reuploaded
echo.

pause
