# 调试版app.py文件

import os
import datetime
import re
import PyPDF2
import uuid
from docx import Document
import pdfkit

print('开始初始化应用...')

# 尝试导入Flask
try:
    print('尝试导入Flask...')
    from flask import Flask
    print('✓ Flask 导入成功')
    
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print('✓ Flask应用初始化成功')
    
except Exception as e:
    print('✗ Flask 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

print('Flask应用初始化成功，现在退出...')
exit(0)