# 只测试基本的Flask应用启动
print('开始测试Flask应用...')

# 首先导入Flask
from flask import Flask
print('✓ Flask导入成功')

# 创建Flask应用
app = Flask(__name__)
print('✓ Flask应用创建成功')

# 添加一个简单的路由
@app.route('/')
def hello():
    return 'Hello, World!'

print('✓ 路由添加成功')

# 启动应用
if __name__ == '__main__':
    print('启动Flask应用...')
    print('访问地址: http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)