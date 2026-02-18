# 测试脚本 - 逐个导入app.py中使用的其他模块

print('开始测试模块导入...')

# 导入Flask
print('\n1. 导入Flask...')
try:
    from flask import Flask
    print('✓ Flask 导入成功')
except Exception as e:
    print('✗ Flask 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 导入SQLAlchemy
print('\n2. 导入SQLAlchemy...')
try:
    from flask_sqlalchemy import SQLAlchemy
    print('✓ SQLAlchemy 导入成功')
except Exception as e:
    print('✗ SQLAlchemy 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 导入pdfkit
print('\n3. 导入pdfkit...')
try:
    import pdfkit
    print('✓ pdfkit 导入成功')
except Exception as e:
    print('✗ pdfkit 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 导入PyPDF2
print('\n4. 导入PyPDF2...')
try:
    import PyPDF2
    print('✓ PyPDF2 导入成功')
except Exception as e:
    print('✗ PyPDF2 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 导入docx
print('\n5. 导入docx...')
try:
    from docx import Document
    print('✓ docx 导入成功')
except Exception as e:
    print('✗ docx 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 导入werkzeug.security
print('\n6. 导入werkzeug.security...')
try:
    from werkzeug.security import generate_password_hash, check_password_hash
    print('✓ werkzeug.security 导入成功')
except Exception as e:
    print('✗ werkzeug.security 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 导入schedule
print('\n7. 导入schedule...')
try:
    import schedule
    print('✓ schedule 导入成功')
except Exception as e:
    print('✗ schedule 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 导入parse_resume_optimized
print('\n8. 导入parse_resume_optimized...')
try:
    from parse_resume_optimized import parse_resume_optimized
    print('✓ parse_resume_optimized 导入成功')
except Exception as e:
    print('✗ parse_resume_optimized 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

print('\n所有模块导入成功！')
print('测试完成。')