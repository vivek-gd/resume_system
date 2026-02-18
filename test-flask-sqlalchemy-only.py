# 测试脚本 - 只导入pdfkit模块、Flask类和SQLAlchemy，然后打印一条消息，然后立即退出

import pdfkit

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

print('Flask and SQLAlchemy imported successfully!')