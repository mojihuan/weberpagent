# -*- coding: utf-8 -*-
import os
import re


def clean_constant_name(method_name, file_name=None):
    """
    清理常量名：去除'test_'前缀和数字，文件名仅取前3个字母，并作为前缀添加
    Args:
        method_name (str): 原始方法名
        file_name (str, optional): 文件名作为前缀
    Returns:
        str: 清理后的常量名
    """
    # 去除方法名中的'test_'前缀
    if method_name.startswith('test_'):
        cleaned_name = method_name[5:]  # 去除'test_'前缀
    else:
        cleaned_name = method_name

    # 去除开头的数字
    cleaned_name = re.sub(r'^\d+', '', cleaned_name)

    # 额外确保去除任何残留的"test_"字符串
    cleaned_name = cleaned_name.replace('test_', '')

    # 如果清理后名称为空，则使用去除了test_前缀的原始名称
    if not cleaned_name:
        cleaned_name = method_name[5:] if method_name.startswith('test_') else method_name

    # 处理文件名，去除其中的'test_'前缀和.py后缀，并只取前3个字母
    cleaned_file_name = None
    if file_name:
        # 去除文件名中的'test_'前缀
        if file_name.startswith('test_'):
            cleaned_file_name = file_name[5:]
        else:
            cleaned_file_name = file_name

        # 去除.py后缀
        if cleaned_file_name.endswith('.py'):
            cleaned_file_name = cleaned_file_name[:-3]

        # 额外确保去除任何残留的"test_"字符串
        cleaned_file_name = cleaned_file_name.replace('test_', '')

        # 【新增逻辑】只取前3个字母
        if cleaned_file_name:
            cleaned_file_name = cleaned_file_name[:1]

    # 如果提供了文件名，将其作为前缀添加
    if cleaned_file_name:
        cleaned_name = f"{cleaned_file_name}_{cleaned_name}"

    return cleaned_name.lower()


def extract_test_method_comments(file_path):
    """
    提取指定Python文件中所有test_开头方法的注释和文档字符串

    Args:
        file_path (str): 文件路径

    Returns:
        dict: 方法名与对应注释的映射
    """
    import ast

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError as e:
            print(f"解析文件 {file_path} 时出现语法错误: {e}")
            return {}

    comments = {}
    source_lines = None

    # 读取行内容用于查找注释
    with open(file_path, 'r', encoding='utf-8') as f:
        source_lines = f.readlines()

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
            method_name = node.name

            # 获取函数的文档字符串
            docstring = ast.get_docstring(node)

            # 获取函数起始行号（ast行号从1开始）
            lineno = node.lineno - 1

            # 向上查找最近的注释行
            comment = ""
            for i in range(lineno - 1, -1, -1):
                line = source_lines[i].strip()
                if line.startswith('#'):
                    comment = line[1:].strip()  # 去掉 # 号和空格
                    break
                elif line:  # 遇到非注释非空行则停止
                    break

            # 合并注释和文档字符串
            if docstring and comment:
                # 如果既有注释又有文档字符串，将两者合并
                full_comment = f"{comment}\n{docstring}"
            elif docstring:
                # 只有文档字符串
                full_comment = docstring
            else:
                # 只有注释或都没有
                full_comment = comment

            comments[method_name] = full_comment

    return comments


def collect_test_comments_from_directory(directory_path):
    """
    收集目录下所有测试文件中的test_方法注释
    """
    if not os.path.exists(directory_path):
        print(f"目录 {directory_path} 不存在")
        return {}

    all_comments = {}

    # 遍历目录中的所有Python文件
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.startswith('test_') and file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    file_comments = extract_test_method_comments(file_path)
                    if file_comments:
                        # 以文件名作为键存储
                        relative_path = os.path.relpath(file_path, directory_path)
                        # 移除.py扩展名，方便引用
                        module_name = relative_path.replace('.py', '').replace(os.sep, '.')
                        all_comments[file] = file_comments  # 改为使用文件名作为键
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {e}")

    return all_comments


def save_comments_as_python_constants(comments_dict, output_file, directory_path):
    """
    将注释保存为独立的Python常量文件，常量名使用小写并清理，添加文件名前缀

    Args:
        comments_dict (dict): 注释字典
        output_file (str): 输出文件路径
        directory_path (str): 测试目录路径
    """
    # 读取现有文件内容，提取doc方法定义（如果存在）
    existing_doc_method = None
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 查找doc方法定义
                doc_method_match = re.search(r'def\s+doc\([^)]*\):.*?(?=\n\w|\Z)', content, re.DOTALL)
                if doc_method_match:
                    existing_doc_method = doc_method_match.group(0)
        except Exception as e:
            print(f"读取现有文件时出错: {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        # 写入文件头
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("# 测试方法注释常量\n")
        f.write("# 由desc.py自动生成，请勿手动修改\n\n")

        # 写入增强版doc装饰器
        f.write("def doc(description_constant):\n")
        f.write("    \"\"\"\n")
        f.write("    文档装饰器，用于为函数添加描述信息\n")
        f.write("    \n")
        f.write("    Args:\n")
        f.write("        description_constant (str): 描述信息常量\n")
        f.write("    \"\"\"\n")
        f.write("    def decorator(func):\n")
        f.write("        # 将描述信息添加到函数的文档字符串中\n")
        f.write("        if func.__doc__:\n")
        f.write("            func.__doc__ = f'{func.__doc__}\\n\\n描述: {description_constant}'\n")
        f.write("        else:\n")
        f.write("            func.__doc__ = f'描述: {description_constant}'\n")
        f.write("        return func\n")
        f.write("    return decorator\n\n")

        if not comments_dict:
            f.write("# 未找到任何测试方法注释\n")
            return

        # 为每个方法生成常量
        for file_name, methods in comments_dict.items():
            # 写入文件标题
            f.write(f"# 文件: {file_name}\n")

            for method_name, comment in methods.items():
                # 生成清理后的常量名，添加文件名前缀
                constant_name = clean_constant_name(method_name, file_name)

                # 处理注释内容，确保能作为Python字符串
                # 使用三引号格式，需要转义可能存在的三引号
                escaped_comment = comment.replace('\"\"\"', '\\\"\\\"\\\"')

                # 写入常量定义，使用三引号格式
                f.write(f'{constant_name} = \"\"\"{escaped_comment}\"\"\"\n')

            # 在每个文件后添加空行
            f.write("\n")


# 使用示例
if __name__ == "__main__":
    # 指定测试目录路径
    # 获取项目根目录
    project_path = ['',]
    for project_path_item in project_path:
        project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), project_path_item)
        testcase_directory = os.path.join(project_root, 'testcase')
        print('--project_root:', project_root, '--testcase_directory:', testcase_directory)
        # 输出文件路径
        python_output_file = os.path.join(project_root, 'common', 'import_desc.py')
        print(f"指定目录路径: {testcase_directory}, {python_output_file}")

        # 收集所有注释
        all_comments = collect_test_comments_from_directory(testcase_directory)

        if all_comments:
            # 保存注释为Python常量文件，传递目录路径
            save_comments_as_python_constants(all_comments, python_output_file, testcase_directory)

            print(f"已收集所有测试方法注释并保存到 {python_output_file}")
            print(f"总共收集到 {len(all_comments)} 个文件的注释")
            for file, methods in all_comments.items():
                print(f"  文件 {file}: {len(methods)} 个方法")
        else:
            print("未收集到任何注释，请检查目录路径是否正确")

            # 即使没有注释也生成一个空的常量文件
            with open(python_output_file, 'w', encoding='utf-8') as f:
                f.write("# -*- coding: utf-8 -*-\n")
                f.write("# 测试方法注释常量\n")
                f.write("# 由desc.py自动生成，请勿手动修改\n\n")
                f.write("# 未找到任何测试方法注释\n")
