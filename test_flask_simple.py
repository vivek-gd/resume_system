# 简单测试Flask导入
print('开始测试Flask导入...')

# 尝试导入Flask
try:
    print('尝试导入Flask...')
    from flask import Flask
    print('✓ Flask 导入成功')
    
    print('测试完成')
except Exception as e:
    print('✗ 错误:', str(e))
    import traceback
    traceback.print_exc()