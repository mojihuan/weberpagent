# coding: utf-8
import importlib
import inspect
import os
import re


def camel_to_snake(name):
    """
    查询api、request目录的.py文件，并自动导包初始化

    去除API后缀：自动移除类名末尾的"Api"或"Request"字符串
    驼峰转下划线：将驼峰命名风格转换为下划线命名风格
    """
    if name.lower().endswith('api'):
        name = name[:-3]
    elif name.lower().endswith('request'):
        name = name[:-7]
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    snake_case = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return snake_case


def generate_import_files(project_paths=None, dir_paths=None, verbose=True):
    """
    生成 import_api.py 和 import_request.py 文件的汇总方法

    :param project_paths: 项目路径列表，默认为 ['']
    :param dir_paths: 目录路径列表，默认为 ['api', 'request']
    :param verbose: 是否打印详细日志，默认为 True
    :return: 生成的文件路径列表
    """
    if project_paths is None:
        project_paths = ['']
    if dir_paths is None:
        dir_paths = ['api', 'request']

    generated_files = []

    for project_path_item in project_paths:
        for dir_path_item in dir_paths:
            common_import_api_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                project_path_item, 'common',
                'import_' + dir_path_item + '.py'
            )

            project_root = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                project_path_item,
                dir_path_item
            )

            # 收集所有需要导入的模块
            imports = []
            module_mappings = []
            imported_classes = set()  # 用于避免重复导入类
            success_count = 0
            failed_count = 0
            failed_details = []  # 记录失败的详细信息

            for root, dirs, files in os.walk(project_root):
                for file in files:
                    if file.startswith(dir_path_item + '_') and file.endswith('.py') and not file.startswith(
                            '_') and not file.startswith(
                        'assert_') and file != 'api_login.py':
                        # 计算相对模块路径
                        rel_dir = os.path.relpath(root, project_root)
                        rel_file = os.path.splitext(file)[0]

                        # 构建模块路径
                        if rel_dir == '.':
                            module_path = rel_file
                        else:
                            module_path = rel_dir.replace(os.sep, '.') + '.' + rel_file

                        all_path = dir_path_item + '.' + module_path
                        if project_path_item != '':
                            all_path = project_path_item + '.' + all_path
                        try:
                            # 动态导入模块
                            module = importlib.import_module(all_path)

                            # 自动查找模块中继承自 BaseApi 的所有类
                            from common.base_api import BaseApi

                            target_classes = []

                            for name, obj in inspect.getmembers(module, inspect.isclass):
                                if obj.__module__ == module.__name__ and issubclass(obj, BaseApi):
                                    target_classes.append(obj)

                            if target_classes:
                                for target_cls in target_classes:
                                    # 避免重复导入相同的类名
                                    if target_cls.__name__ not in imported_classes:
                                        # 构建导入语句，导入具体的类名
                                        import_statement = f"from {all_path} import {target_cls.__name__}"
                                        imports.append(import_statement)
                                        imported_classes.add(target_cls.__name__)

                                    # 构建映射条目（不包含注释）
                                    # 直接使用原始类名作为键，不再进行驼峰转下划线转换
                                    mapping_entry = f"        '{target_cls.__name__}': {target_cls.__name__},"
                                    module_mappings.append(mapping_entry)
                                    success_count += 1
                            else:
                                failed_count += 1
                                failed_details.append(f"模块 {all_path}: 未找到继承自 BaseApi 的类")

                        except Exception as e:
                            failed_count += 1
                            failed_details.append(f"模块 {all_path}: {str(e)}")

            # 读取模板文件内容
            template_content = '''# coding: utf-8
{}

class Import{}:
    """
    ImportApi 是一个聚合类，用于统一管理多个模块的 API 断言类。
    通过延迟加载方式按需实例化各个模块的断言类，提高性能并避免重复初始化。
    """

    # ===== 模块与API类映射表 =====
    _module_map = {{
{}

    }}

    def __init__(self):
        # 不使用 __slots__ 以避免兼容性问题
        self._initialized = {{}}

    def __getattr__(self, item):
        """
        动态获取模块对应的 API 实例
        :param item: 模块名
        :return: 对应的 API 实例
        """
        if item in self._module_map:
            # 检查是否已经初始化过该模块
            if item in self._initialized:
                # 如果已经初始化，则直接返回缓存的实例
                return self._initialized[item]

            # 创建实例
            instance = self._module_map[item]()
            # 缓存实例，避免重复创建
            self._initialized[item] = instance
            return instance
        raise AttributeError(f"'Import{}' object has no attribute '{{item}}'")
'''

            # 格式化导入语句和映射表
            import_section = '\n'.join(imports)
            mapping_section = '\n'.join(module_mappings)

            new_class_name = ''
            # 生成最终内容
            if project_path_item != '':
                # 根据mini拆分字符
                new_project_path_item = project_path_item.replace('mini', '')
                new_class_name = 'Mini' + new_project_path_item.capitalize() + dir_path_item.capitalize()

                dir_path_item_classname = project_path_item.capitalize() + dir_path_item.capitalize()
            else:
                dir_path_item_classname = dir_path_item.capitalize()
                new_class_name = dir_path_item.capitalize()

            final_content = template_content.format(import_section, new_class_name, mapping_section,
                                                    dir_path_item_classname)

            # 写入文件
            with open(common_import_api_file, 'w', encoding='utf-8') as f:
                f.write(final_content)

            generated_files.append(common_import_api_file)

            if verbose:
                print(f"import_{dir_path_item}.py: 成功了 {success_count} 个，失败了 {failed_count} 个")
                if failed_details:
                    print("失败详情：")
                    for detail in failed_details:
                        print(f"  - {detail}")

    return generated_files


if __name__ == '__main__':
    """执行生成import_api或者import_request文件"""
    generate_import_files()

