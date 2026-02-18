# 测试脚本 - 使用try-except块来捕获导入Flask时可能出现的异常，但是在导入Flask之前，不导入任何其他的模块

print('开始测试...')

# 直接导入Flask类，使用try-except块来捕获可能出现的异常
try:
    from flask import Flask
    print('Flask imported successfully!')
except Exception as e:
    print('Flask导入失败:', str(e))
    import traceback
    traceback.print_exc()

print('测试完成！')