# 测试脚本 - 只导入sqlalchemy核心模块，然后立即退出

print('开始测试sqlalchemy核心模块导入...')

import sqlalchemy

print('sqlalchemy核心模块 imported successfully!')
print('sqlalchemy版本:', sqlalchemy.__version__)