# 测试脚本 - 逐步导入app.py中的模块和功能

print('开始逐步导入测试...')

# 测试1: 导入基本模块
print('\n测试1: 导入基本模块')
try:
    import os
    import datetime
    import uuid
    import re
    import PyPDF2
    from docx import Document
    from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
    from flask_sqlalchemy import SQLAlchemy
    import pdfkit
    print('✓ 基本模块导入成功')
except Exception as e:
    print('✗ 基本模块导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 测试2: 初始化Flask应用
print('\n测试2: 初始化Flask应用')
try:
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print('✓ Flask应用初始化成功')
except Exception as e:
    print('✗ Flask应用初始化失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 测试3: 初始化PDF配置
print('\n测试3: 初始化PDF配置')
try:
    if os.name == 'nt':
        wkhtmltopdf_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        if not os.path.exists(wkhtmltopdf_path):
            wkhtmltopdf_path = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
        if os.path.exists(wkhtmltopdf_path):
            app.config['WKHTMLTOPDF_PATH'] = wkhtmltopdf_path
        else:
            app.config['WKHTMLTOPDF_PATH'] = None
            print('[WARNING] wkhtmltopdf not found. PDF export will be disabled.')
    else:
        app.config['WKHTMLTOPDF_PATH'] = 'wkhtmltopdf'
    
    pdf_config = None
    if app.config['WKHTMLTOPDF_PATH']:
        try:
            pdf_config = pdfkit.configuration(wkhtmltopdf=app.config['WKHTMLTOPDF_PATH'])
        except:
            pdf_config = None
            print('[WARNING] wkhtmltopdf configuration failed. PDF export will be disabled.')
    print('✓ PDF配置初始化成功')
except Exception as e:
    print('✗ PDF配置初始化失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 测试4: 初始化SQLAlchemy
print('\n测试4: 初始化SQLAlchemy')
try:
    db = SQLAlchemy(app)
    print('✓ SQLAlchemy初始化成功')
except Exception as e:
    print('✗ SQLAlchemy初始化失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 测试5: 定义数据库模型
print('\n测试5: 定义数据库模型')
try:
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
    print('✓ 数据库模型定义成功')
except Exception as e:
    print('✗ 数据库模型定义失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 测试6: 导入密码哈希处理
print('\n测试6: 导入密码哈希处理')
try:
    from werkzeug.security import generate_password_hash, check_password_hash
    
    def hash_password(password):
        return generate_password_hash(password)
    
    def verify_password(password, hashed):
        return check_password_hash(hashed, password)
    print('✓ 密码哈希处理导入成功')
except Exception as e:
    print('✗ 密码哈希处理导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 测试7: 导入parse_resume函数
print('\n测试7: 导入parse_resume函数')
try:
    from parse_resume_optimized import parse_resume_optimized as parse_resume
    print('✓ parse_resume函数导入成功')
except Exception as e:
    print('✗ parse_resume函数导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 测试8: 导入schedule模块
print('\n测试8: 导入schedule模块')
try:
    import schedule
    import time
    import threading
    
    def clean_old_histories():
        with app.app_context():
            threshold = datetime.datetime.now() - datetime.timedelta(days=90)
            old_histories = ResumeHistory.query.filter(ResumeHistory.modify_time < threshold).all()
            for h in old_histories:
                db.session.delete(h)
            db.session.commit()
            print(f"清理完成，共删除{len(old_histories)}条旧记录")
    
    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    schedule.every().day.at("02:00").do(clean_old_histories)
    print('✓ schedule模块导入成功')
except Exception as e:
    print('✗ schedule模块导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

print('\n所有测试通过！应用程序应该可以正常启动。')
print('现在尝试运行完整的app.py文件...')

# 尝试运行完整的app.py文件
try:
    import app
    print('✓ app模块导入成功')
    print('应用程序可以正常启动！')
except Exception as e:
    print('✗ app模块导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

print('\n测试完成！')