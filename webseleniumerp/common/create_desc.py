# -*- coding: utf-8 -*-
import os
import re


def clean_constant_name(method_name, file_name=None):
    """
    清理常量名：去除'test_'前缀和数字，文件名仅取前 3 个字母，并作为前缀添加
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

    # 如果清理后名称为空，则使用去除了 test_前缀的原始名称
    if not cleaned_name:
        cleaned_name = method_name[5:] if method_name.startswith('test_') else method_name

    # 处理文件名，去除其中的'test_'前缀和.py 后缀，并只取前 3 个字母
    cleaned_file_name = None
    if file_name:
        # 去除文件名中的'test_'前缀
        if file_name.startswith('test_'):
            cleaned_file_name = file_name[5:]
        else:
            cleaned_file_name = file_name

        # 去除.py 后缀
        if cleaned_file_name.endswith('.py'):
            cleaned_file_name = cleaned_file_name[:-3]

        # 额外确保去除任何残留的"test_"字符串
        cleaned_file_name = cleaned_file_name.replace('test_', '')

        # 【新增逻辑】只取前 3 个字母
        if cleaned_file_name:
            cleaned_file_name = cleaned_file_name[:0]

    # 如果提供了文件名，将其作为前缀添加
    if cleaned_file_name:
        cleaned_name = f"{cleaned_file_name}_{cleaned_name}"

    return cleaned_name


def extract_test_method_comments(file_path):
    """
    提取指定 Python 文件中所有 test_开头方法的注释和文档字符串

    Args:
        file_path (str): 文件路径

    Returns:
        dict: 方法名与对应注释的映射
    """
    import ast

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except SyntaxError:
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

            # 获取函数起始行号（ast 行号从 1 开始）
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
    收集目录下所有测试文件中的 test_方法注释
    """
    if not os.path.exists(directory_path):
        return {}

    all_comments = {}
    failed_count = 0

    # 遍历目录中的所有 Python 文件
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.startswith('test_') and file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    file_comments = extract_test_method_comments(file_path)
                    if file_comments:
                        # 以文件名作为键存储
                        relative_path = os.path.relpath(file_path, directory_path)
                        # 移除.py 扩展名，方便引用
                        module_name = relative_path.replace('.py', '').replace(os.sep, '.')
                        all_comments[file] = file_comments  # 改为使用文件名作为键
                except Exception:
                    failed_count += 1

    return all_comments, failed_count


def save_comments_as_python_constants(comments_dict, output_file, directory_path):
    """
    将注释保存为独立的 Python 常量文件，常量名使用小写并清理，添加文件名前缀

    Args:
        comments_dict (dict): 注释字典
        output_file (str): 输出文件路径
        directory_path (str): 测试目录路径
    """
    # 读取现有文件内容，提取 doc 方法定义（如果存在）
    existing_doc_method = None
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 查找 doc 方法定义
                doc_method_match = re.search(r'def\s+doc\([^)]*\):.*?(?=\n\w|\Z)', content, re.DOTALL)
                if doc_method_match:
                    existing_doc_method = doc_method_match.group(0)
        except Exception:
            pass

    with open(output_file, 'w', encoding='utf-8') as f:
        # 写入文件头
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("# 测试方法注释常量\n")
        f.write("# 由 desc.py 自动生成，请勿手动修改\n\n")

        # 写入增强版 doc 装饰器
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
        f.write("            func.__doc__ = f'{func.__doc__}\\n\\n描述：{description_constant}'\n")
        f.write("        else:\n")
        f.write("            func.__doc__ = f'描述：{description_constant}'\n")
        f.write("        return func\n")
        f.write("    return decorator\n\n")

        if not comments_dict:
            f.write("# 未找到任何测试方法注释\n")
            return

        # 为每个方法生成常量
        for file_name, methods in comments_dict.items():
            # 写入文件标题
            f.write(f"# 文件：{file_name}\n")

            for method_name, comment in methods.items():
                # 生成清理后的常量名，添加文件名前缀
                constant_name = clean_constant_name(method_name, file_name)

                # 处理注释内容，确保能作为 Python 字符串
                # 使用三引号格式，需要转义可能存在的三引号
                escaped_comment = comment.replace('\"\"\"', '\\\"\\\"\\\"')

                # 写入常量定义，使用三引号格式
                f.write(f'{constant_name} = """{escaped_comment}"""\n')

            # 在每个文件后添加空行
            f.write("\n")


def generate_test_desc(testcase_directory=None, output_file=None, run_count=1, verbose=True):
    """
    生成测试用例描述文件的统一接口方法

    该方法整合了提取测试方法注释、收集注释、保存为常量文件的完整流程，
    可供其他文件直接调用。

    Args:
        testcase_directory (str, optional): 测试用例目录路径。
                                           如果为 None，则默认使用项目根目录下的 testcase 目录
        output_file (str, optional): 输出文件路径。
                                    如果为 None，则默认生成到 common/import_desc.py
        run_count (int, optional): 循环运行次数，默认为 1
        verbose (bool, optional): 是否打印详细信息，默认为 True

    Returns:
        tuple: (收集到的注释字典, 更新数量, 失败数量)
              如果出错或没有注释，返回 ({}, 0, 0)

    Examples:
        # >>> from common.create_desc import generate_test_desc
        # >>>
        # >>> # 简单使用，使用默认参数
        # >>> result = generate_test_desc()
        # >>>
        # >>> # 自定义测试目录
        # >>> result = generate_test_desc(testcase_directory='D:/project/testcase')
        # >>>
        # >>> # 自定义输出文件和循环次数
        # >>> result = generate_test_desc(
        # ...     testcase_directory='D:/project/testcase',
        # ...     output_file='D:/project/common/my_desc.py',
        # ...     run_count=2
        # ... )
    """
    # 如果没有指定测试目录，使用默认的项目结构
    if testcase_directory is None:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        testcase_directory = os.path.join(project_root, 'testcase')

    # 如果没有指定输出文件，使用默认路径
    if output_file is None:
        output_file = os.path.join(
            testcase_directory.replace('testcase', ''),
            r'common\import_desc.py'
        )

    total_updated = 0
    total_failed = 0

    # 循环运行指定次数
    for run_index in range(1, run_count + 1):
        # 收集所有注释
        result = collect_test_comments_from_directory(testcase_directory)

        # 兼容旧版本返回值（单个值）和新版本返回值（元组）
        if isinstance(result, tuple):
            all_comments, failed_count = result
        else:
            all_comments = result
            failed_count = 0

        if all_comments:
            # 保存注释为 Python 常量文件
            save_comments_as_python_constants(all_comments, output_file, testcase_directory)
            total_updated += len(all_comments)
            total_failed += failed_count
        else:
            # 即使没有注释也生成一个空的常量文件
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("# -*- coding: utf-8 -*-\n")
                f.write("# 测试方法注释常量\n")
                f.write("# 由 desc.py 自动生成，请勿手动修改\n\n")
                f.write("# 未找到任何测试方法注释\n")
            total_failed += failed_count

    if verbose:
        print(f"import_desc.py: 更新了 {total_updated} 个，失败了 {total_failed} 个")

    return all_comments if all_comments else {}


if __name__ == "__main__":
    # 配置循环次数
    RUN_COUNT = 2  # 可以修改这个数字来改变循环次数

    # 循环运行指定次数
    for run_index in range(1, RUN_COUNT + 1):
        # 指定测试目录路径
        # 获取项目根目录
        project_path = ['', ]
        for project_path_item in project_path:
            project_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), project_path_item)
            testcase_directory = os.path.join(project_root, 'testcase')

            # 输出文件路径
            python_output_file = os.path.join(testcase_directory.replace('testcase', ''), r'common\import_desc.py')

            # 收集所有注释
            result = collect_test_comments_from_directory(testcase_directory)

            # 兼容旧版本返回值（单个值）和新版本返回值（元组）
            if isinstance(result, tuple):
                all_comments, failed_count = result
            else:
                all_comments = result
                failed_count = 0

            if all_comments:
                # 保存注释为 Python 常量文件，传递目录路径
                save_comments_as_python_constants(all_comments, python_output_file, testcase_directory)
            else:
                # 即使没有注释也生成一个空的常量文件
                with open(python_output_file, 'w', encoding='utf-8') as f:
                    f.write("# -*- coding: utf-8 -*-\n")
                    f.write("# 测试方法注释常量\n")
                    f.write("# 由 desc.py 自动生成，请勿手动修改\n\n")
                    f.write("# 未找到任何测试方法注释\n")

    print(f"import_desc.py: 更新了 {len(all_comments) if all_comments else 0} 个文件，失败了 {failed_count if 'failed_count' in locals() else 0} 个文件")

