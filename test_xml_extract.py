#!/usr/bin/env python3
# 从docx文件的XML中直接提取文本

import os
import sys
import zipfile
import xml.etree.ElementTree as ET

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def extract_text_from_docx(file_path):
    """从docx文件中提取所有文本"""
    print(f"从文件提取文本: {file_path}")
    
    try:
        with zipfile.ZipFile(file_path, 'r') as zf:
            # 读取document.xml
            if 'word/document.xml' in zf.namelist():
                with zf.open('word/document.xml') as f:
                    xml_content = f.read().decode('utf-8', errors='ignore')
                    
                # 解析XML
                root = ET.fromstring(xml_content)
                
                # Word XML命名空间
                ns = {
                    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
                }
                
                # 提取所有文本节点
                text_nodes = []
                for elem in root.findall('.//w:t', ns):
                    if elem.text:
                        text_nodes.append(elem.text)
                
                # 提取所有表格单元格文本
                table_cells = []
                for cell in root.findall('.//w:tc', ns):
                    cell_text = []
                    for t in cell.findall('.//w:t', ns):
                        if t.text:
                            cell_text.append(t.text)
                    if cell_text:
                        table_cells.append(' '.join(cell_text))
                
                print(f"找到 {len(text_nodes)} 个文本节点")
                print(f"找到 {len(table_cells)} 个表格单元格")
                
                # 显示文本节点
                print("\n文本节点内容:")
                for i, text in enumerate(text_nodes):
                    if text.strip():
                        print(f"  文本 {i+1}: '{text}'")
                
                # 显示表格单元格
                print("\n表格单元格内容:")
                for i, cell in enumerate(table_cells):
                    if cell.strip():
                        print(f"  单元格 {i+1}: '{cell}'")
                
                # 合并所有文本
                all_text = ' '.join([t for t in text_nodes if t.strip()])
                print(f"\n合并后的文本: '{all_text}'")
                
                return all_text
            else:
                print("未找到word/document.xml")
                return ""
                
    except Exception as e:
        print(f"提取失败: {e}")
        import traceback
        traceback.print_exc()
        return ""

def test_xml_extract():
    """测试XML提取"""
    print("=== 测试从XML中提取文本 ===")
    
    # 测试用户提到的文件
    test_file = "5d44f5537ce7466d8dfee1a15f42c432.docx"
    documents_dir = os.path.join('static', 'documents')
    file_path = os.path.join(documents_dir, test_file)
    
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        # 查找其他docx文件
        if os.path.exists(documents_dir):
            docx_files = [f for f in os.listdir(documents_dir) if f.endswith('.docx')]
            if docx_files:
                test_file = docx_files[0]
                file_path = os.path.join(documents_dir, test_file)
                print(f"使用文件: {test_file}")
            else:
                print("没有找到docx文件")
                return
        else:
            print("documents目录不存在")
            return
    
    print(f"测试文件: {file_path}")
    print(f"文件大小: {os.path.getsize(file_path)} bytes")
    
    # 提取文本
    extracted_text = extract_text_from_docx(file_path)
    print(f"\n提取到的文本长度: {len(extracted_text)} 字符")
    
    # 尝试解析提取到的文本
    if extracted_text:
        print("\n尝试解析提取到的文本...")
        try:
            from parse_resume_optimized import parse_resume_optimized as parse_resume
            
            # 创建临时文件
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
                f.write(extracted_text)
                temp_file = f.name
            
            # 解析临时文件
            result = parse_resume(temp_file)
            print(f"解析结果: {result}")
            
            # 清理临时文件
            os.unlink(temp_file)
            
        except Exception as e:
            print(f"解析失败: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_xml_extract()