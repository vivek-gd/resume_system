# 只测试docx模块的导入
print('开始测试docx模块...')
try:
    print('尝试导入docx模块...')
    from docx import Document
    print('✓ docx模块导入成功')
    print('测试完成！')
except Exception as e:
    print('✗ docx模块导入失败:', str(e))
    import traceback
    traceback.print_exc()
print('脚本执行结束。')