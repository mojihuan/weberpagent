# coding: utf-8
import ast
import os
import re
import sys


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ensure_project_root_in_sys_path():
    """确保动态导入时能够解析到顶层包目录。"""
    while CURRENT_DIR in sys.path:
        sys.path.remove(CURRENT_DIR)
    if PROJECT_ROOT not in sys.path:
        sys.path.insert(0, PROJECT_ROOT)


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


def get_base_name(base):
    """提取 AST 基类节点的名称。"""
    if isinstance(base, ast.Name):
        return base.id
    if isinstance(base, ast.Attribute):
        return base.attr
    if isinstance(base, ast.Subscript):
        return get_base_name(base.value)
    if isinstance(base, ast.Call):
        return get_base_name(base.func)
    return None


def find_target_classes(file_path, dir_path_item):
    """静态扫描文件中的目标类，避免导入模块时执行顶层代码。"""
    target_base_names = {'BaseApi'}
    if dir_path_item == 'request':
        target_base_names.update({'InitializeParams', 'BaseImport'})

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            tree = ast.parse(file.read(), filename=file_path)
    except SyntaxError as exc:
        print(f"❌ 解析文件 {file_path} 失败: {exc}")
        return []

    target_classes = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue

        base_names = {get_base_name(base) for base in node.bases}
        if base_names & target_base_names:
            target_classes.append(node.name)

    return target_classes


if __name__ == '__main__':
    """执行生成import_api或者import_request文件"""
    ensure_project_root_in_sys_path()
    project_path = ['',]
    dir_path = ['api', 'request']
    for project_path_item in project_path:
        for dir_path_item in dir_path:
            print('project_path_item:', project_path_item)
            print('dir_path_item:', dir_path_item)
            common_import_api_file = os.path.join(PROJECT_ROOT, project_path_item, 'common',
                                                  'import_' + dir_path_item + '.py')
            print('common_import_api_file:', common_import_api_file)
            project_root = os.path.join(PROJECT_ROOT, project_path_item, dir_path_item)

            print('project_root:', project_root)
            # 收集所有需要导入的模块
            imports = []
            module_mappings = []
            imported_classes = set()  # 用于避免重复导入类

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
                        file_path = os.path.join(root, file)
                        target_classes = find_target_classes(file_path, dir_path_item)

                        if target_classes:
                            for class_name in target_classes:
                                if class_name not in imported_classes:
                                    import_statement = f"# lazy import: {all_path}.{class_name}"
                                    print('--impor:', import_statement)
                                    imports.append(import_statement)
                                    imported_classes.add(class_name)

                                key_name = camel_to_snake(class_name)
                                mapping_entry = f"        '{key_name}': ('{all_path}', '{class_name}'),"
                                module_mappings.append(mapping_entry)
                                print(f"✅ 成功加载类: {class_name}")
                        else:
                            print(f"⚠️ 未在模块 {all_path} 中找到目标类")

            # 读取模板文件内容
            template_content = '''# coding: utf-8
import importlib

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

            module_path, class_name = self._module_map[item]
            module = importlib.import_module(module_path)
            instance_class = getattr(module, class_name)
            # 创建实例
            instance = instance_class()
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
                print('---new:', new_class_name)
            else:
                dir_path_item_classname = dir_path_item.capitalize()
                new_class_name = dir_path_item.capitalize()
            print('---:::', dir_path_item_classname)
            final_content = template_content.format(import_section, new_class_name, mapping_section,
                                                    dir_path_item_classname)

            # 写入文件
            with open(common_import_api_file, 'w', encoding='utf-8') as f:
                f.write(final_content)

            print(f"✅ 成功更新 {common_import_api_file}")
