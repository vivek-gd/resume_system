# 测试所有必要的模块导入
print('开始测试模块导入...')

try:
    import os
    print('✓ os 导入成功')
except Exception as e:
    print('✗ os 导入失败:', str(e))

try:
    import datetime
    print('✓ datetime 导入成功')
except Exception as e:
    print('✗ datetime 导入失败:', str(e))

try:
    import re
    print('✓ re 导入成功')
except Exception as e:
    print('✗ re 导入失败:', str(e))

try:
    import PyPDF2
    print('✓ PyPDF2 导入成功')
except Exception as e:
    print('✗ PyPDF2 导入失败:', str(e))

try:
    from docx import Document
    print('✓ python-docx 导入成功')
except Exception as e:
    print('✗ python-docx 导入失败:', str(e))

try:
    import pdfkit
    print('✓ pdfkit 导入成功')
except Exception as e:
    print('✗ pdfkit 导入失败:', str(e))

try:
    import uuid
    print('✓ uuid 导入成功')
except Exception as e:
    print('✗ uuid 导入失败:', str(e))

try:
    from flask import Flask
    print('✓ Flask 导入成功')
except Exception as e:
    print('✗ Flask 导入失败:', str(e))

try:
    from flask_sqlalchemy import SQLAlchemy
    print('✓ Flask-SQLAlchemy 导入成功')
except Exception as e:
    print('✗ Flask-SQLAlchemy 导入失败:', str(e))

try:
    from werkzeug.security import generate_password_hash, check_password_hash
    print('✓ werkzeug.security 导入成功')
except Exception as e:
    print('✗ werkzeug.security 导入失败:', str(e))

try:
    import schedule
    print('✓ schedule 导入成功')
except Exception as e:
    print('✗ schedule 导入失败:', str(e))

print('模块导入测试完成！')