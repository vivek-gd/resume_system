# 测试app.py的导入方式
print('开始测试app.py的导入方式...')

try:
    print('尝试导入parse_resume_optimized...')
    from parse_resume_optimized import parse_resume_optimized as parse_resume
    print('✓ parse_resume函数导入成功')
    
    # 测试解析文件
    print('尝试解析测试文件...')
    result = parse_resume('test_resume_valid.docx')
    print('✓ 解析成功，结果:', result)
except Exception as e:
    print('✗ 错误:', str(e))
    import traceback
    traceback.print_exc()
print('测试完成')