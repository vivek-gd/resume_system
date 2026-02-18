# 测试脚本 - 导入所有的模块，然后创建一个Flask应用，然后打印一条消息，然后立即退出

print('开始测试...')

# 先导入一些其他的模块
import os
import datetime
import re
import PyPDF2
import uuid
from docx import Document
import pdfkit

print('其他模块导入成功！')

# 然后导入Flask类
try:
    from flask import Flask
    print('Flask imported successfully!')
except Exception as e:
    print('Flask导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 创建Flask应用
try:
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print('Flask app created successfully!')
except Exception as e:
    print('Flask app creation failed:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 导入SQLAlchemy
try:
    from flask_sqlalchemy import SQLAlchemy
    print('SQLAlchemy imported successfully!')
except Exception as e:
    print('SQLAlchemy import failed:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

# 初始化SQLAlchemy
try:
    db = SQLAlchemy(app)
    print('SQLAlchemy initialized successfully!')
except Exception as e:
    print('SQLAlchemy initialization failed:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

print('测试完成！')