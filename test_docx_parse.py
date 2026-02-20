# 测试解析DOCX文件
import os
from parse_resume_optimized import parse_resume_optimized as parse_resume

print('开始测试解析DOCX文件...')
docx_path = 'test_resume_valid.docx'
if os.path.exists(docx_path):
    print('测试文件存在:', docx_path)
    print('文件大小:', os.path.getsize(docx_path))
    result = parse_resume(docx_path)
    print('解析结果:', result)
else:
    print('测试文件不存在:', docx_path)
print('测试完成')