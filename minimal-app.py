# 最小化版本的简历系统应用
import os
import datetime
import uuid
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

print('开始初始化最小化应用...')

# 初始化Flask应用
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化SQLAlchemy
db = SQLAlchemy(app)
print('✓ SQLAlchemy初始化成功')

# 数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    resumes = db.relationship('Resume', backref='user', lazy=True)
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

# 初始化数据库
def init_db():
    with app.app_context():
        db.create_all()
        # 为现有用户添加unique_id
        users = User.query.all()
        for user in users:
            if not user.unique_id:
                user.unique_id = str(uuid.uuid4())
        db.session.commit()
        print('✓ 数据库初始化成功')

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
    print(f'[DEBUG] 访问根路径，session: {session}')
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
        print(f'[DEBUG] 已登录用户 {user_id}，显示简历 {resume.id}')
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
    print(f'[DEBUG] 未登录用户，显示公开简历 {resume.id}')
    return render_template('index.html', resume=resume, is_owner=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # 尝试查找用户
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            print(f'[DEBUG] 用户 {username} 登录成功')
            return redirect(url_for('index'))
        
        flash('账号或密码错误！')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
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
            password=generate_password_hash(password),
            email=email,
            unique_id=str(uuid.uuid4())
        )
        db.session.add(new_user)
        db.session.commit()
        
        # 自动登录
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        
        flash('注册成功！欢迎加入简历管理系统。', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
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

    if request.method == 'POST':
        # 保存修改
        resume.name = request.form.get('name') or resume.name
        resume.job = request.form.get('job') or resume.job
        resume.intro = request.form.get('intro', '') or resume.intro
        resume.phone = request.form.get('phone', '') or resume.phone
        resume.email = request.form.get('email', '') or resume.email
        resume.education = request.form.get('education', '') or resume.education
        resume.experience = request.form.get('experience', '') or resume.experience
        resume.skills = request.form.get('skills', '') or resume.skills
        resume.certificates = request.form.get('certificates', '') or resume.certificates
        resume.is_public = request.form.get('is_public', 'off') == 'on'
        
        db.session.commit()
        flash('简历更新成功！', 'success')
        return redirect(url_for('edit'))
    
    return render_template('edit.html', resume=resume)

@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    resumes = Resume.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', user=user, resumes=resumes)

@app.route('/profile/<string:unique_id>')
def profile(unique_id):
    print(f'[DEBUG] 访问个人简历 {unique_id}')
    # 根据唯一标识符查找用户
    user = User.query.filter_by(unique_id=unique_id).first()
    if not user:
        print(f'[DEBUG] 用户 {unique_id} 不存在')
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
    
    print(f'[DEBUG] 显示用户 {user.username} 的简历，is_owner: {is_owner}')
    return render_template('index.html', resume=resume, is_owner=is_owner)

# 主函数
if __name__ == '__main__':
    print('初始化数据库...')
    init_db()
    print('启动应用程序...')
    print('访问地址: http://localhost:5000')
    # 绑定到所有地址，确保localhost和127.0.0.1都能访问
    app.run(debug=True, host='0.0.0.0', port=5000)