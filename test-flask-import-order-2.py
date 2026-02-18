# 测试脚本 - 先导入一些其他的模块，然后使用try-except块来捕获导入Flask时可能出现的异常

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

print('测试完成！')