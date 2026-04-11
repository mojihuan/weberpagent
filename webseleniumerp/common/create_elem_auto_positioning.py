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

        # 使用正则表达式提取所有已存在的 key（适配新格式）
        pattern = r'"([^"]+)":\s*"'
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

                # 提取 p_tag 参数（父元素标签）
                p_tag_match = re.search(r"p_tag\s*=\s*['\"]([^'\"]+)['\"]", args_str)
                p_tag = p_tag_match.group(1) if p_tag_match else None

                # 提取 p_name 参数（父元素类名）
                p_name_match = re.search(r"p_name\s*=\s*['\"]([^'\"]+)['\"]", args_str)
                p_name = p_name_match.group(1) if p_name_match else None

                # 提取 o_tag 参数（祖父元素标签）
                o_tag_match = re.search(r"o_tag\s*=\s*['\"]([^'\"]+)['\"]", args_str)
                o_tag = o_tag_match.group(1) if o_tag_match else None

                # 提取 o_name 参数（祖父元素属性）
                o_name_match = re.search(r"o_name\s*=\s*['\"]([^'\"]+)['\"]", args_str)
                o_name = o_name_match.group(1) if o_name_match else None

                keys_info.append({
                    'key': key,
                    'desc': desc,
                    'tag': tag,
                    'index': index,
                    'p_tag': p_tag,
                    'p_name': p_name,
                    'o_tag': o_tag,
                    'o_name': o_name,
                    'file': os.path.basename(file_path)
                })

            i += 1

        return keys_info

    def generate_xpath(self, tag, desc, index, p_tag=None, p_name=None, o_tag=None, o_name=None):
        """
        根据 tag 类型生成 XPath
        :param tag: HTML 标签类型
        :param desc: description 参数值
        :param index: index 参数值
        :param p_tag: 父元素标签类型（可选）
        :param p_name: 父元素类名（可选）
        :param o_tag: 祖父元素标签类型（可选）
        :param o_name: 祖父元素属性（可选）
        :return: XPath 字符串
        """
        # 生成子元素的定位部分
        if '@' in desc:
            # desc 包含@符号，只使用 tag
            child_xpath = f"//{tag}"
        else:
            # desc 不包含@符号，根据 tag 类型生成不同的定位
            if tag == 'span':
                child_xpath = f"//span[normalize-space()='{desc}']"
            elif tag == 'div':
                child_xpath = f"//div[normalize-space()='{desc}']"
            elif tag == 'input':
                child_xpath = f"//input[@placeholder='{desc}']"
            elif tag == 'textarea':
                child_xpath = f"//textarea[@placeholder='{desc}']"
            else:
                # 默认使用 span
                child_xpath = f"//span[normalize-space()='{desc}']"

        # 如果同时有祖父元素和父元素，构建三层嵌套
        if o_tag and o_name and p_tag and p_name:
            # 判断 o_name 是否为中文
            is_chinese = bool(re.search(r'[\u4e00-\u9fa5]', o_name))

            if is_chinese:
                # 第一种场景：o_name 是中文，使用@aria-label 属性匹配
                grandparent_xpath = f"//{o_tag}[@aria-label='{o_name}']"
            else:
                # 第二种场景：o_name 是非中文，使用@class 属性匹配
                grandparent_xpath = f"//{o_tag}[@class='{o_name}']"

            parent_xpath = f"//{p_tag}[@class='{p_name}']"
            # 构建：祖父 -> 父 -> 子 的三层嵌套结构
            full_xpath = f"({grandparent_xpath}{parent_xpath}{child_xpath})[{index}]"
        # 如果只有祖父元素，使用祖父元素定位
        elif o_tag and o_name:
            # 判断 o_name 是否为中文
            is_chinese = bool(re.search(r'[\u4e00-\u9fa5]', o_name))

            if is_chinese:
                # 第一种场景：o_name 是中文，使用@aria-label 属性匹配
                grandparent_xpath = f"//{o_tag}[@aria-label='{o_name}']"
            else:
                # 第二种场景：o_name 是非中文，使用@class 属性匹配
                grandparent_xpath = f"//{o_tag}[@class='{o_name}']"

            full_xpath = f"({grandparent_xpath}{child_xpath})[{index}]"
        # 如果只有父元素，使用父元素定位
        elif p_tag and p_name:
            parent_xpath = f"//{p_tag}[@class='{p_name}']"
            full_xpath = f"({parent_xpath}{child_xpath})[{index}]"
        else:
            # 没有父元素，使用原来的格式
            if '@' in desc:
                full_xpath = f"({child_xpath})[{index}]"
            else:
                full_xpath = f"({child_xpath})[{index}]"

        return full_xpath

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
            xpath = self.generate_xpath(info['tag'], info['desc'], info['index'], info.get('p_tag'), info.get('p_name'), info.get('o_tag'), info.get('o_name'))
            # 格式："key 名": "XPath",
            line = f'        "{info["key"]}": "{xpath}",'
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
        last_key_pattern = r'(\s+"[^"]+":\s*"[^"]*",\s*)\n(\s*}\s*)'
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
                f.write(f"  P_Tag: {info.get('p_tag', 'None')}\n")
                f.write(f"  P_Name: {info.get('p_name', 'None')}\n")
                f.write(f"  O_Tag: {info.get('o_tag', 'None')}\n")
                f.write(f"  O_Name: {info.get('o_name', 'None')}\n")
                xpath = self.generate_xpath(info['tag'], info['desc'], info['index'], info.get('p_tag'), info.get('p_name'), info.get('o_tag'), info.get('o_name'))
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
            xpath = self.generate_xpath(info['tag'], info['desc'], info['index'], info.get('p_tag'), info.get('p_name'), info.get('o_tag'), info.get('o_name'))
            print(f"{i}. {info['key']} (来自 {info['file']})")
            print(f"   生成：{xpath}")

        if len(self.missing_keys) > 10:
            print(f"... 还有 {len(self.missing_keys) - 10} 个未显示")

        # 4. 直接更新文件（不再询问）
        self.update_element_positioning_file()

        print("=" * 60)


def auto_generate_element_positioning(pages_dir=None, element_positioning_file=None,
                                      specific_files=None, verbose=True,
                                      export_file=None):
    """
    自动生成元素定位的统一接口方法

    该方法整合了 AutoGenerateElementPositioning 类的完整流程，
    可供其他文件直接调用。

    Args:
        pages_dir (str, optional): pages 目录路径。
                                  如果为 None，则默认使用项目根目录下的 pages 目录
        element_positioning_file (str, optional): element_positioning.py 文件路径。
                                                  如果为 None，则默认生成到 common/element_positioning.py
        specific_files (list, optional): 指定要处理的文件列表（可选）。
                                        可以是文件名、相对路径或绝对路径。
                                        如果为 None，则扫描整个 pages 目录
        verbose (bool, optional): 是否打印详细信息，默认为 True
        export_file (str, optional): 导出缺失 key 的文件路径（可选）。
                                   如果指定，会将缺失的 key 导出到该文件

    Returns:
        dict: 包含处理结果信息的字典：
              - 'missing_keys': 缺失的 key 列表
              - 'existing_keys_count': 已存在的 key 数量
              - 'processed_files_count': 处理的文件数量
              - 'success': 是否成功完成

    Examples:
        from common.create_elem_auto_positioning import auto_generate_element_positioning

        # 简单使用，使用默认参数
        result = auto_generate_element_positioning()

        # 自定义 pages 目录
        result = auto_generate_element_positioning(
        ...     pages_dir='D:/project/pages'
        ... )

        # 指定特定文件和输出文件
        result = auto_generate_element_positioning(
        ...     pages_dir='D:/project/pages',
        ...     element_positioning_file='D:/project/common/element_positioning.py',
        ...     specific_files=['pages_attachment.py', 'pages_login.py'],
        ...     export_file='missing_keys.txt'
        ... )

        # 静默模式，不打印详细信息
        result = auto_generate_element_positioning(verbose=False)
    """
    try:
        # 如果没有指定 pages 目录，使用默认的项目结构
        if pages_dir is None:
            base_dir = Path(__file__).parent.parent
            pages_dir = base_dir / 'pages'

        # 如果没有指定 element_positioning_file，使用默认路径
        if element_positioning_file is None:
            base_dir = Path(__file__).parent.parent
            element_positioning_file = base_dir / 'common' / 'element_positioning.py'

        # 转换为字符串路径
        pages_dir = str(pages_dir)
        element_positioning_file = str(element_positioning_file)

        if verbose:
            print(f"Pages 目录：{pages_dir}")
            print(f"Element positioning 文件：{element_positioning_file}")
            if specific_files:
                print(f"指定文件：{specific_files}")

        # 创建实例
        generator = AutoGenerateElementPositioning(
            pages_dir=pages_dir,
            element_positioning_file=element_positioning_file,
            specific_files=specific_files if specific_files else []
        )

        # 执行完整流程
        generator.run()

        # 如果指定了导出文件，导出缺失的 key
        if export_file and generator.missing_keys:
            generator.export_to_file(export_file)

        # 返回结果字典
        return {
            'missing_keys': generator.missing_keys,
            'existing_keys_count': len(generator.existing_keys),
            'processed_files_count': len(specific_files) if specific_files else len(generator.find_all_py_files()),
            'success': True
        }

    except Exception as e:
        if verbose:
            print(f"执行过程中出错：{e}")
        return {
            'missing_keys': [],
            'existing_keys_count': 0,
            'processed_files_count': 0,
            'success': False,
            'error': str(e)
        }


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
