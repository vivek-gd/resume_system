# 测试导入路径和模块是否存在
import os
import sys

print('开始测试导入路径和模块是否存在...')

# 打印当前目录和Python搜索路径
print('当前目录:', os.getcwd())
print('Python搜索路径:', sys.path)

# 检查parse_resume_optimized.py文件是否存在
file_path = 'parse_resume_optimized.py'
if os.path.exists(file_path):
    print(f'✓ {file_path} 文件存在')
    print('文件大小:', os.path.getsize(file_path))
else:
    print(f'✗ {file_path} 文件不存在')

# 尝试使用importlib导入模块
print('尝试使用importlib导入模块...')
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("parse_resume_optimized", file_path)
    if spec:
        print('✓ 模块规格创建成功')
        module = importlib.util.module_from_spec(spec)
        if module:
            print('✓ 模块创建成功')
            sys.modules["parse_resume_optimized"] = module
            try:
                spec.loader.exec_module(module)
                print('✓ 模块执行成功')
                if hasattr(module, 'parse_resume_optimized'):
                    print('✓ parse_resume_optimized函数存在')
                else:
                    print('✗ parse_resume_optimized函数不存在')
            except Exception as e:
                print('✗ 模块执行失败:', str(e))
                import traceback
                traceback.print_exc()
        else:
            print('✗ 模块创建失败')
    else:
        print('✗ 模块规格创建失败')
except Exception as e:
    print('✗ importlib导入失败:', str(e))
    import traceback
    traceback.print_exc()

print('测试完成')