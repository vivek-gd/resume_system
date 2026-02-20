# 使用importlib测试SQLAlchemy导入
print('开始使用importlib测试SQLAlchemy导入...')

import importlib
import sys

try:
    print('尝试导入Flask...')
    flask_module = importlib.import_module('flask')
    print('✓ Flask 导入成功')
    Flask = flask_module.Flask
    app = Flask(__name__)
    print('✓ Flask应用创建成功')
    
    print('尝试导入sqlalchemy...')
    sqlalchemy_module = importlib.import_module('sqlalchemy')
    print('✓ sqlalchemy 导入成功')
    
    print('尝试导入flask_sqlalchemy...')
    flask_sqlalchemy_module = importlib.import_module('flask_sqlalchemy')
    print('✓ flask_sqlalchemy 导入成功')
    SQLAlchemy = flask_sqlalchemy_module.SQLAlchemy
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy(app)
    print('✓ SQLAlchemy初始化成功')
    
    print('测试完成')
except Exception as e:
    print('✗ 错误:', str(e))
    import traceback
    traceback.print_exc()
    print('Python路径:', sys.path)