# 测试脚本 - 导入Flask类，创建Flask应用，然后打印一条消息，然后立即退出

from flask import Flask

app = Flask(__name__)

print('Flask app created successfully!')