#!/bin/bash
echo "========================================"
echo "  简历管理系统启动脚本"
echo "========================================"
echo

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python环境，请先安装Python 3.7+"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "[提示] 正在创建虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[错误] 创建虚拟环境失败"
        exit 1
    fi
    echo "[成功] 虚拟环境创建完成"
fi

# 激活虚拟环境
source venv/bin/activate

# 检查依赖
echo "[提示] 检查依赖包..."
pip show Flask &> /dev/null
if [ $? -ne 0 ]; then
    echo "[提示] 正在安装依赖包..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[错误] 依赖安装失败"
        exit 1
    fi
fi

# 检查wkhtmltopdf
echo "[提示] 检查PDF导出工具..."
if ! command -v wkhtmltopdf &> /dev/null; then
    echo "[警告] 未检测到wkhtmltopdf，PDF导出功能将不可用"
    echo "[提示] 请运行: sudo apt-get install wkhtmltopdf"
fi

# 启动服务
echo
echo "[成功] 服务正在启动..."
echo "[提示] 访问地址: http://localhost:5000"
echo "[提示] 登录账号: admin"
echo "[提示] 默认密码: your_new_password (请在app.py中修改)"
echo
echo "按Ctrl+C停止服务"
echo

python app.py
