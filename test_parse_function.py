# 测试parse_resume_optimized函数
import os
print('开始测试parse_resume_optimized函数...')

try:
    print('尝试导入parse_resume_optimized...')
    from parse_resume_optimized import parse_resume_optimized as parse_resume
    print('✓ parse_resume_optimized导入成功')
    
    # 测试解析PDF文件
    print('\n测试解析PDF文件...')
    pdf_path = 'test_resume.pdf'
    if os.path.exists(pdf_path):
        pdf_result = parse_resume(pdf_path)
        print('PDF解析结果:', pdf_result)
    else:
        print('测试PDF文件不存在，跳过PDF测试')
    
    # 测试解析DOCX文件
    print('\n测试解析DOCX文件...')
    docx_path = 'test_resume.docx'
    if os.path.exists(docx_path):
        docx_result = parse_resume(docx_path)
        print('DOCX解析结果:', docx_result)
    else:
        print('测试DOCX文件不存在，跳过DOCX测试')
    
    print('\n测试完成')
except Exception as e:
    print('✗ 错误:', str(e))
    import traceback
    traceback.print_exc()