# 测试schedule模块导入
print('开始测试schedule模块导入...')

try:
    import schedule
    print('✓ schedule 导入成功')
    
    import time
    print('✓ time 导入成功')
    
    import threading
    print('✓ threading 导入成功')
    
    print('测试完成')
except Exception as e:
    print('✗ 错误:', str(e))
    import traceback
    traceback.print_exc()