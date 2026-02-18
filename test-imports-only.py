# 只测试模块导入
print('开始测试模块导入...')

# 逐个测试模块导入
try:
    import flask
    print('✓ flask 导入成功')
except Exception as e:
    print('✗ flask 导入失败:', str(e))
    import traceback
    traceback.print_exc()

try:
    from flask import Flask
    print('✓ Flask 导入成功')
except Exception as e:
    print('✗ Flask 导入失败:', str(e))
    import traceback
    traceback.print_exc()

try:
    import sqlalchemy
    print('✓ sqlalchemy 导入成功')
except Exception as e:
    print('✗ sqlalchemy 导入失败:', str(e))
    import traceback
    traceback.print_exc()

try:
    from flask_sqlalchemy import SQLAlchemy
    print('✓ Flask-SQLAlchemy 导入成功')
except Exception as e:
    print('✗ Flask-SQLAlchemy 导入失败:', str(e))
    import traceback
    traceback.print_exc()

try:
    import werkzeug
    print('✓ werkzeug 导入成功')
except Exception as e:
    print('✗ werkzeug 导入失败:', str(e))
    import traceback
    traceback.print_exc()

try:
    from werkzeug.security import generate_password_hash, check_password_hash
    print('✓ werkzeug.security 导入成功')
except Exception as e:
    print('✗ werkzeug.security 导入失败:', str(e))
    import traceback
    traceback.print_exc()

print('模块导入测试完成！')