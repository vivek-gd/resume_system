# 测试脚本 - 先导入pdfkit模块，然后再导入Flask类，然后创建一个Flask应用，然后打印一条消息，然后立即退出

import pdfkit

from flask import Flask

app = Flask(__name__)

print('Flask app created successfully!')