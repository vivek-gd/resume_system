# 测试打开和读取PDF文件
import PyPDF2

print('开始测试打开和读取PDF文件...')

pdf_path = 'static/documents/16c808a8d8a7471e84ccb837bdae4282.pdf'
try:
    with open(pdf_path, 'rb') as f:
        print('✓ 成功打开PDF文件')
        reader = PyPDF2.PdfReader(f)
        print('✓ 成功创建PdfReader对象')
        print('PDF页数:', len(reader.pages))
        page = reader.pages[0]
        print('✓ 成功获取第一页')
        text = page.extract_text()
        print('✓ 成功提取文本')
        print('提取的文本长度:', len(text))
        print('提取的文本:', text[:500])  # 只打印前500个字符
except Exception as e:
    print('✗ 错误:', str(e))
    import traceback
    traceback.print_exc()

print('测试完成！')