# 简单测试SQLAlchemy导入
print('开始测试SQLAlchemy导入...')

# 只导入SQLAlchemy
try:
    print('尝试导入SQLAlchemy...')
    from flask_sqlalchemy import SQLAlchemy
    print('✓ SQLAlchemy 导入成功')
    
    print('测试完成')
except Exception as e:
    print('✗ 错误:', str(e))
    import traceback
    traceback.print_exc()