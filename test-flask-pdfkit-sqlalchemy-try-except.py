# 测试脚本 - 先导入pdfkit模块，然后再导入Flask类，然后尝试导入SQLAlchemy，但是使用try-except块来捕获可能出现的异常

import pdfkit

from flask import Flask

print('Flask imported successfully!')

try:
    from flask_sqlalchemy import SQLAlchemy
    print('SQLAlchemy imported successfully!')
except Exception as e:
    print('SQLAlchemy导入失败:', str(e))
    import traceback
    traceback.print_exc()

print('测试完成！')