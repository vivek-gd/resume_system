# 简历系统部署方案

## 方案一: 本地快速部署

### Windows系统
双击运行 `start.bat`，自动完成以下操作:
1. 创建Python虚拟环境
2. 安装依赖包
3. 检查wkhtmltopdf
4. 启动服务

### Linux/Mac系统
```bash
chmod +x start.sh
./start.sh
```

---

## 方案二: 云服务器部署(推荐)

### 1. 购买服务器
推荐云服务商:
- 阿里云/腾讯云(2核4G)
- 华为云/百度云

### 2. 环境安装
```bash
# Ubuntu/Debian系统
sudo apt-get update
sudo apt-get install python3 python3-pip python3-venv nginx
sudo apt-get install wkhtmltopdf

# CentOS/RHEL系统
sudo yum install python3 python3-pip nginx
sudo yum install wkhtmltopdf
```

### 3. 上传代码
```bash
# 在本地打包项目
tar -czf resume-system.tar.gz resume-system/

# 上传到服务器
scp resume-system.tar.gz root@your-server-ip:/root/

# 在服务器解压
ssh root@your-server-ip
cd /root/
tar -xzf resume-system.tar.gz
cd resume-system
```

### 4. 配置环境
```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
pip install gunicorn  # 生产环境Web服务器
```

### 5. 修改密码
```bash
nano app.py
# 修改第24行: app.config['EDITS_PASSWORD'] = '你的强密码'
```

### 6. 测试运行
```bash
python app.py
# 访问 http://your-server-ip:5000 测试
```

### 7. 使用Gunicorn生产部署
```bash
# 使用4个工作进程启动
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 或者使用nohup后台运行
nohup gunicorn -w 4 -b 0.0.0.0:5000 app:app > app.log 2>&1 &
```

### 8. 配置Nginx反向代理
```bash
sudo nano /etc/nginx/sites-available/resume
```

添加以下配置:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # 改成你的域名或IP

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /root/resume-system/static;
        expires 30d;
    }
}
```

启用配置:
```bash
sudo ln -s /etc/nginx/sites-available/resume /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. 配置SSL证书(HTTPS)
```bash
# 安装certbot
sudo apt-get install certbot python3-certbot-nginx

# 自动获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

---

## 方案三: Docker容器部署

### 1. 创建Dockerfile
```dockerfile
FROM python:3.9-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### 2. 构建镜像
```bash
docker build -t resume-system:latest .
```

### 3. 运行容器
```bash
docker run -d \
  --name resume-system \
  -p 5000:5000 \
  -v $(pwd)/resume.db:/app/resume.db \
  -v $(pwd)/static:/app/static \
  --restart unless-stopped \
  resume-system:latest
```

### 4. 使用Docker Compose(推荐)
创建 `docker-compose.yml`:
```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: resume-system
    ports:
      - "5000:5000"
    volumes:
      - ./resume.db:/app/resume.db
      - ./static:/app/static
    restart: unless-stopped
    environment:
      - FLASK_ENV=production

  nginx:
    image: nginx:alpine
    container_name: resume-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./static:/usr/share/nginx/html/static
    depends_on:
      - app
    restart: unless-stopped
```

启动:
```bash
docker-compose up -d
```

---

## 方案四: 云托管平台部署

### 1. 使用Render.com
1. Fork代码到GitHub
2. 登录render.com创建新Web Service
3. 连接GitHub仓库
4. 设置构建命令: `pip install -r requirements.txt`
5. 设置启动命令: `gunicorn app:app`
6. 自动部署完成

### 2. 使用Railway.app
1. 安装Railway CLI: `npm install -g @railway/cli`
2. 登录: `railway login`
3. 部署: `railway up`
4. 自动获得公网URL

### 3. 使用Heroku
```bash
# 安装Heroku CLI
# 创建Procfile
echo "web: gunicorn app:app" > Procfile

# 创建runtime.txt
echo "python-3.9.16" > runtime.txt

# 部署
heroku create
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

---

## 安全建议

1. **修改默认密码**
   - 编辑 `app.py` 第24行
   - 使用强密码(16位以上,含大小写字母+数字+符号)

2. **限制登录尝试**
   - 可添加验证码功能
   - 实现登录失败锁定

3. **启用HTTPS**
   - 使用Let's Encrypt免费SSL证书
   - 强制HTTPS访问

4. **定期备份数据**
   - 每日备份 `resume.db`
   - 备份 `static` 目录

5. **防火墙配置**
   - 只开放80、443端口
   - 禁止直接访问5000端口

---

## 监控与维护

### 查看日志
```bash
# Gunicorn日志
tail -f app.log

# Nginx日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### 性能优化
```bash
# 增加Gunicorn工作进程数
gunicorn -w 8 -b 0.0.0.0:5000 app:app

# 使用gthread模式(适合多线程)
gunicorn -w 4 --threads 2 -b 0.0.0.0:5000 app:app
```

### 自动重启服务
```bash
# 使用systemd管理服务
sudo nano /etc/systemd/system/resume.service
```

添加内容:
```ini
[Unit]
Description=Resume System
After=network.target

[Service]
User=root
WorkingDirectory=/root/resume-system
Environment="PATH=/root/resume-system/venv/bin"
ExecStart=/root/resume-system/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

启用服务:
```bash
sudo systemctl daemon-reload
sudo systemctl enable resume
sudo systemctl start resume
sudo systemctl status resume
```

---

## 故障排除

### 服务无法启动
- 检查端口占用: `netstat -tunlp | grep 5000`
- 检查日志: `tail -f app.log`

### PDF导出失败
- 确认wkhtmltopdf安装: `wkhtmltopdf --version`
- 检查路径配置: `app.py` 第27行

### 上传失败
- 检查目录权限: `chmod 755 static/photos static/documents`
- 检查磁盘空间: `df -h`

---

## 域名绑定

1. 购买域名(阿里云、腾讯云等)
2. DNS解析指向服务器IP
3. 修改Nginx配置中的 `server_name`
4. 重启Nginx: `sudo systemctl restart nginx`

完成! 现在可以通过域名访问你的简历网站了。
