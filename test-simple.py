# 简单测试脚本 - 只导入Flask类并运行一个简单的路由

print('开始测试简单Flask应用...')

# 只导入Flask类
try:
    from flask import Flask
    print('✓ Flask 导入成功')
except Exception as e:
    print('✗ Flask 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 创建Flask应用
try:
    app = Flask(__name__)
    print('✓ Flask应用创建成功')
except Exception as e:
    print('✗ Flask应用创建失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 定义一个简单的路由
@app.route('/')
def index():
    return 'Hello, World!'

# 主函数
if __name__ == '__main__':
    print('启动Flask应用...')
    print('访问地址: http://localhost:5000')
    app.run(debug=False, host='0.0.0.0', port=5000)