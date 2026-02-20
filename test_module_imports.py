# 逐个测试parse_resume_optimized.py中导入的模块
print('开始测试模块导入...')

# 测试re模块
print('\n测试re模块...')
try:
    import re
    print('✓ re模块导入成功')
except Exception as e:
    print('✗ re模块导入失败:', str(e))

# 测试os模块
print('\n测试os模块...')
try:
    import os
    print('✓ os模块导入成功')
except Exception as e:
    print('✗ os模块导入失败:', str(e))

# 测试PyPDF2模块
print('\n测试PyPDF2模块...')
try:
    import PyPDF2
    print('✓ PyPDF2模块导入成功')
    print('PyPDF2版本:', PyPDF2.__version__)
except Exception as e:
    print('✗ PyPDF2模块导入失败:', str(e))

# 测试docx模块
print('\n测试docx模块...')
try:
    from docx import Document
    print('✓ docx模块导入成功')
except Exception as e:
    print('✗ docx模块导入失败:', str(e))

print('\n测试完成！')