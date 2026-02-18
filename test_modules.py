# 测试必要的模块是否存在
print('开始测试必要的模块...')

modules = [
    'flask',
    'flask_sqlalchemy',
    'PyPDF2',
    'docx',
    'pdfkit',
    'werkzeug.security'
]

for module in modules:
    try:
        __import__(module)
        print(f'✓ {module} 模块导入成功')
    except Exception as e:
        print(f'✗ {module} 模块导入失败:', str(e))

print('模块测试完成！')