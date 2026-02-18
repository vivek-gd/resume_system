@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo    简历管理系统启动脚本
echo ============================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] 未找到Python，请先安装Python 3.7+
    echo [INFO] 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python已找到

REM 检查虚拟环境是否存在
if not exist "venv" (
    echo [INFO] 创建虚拟环境...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo [OK] 虚拟环境创建成功
)

REM 激活虚拟环境
echo [INFO] 激活虚拟环境...
call "venv\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo [ERROR] 激活虚拟环境失败
    pause
    exit /b 1
)
echo [OK] 虚拟环境激活成功

REM 升级pip
echo [INFO] 升级pip...
pip install --upgrade pip >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] 升级pip失败，但继续执行
)

REM 安装依赖
echo [INFO] 安装项目依赖...
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 PyPDF2==3.0.1 python-docx==1.1.0 pdfkit==1.0.0 schedule==1.2.0
if %errorlevel% neq 0 (
    echo [ERROR] 安装依赖失败
    pause
    exit /b 1
)
echo [OK] 依赖安装成功

REM 检查wkhtmltopdf（PDF导出需要）
echo [INFO] 检查wkhtmltopdf...
if exist "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" (
    echo [OK] wkhtmltopdf已找到（64位）
) else if exist "C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe" (
    echo [OK] wkhtmltopdf已找到（32位）
) else (
    echo [WARNING] 未找到wkhtmltopdf，PDF导出功能将不可用
    echo [INFO] 建议下载安装: https://wkhtmltopdf.org/downloads.html
)

REM 启动应用
echo.
echo [INFO] 启动Flask应用...
echo [INFO] 访问地址: http://localhost:5000
echo [INFO] 按 Ctrl+C 停止服务
echo.
python app.py

REM 如果应用程序意外退出，显示错误信息
if %errorlevel% neq 0 (
    echo [ERROR] 应用程序启动失败
    pause
    exit /b 1
)

pause