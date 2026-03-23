import ast
import os
import pandas as pd

def extract_test_methods_with_decorators_from_directory(directory_path):
    """导出测试报告数据，变更为excel用例"""
    results = []

    # 递归遍历目录中的所有 .py 文件
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=file_path)

                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):  # 找到类定义
                            class_name = node.name
                            # 提取类的文档字符串（类注释）
                            class_docstring = ast.get_docstring(node)
                            class_comment = class_docstring.strip() if class_docstring else ""

                            for item in node.body:
                                if isinstance(item, ast.FunctionDef) and item.name.startswith("test_"):  # 找到test方法
                                    # 提取装饰器信息
                                    decorators = []
                                    for decorator in item.decorator_list:
                                        if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                                            decorator_name = decorator.func.attr
                                            # 过滤掉 @retry_with() 装饰器
                                            if decorator_name == "retry_with":
                                                continue
                                            args = [ast.literal_eval(arg) for arg in decorator.args]
                                            decorators.append(f"@{decorator_name}({', '.join(map(repr, args))})")

                                    # 提取方法的文档字符串（方法注释）
                                    method_docstring = ast.get_docstring(item)
                                    method_comment = method_docstring.strip() if method_docstring else ""

                                    results.append({
                                        "文件路径": file_path,
                                        "类名": class_name,
                                        "类注释": class_comment,
                                        "test方法": item.name,
                                        "方法注释": method_comment,
                                        "装饰器": ", ".join(decorators)  # 装饰器合并为字符串
                                    })
                except Exception as e:
                    print(f"解析文件 {file_path} 时出错: {e}")

    return results

# 使用示例
directory_path = r"D:\webseleniumerp\testcase"
results = extract_test_methods_with_decorators_from_directory(directory_path)

# 将结果转换为 DataFrame 并导出到 Excel
if results:
    df = pd.DataFrame(results)
    output_file = r"D:\webseleniumerp\testcase_export.xlsx"
    df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"数据已成功导出到: {output_file}")
else:
    print("未找到任何 test 方法！")
