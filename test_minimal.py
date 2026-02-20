# 最小化测试文件
print('开始最小化测试...')

# 只导入必要的模块
try:
    print('尝试导入Flask...')
    from flask import Flask
    print('✓ Flask 导入成功')
    
    app = Flask(__name__)
    print('✓ Flask应用创建成功')
    
    print('尝试导入SQLAlchemy...')
    from flask_sqlalchemy import SQLAlchemy
    print('✓ SQLAlchemy 导入成功')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resume.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy(app)
    print('✓ SQLAlchemy初始化成功')
    
    print('测试完成')
except Exception as e:
    print('✗ 错误:', str(e))
    import traceback
    traceback.print_exc()