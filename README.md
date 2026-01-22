# 简历管理系统部署指南

## 功能特性
- ✅ PDF/Word简历上传解析
- ✅ 可视化富文本编辑
- ✅ 版本历史记录与回滚
- ✅ 版本差异对比
- ✅ PDF导出下载
- ✅ 响应式设计
- ✅ 权限管理(登录后才能编辑)

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 安装wkhtmltopdf(PDF导出必需)
**Windows系统:**
1. 下载安装: https://wkhtmltopdf.org/downloads.html
2. 默认安装路径: `C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`
3. 如安装在其他路径,需修改 `app.py` 第27行的路径

**Linux系统:**
```bash
sudo apt-get install wkhtmltopdf
```

**MacOS系统:**
```bash
brew install wkhtmltopdf
```

### 3. 修改管理员密码
编辑 `app.py` 第24行,将 `your_new_password` 改为你的密码:
```python
app.config['EDITS_PASSWORD'] = '你的新密码'
```

### 4. 启动服务
```bash
python app.py
```
服务将运行在: http://localhost:5000

### 5. 访问使用
- **查看简历**: http://localhost:5000/
- **管理登录**: http://localhost:5000/login (用户名: admin)
- **编辑简历**: http://localhost:5000/edit
- **版本历史**: http://localhost:5000/history

## 部署到生产环境

### 使用Gunicorn部署(Linux推荐)
```bash
# 安装gunicorn
pip install gunicorn

# 启动服务(关闭debug模式)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 使用Nginx反向代理
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/resume-system/static;
    }
}
```

### 使用Docker部署
创建 `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y wkhtmltopdf
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

构建运行:
```bash
docker build -t resume-system .
docker run -p 5000:5000 resume-system
```

## 目录结构
```
resume-system/
├── app.py              # 主应用文件
├── resume.db           # SQLite数据库(自动生成)
├── requirements.txt    # Python依赖
├── static/            # 静态资源
│   ├── photos/        # 头像上传
│   ├── documents/     # 简历文档上传
│   ├── css/           # 样式文件
│   ├── js/            # 脚本文件
│   └── fonts/         # 字体文件
└── templates/         # HTML模板
    ├── base.html
    ├── index.html     # 简历展示页
    ├── edit.html      # 编辑页面
    ├── history.html   # 版本记录页
    └── login.html     # 登录页面
```

## 注意事项
1. 首次运行会自动创建数据库和必要目录
2. 简历解析依赖文档格式,建议上传标准格式简历
3. PDF导出需要安装wkhtmltopdf
4. 生产环境请关闭debug模式(app.py第366行设置debug=False)
5. 定时清理任务每天凌晨2点自动清理90天前的版本记录

## 数据库备份
定期备份 `resume.db` 文件即可恢复简历数据。

## 故障排除
1. **PDF导出失败**: 检查wkhtmltopdf是否正确安装
2. **文件上传失败**: 检查static目录权限
3. **富文本编辑器不显示**: 检查网络连接(CDN资源)
"# resume_system" 
