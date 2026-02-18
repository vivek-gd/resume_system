# 测试脚本 - 检查pdfkit是否能正常导入

print('开始测试pdfkit导入...')

try:
    import pdfkit
    print('pdfkit导入成功！')
    print('pdfkit版本:', pdfkit.__version__)
    print('测试完成，pdfkit可以正常使用。')
except Exception as e:
    print('错误:', str(e))
    import traceback
    traceback.print_exc()
    print('测试失败，pdfkit导入失败。')

print('测试脚本执行完毕。')
input('按回车键退出...')