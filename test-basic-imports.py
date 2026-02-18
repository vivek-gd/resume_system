# 测试脚本 - 只导入基本模块

print('开始测试基本模块导入...')

# 逐个测试导入
test_modules = [
    'os',
    'datetime',
    're',
    'PyPDF2',
    'uuid',
    'docx',
    'flask',
    'flask_sqlalchemy',
    'pdfkit'
]

for module in test_modules:
    print(f'\n测试导入 {module}...')
    try:
        if module == 'docx':
            from docx import Document
        elif module == 'flask':
            from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, make_response
        elif module == 'flask_sqlalchemy':
            from flask_sqlalchemy import SQLAlchemy
        else:
            __import__(module)
        print(f'✓ {module} 导入成功')
    except Exception as e:
        print(f'✗ {module} 导入失败:', str(e))
        import traceback
        traceback.print_exc()
        exit(1)

print('\n所有基本模块导入成功！')
print('测试完成。')