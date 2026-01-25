import os
import datetime
import re
import PyPDF2
from docx import Document
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL, UploadSet
import pdfkit  # 新增：PDF导出依赖

# 初始化Flask应用
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Session加密
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 文件上传配置
app.config['UPLOADED_PHOTOS_DEST'] = 'static/photos'
app.config['UPLOADED_DOCUMENTS_DEST'] = 'static/documents'
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

# 初始化扩展
db = SQLAlchemy(app)
photos = UploadSet('photos', IMAGES)
documents = UploadSet('documents')
configure_uploads(app, [photos, documents])
# 配置文档上传允许的文件类型
app.config['UPLOADS_DOCUMENTS_ALLOW'] = ('pdf', 'docx')
# 新增：初始化PDF配置
if app.config['WKHTMLTOPDF_PATH']:
    try:
        pdf_config = pdfkit.configuration(wkhtmltopdf=app.config['WKHTMLTOPDF_PATH'])
    except:
        pdf_config = None
        print('[WARNING] wkhtmltopdf configuration failed. PDF export will be disabled.')
else:
    pdf_config = None

# ---------------------- 数据库模型 ----------------------
# 简历主表
class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

# ---------------------- 简历解析函数 ----------------------
# 导入优化后的解析函数
from parse_resume_optimized import parse_resume_optimized as parse_resume

# ---------------------- 权限装饰器 ----------------------
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# ---------------------- 路由接口 ----------------------
# 登录页
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == app.config['EDITS_USERNAME'] and password == app.config['EDITS_PASSWORD']:
            session['username'] = username
            return redirect(url_for('edit'))
        flash('账号或密码错误！')
    return render_template('login.html')

# 简历展示页（所有人可访问，高颜值布局）
@app.route('/')
def index():
    resume = Resume.query.first()
    if not resume:
        resume = Resume(
            name='你的名字', job='求职意向',
            intro='', phone='', email='',
            education='暂无教育经历', experience='暂无工作/项目经历',
            skills='暂无技能信息', certificates=''
        )
        db.session.add(resume)
        db.session.commit()
    return render_template('index.html', resume=resume)

# 可视化编辑页（仅管理员可访问）
@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    resume = Resume.query.first()
    if not resume:
        resume = Resume(
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
        # 处理头像上传
        if 'avatar' in request.files and request.files['avatar'].filename != '':
            try:
                filename = photos.save(request.files['avatar'])
                resume.avatar = f'/static/photos/{filename}'
            except:
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

# 简历上传解析接口
@app.route('/upload_resume', methods=['POST'])
@login_required
def upload_resume():
    print('[DEBUG] upload_resume called')
    print('[DEBUG] request.files:', request.files)

    if 'resume_file' not in request.files:
        flash('请选择PDF/Word文件！', 'error')
        print('[DEBUG] No resume_file in request.files')
        return redirect(url_for('edit'))

    file = request.files['resume_file']
    print('[DEBUG] file:', file, 'filename:', file.filename)

    if file.filename == '':
        flash('文件名称不能为空！', 'error')
        print('[DEBUG] Empty filename')
        return redirect(url_for('edit'))

    # 检查文件类型
    if not (file.filename.endswith('.pdf') or file.filename.endswith('.docx')):
        flash('仅支持 PDF 和 Word (.docx) 格式！', 'error')
        print('[DEBUG] Invalid file type')
        return redirect(url_for('edit'))

    # 保存文件并解析
    try:
        print('[DEBUG] Attempting to save file...')

        # 保留中文文件名，只过滤特殊字符
        import uuid
        ext = os.path.splitext(file.filename)[1]  # 获取文件扩展名
        unique_filename = f"{uuid.uuid4().hex}{ext}"  # 使用UUID生成唯一文件名
        print('[DEBUG] Generated filename:', unique_filename)

        # 确保目录存在
        os.makedirs(app.config['UPLOADED_DOCUMENTS_DEST'], exist_ok=True)

        # 保存文件
        file_path = os.path.join(app.config['UPLOADED_DOCUMENTS_DEST'], unique_filename)
        print('[DEBUG] Saving to:', file_path)
        file.save(file_path)
        print('[DEBUG] File saved successfully')

        # 解析简历
        resume_data = parse_resume(file_path)
        print('[DEBUG] Parsed data:', resume_data)

        if resume_data and len(resume_data) > 0:
            session['parsed_resume'] = resume_data
            parsed_fields = ', '.join([k for k in resume_data.keys()])
            flash(f'简历解析成功！已提取：{parsed_fields}，请在各选项卡中查看。', 'success')
        else:
            flash('解析完成，但未能从文件中提取到有效信息，请检查文件格式或手动填写。', 'warning')
    except Exception as e:
        print('[DEBUG] Exception:', str(e))
        import traceback
        traceback.print_exc()
        flash(f'解析失败：{str(e)}', 'error')

    return redirect(url_for('edit'))

# 版本历史记录页
@app.route('/history')
@login_required
def history():
    resume = Resume.query.first()
    if not resume:
        flash('暂无简历数据')
        return redirect(url_for('edit'))
    # 按修改时间倒序查询
    histories = ResumeHistory.query.filter_by(resume_id=resume.id).order_by(ResumeHistory.modify_time.desc()).all()
    return render_template('history.html', histories=histories, resume=resume)

# 版本回滚接口
@app.route('/rollback/<int:history_id>')
@login_required
def rollback(history_id):
    history = ResumeHistory.query.get_or_404(history_id)
    resume = Resume.query.get_or_404(history.resume_id)
    # 先记录当前版本（避免回滚后丢失原内容）
    current_history = ResumeHistory(
        resume_id=resume.id,
        old_name=resume.name, old_job=resume.job,
        old_intro=resume.intro or '', old_phone=resume.phone or '', old_email=resume.email or '',
        old_education=resume.education, old_experience=resume.experience,
        old_skills=resume.skills, old_certificates=resume.certificates or '',
        old_avatar=resume.avatar,
        remark=f'回滚至{history.modify_time.strftime("%Y-%m-%d %H:%M")}版本'
    )
    db.session.add(current_history)
    # 回滚数据
    resume.name = history.old_name
    resume.job = history.old_job
    resume.intro = history.old_intro or ''
    resume.phone = history.old_phone or ''
    resume.email = history.old_email or ''
    resume.education = history.old_education
    resume.experience = history.old_experience
    resume.skills = history.old_skills
    resume.certificates = history.old_certificates or ''
    resume.avatar = history.old_avatar
    db.session.commit()
    flash(f'已回滚到 {history.modify_time.strftime("%Y-%m-%d %H:%M:%S")} 的版本')
    return redirect(url_for('edit'))

# 版本差异对比接口（返回JSON数据）
@app.route('/diff/<int:history_id>')
@login_required
def diff(history_id):
    history = ResumeHistory.query.get_or_404(history_id)
    resume = Resume.query.get_or_404(history.resume_id)
    # 对比核心字段差异
    diff_data = {
        'name': {'old': history.old_name or '', 'new': resume.name or ''},
        'job': {'old': history.old_job or '', 'new': resume.job or ''},
        'education': {'old': history.old_education or '', 'new': resume.education or ''},
        'experience': {'old': history.old_experience or '', 'new': resume.experience or ''},
        'skills': {'old': history.old_skills or '', 'new': resume.skills or ''}
    }
    return jsonify(diff_data)

# 新增：导出当前版本简历PDF（所有人可访问，展示页调用）
@app.route('/export_current_pdf')
def export_current_pdf():
    # 检查PDF导出配置
    if not pdf_config:
        flash('PDF导出功能未配置或配置失败，请检查wkhtmltopdf是否正确安装', 'error')
        return redirect(url_for('index'))

    resume = Resume.query.first()
    if not resume:
        flash('暂无简历数据可导出')
        return redirect(url_for('index'))
    # 构造当前版本简历数据
    resume_data = {
        'name': resume.name,
        'job': resume.job,
        'phone': resume.phone,
        'email': resume.email,
        'intro': resume.intro,
        'education': resume.education,
        'experience': resume.experience,
        'skills': resume.skills,
        'certificates': resume.certificates,
        'avatar': resume.avatar,
        'update_time': resume.update_time
    }
    # 渲染模板为HTML（使用展示页模板，保留排版）
    html = render_template('index.html', resume=resume_data)

    # 获取应用的基础URL，用于图片加载
    from flask import request
    base_url = request.url_root

    # 将相对路径转换为绝对路径
    html = html.replace('src="/static/', f'src="{base_url}static/')
    html = html.replace('href="/static/', f'href="{base_url}static/')

    # 替换CSS变量为实际颜色值，提高PDF兼容性
    html = html.replace('var(--primary-color)', '#667eea')
    html = html.replace('var(--secondary-color)', '#764ba2')

    # 隐藏导出按钮
    html = html.replace('<a href="' + url_for('export_current_pdf') + '" class="btn export-btn">', '<a href="#" class="btn export-btn" style="display:none;">')

    # 添加PDF专用样式，优化排版和布局
    pdf_style = """
    <style>
        @page { margin: 0; size: A4; }
        html, body { 
            -webkit-print-color-adjust: exact; 
            print-color-adjust: exact; 
            background: #f5f5f5 !important; 
            margin: 0;
            padding: 0;
            height: 100%;
            min-height: 297mm;
        }
        body { padding: 15px 15px; }
        .resume-container { 
            background: white !important; 
            margin: 0 auto !important; 
            max-width: 210mm !important;
            min-height: 267mm !important;
            box-shadow: none !important;
            padding: 0 !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            display: flex !important;
            flex-direction: column !important;
        }
        .resume-header { 
            background: #667eea !important; 
            padding: 2.5rem 2rem !important; 
            color: white !important;
        }
        .avatar { 
            width: 120px !important; 
            height: 120px !important;
            border: 4px solid rgba(255,255,255,0.9) !important;
            border-radius: 50% !important;
        }
        .resume-name { font-size: 2rem !important; margin-bottom: 0.3rem !important; }
        .resume-job { font-size: 1.2rem !important; margin-bottom: 1rem !important; }
        .contact-info { 
            display: flex !important; 
            justify-content: center !important; 
            gap: 1.5rem !important; 
            flex-wrap: wrap !important; 
            margin-top: 1rem !important;
        }
        .contact-item { color: white !important; }
        .resume-body { padding: 2rem !important; }
        .section-title { 
            font-size: 1.3rem !important; 
            margin-bottom: 1rem !important; 
            padding-bottom: 0.5rem !important; 
        }
        .section-icon { 
            width: 35px !important; 
            height: 35px !important; 
            background: #667eea !important; 
            border-radius: 8px !important;
        }
        .skill-tag { 
            background: #f0f2ff !important; 
            padding: 0.4rem 1rem !important; 
            margin: 0.3rem 0.2rem !important; 
            font-size: 0.9rem !important;
            border-radius: 20px !important;
        }
        .intro-box { 
            background: #f8f9ff !important; 
            padding: 1rem !important; 
            margin-bottom: 1.5rem !important; 
            border-radius: 8px !important;
        }
        .education-item, .experience-item { margin-bottom: 1.2rem !important; }
        .update-time { margin-top: 0.3rem !important; padding-top: 0.3rem !important; }
        .resume-body { padding-bottom: 1rem !important; }
        .export-btn { display: none !important; }
    </style>
    """
    html = html.replace('</head>', pdf_style + '</head>')

    # 转换为PDF（优化中文显示和排版）
    pdf_options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'no-outline': None,
        'disable-smart-shrinking': None,
        'enable-local-file-access': None,
        'no-stop-slow-scripts': None,
        'debug-javascript': None,
        'load-error-handling': 'ignore',
        'load-media-error-handling': 'ignore',
        'images': None,
        'enable-external-links': None,
        'print-media-type': None,
        'background': None,  # 启用背景渲染
        'dpi': 96,
        'image-dpi': 96
    }
    try:
        print(f'[DEBUG] 开始生成PDF...')
        pdf = pdfkit.from_string(html, False, configuration=pdf_config, options=pdf_options)
        print(f'[DEBUG] PDF生成成功')
        # 响应下载
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        # 使用URL编码处理中文文件名
        from urllib.parse import quote
        filename = f"{resume.name}_当前版本_{resume.update_time.strftime('%Y%m%d%H%M%S')}.pdf"
        response.headers['Content-Disposition'] = f"attachment; filename*=UTF-8''{quote(filename)}"
        return response
    except Exception as e:
        print(f'[ERROR] PDF导出失败：{str(e)}')
        import traceback
        traceback.print_exc()
        flash(f'PDF导出失败：{str(e)}', 'error')
        return redirect(url_for('index'))

# 新增：导出指定历史版本简历PDF（仅管理员可访问，版本页调用）
@app.route('/export_version/<int:history_id>')
@login_required
def export_version(history_id):
    # 检查PDF导出配置
    if not pdf_config:
        flash('PDF导出功能未配置或配置失败，请检查wkhtmltopdf是否正确安装', 'error')
        return redirect(url_for('history'))

    history = ResumeHistory.query.get_or_404(history_id)
    resume = Resume.query.get_or_404(history.resume_id)
    # 构造历史版本简历数据
    resume_data = {
        'name': history.old_name,
        'job': history.old_job,
        'phone': history.old_phone,
        'email': history.old_email,
        'intro': history.old_intro,
        'education': history.old_education,
        'experience': history.old_experience,
        'skills': history.old_skills,
        'certificates': history.old_certificates,
        'avatar': history.old_avatar,
        'update_time': history.modify_time
    }
    # 渲染模板为HTML
    html = render_template('index.html', resume=resume_data)

    # 获取应用的基础URL，用于图片加载
    from flask import request
    base_url = request.url_root

    # 将相对路径转换为绝对路径
    html = html.replace('src="/static/', f'src="{base_url}static/')
    html = html.replace('href="/static/', f'href="{base_url}static/')

    # 替换CSS变量为实际颜色值，提高PDF兼容性
    html = html.replace('var(--primary-color)', '#667eea')
    html = html.replace('var(--secondary-color)', '#764ba2')

    # 隐藏导出按钮
    html = html.replace('<a href="' + url_for('export_current_pdf') + '" class="btn export-btn">', '<a href="#" class="btn export-btn" style="display:none;">')

    # 添加PDF专用样式，优化排版和布局
    pdf_style = """
    <style>
        @page { margin: 0; size: A4; }
        html, body { 
            -webkit-print-color-adjust: exact; 
            print-color-adjust: exact; 
            background: #f5f5f5 !important; 
            margin: 0;
            padding: 0;
            height: 100%;
            min-height: 297mm;
        }
        body { padding: 15px 15px; }
        .resume-container { 
            background: white !important; 
            margin: 0 auto !important; 
            max-width: 210mm !important;
            min-height: 267mm !important;
            box-shadow: none !important;
            padding: 0 !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            display: flex !important;
            flex-direction: column !important;
        }
        .resume-header { 
            background: #667eea !important; 
            padding: 2.5rem 2rem !important; 
            color: white !important;
        }
        .avatar { 
            width: 120px !important; 
            height: 120px !important;
            border: 4px solid rgba(255,255,255,0.9) !important;
            border-radius: 50% !important;
        }
        .resume-name { font-size: 2rem !important; margin-bottom: 0.3rem !important; }
        .resume-job { font-size: 1.2rem !important; margin-bottom: 1rem !important; }
        .contact-info { 
            display: flex !important; 
            justify-content: center !important; 
            gap: 1.5rem !important; 
            flex-wrap: wrap !important; 
            margin-top: 1rem !important;
        }
        .contact-item { color: white !important; }
        .resume-body { padding: 2rem !important; }
        .section-title { 
            font-size: 1.3rem !important; 
            margin-bottom: 1rem !important; 
            padding-bottom: 0.5rem !important; 
        }
        .section-icon { 
            width: 35px !important; 
            height: 35px !important; 
            background: #667eea !important; 
            border-radius: 8px !important;
        }
        .skill-tag { 
            background: #f0f2ff !important; 
            padding: 0.4rem 1rem !important; 
            margin: 0.3rem 0.2rem !important; 
            font-size: 0.9rem !important;
            border-radius: 20px !important;
        }
        .intro-box { 
            background: #f8f9ff !important; 
            padding: 1rem !important; 
            margin-bottom: 1.5rem !important; 
            border-radius: 8px !important;
        }
        .education-item, .experience-item { margin-bottom: 1.2rem !important; }
        .update-time { margin-top: 0.3rem !important; padding-top: 0.3rem !important; }
        .resume-body { padding-bottom: 1rem !important; }
        .export-btn { display: none !important; }
    </style>
    """
    html = html.replace('</head>', pdf_style + '</head>')

    # 转换为PDF（优化中文显示和排版）
    pdf_options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'no-outline': None,
        'disable-smart-shrinking': None,
        'enable-local-file-access': None,
        'no-stop-slow-scripts': None,
        'debug-javascript': None,
        'load-error-handling': 'ignore',
        'load-media-error-handling': 'ignore',
        'images': None,
        'enable-external-links': None,
        'print-media-type': None,
        'background': None,  # 启用背景渲染
        'dpi': 96,
        'image-dpi': 96
    }
    try:
        pdf = pdfkit.from_string(html, False, configuration=pdf_config, options=pdf_options)
        # 响应下载
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        # 使用URL编码处理中文文件名
        from urllib.parse import quote
        filename = f"{history.old_name}_{history.modify_time.strftime('%Y%m%d%H%M%S')}_历史版本.pdf"
        response.headers['Content-Disposition'] = f"attachment; filename*=UTF-8''{quote(filename)}"
        return response
    except Exception as e:
        flash(f'PDF导出失败：{str(e)}', 'error')
        return redirect(url_for('history'))

# 退出登录
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# 初始化数据库（首次运行）
with app.app_context():
    db.create_all()
    # 创建默认文件夹
    os.makedirs('static/photos', exist_ok=True)
    os.makedirs('static/documents', exist_ok=True)

# 新增：定时清理旧版本记录（集成到启动逻辑）
import schedule
import time
import threading
def clean_old_histories():
    with app.app_context():
        # 删除3个月前的记录
        threshold = datetime.datetime.now() - datetime.timedelta(days=90)
        old_histories = ResumeHistory.query.filter(ResumeHistory.modify_time < threshold).all()
        for h in old_histories:
            db.session.delete(h)
        db.session.commit()
        print(f"清理完成，共删除{len(old_histories)}条旧记录")

# 每天凌晨2点执行清理
schedule.every().day.at("02:00").do(clean_old_histories)

# 启动定时任务（独立线程，避免阻塞服务）
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    # 启动定时任务线程
    threading.Thread(target=run_schedule, daemon=True).start()
    app.run(debug=False, host='0.0.0.0', port=5000)
    app.run(debug=False, host='0.0.0.0')  # 部署时关闭debug