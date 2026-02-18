# 测试脚本 - 只导入Flask类

print('开始测试Flask导入...')

# 只导入Flask类
try:
    from flask import Flask
    print('✓ Flask 导入成功')
except Exception as e:
    print('✗ Flask 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 测试创建Flask应用
try:
    app = Flask(__name__)
    print('✓ Flask应用创建成功')
except Exception as e:
    print('✗ Flask应用创建失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

print('\nFlask测试通过！')
print('测试完成。')