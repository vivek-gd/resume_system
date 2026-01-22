@echo off
chcp 65001 >nul 2>&1
cls
echo ========================================
echo   Resume System Launcher
echo ========================================
echo.

:: Check Python environment
where python >nul 2>&1
if errorlevel 1 (
    where python3 >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python not found, please install Python 3.7+
        echo         Download: https://www.python.org/downloads/
        pause
        exit /b 1
    ) else (
        set PYTHON=python3
    )
) else (
    set PYTHON=python
)
%PYTHON% --version

:: 检查虚拟环境
if not exist "venv" (
    echo [提示] 正在创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo [成功] 虚拟环境创建完成
)

:: Check virtual environment
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    %PYTHON% -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created
)

:: Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] venv\Scripts\activate.bat not found
    pause
    exit /b 1
)

:: Check dependencies
echo [INFO] Checking dependencies...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [SUCCESS] Dependencies installed
)

:: Check wkhtmltopdf
echo [INFO] Checking PDF export tool...
if not exist "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" (
    if not exist "C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe" (
        echo [WARNING] wkhtmltopdf not found, PDF export unavailable
        echo [INFO] Download: https://wkhtmltopdf.org/downloads.html
        echo.
    )
)

:: Start service
echo.
echo [SUCCESS] Starting service...
echo [INFO] Access URL: http://localhost:5000
echo [INFO] Login username: admin
echo [INFO] Default password: your_new_password (change in app.py)
echo.
echo Press Ctrl+C to stop service
echo.

python app.py

pause
