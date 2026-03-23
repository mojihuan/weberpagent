import os
import ast
import traceback
import importlib.util
import sys


def scan_python_errors(project_path):
    """
    扫描项目中的Python文件，检查语法错误和导入错误
    """
    error_files = []

    # 定义需要忽略的目录名
    ignored_dirs = {'.venv', 'report'}

    for root, _, files in os.walk(project_path):
        # 检查当前路径是否包含需要忽略的目录
        if any(ignored_dir in root.split(os.sep) for ignored_dir in ignored_dirs):
            continue

        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # 尝试解析Python语法
                        tree = ast.parse(content)

                        # 检查导入错误
                        check_import_errors(tree, full_path, error_files)
                except SyntaxError as e:
                    error_files.append({
                        'file': full_path,
                        'error': str(e),
                        'line': e.lineno,
                        'type': 'SyntaxError'
                    })
                except Exception as e:
                    error_files.append({
                        'file': full_path,
                        'error': str(e),
                        'line': None,
                        'type': 'OtherError'
                    })

    return error_files


def check_import_errors(tree, file_path, error_files):
    """
    检查AST树中的导入语句是否存在错误
    """
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            # 对于普通导入 (import module)
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name = alias.name
                    try:
                        importlib.import_module(module_name)
                    except ImportError as e:
                        error_files.append({
                            'file': file_path,
                            'error': f"ImportError: {str(e)}",
                            'line': node.lineno,
                            'type': 'ImportError'
                        })

            # 对于from导入 (from module import name)
            elif isinstance(node, ast.ImportFrom):
                module_name = node.module
                if module_name:  # 确保模块名不是None
                    try:
                        importlib.import_module(module_name)
                    except ImportError as e:
                        error_files.append({
                            'file': file_path,
                            'error': f"ImportError: {str(e)}",
                            'line': node.lineno,
                            'type': 'ImportError'
                        })


# 使用示例
if __name__ == "__main__":
    # 定义需要扫描的项目路径列表
    project_paths = [
        'api',
        'common/base_case.py',
        'common/base_page.py',
        'common/base_params.py',
        'common/base_api.py',
        'common/base_prerequisites.py',
        'common/base_assertions.py',
        'common/base_assertions_field.py',
        'common/base_assert.py',
        'common/base_url.py',
        'common/decorators.py',
        'common/element_positioning.py',
        'common/locust_use.py',
        'common/base_random_mixin.py',
        'request',
        'testcase',
        'pages',
        'config',
        'run_testcase.py',
        'use_testcase_number.py',
        'use_testcase_statics_num.py',
        'use_match_key.py',
        'use_compare_elem_key.py',
        'check_duplicate_urls.py',
        'export_the_use_case.py',
    ]

    all_errors = []

    # 遍历每个项目路径并收集错误
    for project_path in project_paths:
        if os.path.exists(project_path):  # 只扫描存在的目录
            errors = scan_python_errors(project_path)
            all_errors.extend(errors)
        else:
            print(f"警告: 目录 {project_path} 不存在，已跳过")

    # 输出结果
    if all_errors:
        print("发现以下文件存在错误:")
        for error in all_errors:
            print(f"文件: {error['file']}")
            print(f"错误类型: {error.get('type', 'Unknown')}")
            print(f"错误: {error['error']}")
            if error['line']:
                print(f"行号: {error['line']}")
            print("-" * 50)
    else:
        print("未发现明显的语法错误和导入错误")
