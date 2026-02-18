# 测试应用程序初始化
print('开始测试应用程序初始化...')

# 修改应用程序的__name__，避免运行主函数
import sys
sys.modules['__main__'] = sys.modules[__name__]

try:
    # 导入应用程序模块
    import app
    print('✓ 应用程序导入成功')
    print('✓ 所有模块加载完成')
except Exception as e:
    print('✗ 应用程序导入失败:', str(e))
    import traceback
    traceback.print_exc()