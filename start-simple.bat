@echo off

REM 启动脚本 - 简单版本
REM 直接在系统Python环境中安装依赖并启动应用

echo ================================
echo 简历管理系统启动脚本（简单版）
echo ================================

REM 检查Python是否安装
python --version
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python 3.7+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python已找到

REM 升级pip
echo 升级pip...
pip install --upgrade pip
if %errorlevel% neq 0 (
    echo 警告: 升级pip失败，但继续执行
)

REM 安装依赖
echo 安装项目依赖...
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-Reuploaded==1.4.0 PyPDF2==3.0.1 python-docx==1.1.0 pdfkit==1.0.0 schedule==1.2.0
if %errorlevel% neq 0 (
    echo 错误: 安装依赖失败
    pause
    exit /b 1
)

echo 依赖安装成功

REM 检查wkhtmltopdf（PDF导出需要）
echo 检查wkhtmltopdf...
if exist "C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe" (
    echo wkhtmltopdf已找到（64位）
) else if exist "C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe" (
    echo wkhtmltopdf已找到（32位）
) else (
    echo 警告: 未找到wkhtmltopdf，PDF导出功能将不可用
    echo 建议下载安装: https://wkhtmltopdf.org/downloads.html
)

echo ================================
echo 启动应用程序...
echo 访问地址: http://localhost:5000
echo 按 Ctrl+C 停止服务
echo ================================

REM 启动应用
python app.py

REM 如果应用程序意外退出，显示错误信息
if %errorlevel% neq 0 (
    echo 错误: 应用程序启动失败
    pause
    exit /b 1
)