# 测试脚本 - 只导入pdfkit模块、Flask类和SQLAlchemy，但是使用try-except块来捕获可能出现的异常

import pdfkit

print('pdfkit imported successfully!')

try:
    from flask import Flask
    print('Flask imported successfully!')
except Exception as e:
    print('Flask导入失败:', str(e))
    import traceback
    traceback.print_exc()

try:
    from flask_sqlalchemy import SQLAlchemy
    print('SQLAlchemy imported successfully!')
except Exception as e:
    print('SQLAlchemy导入失败:', str(e))
    import traceback
    traceback.print_exc()

print('测试完成！')