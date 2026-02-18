# 简化版Flask应用程序

import os
import datetime
import uuid
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import pdfkit  # 添加pdfkit导入

# 初始化Flask应用
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Session加密
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# PDF导出配置
if os.name == 'nt':  # Windows系统
    wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    if not os.path.exists(wkhtmltopdf_path):
        wkhtmltopdf_path = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
    if os.path.exists(wkhtmltopdf_path):
        app.config['WKHTMLTOPDF_PATH'] = wkhtmltopdf_path
    else:
        app.config['WKHTMLTOPDF_PATH'] = None
        print('[WARNING] wkhtmltopdf not found. PDF export will be disabled.')
else:  # Linux/Mac系统
    app.config['WKHTMLTOPDF_PATH'] = 'wkhtmltopdf'

# 初始化PDF配置
pdf_config = None
if app.config['WKHTMLTOPDF_PATH']:
    try:
        pdf_config = pdfkit.configuration(wkhtmltopdf=app.config['WKHTMLTOPDF_PATH'])
    except:
        pdf_config = None
        print('[WARNING] wkhtmltopdf configuration failed. PDF export will be disabled.')

# 初始化扩展
db = SQLAlchemy(app)

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

class ResumeHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    modify_time = db.Column(db.DateTime, default=datetime.datetime.now)
    operator = db.Column(db.String(20), default='admin')
    old_name = db.Column(db.String(50))
    old_job = db.Column(db.String(50))
    old_intro = db.Column(db.Text)
    old_phone = db.Column(db.String(20))
    old_email = db.Column(db.String(100))
    old_education = db.Column(db.Text)
    old_experience = db.Column(db.Text)
    old_skills = db.Column(db.Text)
    old_certificates = db.Column(db.Text)
    old_avatar = db.Column(db.String(100))
    remark = db.Column(db.String(200))

# 密码哈希处理
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed):
    return check_password_hash(hashed, password)

# 权限装饰器
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# 路由
@app.route('/')
def index():
    return 'Hello, Resume System!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    return 'Login Page'

@app.route('/register', methods=['GET', 'POST'])
def register():
    return 'Register Page'

@app.route('/dashboard')
@login_required
def dashboard():
    return 'Dashboard Page'

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    return 'Edit Page'

@app.route('/history')
@login_required
def history():
    return 'History Page'

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# 初始化数据库
def init_db():
    with app.app_context():
        db.create_all()
        # 创建默认文件夹
        os.makedirs('static/photos', exist_ok=True)
        os.makedirs('static/documents', exist_ok=True)

# 主函数
if __name__ == '__main__':
    # 初始化数据库
    print('初始化数据库...')
    init_db()
    # 启动应用程序
    print('启动应用程序...')
    print('访问地址: http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)