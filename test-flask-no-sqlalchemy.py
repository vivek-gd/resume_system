# 测试脚本 - 不导入Flask-SQLAlchemy，直接运行一个简单的Flask应用程序

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    print('启动Flask应用...')
    print('访问地址: http://localhost:5000')
    app.run(debug=False, host='0.0.0.0', port=5000)