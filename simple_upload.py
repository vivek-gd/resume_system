# 简化版简历上传和解析功能

import os
import uuid
from flask import Flask, request, redirect, url_for, session, flash, render_template

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'static'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 允许的文件类型
ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

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
    return render_template('simple_upload.html')

# 简历上传解析接口
@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    print('[DEBUG] upload_resume called')
    print('[DEBUG] request.files:', request.files)

    if 'resume_file' not in request.files:
        flash('请选择PDF/Word文件！', 'error')
        print('[DEBUG] No resume_file in request.files')
        return redirect(url_for('index'))

    file = request.files['resume_file']
    print('[DEBUG] file:', file, 'filename:', file.filename)

    if file.filename == '':
        flash('文件名称不能为空！', 'error')
        print('[DEBUG] Empty filename')
        return redirect(url_for('index'))

    # 检查文件类型
    if not (file.filename.endswith('.pdf') or file.filename.endswith('.docx')):
        flash('仅支持 PDF 和 Word (.docx) 格式！', 'error')
        print('[DEBUG] Invalid file type')
        return redirect(url_for('index'))

    # 保存文件并解析
    try:
        print('[DEBUG] Attempting to save file...')

        # 保留中文文件名，只过滤特殊字符
        ext = os.path.splitext(file.filename)[1]  # 获取文件扩展名
        unique_filename = f"{uuid.uuid4().hex}{ext}"  # 使用UUID生成唯一文件名
        print('[DEBUG] Generated filename:', unique_filename)

        # 确保目录存在
        documents_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'documents')
        os.makedirs(documents_dir, exist_ok=True)

        # 保存文件
        file_path = os.path.join(documents_dir, unique_filename)
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

    return redirect(url_for('index'))

if __name__ == '__main__':
    print('启动应用程序...')
    print('访问地址: http://localhost:5000')
    app.run(debug=True, host='0.0.0.0', port=5000)