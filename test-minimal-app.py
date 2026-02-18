# 测试脚本 - 只包含最基本的Flask应用程序结构

import pdfkit

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    print('启动Flask应用...')
    print('访问地址: http://localhost:5000')
    app.run(debug=False, host='0.0.0.0', port=5000)