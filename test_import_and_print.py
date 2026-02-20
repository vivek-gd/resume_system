# 测试导入parse_resume_optimized函数并打印消息
print('开始测试...')
try:
    print('尝试导入parse_resume_optimized...')
    from parse_resume_optimized import parse_resume_optimized
    print('✓ 导入成功！')
    print('测试完成，没有错误。')
except Exception as e:
    print('✗ 导入失败:', str(e))
    import traceback
    traceback.print_exc()
print('脚本执行结束。')