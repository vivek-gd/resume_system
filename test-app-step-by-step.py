# 测试脚本 - 复制app.py文件的内容，但是只保留最基本的部分，然后逐步添加其他部分

import pdfkit

print('1. pdfkit imported successfully!')

try:
    from flask import Flask
    print('2. Flask imported successfully!')
except Exception as e:
    print('2. Flask导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

print('3. Creating Flask app...')
app = Flask(__name__)
app.secret_key = 'test-secret-key'
print('4. Flask app created successfully!')

print('5. Importing SQLAlchemy...')
try:
    from flask_sqlalchemy import SQLAlchemy
    print('6. SQLAlchemy imported successfully!')
except Exception as e:
    print('6. SQLAlchemy导入失败:', str(e))
    import traceback
    traceback.print_exc()
    exit(1)

print('7. Initializing SQLAlchemy...')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
print('8. SQLAlchemy initialized successfully!')

print('9. Defining database models...')
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    resumes = db.relationship('Resume', backref='user', lazy=True)
    unique_id = db.Column(db.String(36), unique=True, nullable=True)

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    job = db.Column(db.String(50))

print('10. Database models defined successfully!')

print('11. Creating database tables...')
with app.app_context():
    db.create_all()
print('12. Database tables created successfully!')

@app.route('/')
def index():
    return 'Hello, World!'

print('13. Route defined successfully!')

print('14. Starting Flask app...')
print('访问地址: http://localhost:5000')
app.run(debug=False, host='0.0.0.0', port=5000)