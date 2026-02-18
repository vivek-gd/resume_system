# 测试Flask-SQLAlchemy导入
print('开始测试Flask-SQLAlchemy导入...')

try:
    from flask import Flask
    print('✓ Flask 导入成功')
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    print('✓ Flask应用初始化成功')
    
    from flask_sqlalchemy import SQLAlchemy
    print('✓ Flask-SQLAlchemy 导入成功')
    
    db = SQLAlchemy(app)
    print('✓ SQLAlchemy初始化成功')
    
    # 定义一个简单的模型
    class Test(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50))
    
    print('✓ 数据库模型定义成功')
    
    # 初始化数据库
    with app.app_context():
        db.create_all()
        print('✓ 数据库初始化成功')
    
    print('所有测试都通过了！')
except Exception as e:
    print('✗ 测试失败:', str(e))
    import traceback
    traceback.print_exc()

print('测试完成！')