# 逐步测试app.py
print('开始逐步测试app.py...')

try:
    import sys
    import os
    
    # 添加当前目录到Python路径
    sys.path.insert(0, os.path.abspath('.'))
    
    print('1. 测试基础导入...')
    import os
    import datetime
    import re
    import PyPDF2
    import uuid
    from docx import Document
    import pdfkit
    print('✓ 基础导入成功')
    
    print('2. 测试Flask导入...')
    from flask import Flask
    print('✓ Flask导入成功')
    
    print('3. 测试SQLAlchemy导入...')
    from flask_sqlalchemy import SQLAlchemy
    print('✓ SQLAlchemy导入成功')
    
    print('4. 测试parse_resume导入...')
    from parse_resume_optimized import parse_resume_optimized as parse_resume
    print('✓ parse_resume导入成功')
    
    print('5. 测试werkzeug.security导入...')
    from werkzeug.security import generate_password_hash, check_password_hash
    print('✓ werkzeug.security导入成功')
    
    print('6. 测试schedule导入...')
    import schedule
    import time
    import threading
    print('✓ schedule导入成功')
    
    print('测试完成')
except Exception as e:
    print('✗ 错误:', str(e))
    import traceback
    traceback.print_exc()