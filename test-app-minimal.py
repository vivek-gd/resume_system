# 测试脚本 - 复制app.py文件的内容，但是只保留最基本的部分

import os
import datetime
import re
import PyPDF2
import uuid
from docx import Document
import pdfkit  # 先导入pdfkit模块，然后再导入Flask类

print('开始初始化应用...')

# 延迟导入Flask和其他模块
try:
    from flask import Flask
    print('✓ Flask 导入成功')
except Exception as e:
    print('✗ Flask 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 初始化Flask应用
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Session加密
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 文件上传配置
app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
# 富文本编辑配置
app.config['EDITS_SUMMERNOTE'] = True  # 启用Summernote编辑器
app.config['EDITS_LOCKED'] = True      # 启用编辑锁
app.config['EDITS_USERNAME'] = 'admin' # 编辑账号
app.config['EDITS_PASSWORD'] = 'your_new_password' # 请修改密码
# 新增：PDF导出配置（wkhtmltopdf路径，Windows需指定，Linux/Mac可省略）
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

print('✓ Flask应用初始化成功')

# 延迟导入SQLAlchemy
try:
    from flask_sqlalchemy import SQLAlchemy
    print('✓ SQLAlchemy 导入成功')
except Exception as e:
    print('✗ SQLAlchemy 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 初始化扩展
db = SQLAlchemy(app)
print('✓ SQLAlchemy初始化成功')

# 允许的文件类型
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# 新增：初始化PDF配置
if app.config['WKHTMLTOPDF_PATH']:
    try:
        pdf_config = pdfkit.configuration(wkhtmltopdf=app.config['WKHTMLTOPDF_PATH'])
        print('✓ PDF配置初始化成功')
    except:
        pdf_config = None
        print('[WARNING] wkhtmltopdf configuration failed. PDF export will be disabled.')
else:
    pdf_config = None

# ---------------------- 数据库模型 ----------------------
# 用户表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # 存储哈希后的密码
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    resumes = db.relationship('Resume', backref='user', lazy=True)
    # 新增：用户唯一标识符，用于生成个人简历链接
    unique_id = db.Column(db.String(36), unique=True, nullable=True)

# 简历主表
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    job = db.Column(db.String(50))
    intro = db.Column(db.Text)  # 个人简介
    phone = db.Column(db.String(20))  # 联系电话
    email = db.Column(db.String(100))  # 电子邮箱
    education = db.Column(db.Text)  # 教育经历（富文本）
    experience = db.Column(db.Text) # 工作/项目经历（富文本）
    skills = db.Column(db.Text)     # 技能清单
    certificates = db.Column(db.Text)  # 证书/荣誉
    avatar = db.Column(db.String(100)) # 头像路径
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    is_public = db.Column(db.Boolean, default=True)  # 是否公开简历

# 版本记录主表
class ResumeHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    modify_time = db.Column(db.DateTime, default=datetime.datetime.now)
    operator = db.Column(db.String(20), default='admin')  # 操作人
    # 存储修改前的内容
    old_name = db.Column(db.String(50))
    old_job = db.Column(db.String(50))
    old_intro = db.Column(db.Text)  # 个人简介
    old_phone = db.Column(db.String(20))  # 联系电话
    old_email = db.Column(db.String(100))  # 电子邮箱
    old_education = db.Column(db.Text)
    old_experience = db.Column(db.Text)
    old_skills = db.Column(db.Text)
    old_certificates = db.Column(db.Text)  # 证书/荣誉
    old_avatar = db.Column(db.String(100))
    # 新增：版本备注字段
    remark = db.Column(db.String(200))  # 版本备注

print('✓ 数据库模型定义成功')

# ---------------------- 密码哈希处理函数 ----------------------
try:
    from werkzeug.security import generate_password_hash, check_password_hash
    print('✓ werkzeug.security 导入成功')
except Exception as e:
    print('✗ werkzeug.security 导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

def hash_password(password):
    """生成密码哈希值"""
    return generate_password_hash(password)

def verify_password(password, hashed):
    """验证密码"""
    return check_password_hash(hashed, password)

# ---------------------- 权限装饰器 ----------------------
def login_required(f):
    def wrapper(*args, **kwargs):
        from flask import session, redirect, url_for
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# ---------------------- 路由接口 ----------------------
# 登录页
@app.route('/login', methods=['GET', 'POST'])
def login():
    from flask import request, redirect, url_for, session, flash, render_template
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # 尝试查找用户
        user = User.query.filter_by(username=username).first()
        
        if user and verify_password(password, user.password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))
        
        # 兼容旧的管理员登录方式
        if username == app.config['EDITS_USERNAME'] and password == app.config['EDITS_PASSWORD']:
            # 检查管理员用户是否存在，不存在则创建
            admin_user = User.query.filter_by(username=username).first()
            if not admin_user:
                admin_user = User(
                    username=username,
                    password=hash_password(password),
                    email='admin@example.com',
                    unique_id=str(uuid.uuid4())
                )
                db.session.add(admin_user)
                db.session.commit()
            else:
                # 如果管理员用户存在但没有unique_id，则生成一个
                if not admin_user.unique_id:
                    admin_user.unique_id = str(uuid.uuid4())
                    db.session.commit()
            
            session['user_id'] = admin_user.id
            session['username'] = admin_user.username
            return redirect(url_for('dashboard'))
        
        flash('账号或密码错误！')
    return render_template('login.html')

# 注册页
@app.route('/register', methods=['GET', 'POST'])
def register():
    from flask import request, redirect, url_for, session, flash, render_template
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        email = request.form.get('email', '')
        
        # 验证输入
        if not username or not password or not email:
            flash('请填写所有必填字段！', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('两次输入的密码不一致！', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('密码长度至少为6位！', 'error')
            return render_template('register.html')
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            flash('用户名已存在，请选择其他用户名！', 'error')
            return render_template('register.html')
        
        # 检查邮箱是否已存在
        if User.query.filter_by(email=email).first():
            flash('邮箱已被注册，请使用其他邮箱！', 'error')
            return render_template('register.html')
        
        # 创建新用户
        new_user = User(
            username=username,
            password=hash_password(password),
            email=email,
            unique_id=str(uuid.uuid4())
        )
        db.session.add(new_user)
        db.session.commit()
        
        # 自动登录
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        
        flash('注册成功！欢迎加入简历管理系统。', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

# 用户仪表板
@app.route('/dashboard')
@login_required
def dashboard():
    from flask import session, render_template
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    # 获取用户的所有简历
    resumes = Resume.query.filter_by(user_id=user_id).all()
    
    return render_template('dashboard.html', user=user, resumes=resumes)

# 简历展示页（所有人可访问，高颜值布局）
@app.route('/')
def index():
    from flask import session, render_template
    # 如果用户已登录，显示用户的简历
    if 'user_id' in session:
        user_id = session.get('user_id')
        resume = Resume.query.filter_by(user_id=user_id).first()
        if not resume:
            resume = Resume(
                user_id=user_id,
                name='你的名字', job='求职意向',
                intro='', phone='', email='',
                education='暂无教育经历', experience='暂无工作/项目经历',
                skills='暂无技能信息', certificates=''  
            )
            db.session.add(resume)
            db.session.commit()
        return render_template('index.html', resume=resume, is_owner=True)
    
    # 未登录用户可以查看公开的简历
    resume = Resume.query.filter_by(is_public=True).first()
    if not resume:
        resume = Resume(
            user_id=1,  # 默认使用第一个用户
            name='你的名字', job='求职意向',
            intro='', phone='', email='',
            education='暂无教育经历', experience='暂无工作/项目经历',
            skills='暂无技能信息', certificates=''  
        )
        db.session.add(resume)
        db.session.commit()
    return render_template('index.html', resume=resume, is_owner=False)

# 个人简历展示页（根据用户唯一标识符）
@app.route('/profile/<string:unique_id>')
def profile(unique_id):
    from flask import session, render_template
    # 根据唯一标识符查找用户
    user = User.query.filter_by(unique_id=unique_id).first()
    if not user:
        return render_template('index.html', error='用户不存在'), 404
    
    # 查找用户的简历
    resume = Resume.query.filter_by(user_id=user.id).first()
    if not resume:
        resume = Resume(
            user_id=user.id,
            name='你的名字', job='求职意向',
            intro='', phone='', email='',
            education='暂无教育经历', experience='暂无工作/项目经历',
            skills='暂无技能信息', certificates=''  
        )
        db.session.add(resume)
        db.session.commit()
    
    # 判断当前用户是否为简历所有者
    is_owner = False
    if 'user_id' in session:
        is_owner = session.get('user_id') == user.id
    
    return render_template('index.html', resume=resume, is_owner=is_owner)

# 可视化编辑页（仅登录用户可访问）
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    from flask import request, redirect, url_for, session, flash, render_template
    user_id = session.get('user_id')
    resume = Resume.query.filter_by(user_id=user_id).first()
    
    if not resume:
        resume = Resume(
            user_id=user_id,
            name='你的名字', job='求职意向',
            intro='', phone='', email='',
            education='暂无教育经历', experience='暂无工作/项目经历',
            skills='暂无技能信息', certificates=''  
        )
        db.session.add(resume)
        db.session.commit()

    # 保存修改（自动记录版本）
    if request.method == 'POST':
        # 已有简历则记录版本
        if resume.id:
            history = ResumeHistory(
                resume_id=resume.id,
                operator=session.get('username', 'unknown'),
                old_name=resume.name or '', old_job=resume.job or '',
                old_intro=resume.intro or '', old_phone=resume.phone or '', old_email=resume.email or '',
                old_education=resume.education or '', old_experience=resume.experience or '',
                old_skills=resume.skills or '', old_certificates=resume.certificates or '',
                old_avatar=resume.avatar or '',
                remark=request.form.get('remark', '')
            )
            db.session.add(history)
        # 更新简历内容
        resume.name = request.form.get('name') or resume.name
        resume.job = request.form.get('job') or resume.job
        resume.intro = request.form.get('intro', '') or resume.intro
        resume.phone = request.form.get('phone', '') or resume.phone
        resume.email = request.form.get('email', '') or resume.email
        resume.education = request.form.get('education', '') or resume.education
        resume.experience = request.form.get('experience', '') or resume.experience
        resume.skills = request.form.get('skills', '') or resume.skills
        resume.certificates = request.form.get('certificates', '') or resume.certificates
        # 处理是否公开简历
        resume.is_public = request.form.get('is_public', 'off') == 'on'
        # 处理头像上传
        if 'avatar' in request.files and request.files['avatar'].filename != '':
            try:
                file = request.files['avatar']
                if allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
                    # 生成唯一文件名
                    import uuid
                    filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                    # 确保photos目录存在
                    photos_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'photos')
                    os.makedirs(photos_dir, exist_ok=True)
                    # 保存文件
                    file_path = os.path.join(photos_dir, filename)
                    file.save(file_path)
                    resume.avatar = f'/static/photos/{filename}'
            except Exception as e:
                print(f"头像上传失败: {str(e)}")
                pass  # 头像上传失败不影响其他字段保存
        # 提交保存
        db.session.commit()
        flash('简历更新成功！版本记录已保存', 'success')
        return redirect(url_for('edit'))
    # 回填解析的简历内容
    parsed_resume = session.pop('parsed_resume', None)
    if parsed_resume:
        for key, val in parsed_resume.items():
            if val and (not getattr(resume, key, None) or val):
                setattr(resume, key, val)
        db.session.commit()
        flash('简历解析成功！内容已填充，请在各选项卡中查看和编辑', 'success')
    return render_template('edit.html', resume=resume)

# 版本历史记录页
@app.route('/history')
@login_required
def history():
    from flask import session, redirect, url_for, flash, render_template
    user_id = session.get('user_id')
    resume = Resume.query.filter_by(user_id=user_id).first()
    if not resume:
        flash('暂无简历数据')
        return redirect(url_for('edit'))
    # 按修改时间倒序查询
    histories = ResumeHistory.query.filter_by(resume_id=resume.id).order_by(ResumeHistory.modify_time.desc()).all()
    return render_template('history.html', histories=histories, resume=resume)

# 退出登录
@app.route('/logout')
def logout():
    from flask import session, redirect, url_for
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

# 初始化数据库函数
def init_db():
    with app.app_context():
        # 首先创建所有表
        db.create_all()
        # 为现有用户添加unique_id字段
        from sqlalchemy.exc import SQLAlchemyError
        try:
            users = User.query.all()
            for user in users:
                if not user.unique_id:
                    user.unique_id = str(uuid.uuid4())
            db.session.commit()
        except SQLAlchemyError as e:
            print(f"[WARNING] 数据库初始化时出现错误: {str(e)}")
            db.session.rollback()
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
    app.run(debug=False, host='0.0.0.0', port=5000)