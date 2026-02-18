# 测试脚本 - 先导入pdfkit模块，然后再导入Flask类，然后导入SQLAlchemy，然后创建一个Flask应用，然后初始化SQLAlchemy，然后打印一条消息，然后立即退出

import pdfkit

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print('Flask app and SQLAlchemy initialized successfully!')