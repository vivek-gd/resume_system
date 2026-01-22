@echo off
chcp 65001 >nul 2>&1
cls
echo ============================================
echo    Checking Flask-Reuploaded Package
echo ============================================
echo.

call venv\Scripts\activate.bat

echo [1] Checking if Flask-Reuploaded is installed:
pip show Flask-Reuploaded
echo.

echo [2] Listing all Flask packages:
pip list | findstr -i flask
echo.

echo [3] Checking package files in site-packages:
dir venv\Lib\site-packages\ | findstr -i flask
echo.

echo [4] Testing different import names:
python -c "import flask_reuploaded; print('flask_reuploaded: OK')" 2>&1
python -c "from flask_reuploaded import *; print('from flask_reuploaded: OK')" 2>&1
python -c "import flask_uploads; print('flask_uploads: OK')" 2>&1
python -c "from flask_uploads import *; print('from flask_uploads: OK')" 2>&1
echo.

pause
