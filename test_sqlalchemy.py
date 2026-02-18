# 测试SQLAlchemy导入
print('开始测试SQLAlchemy导入...')

try:
    import sqlalchemy
    print('✓ sqlalchemy 导入成功')
    print('SQLAlchemy版本:', sqlalchemy.__version__)
except Exception as e:
    print('✗ sqlalchemy 导入失败:', str(e))
    import traceback
    traceback.print_exc()

print('测试完成！')