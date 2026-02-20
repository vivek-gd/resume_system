# 测试简历解析功能
print('开始测试简历解析功能...')

try:
    print('尝试导入parse_resume...')
    from parse_resume_optimized import parse_resume_optimized as parse_resume
    print('✓ parse_resume 导入成功')
    
    print('测试完成')
except Exception as e:
    print('✗ 错误:', str(e))
    import traceback
    traceback.print_exc()