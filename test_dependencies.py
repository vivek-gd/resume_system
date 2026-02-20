# 逐个测试依赖项
print('开始逐个测试依赖项...')

try:
    print('1. 测试Flask...')
    from flask import Flask
    app = Flask(__name__)
    print('✓ Flask 测试成功')
    
except Exception as e:
    print('✗ Flask 测试失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

try:
    print('2. 测试SQLAlchemy...')
    from flask_sqlalchemy import SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    print('✓ SQLAlchemy 测试成功')
    
except Exception as e:
    print('✗ SQLAlchemy 测试失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

try:
    print('3. 测试PyPDF2...')
    import PyPDF2
    print('✓ PyPDF2 测试成功')
    
except Exception as e:
    print('✗ PyPDF2 测试失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

try:
    print('4. 测试python-docx...')
    from docx import Document
    print('✓ python-docx 测试成功')
    
except Exception as e:
    print('✗ python-docx 测试失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

try:
    print('5. 测试pdfkit...')
    import pdfkit
    print('✓ pdfkit 测试成功')
    
except Exception as e:
    print('✗ pdfkit 测试失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

try:
    print('6. 测试schedule...')
    import schedule
    import time
    import threading
    print('✓ schedule 测试成功')
    
except Exception as e:
    print('✗ schedule 测试失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

try:
    print('7. 测试parse_resume...')
    from parse_resume_optimized import parse_resume_optimized as parse_resume
    print('✓ parse_resume 测试成功')
    
except Exception as e:
    print('✗ parse_resume 测试失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

print('所有依赖项测试成功！')