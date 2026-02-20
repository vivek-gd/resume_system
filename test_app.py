# 测试app.py导入
print('开始测试app.py导入...')

try:
    import sys
    import os
    
    # 添加当前目录到Python路径
    sys.path.insert(0, os.path.abspath('.'))
    
    print('尝试导入app.py...')
    import app
    print('✓ app.py 导入成功')
    
    print('测试完成')
except Exception as e:
    print('✗ 错误:', str(e))
    import traceback
    traceback.print_exc()