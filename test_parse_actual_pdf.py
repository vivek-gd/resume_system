# 测试解析实际的PDF简历文件
import os
from parse_resume_optimized import parse_resume_optimized as parse_resume

print('开始测试解析实际的PDF简历文件...')

# 测试解析PDF文件
pdf_path = 'static/documents/16c808a8d8a7471e84ccb837bdae4282.pdf'
if os.path.exists(pdf_path):
    print('测试文件存在:', pdf_path)
    print('文件大小:', os.path.getsize(pdf_path))
    try:
        result = parse_resume(pdf_path)
        print('解析结果:', result)
        print('解析成功！')
    except Exception as e:
        print('解析失败:', str(e))
        import traceback
        traceback.print_exc()
else:
    print('测试文件不存在:', pdf_path)

print('\n测试完成！')