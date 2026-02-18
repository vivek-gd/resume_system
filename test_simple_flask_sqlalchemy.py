# 简单测试Flask-SQLAlchemy导入
print('开始测试Flask-SQLAlchemy导入...')

try:
    print('尝试导入Flask...')
    from flask import Flask
    print('✓ Flask 导入成功')
    
    print('尝试导入Flask-SQLAlchemy...')
    from flask_sqlalchemy import SQLAlchemy
    print('✓ Flask-SQLAlchemy 导入成功')
    
    print('所有测试都通过了！')
except Exception as e:
    print('✗ 测试失败:', str(e))
    import traceback
    traceback.print_exc()

print('测试完成！')