# 简化版app.py文件

import os
import datetime
import re
import PyPDF2
import uuid
from docx import Document
import pdfkit

print('开始初始化应用...')

try:
    from flask import Flask
    print('✓ Flask 导入成功')
    
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print('✓ Flask应用初始化成功')
    
except Exception as e:
    print('✗ Flask 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

try:
    from flask_sqlalchemy import SQLAlchemy
    print('✓ SQLAlchemy 导入成功')
    
    db = SQLAlchemy(app)
    print('✓ SQLAlchemy初始化成功')
    
except Exception as e:
    print('✗ SQLAlchemy 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    unique_id = db.Column(db.String(36), unique=True, nullable=True)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    job = db.Column(db.String(50))
    intro = db.Column(db.Text)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    education = db.Column(db.Text)
    experience = db.Column(db.Text)
    skills = db.Column(db.Text)
    certificates = db.Column(db.Text)
    avatar = db.Column(db.String(100))
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    is_public = db.Column(db.Boolean, default=True)

print('✓ 数据库模型定义成功')

# 导入解析函数
try:
    from parse_resume_optimized import parse_resume_optimized as parse_resume
    print('✓ parse_resume函数导入成功')
except Exception as e:
    print('✗ parse_resume函数导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 路由
@app.route('/')
def index():
    return 'Hello, World!'

# 初始化数据库
def init_db():
    with app.app_context():
        db.create_all()
        print('✓ 数据库初始化成功')

# 主函数
if __name__ == '__main__':
    print('初始化数据库...')
    init_db()
    print('启动应用程序...')
    print('访问地址: http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)