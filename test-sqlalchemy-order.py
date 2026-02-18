# 测试脚本 - 先导入pdfkit模块，然后导入Flask类，然后导入SQLAlchemy，然后创建Flask应用，然后初始化SQLAlchemy，然后打印一条消息，然后立即退出

import pdfkit

print('1. pdfkit imported successfully!')

from flask import Flask

print('2. Flask imported successfully!')

from flask_sqlalchemy import SQLAlchemy

print('3. SQLAlchemy imported successfully!')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print('4. Flask app created successfully!')

db = SQLAlchemy(app)

print('5. SQLAlchemy initialized successfully!')

print('测试完成！')