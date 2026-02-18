# 测试脚本 - 导入Flask类，创建Flask应用，导入SQLAlchemy，创建SQLAlchemy实例，然后立即退出

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

print('Flask app and SQLAlchemy instance created successfully!')