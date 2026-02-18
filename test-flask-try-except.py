# 测试脚本 - 使用try-except块来捕获导入Flask时可能出现的异常

print('开始测试...')

try:
    from flask import Flask
    print('Flask imported successfully!')
except Exception as e:
    print('Flask导入失败:', str(e))
    import traceback
    traceback.print_exc()

print('测试完成！')