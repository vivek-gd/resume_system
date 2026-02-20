# 测试导入模块
print('开始测试导入模块...')

# 测试导入PyPDF2
try:
    import PyPDF2
    print('✓ PyPDF2 导入成功')
except Exception as e:
    print('✗ PyPDF2 导入失败:', str(e))

# 测试导入docx
try:
    from docx import Document
    print('✓ docx 导入成功')
except Exception as e:
    print('✗ docx 导入失败:', str(e))

# 测试导入pdfkit
try:
    import pdfkit
    print('✓ pdfkit 导入成功')
except Exception as e:
    print('✗ pdfkit 导入失败:', str(e))

print('开始测试Flask导入...')
# 测试导入Flask
try:
    print('尝试导入Flask...')
    from flask import Flask
    print('✓ Flask 导入成功')
except Exception as e:
    print('✗ Flask 导入失败:', str(e))
    import traceback
    traceback.print_exc()

print('开始测试Flask-SQLAlchemy导入...')
# 测试导入Flask-SQLAlchemy
try:
    print('尝试导入Flask-SQLAlchemy...')
    from flask_sqlalchemy import SQLAlchemy
    print('✓ Flask-SQLAlchemy 导入成功')
except Exception as e:
    print('✗ Flask-SQLAlchemy 导入失败:', str(e))
    import traceback
    traceback.print_exc()

print('测试完成')