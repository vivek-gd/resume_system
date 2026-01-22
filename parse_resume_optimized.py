# 优化后的简历解析函数
import re

def parse_resume_optimized(file_path):
    """解析PDF/Word简历，提取结构化字段 - 优化版本"""
    import PyPDF2
    from docx import Document

    text = ""
    # 解析PDF
    if file_path.endswith('.pdf'):
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
    # 解析Word（docx）
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        return None

    print('[DEBUG] Extracted text length:', len(text))
    print('[DEBUG] First 500 chars of text:', text[:500])

    # 字段提取（支持多种简历格式）
    resume_data = {
        'name': '', 'job': '', 'intro': '', 'phone': '', 'email': '',
        'education': '', 'experience': '', 'skills': '', 'certificates': ''
    }

    # 提取姓名 - 支持多种格式
    name_patterns = [
        r'姓名[:：]\s*([^\s\n]{2,4})',
        r'Name[:：]\s*([^\s\n]{2,20})',
        r'^\s*([^\s\n]{2,4})\s*(?:男|女|\d+岁)',  # 开头可能的名字
        r'个人资料.*?姓名[:：]\s*([^\s\n]{2,4})'
    ]
    for pattern in name_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            resume_data['name'] = match.group(1).strip()
            print('[DEBUG] Found name:', resume_data['name'])
            break

    # 提取求职意向
    job_patterns = [
        r'求职意向[:：]\s*(.+?)(?:\n|$)',
        r'应聘岗位[:：]\s*(.+?)(?:\n|$)',
        r'Position[:：]\s*(.+?)(?:\n|$)',
        r'意向岗位[:：]\s*(.+?)(?:\n|$)'
    ]
    for pattern in job_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            resume_data['job'] = match.group(1).strip()
            print('[DEBUG] Found job:', resume_data['job'])
            break

    # 提取联系电话
    phone_patterns = [
        r'电话[:：]\s*(\d{11}|\d{3,4}-?\d{7,8})',
        r'手机[:：]\s*(\d{11})',
        r'Phone[:：]\s*(\d{11}|\d{3,4}-?\d{7,8})',
        r'联系方式[:：].*?(\d{11})',
        r'[^\d](1[3-9]\d{9})[^\d]'  # 直接匹配11位手机号
    ]
    for pattern in phone_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            resume_data['phone'] = match.group(1).strip()
            print('[DEBUG] Found phone:', resume_data['phone'])
            break

    # 提取邮箱 - 优先提取学校邮箱
    # 学校邮箱模式：匹配 .edu.cn、.edu、.ac.cn 等教育机构邮箱
    edu_email_patterns = [
        r'[\w\.-]+@(?:[\w-]+\.)?edu(?:\.[\w-]+)+',  # .edu.cn, .edu等
        r'[\w\.-]+@(?:[\w-]+\.)?ac(?:\.[\w-]+)+',   # .ac.cn等学术机构
        r'[\w\.-]+@[\w-]*\.(?:edu|ac)\.[a-z]{2,3}'   # 其他教育域名
    ]

    # 先尝试提取学校邮箱
    for pattern in edu_email_patterns:
        edu_email_match = re.search(pattern, text, re.IGNORECASE)
        if edu_email_match:
            resume_data['email'] = edu_email_match.group(0)
            print('[DEBUG] Found education email:', resume_data['email'])
            break

    # 如果没有找到学校邮箱，再提取普通邮箱
    if not resume_data['email']:
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        if email_match:
            resume_data['email'] = email_match.group(0)
            print('[DEBUG] Found regular email:', resume_data['email'])

    # 提取教育经历 - 支持更多格式
    edu_patterns = [
        r'(教育经历|学历|Education)[:：]?\s*(.*?)(?=工作经历|项目经历|实习经历|技能|自我评价|专业技能|$)',
        r'(教育背景|学历背景)[:：]?\s*(.*?)(?=工作经历|项目经历|技能|$)'
    ]
    for pattern in edu_patterns:
        edu_section = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if edu_section:
            edu_text = edu_section.group(2).strip()
            print('[DEBUG] Education section found, length:', len(edu_text))

            # 从教育经历中提取学校邮箱
            edu_emails = re.findall(r'[\w\.-]+@(?:[\w-]+\.)?edu(?:\.[\w-]+)+', edu_text, re.IGNORECASE)
            if edu_emails:
                resume_data['email'] = edu_emails[0]
                print('[DEBUG] Found education email in education section:', resume_data['email'])

            # 改进的教育经历提取：支持多种格式
            edu_items = []

            # 尝试匹配包含时间段的教育经历
            time_pattern = r'(\d{4}\.?\d{0,2}?\.?\d{0,2}?\s*[-~至到]+\s*\d{4}\.?\d{0,2}?\.?\d{0,2}?)'

            # 按行分割并处理
            lines = [line.strip() for line in edu_text.split('\n') if line.strip()]
            current_edu = []

            for line in lines:
                # 如果包含时间段，可能是新的教育经历开始
                if re.search(time_pattern, line):
                    if current_edu:
                        edu_items.append(' '.join(current_edu))
                    current_edu = [line]
                else:
                    # 检查是否是新的教育经历（包含学校名称）
                    if any(keyword in line for keyword in ['大学', '学院', '学校', 'University', 'College', 'School']):
                        if current_edu:
                            edu_items.append(' '.join(current_edu))
                        current_edu = [line]
                    else:
                        # 继续当前教育经历
                        if current_edu:
                            current_edu.append(line)

            # 添加最后一条
            if current_edu:
                edu_items.append(' '.join(current_edu))

            # 如果没有找到结构化内容，尝试另一种方式提取
            if not edu_items:
                # 尝试匹配包含学校名称的段落
                school_pattern = r'([^\n]{20,200}(?:大学|学院|学校|University|College|School)[^\n]*)'
                edu_items = re.findall(school_pattern, edu_text)

            if edu_items:
                # 格式化教育经历，确保包含关键信息
                formatted_edu = []
                for item in edu_items[:3]:  # 最多保留3条
                    # 提取时间段
                    time_match = re.search(time_pattern, item)
                    # 提取学校名称
                    school_match = re.search(r'(.*?(?:大学|学院|学校|University|College|School).*?)(?:专业|学位|$)', item, re.IGNORECASE)
                    # 提取专业
                    major_match = re.search(r'(?:专业|Major)[:：]?\s*([^\n]{5,50})', item, re.IGNORECASE)
                    # 提取学位
                    degree_match = re.search(r'(?:学位|Degree)[:：]?\s*([^\n]{2,20})', item, re.IGNORECASE)

                    parts = []
                    if time_match:
                        parts.append(time_match.group(1))
                    if school_match:
                        parts.append(school_match.group(1).strip())
                    if major_match:
                        parts.append(major_match.group(1).strip())
                    if degree_match:
                        parts.append(degree_match.group(1).strip())

                    if parts:
                        formatted_edu.append(' | '.join(parts))
                    else:
                        formatted_edu.append(item[:150])

                resume_data['education'] = '\n\n'.join(formatted_edu)
                print('[DEBUG] Found education items:', len(formatted_edu))
            else:
                resume_data['education'] = edu_text[:800]
            break

    # 提取工作/项目经历
    exp_patterns = [
        r'(工作经历|项目经历|实习经历|Experience)[:：]?\s*(.*?)(?=教育经历|学历|技能|自我评价|专业技能|$)',
        r'(工作背景|项目背景|实践经历)[:：]?\s*(.*?)(?=教育经历|技能|$)'
    ]
    for pattern in exp_patterns:
        exp_section = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if exp_section:
            exp_text = exp_section.group(2).strip()
            print('[DEBUG] Experience section found, length:', len(exp_text))
            # 尝试提取时间段+公司+职位格式，使用换行符分隔
            exp_items = re.findall(r'(\d{4}\.?\d{2}?\.?\d{2}?\s*[-~至到]+\s*\d{4}\.?\d{2}?\.?\d{2}?.*?[公司部门单位].*?[:：].*?(\n|$))', exp_text, re.DOTALL)
            if exp_items:
                resume_data['experience'] = '\n\n'.join([item[0][:200].strip() for item in exp_items[:3]])
                print('[DEBUG] Found experience items:', len(exp_items))
            else:
                resume_data['experience'] = exp_text[:800]
            break

    # 提取技能
    skill_patterns = [
        r'(技能|专业技能|Skills)[:：]?\s*(.*?)(?=教育经历|工作经历|自我评价|证书|$)',
        r'(技术栈|专长)[:：]?\s*(.*?)(?=教育经历|工作经历|$)'
    ]
    for pattern in skill_patterns:
        skill_section = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if skill_section:
            resume_data['skills'] = skill_section.group(2).strip()[:300]
            print('[DEBUG] Found skills')
            break

    # 提取证书/荣誉
    cert_patterns = [
        r'(证书|荣誉|奖项|Certificates)[:：]?\s*(.*?)(?=教育经历|工作经历|技能|$)',
        r'(证书荣誉|获奖情况)[:：]?\s*(.*?)(?=教育经历|工作经历|技能|$)'
    ]
    for pattern in cert_patterns:
        cert_section = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if cert_section:
            resume_data['certificates'] = cert_section.group(2).strip()[:300]
            print('[DEBUG] Found certificates')
            break

    # 过滤空值
    result = {k: v for k, v in resume_data.items() if v}
    print('[DEBUG] Final parsed data:', result)
    return result
