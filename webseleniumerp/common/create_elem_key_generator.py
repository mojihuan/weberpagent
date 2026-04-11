# coding: utf-8
import os
import re
from common.base_random_mixin import BaseRandomMixin
from common.create_elem_auto_positioning import auto_generate_element_positioning
from config.settings import DATA_PATHS

# 页面步骤key名 13位
class ElementKeyGenerator:
    """元素 key 生成器，用于自动为 key='' 的元素生成随机 key"""

    def __init__(self):
        self.pages_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'pages')
        self.random_generator = BaseRandomMixin()

    @staticmethod
    def is_clear_mode():
        """检查是否开启清除模式"""
        return DATA_PATHS.get('clear_element_keys', False)

    def find_py_files(self):
        """查找 pages 目录下所有以 pages_ 开头的 Python 文件"""
        py_files = []
        if not os.path.exists(self.pages_dir):
            print(f"❌ 目录不存在：{self.pages_dir}")
            return py_files

        for filename in os.listdir(self.pages_dir):
            if filename.startswith('pages_') and filename.endswith('.py'):
                py_files.append(os.path.join(self.pages_dir, filename))

        print(f"✅ 找到 {len(py_files)} 个 Python 文件")
        return py_files

    def find_empty_keys(self, file_path):
        """
        查找文件中所有key='' 的代码行
        :param file_path: 文件路径
        :return: 包含空 key 的行号列表和对应的内容
        """
        empty_key_lines = []

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        pattern = r"key\s*=\s*['\"][\'\"]"

        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                empty_key_lines.append({
                    'line_number': i,
                    'content': line.rstrip()
                })

        return empty_key_lines

    def generate_key_for_file(self, file_path):
        """
        为文件中的每个空 key 生成随机字符串
        :param file_path: 文件路径
        :return: 生成的 key 映射字典
        """
        empty_keys = self.find_empty_keys(file_path)
        generated_keys = {}

        for item in empty_keys:
            new_key = self.random_generator.mixed_random(length=13)
            generated_keys[item['line_number']] = {
                'old_line': item['content'],
                'new_key': new_key
            }

        return generated_keys

    def replace_empty_keys(self, file_path, generated_keys):
        """
        替换文件中的空 key
        :param file_path: 文件路径
        :param generated_keys: 生成的 key 映射字典
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_num, key_info in generated_keys.items():
            old_line = key_info['old_line']
            new_key = key_info['new_key']

            new_line = re.sub(
                r"key\s*=\s*['\"][\'\"]",
                f"key='{new_key}'",
                old_line
            )

            lines[line_num - 1] = new_line + '\n'
            print(f"  第 {line_num} 行：key='' → key='{new_key}'")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    def process_all_files(self, dry_run=True):
        """
        处理所有文件
        :param dry_run: 如果为 True，只显示将要执行的替换，不实际修改文件
        """
        print("=" * 80)
        print("🔍 开始扫描 pages 目录下的 Python 文件...")
        print("=" * 80)

        files = self.find_py_files()
        total_replacements = 0

        for file_path in files:
            filename = os.path.basename(file_path)
            generated_keys = self.generate_key_for_file(file_path)

            if generated_keys:
                print(f"\n📄 文件：{filename}")
                print(f"   发现 {len(generated_keys)} 个空 key")

                if dry_run:
                    print("   【预演模式】将要进行的替换：")
                    for line_num, key_info in generated_keys.items():
                        print(f"     第 {line_num} 行：key='' → key='{key_info['new_key']}'")
                else:
                    print("   正在替换...")
                    self.replace_empty_keys(file_path, generated_keys)

                total_replacements += len(generated_keys)

        if dry_run:
            print(f"📊 统计：共发现 {total_replacements} 个空 key（预演模式，未实际修改）")
            print("💡 提示：如需实际修改，请调用 process_all_files(dry_run=False)")
        else:
            print(f"✅ 完成：共替换 {total_replacements} 个空 key")
        print("=" * 80)

        return total_replacements

    def scan_and_report(self):
        """扫描并生成报告，不进行修改"""

        files = self.find_py_files()
        report = []

        for file_path in files:
            empty_keys = self.find_empty_keys(file_path)
            if empty_keys:
                report.append({
                    'filename': os.path.basename(file_path),
                    'count': len(empty_keys),
                    'lines': [item['line_number'] for item in empty_keys]
                })

        if report:
            print(f"\n发现 {len(report)} 个文件包含空 key：\n")
            for item in report:
                lines_str = ', '.join(map(str, item['lines'][:10]))
                if len(item['lines']) > 10:
                    lines_str += f"... 等共 {len(item['lines'])} 处"
                print(f"  📄 {item['filename']}: {item['count']} 处")
                print(f"     行号：{lines_str}\n")
        else:
            pass

        total = sum(item['count'] for item in report)
        print(f"📊 总计：{len(report)} 个文件，{total} 个空 key")

        return report

    def clear_all_keys(self, dry_run=True):
        """
        清除所有key 的值，将 key='xxx' 改为 key=''
        :param dry_run: 如果为 True，只显示将要执行的替换，不实际修改文件；False 则执行实际清除
        """
        print("=" * 80)
        print("🔍 开始扫描 pages 目录下的 Python 文件...")
        print("=" * 80)

        files = self.find_py_files()
        total_replacements = 0

        for file_path in files:
            filename = os.path.basename(file_path)
            keys_to_clear = self.find_all_keys(file_path)

            if keys_to_clear:
                print(f"\n📄 文件：{filename}")
                print(f"   发现 {len(keys_to_clear)} 个 key")

                if dry_run:
                    print("   【预演模式】将要清除的 key：")
                    for line_num, key_info in keys_to_clear.items():
                        print(f"     第 {line_num} 行：key='{key_info['old_key']}' → key=''")
                else:
                    print("   正在清除...")
                    self.execute_clear_keys(file_path, keys_to_clear)

                total_replacements += len(keys_to_clear)

        if dry_run:
            print(f"\n📊 统计：共发现 {total_replacements} 个 key（预演模式，未实际修改）")
            print("💡 提示：如需实际清除，请调用 clear_all_keys(dry_run=False)")
        else:
            print(f"\n✅ 完成：共清除 {total_replacements} 个 key 的值")
        print("=" * 80)

        return total_replacements

    def find_all_keys(self, file_path):
        """
        查找文件中所有key='xxx' 的代码行
        :param file_path: 文件路径
        :return: 包含 key 的行号列表和对应的内容
        """
        key_lines = {}

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        pattern = r"key\s*=\s*['\"]([^'\"]+)['\"]"

        for i, line in enumerate(lines, 1):
            match = re.search(pattern, line)
            if match:
                old_key = match.group(1)
                key_lines[i] = {
                    'line_number': i,
                    'content': line.rstrip(),
                    'old_key': old_key
                }

        return key_lines

    def execute_clear_keys(self, file_path, keys_to_clear):
        """
        执行清除 key 值的操作
        :param file_path: 文件路径
        :param keys_to_clear: 需要清除的 key 映射字典
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line_num, key_info in keys_to_clear.items():
            old_line = key_info['content']

            new_line = re.sub(
                r"key\s*=\s*['\"][^'\"]+['\"]",
                "key=''",
                old_line
            )

            lines[line_num - 1] = new_line + '\n'
            print(f"  第 {line_num} 行：key='{key_info['old_key']}' → key=''")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)


def main():
    """主函数"""
    clear_mode = ElementKeyGenerator.is_clear_mode()
    generator = ElementKeyGenerator()

    if clear_mode:
        print("\n检测到清除模式已开启，将执行清除所有key 值的操作...")
        total = generator.clear_all_keys(dry_run=False)
        print(f"\n✅ 全部完成！共清除 {total} 个 key 的值")
    else:
        print("\n检测到清除模式未开启，将执行填充空 key 操作...")
        report = generator.scan_and_report()
        if not report:
            print("\n✅ 未发现需要填充的空 key，任务结束")
            return
        total = generator.process_all_files(dry_run=False)
        print(f"\n✅ 全部完成！共填充 {total} 个空 key")


if __name__ == '__main__':
    main()

    # 自动生成元素定位
    result = auto_generate_element_positioning()
    if result['success']:
        print(f"找到 {len(result['missing_keys'])} 个缺失的 key")
        print(f"已存在的 key 数量：{result['existing_keys_count']}")
