# 测试脚本 - 检查app.py是否有语法错误

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, '.')

try:
    print('正在导入app模块...')
    import app
    print('App模块导入成功！')
    print('应用程序名称:', app.app.name)
    print('数据库URI:', app.app.config.get('SQLALCHEMY_DATABASE_URI'))
    print('测试完成，app.py文件没有语法错误。')
except Exception as e:
    print('错误:', str(e))
    import traceback
    traceback.print_exc()
    print('测试失败，app.py文件有错误。')