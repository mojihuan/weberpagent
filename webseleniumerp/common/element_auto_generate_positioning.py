# coding: utf-8
"""
自动识别 pages 目录下所有 py 文件中的方法 key 值，
并在 element_positioning.py 文件中自动生成缺失的元素定位
"""

import os
import re
from pathlib import Path


class AutoGenerateElementPositioning:
    """自动生成元素定位类"""

    def __init__(self, pages_dir, element_positioning_file, specific_files=None):
        """
        初始化
        :param pages_dir: pages 目录路径
        :param element_positioning_file: element_positioning.py 文件路径
        :param specific_files: 指定的文件列表（可选），格式可以是：
                              - ['pages_attachment.py']  # 只指定文件名
                              - ['pages/pages_attachment.py']  # 相对路径
                              - ['D:\\webseleniumerp\\pages\\pages_attachment.py']  # 绝对路径
        """
        if specific_files is None:
            specific_files = []
        self.pages_dir = pages_dir
        self.element_positioning_file = element_positioning_file
        self.specific_files = specific_files  # 指定的文件列表
        self.existing_keys = set()  # 已存在的 key 集合
        self.missing_keys = []  # 缺失的 key 列表

    def read_element_positioning(self):
        """读取 element_positioning.py 文件，获取已存在的 key"""
        if not os.path.exists(self.element_positioning_file):
            print(f"文件不存在：{self.element_positioning_file}")
            return

        with open(self.element_positioning_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用正则表达式提取所有已存在的 key
        pattern = r'"([^"]+)":\s*\['
        matches = re.findall(pattern, content)
        self.existing_keys = set(matches)
        print(f"已从 element_positioning.py 中读取 {len(self.existing_keys)} 个已存在的 key")

    def find_all_py_files(self):
        """查找 pages 目录下所有 py 文件或指定的文件"""
        py_files = []

        # 如果指定了文件，只处理指定的文件
        if self.specific_files:
            print(f"\n将处理指定的 {len(self.specific_files)} 个文件:")
            for file in self.specific_files:
                # 如果是绝对路径
                if os.path.isabs(file):
                    if os.path.exists(file):
                        py_files.append(file)
                        print(f"  ✓ {file}")
                    else:
                        print(f"  ✗ 文件不存在：{file}")
                else:
                    # 如果是相对路径或文件名，在 pages_dir 下查找
                    full_path = os.path.join(self.pages_dir, file)
                    if os.path.exists(full_path):
                        py_files.append(full_path)
                        print(f"  ✓ {full_path}")
                    else:
                        # 尝试直接在 pages_dir 下查找文件名
                        found = False
                        for root, dirs, files in os.walk(self.pages_dir):
                            if file in files:
                                py_files.append(os.path.join(root, file))
                                print(f"  ✓ {os.path.join(root, file)}")
                                found = True
                                break
                        if not found:
                            print(f"  ✗ 文件不存在：{file}")
        else:
            # 否则扫描整个 pages 目录
            for root, dirs, files in os.walk(self.pages_dir):
                for file in files:
                    if file.endswith('.py') and not file.startswith('__'):
                        py_files.append(os.path.join(root, file))
            print(f"在 pages 目录下找到 {len(py_files)} 个 py 文件")

        return py_files

    def extract_method_calls(self, file_path):
        """
        从 py 文件中提取方法调用及其参数
        :param file_path: py 文件路径
        :return: 提取到的 key 信息列表
        """
        keys_info = []

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            line = lines[i]

            # 匹配 self.click( 或 self.input( 等方法调用
            match = re.search(r'self\.(?:click|input)\s*\(', line)
            if match:
                # 找到方法调用的开始位置
                start_pos = match.end()

                # 收集完整的参数内容，直到匹配的闭括号
                args_parts = [line[start_pos:]]
                paren_count = 1  # 括号计数，用于处理嵌套括号
                j = i + 1

                # 如果当前行没有闭合括号，继续读取后续行
                while paren_count > 0 and j < len(lines):
                    # 检查当前累积的内容中括号是否平衡
                    temp_content = ''.join(args_parts)
                    paren_count = temp_content.count('(') - temp_content.count(')')

                    if paren_count > 0:
                        args_parts.append(lines[j])
                        j += 1
                    else:
                        break

                # 合并所有行的参数部分
                full_args = ''.join(args_parts)

                # 提取到第一个未匹配的闭括号之前
                # 重新计算括号平衡，找到正确的结束位置
                paren_count = 1
                end_index = 0
                for idx, char in enumerate(full_args):
                    if char == '(':
                        paren_count += 1
                    elif char == ')':
                        paren_count -= 1
                        if paren_count == 0:
                            end_index = idx
                            break

                args_str = full_args[:end_index]

                # 如果该行包含 auto=False，直接跳过
                if 'auto=False' in line:
                    i += 1
                    continue

                # 提取 key 参数
                key_match = re.search(r"key\s*=\s*['\"]([^'\"]+)['\"]", args_str)
                if not key_match:
                    i += 1
                    continue

                key = key_match.group(1)

                # 跳过已存在的 key
                if key in self.existing_keys:
                    i += 1
                    continue

                # 提取 desc 参数
                desc_match = re.search(r"desc\s*=\s*['\"]([^'\"]+)['\"]", args_str)
                desc = desc_match.group(1) if desc_match else ''

                # 提取 tag 参数
                tag_match = re.search(r"tag\s*=\s*['\"]([^'\"]+)['\"]", args_str)
                tag = tag_match.group(1) if tag_match else 'span'

                # 提取 index 参数
                index_match = re.search(r"index\s*=\s*(\d+)", args_str)
                index = int(index_match.group(1)) if index_match else 1

                keys_info.append({
                    'key': key,
                    'desc': desc,
                    'tag': tag,
                    'index': index,
                    'file': os.path.basename(file_path)
                })

            i += 1

        return keys_info

    def generate_xpath(self, tag, desc, index):
        """
        根据 tag 类型生成 XPath
        :param tag: HTML 标签类型
        :param desc: description 参数值
        :param index: index 参数值
        :return: XPath 字符串
        """
        if tag == 'span':
            xpath = f"(//span[normalize-space()='{desc}'])[{index}]"
        elif tag == 'input':
            xpath = f"(//input[@placeholder='{desc}'])[{index}]"
        elif tag == 'textarea':
            xpath = f"(//textarea[@placeholder='{desc}'])[{index}]"
        else:
            # 默认使用 span
            xpath = f"(//span[normalize-space()='{desc}'])[{index}]"

        return xpath

    def collect_all_missing_keys(self):
        """收集所有缺失的 key"""
        py_files = self.find_all_py_files()

        for file_path in py_files:
            keys_info = self.extract_method_calls(file_path)
            for info in keys_info:
                if info['key'] not in self.existing_keys:
                    self.missing_keys.append(info)
                    self.existing_keys.add(info['key'])  # 添加到已存在集合，避免重复

        print(f"\n共发现 {len(self.missing_keys)} 个缺失的 key")

    def generate_positioning_code(self):
        """生成元素定位代码"""
        positioning_lines = []

        for info in self.missing_keys:
            xpath = self.generate_xpath(info['tag'], info['desc'], info['index'])
            # 格式："key 名": ["XPath", "", "", "", ""],
            line = f'        "{info["key"]}": ["{xpath}", "", "", "", ""],'
            positioning_lines.append(line)

        return '\n'.join(positioning_lines)

    def update_element_positioning_file(self):
        """更新 element_positioning.py 文件"""
        if not self.missing_keys:
            print("没有需要添加的元素定位")
            return

        # 读取原文件
        with open(self.element_positioning_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 生成新的定位代码
        new_positioning = self.generate_positioning_code()

        # 找到 positioning 字典的结尾位置
        # 策略：在最后一个已有的 key 后面添加
        last_key_pattern = r'(\s+"[^"]+":\s*\[[^\]]*\],\s*)\n(\s*}\s*)'
        match = re.search(last_key_pattern, content, re.MULTILINE)

        if match:
            # 在最后一个 key 后面插入新内容
            insert_pos = match.end(1)
            new_content = content[:insert_pos] + '\n' + new_positioning + '\n' + content[insert_pos:]
        else:
            # 如果找不到合适的插入位置，尝试找到 positioning 字典的开始位置
            positioning_dict_pattern = r'positioning\s*=\s*\{'
            dict_match = re.search(positioning_dict_pattern, content)

            if dict_match:
                # 在 { 后面直接插入
                insert_pos = dict_match.end()
                new_content = content[:insert_pos] + '\n' + new_positioning + '\n' + content[insert_pos:]
            else:
                print("错误：无法找到 positioning 字典")
                return

        # 写入新内容
        with open(self.element_positioning_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"\n已成功添加 {len(self.missing_keys)} 个元素定位到 element_positioning.py")

    def export_to_file(self, output_file='missing_keys.txt'):
        """
        导出缺失的 key 到文本文件（可选功能）
        :param output_file: 输出文件名
        """
        if not self.missing_keys:
            return

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# 缺失的元素定位 Key 列表\n\n")
            for info in self.missing_keys:
                f.write(f"Key: {info['key']}\n")
                f.write(f"  文件：{info['file']}\n")
                f.write(f"  Tag: {info['tag']}\n")
                f.write(f"  Desc: {info['desc']}\n")
                f.write(f"  Index: {info['index']}\n")
                xpath = self.generate_xpath(info['tag'], info['desc'], info['index'])
                f.write(f"  生成的 XPath: {xpath}\n")
                f.write("\n")

        print(f"缺失的 key 已导出到：{output_file}")

    def run(self):
        """执行完整流程"""
        print("=" * 60)
        print("开始自动识别并生成元素定位...")
        if self.specific_files:
            print(f"模式：仅处理指定的 {len(self.specific_files)} 个文件")
        else:
            print("模式：扫描整个 pages 目录")
        print("=" * 60)

        # 1. 读取已存在的 key
        self.read_element_positioning()

        # 2. 收集所有缺失的 key
        self.collect_all_missing_keys()

        if not self.missing_keys:
            print("\n✓ 所有 key 都已存在于 element_positioning.py 中")
            return

        # 3. 显示缺失的 key 信息
        print(f"\n发现以下 {len(self.missing_keys)} 个缺失的 key:")
        for i, info in enumerate(self.missing_keys[:10], 1):  # 只显示前 10 个
            xpath = self.generate_xpath(info['tag'], info['desc'], info['index'])
            print(f"{i}. {info['key']} (来自 {info['file']})")
            print(f"   生成：{xpath}")

        if len(self.missing_keys) > 10:
            print(f"... 还有 {len(self.missing_keys) - 10} 个未显示")

        # 4. 直接更新文件（不再询问）
        self.update_element_positioning_file()

        print("=" * 60)


def main():
    """主函数"""
    # ==================== 在这里直接修改配置 ====================

    # 方式 1: 设置基础路径（默认是当前文件的父目录）
    base_dir = Path(__file__).parent.parent

    # 方式 2: 直接指定 pages 目录的绝对路径（如果需要，取消下面的注释并修改路径）
    # base_dir = Path(r'D:\webseleniumerp')

    pages_dir = base_dir / 'pages'
    element_positioning_file = base_dir / 'common' / 'element_positioning.py'

    # 方式 3: 指定要处理的特定文件（可选）
    # 示例 1: 处理单个文件
    # specific_files = ['pages_attachment.py']

    # 示例 2: 处理多个文件
    # specific_files = ['pages_attachment.py', 'pages_login.py', 'pages_sell.py']

    # 示例 3: 不指定文件，扫描整个 pages 目录（默认）
    specific_files = None

    # ==================== 配置结束 ====================

    # 创建实例并运行
    generator = AutoGenerateElementPositioning(
        pages_dir=str(pages_dir),
        element_positioning_file=str(element_positioning_file),
        specific_files=specific_files
    )
    generator.run()


if __name__ == '__main__':
    main()

