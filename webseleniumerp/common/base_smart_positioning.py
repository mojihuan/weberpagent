# coding: utf-8
"""
智能定位模块
提供基于 HTML 源代码的智能 XPath、CSS 定位器生成功能
"""
import os
import re
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from common.element_positioning import ElementPositioning

desc_collector = []
_html_content_cache = {}
_multi_element_cache = {}

COMPILED_PATTERNS = {
    'style': re.compile(r'<style[^>]*>.*?</style>', flags=re.DOTALL | re.IGNORECASE),
    'script': re.compile(r'<script[^>]*>.*?</script>', flags=re.DOTALL | re.IGNORECASE),
    'inline_style': re.compile(r'\s+style\s*=\s*["\'][^"\']*["\']', flags=re.IGNORECASE),
    'doctype': re.compile(r'(<!DOCTYPE[^>]*>)'),
    'html_tag': re.compile(r'(<html[^>]*>)', flags=re.IGNORECASE),
    'end_html_tag': re.compile(r'(</html>)', flags=re.IGNORECASE),
    'end_tag': re.compile(r'</\w+>'),
    'start_tag': re.compile(r'<\w+[^>]*>(?!</)'),
    'self_closing': re.compile(r'<(meta|link|img|br|hr|input)[^>]*>', flags=re.IGNORECASE),
    'xpath_index': re.compile(r'\[\d+\]$'),
    'path': re.compile(r'<path[^>]*>.*?</path>', flags=re.DOTALL | re.IGNORECASE),
    'symbol': re.compile(r'<symbol[^>]*>.*?</symbol>', flags=re.DOTALL | re.IGNORECASE),
}

BLOCK_TAGS = frozenset(['head', 'body', 'div', 'p', 'table', 'tr', 'td', 'th', 'ul', 'ol', 'li',
                        'form', 'input', 'button', 'select', 'option', 'textarea', 'h1', 'h2',
                        'h3', 'h4', 'h5', 'h6', 'header', 'footer', 'nav', 'section', 'article',
                        'aside', 'main', 'span', 'a', 'img', 'br', 'hr'])


class BaseSmartPositioning:
    """智能定位基础类，提供自动 XPath 生成和更新功能"""

    def __init__(self, *args, **kwargs):
        """初始化方法"""
        super().__init__(*args, **kwargs)
        self.elem_positioning = None
        self.positioning = {}
        self._html_soup_cache = None
        self._html_path_cache = None

    def _build_relative_xpath_with_context(self, element, max_depth=3):
        """
        构建使用 and 逻辑的上下文相关 XPath 定位器（基于层级和关系）
        :param element: BeautifulSoup 元素
        :param max_depth: 最大向上追溯深度
        :return: XPath 字符串，包含父子/同级关系，使用 and 连接多个条件
        """
        if element.name is None:
            return ''

        tag = element.name.lower()

        # 策略 1: 查找包含特定文本的子元素
        text_content = element.get_text(strip=True)
        if text_content and len(text_content) < 50:
            parent = element.parent
            while parent and parent.name and parent.name not in ['html', 'body', '[document]']:
                parent_tag = parent.name.lower()

                # 检查父级是否有 class 或 role 等特征
                if parent.has_attr('class') and parent['class']:
                    parent_class = ' '.join(parent['class'])
                    xpath = f'//{parent_tag}[contains(@class,"{parent_class.split()[0]}") and .//{tag}[normalize-space()="{text_content}"]]'
                    return f'({xpath})[1]'

                parent = parent.parent

        # 策略 2: 查找具有特征的祖先元素
        ancestors = []
        current = element.parent
        depth = 0

        while current and current.name and depth < max_depth:
            if current.name in ['html', 'body', '[document]']:
                break

            ancestor_tag = current.name.lower()
            conditions = []

            if current.has_attr('role') and current['role']:
                conditions.append(f'@role="{current["role"]}"')

            if current.has_attr('class') and current['class']:
                class_val = ' '.join(current['class'])
                conditions.append(f'contains(@class,"{class_val.split()[0]}")')

            if current.has_attr('id') and current['id']:
                conditions.append(f'@id="{current["id"]}"')

            if conditions:
                and_condition = ' and '.join(conditions)
                ancestors.insert(0, f'{ancestor_tag}[{and_condition}]')
            else:
                ancestors.insert(0, ancestor_tag)

            current = current.parent
            depth += 1

        if ancestors:
            ancestor_path = '/'.join(ancestors)
            xpath = f'//{ancestor_path}//{tag}'
            return f'({xpath})[1]'

        xpath = f'//{tag}'
        return f'({xpath})[1]'

    def auto_and_update_xpath_realtime(self, key=None, desc=None, html_path=None, index=1, tag=None, p_tag=None, p_name=None, o_tag=None, o_name=None):
        """
        实时自动生成 XPath 并更新（在 click/input 时立即调用）
        会自动使用最近保存的 HTML 文件
        :param key: 元素 key
        :param desc: desc 文本
        :param html_path: HTML 文件路径
        :param index: 元素索引（从 1 开始）
        :param tag: HTML 标签名
        :param p_tag: 父元素标签类型
        :param p_name: 父元素类名
        :param o_tag: 祖父元素标签类型
        :param o_name: 祖父元素属性值
        :return: bool 是否成功
        """
        try:
            html_file_path = html_path

            if not html_file_path:
                for record in reversed(desc_collector):
                    if record.get('html_path'):
                        html_file_path = record['html_path']
                        break

            if not html_file_path:
                print(f"⚠️  跳过生成 - 尚未保存 HTML 文件 (key={key}, desc={desc})")
                return False

            xpath = self.generate_xpath_from_desc(desc, html_file_path, index=index, tag=tag, p_tag=p_tag, p_name=p_name, o_tag=o_tag, o_name=o_name)

            success = self.update_element_positioning(key, xpath)

            return success

        except Exception as e:
            print(f"✗ 实时生成 XPath 失败：{str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def get_element_by_index(self, desc_text, index=1):
        """
        获取重复元素中指定索引的定位
        :param desc_text: desc 参数文本
        :param index: 元素索引（从 1 开始）
        :return: XPath 定位器，如果索引不存在返回 None
        """
        try:
            global _multi_element_cache
            if _multi_element_cache and _multi_element_cache.get('desc') == desc_text:
                elements = _multi_element_cache.get('elements', [])
                if 0 < index <= len(elements):
                    elem_info = elements[index - 1]
                    return elem_info['xpath']
                else:
                    print(f"⚠️  索引 {index} 超出范围 (1-{len(elements)})")
                    return None

            print(f"🔄 重新生成第 {index} 个元素的定位...")
            html_file_path = desc_collector[-1].get('html_path') if desc_collector else None

            if not html_file_path or not os.path.exists(html_file_path):
                raise FileNotFoundError("未找到已保存的 HTML 文件")

            soup = self._get_soup_from_file(html_file_path)

            tag = None
            if desc_collector:
                last_record = desc_collector[-1]
                if last_record.get('desc') == desc_text:
                    tag = last_record.get('tag')

            target_elements = self._find_elements_by_desc(soup, desc_text, index=index, html_file_path=html_file_path, tag=tag)

            if not target_elements or index > len(target_elements):
                print(f"❌ 找不到第 {index} 个元素 (共找到 {len(target_elements)} 个)")
                return None

            elem = target_elements[index - 1]
            xpath = self._build_xpath(elem)

            if not COMPILED_PATTERNS['xpath_index'].search(xpath):
                xpath = f"{xpath}[{index}]"

            return xpath

        except Exception as e:
            print(f"获取指定索引元素失败：{str(e)}")
            return None

    def refresh_html_source(self, file_name='elem/auto_generated.html'):
        """
        重新获取并保存当前页面的 HTML 源代码
        :param file_name: 保存的文件名
        :return: 保存的文件绝对路径
        """
        time.sleep(0.6)
        html_path = self.save_html_code(file_name=file_name)
        time.sleep(1)
        return html_path

    def _identify_locator(self, locator):
        """
        智能识别定位器类型
        :param locator: 定位字符串
        :return: (By, locator_type)
        """
        if isinstance(locator, tuple) and len(locator) == 2:
            if locator[0] in [By.XPATH, By.CSS_SELECTOR, By.ID, By.CLASS_NAME, By.NAME, By.tag, By.LINK_TEXT,
                              By.PARTIAL_LINK_TEXT]:
                return locator

        if isinstance(locator, list):
            return [self._identify_locator(item) for item in locator]

        if locator.startswith(('//', '/html', 'xpath=', '(//')):
            return self.xp(locator)
        else:
            return self.css(locator)

    def save_html_code(self, file_name=None):
        """
        保存当前页面的 HTML 源代码到文件
        :param file_name: 相对路径文件名
        :return: 保存的文件绝对路径
        """
        try:
            html_source = self.driver.page_source

            if file_name is None:
                timestamp = self.get_time_stamp()
                file_name = f"elem/page_cache_{timestamp}.html"

            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(project_root, file_name)
            abs_file_path = os.path.abspath(file_path)

            dir_path = os.path.dirname(abs_file_path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            with open(abs_file_path, 'w', encoding='utf-8') as f:
                f.write(html_source)

            global desc_collector
            if desc_collector:
                for record in desc_collector:
                    record['html_path'] = abs_file_path

            self._html_path_cache = abs_file_path
            self._html_soup_cache = None

            return abs_file_path

        except Exception as e:
            print(f"保存 HTML 源代码失败：{str(e)}")
            raise

    def format_html(self, html_content):
        """
        格式化 HTML 代码
        :param html_content: HTML 字符串
        :return: 格式化后的 HTML 字符串
        """
        html = COMPILED_PATTERNS['doctype'].sub(r'\1\n', html_content)
        html = COMPILED_PATTERNS['html_tag'].sub(r'\n\1\n', html)
        html = COMPILED_PATTERNS['end_html_tag'].sub(r'\n\1', html)

        for tag in BLOCK_TAGS:
            html = re.sub(rf'(<{tag}[^>]*>)', r'\n\1', html, flags=re.IGNORECASE)
            html = re.sub(rf'(</{tag}>)', r'\1\n', html, flags=re.IGNORECASE)

        html = re.sub(r'\n\s*\n', '\n', html)

        lines = html.split('\n')
        formatted_lines = []
        indent_level = 0
        indent_size = '    '

        for line in lines:
            stripped_line = line.strip()
            if not stripped_line:
                continue

            if COMPILED_PATTERNS['end_tag'].match(stripped_line):
                indent_level = max(0, indent_level - 1)

            formatted_lines.append(indent_size * indent_level + stripped_line)

            if COMPILED_PATTERNS['start_tag'].match(stripped_line) and not COMPILED_PATTERNS['self_closing'].match(stripped_line):
                indent_level += 1

        return '\n'.join(formatted_lines)

    def _get_parent_path(self, element, max_depth=5):
        """
        获取元素的父级路径
        :param element: BeautifulSoup 元素
        :param max_depth: 最大深度
        :return: 父级路径字符串
        """
        path = []
        current = element
        depth = 0

        while current and current.parent and depth < max_depth:
            parent = current.parent
            if parent.name and parent.name not in ['[document]', 'html', 'body']:
                class_val = ' '.join(parent.get('class', []))
                if class_val:
                    path.append(f"{parent.name}.{class_val.split()[0]}")
                else:
                    path.append(parent.name)
            current = parent
            depth += 1

        return ' > '.join(reversed(path))

    def _build_xpath(self, element, depth=0, max_depth=5):
        """
        递归构建元素的 XPath 路径
        :param element: BeautifulSoup 元素
        :param depth: 当前递归深度
        :param max_depth: 最大递归深度
        :return: XPath 字符串
        """
        if depth > max_depth or element.name is None:
            return ''

        tag = element.name.lower()

        text_content = element.get_text(strip=True)
        if text_content and len(text_content) < 200:
            xpath = f"//{tag}[normalize-space()='{text_content}']"
            return f'({xpath})[1]'

        if element.has_attr('id') and element['id']:
            xpath = f'//{tag}[@id="{element["id"]}"]'
            return f'({xpath})[1]'

        if element.has_attr('name') and element['name']:
            xpath = f'//{tag}[@name="{element["name"]}"]'
            return f'({xpath})[1]'

        if element.has_attr('placeholder') and element['placeholder']:
            xpath = f'//{tag}[@placeholder="{element["placeholder"]}"]'
            return f'({xpath})[1]'

        if element.has_attr('class') and element['class']:
            class_val = ' '.join(element['class'])
            siblings_with_same_class = [s for s in element.parent.children
                                        if hasattr(s, 'name') and s.name
                                        and s.has_attr('class')
                                        and ' '.join(s['class']) == class_val] if element.parent else []
            if len(siblings_with_same_class) <= 1:
                xpath = f'//{tag}[@class="{class_val}"]'
                return f'({xpath})[1]'

        path_elements = []
        current_element = element
        current_depth = 0

        while current_element and current_element.parent and current_depth <= max_depth:
            path_elements.insert(0, current_element)
            current_element = current_element.parent
            current_depth += 1

        xpath = '//'
        for idx, elem in enumerate(path_elements):
            tag = elem.name.lower()
            xpath_part = f'/{tag}'

            if elem.has_attr('id') and elem['id']:
                xpath_part = f'/{tag}[@id="{elem["id"]}"]'
            elif elem.has_attr('class') and elem['class']:
                class_val = ' '.join(elem['class'])
                siblings_with_same_class = [s for s in elem.parent.children
                                            if hasattr(s, 'name') and s.name
                                            and s.has_attr('class')
                                            and ' '.join(s['class']) == class_val] if elem.parent else []
                if len(siblings_with_same_class) > 1:
                    index = siblings_with_same_class.index(elem) + 1
                    xpath_part = f'/{tag}[@class="{class_val}"][{index}]'
                else:
                    xpath_part = f'/{tag}[@class="{class_val}"]'
            else:
                siblings = [s for s in elem.parent.children if hasattr(s, 'name') and s.name == tag] if elem.parent else []
                if len(siblings) > 1:
                    index = siblings.index(elem) + 1
                    xpath_part = f'/{tag}[{index}]'

            xpath += xpath_part

        return f'({xpath})[1]'

    def _build_xpath_with_or_logic(self, element):
        """
        构建使用 or 逻辑的组合 XPath 定位器
        :param element: BeautifulSoup 元素
        :return: XPath 字符串
        """
        if element.name is None:
            return ''

        tag = element.name.lower()
        conditions = []

        xpath_base = f'//{tag}'

        if element.has_attr('id') and element['id']:
            conditions.append(f'@id="{element["id"]}"')

        if element.has_attr('name') and element['name']:
            conditions.append(f'@name="{element["name"]}"')

        if element.has_attr('placeholder') and element['placeholder']:
            conditions.append(f'@placeholder="{element["placeholder"]}"')

        if element.has_attr('type') and element['type']:
            conditions.append(f'@type="{element["type"]}"')

        if element.has_attr('autocomplete') and element['autocomplete']:
            conditions.append(f'@autocomplete="{element["autocomplete"]}"')

        if element.has_attr('class') and element['class']:
            class_val = ' '.join(element['class'])
            conditions.append(f'contains(@class,"{class_val.split()[0]}")')

        for attr, value in element.attrs.items():
            if attr.startswith('data-v-') and value:
                conditions.append(f'@{attr}="{value}"')
                break

        if not conditions:
            text_content = element.get_text(strip=True)
            if text_content and len(text_content) < 50:
                return f"//{tag}[normalize-space()='{text_content}']"

        if conditions:
            selected_conditions = conditions[:3]
            if len(selected_conditions) == 1:
                return f'{xpath_base}[{selected_conditions[0]}]'
            else:
                or_conditions = ' or '.join(selected_conditions)
                return f'{xpath_base}[{or_conditions}]'

        return xpath_base

    def collect_desc_info(self, key, desc, html_path=None, index=1, tag=None, p_tag=None, p_name=None, o_tag=None, o_name=None):
        """
        收集 desc 信息用于后续生成 XPath
        :param key: 元素 key
        :param desc: 描述文本
        :param html_path: HTML 文件路径
        :param index: 元素索引
        :param tag: HTML 标签名
        :param p_tag: 父元素标签类型
        :param p_name: 父元素类名
        :param o_tag: 祖父元素标签类型
        :param o_name: 祖父元素属性值（如 aria-label）
        :return: None
        """
        global desc_collector
        desc_collector.append({
            'key': key,
            'desc': desc,
            'html_path': html_path,
            'index': index,
            'tag': tag,
            'p_tag': p_tag,
            'p_name': p_name,
            'o_tag': o_tag,
            'o_name': o_name,
            'timestamp': time.time()
        })

    def update_element_positioning(self, key, xpath_value, positioning_file=None):
        """
        更新 element_positioning.py 中的元素定位
        :param key: 元素 key
        :param xpath_value: XPath 值
        :param positioning_file: 定位文件路径
        :return: bool 是否成功更新
        """
        try:
            if positioning_file is None:
                project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                positioning_file = os.path.join(project_root, 'common', 'element_positioning.py')

            if not os.path.exists(positioning_file):
                raise FileNotFoundError(f"定位文件不存在：{positioning_file}")

            with open(positioning_file, 'r', encoding='utf-8') as f:
                content = f.read()

            xpath_str = repr(xpath_value) if isinstance(xpath_value, str) else repr([xpath_value, '', '', '', ''])

            if f'"{key}"' in content:
                pattern = rf'("{key}"\s*:\s*)\[.*?\](?=\s*,|\s*\n\s*"[a-zA-Z_]|}})'
                replacement = f'\\g<1>{xpath_str}'
                new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

                if new_content == content:
                    return False

            else:
                insert_pattern = r'(positioning\s*=\s*\{[^}]*)(\})'
                match = re.search(insert_pattern, content, re.DOTALL)

                if match:
                    needs_comma = not content.rstrip().endswith(',')
                    comma = ',' if needs_comma else ''

                    new_entry = f'{comma}\n        "{key}": {xpath_str}'
                    new_content = re.sub(
                        insert_pattern,
                        lambda m: m.group(1) + new_entry + '\n    ' + m.group(2),
                        content,
                        flags=re.DOTALL
                    )

                else:
                    print(f"错误：无法找到 positioning 字典结构")
                    return False

            with open(positioning_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            import importlib
            from common import element_positioning
            importlib.reload(element_positioning)

            self.elem_positioning = ElementPositioning.__dict__
            self.positioning = self.elem_positioning['positioning']

            return True

        except Exception as e:
            print(f"更新元素定位失败：{str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def auto_and_update_xpath(self, key=None, desc=None, html_file_path=None):
        """
        自动从 desc 生成 XPath 并更新
        :param key: 元素 key
        :param desc: desc 文本
        :param html_file_path: HTML 文件路径
        :return: bool 是否成功
        """
        try:
            if not key or not desc:
                if not desc_collector:
                    raise ValueError("未提供 key 和 desc，且没有历史记录")
                last_record = desc_collector[-1]
                key = key or last_record['key']
                desc = desc or last_record['desc']
                html_file_path = html_file_path or last_record['html_path']

            xpath = self.generate_xpath_from_desc(desc, html_file_path)

            success = self.update_element_positioning(key, xpath)

            return success

        except Exception as e:
            print(f"自动生成并更新 XPath 失败：{str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def _build_relative_xpath(self, element, max_depth=3):
        """
        构建 XPath 相对路径定位器
        :param element: BeautifulSoup 元素
        :param max_depth: 最大向上追溯深度
        :return: XPath 相对路径字符串
        """
        if element.name is None:
            return ''

        tag = element.name.lower()

        parent = element.parent
        depth = 0

        while parent and parent.name and depth < max_depth:
            if parent.name in ['html', 'body', '[document]']:
                break

            parent_tag = parent.name.lower()

            if parent.has_attr('id') and parent['id']:
                xpath = f'//{parent_tag}[@id="{parent["id"]}"]//{tag}'
                return f'({xpath})[1]'

            if parent.has_attr('class') and parent['class']:
                parent_class = ' '.join(parent['class'])
                siblings_with_same_class = [s for s in parent.parent.children
                                            if hasattr(s, 'name') and s.name
                                            and s.has_attr('class')
                                            and ' '.join(s.get('class', [])) == parent_class]

                if len(siblings_with_same_class) <= 1:
                    xpath = f'//{parent_tag}[@class="{parent_class}"]//{tag}'
                    return f'({xpath})[1]'
                else:
                    index = siblings_with_same_class.index(parent) + 1
                    xpath = f'//{parent_tag}[@class="{parent_class}"][{index}]//{tag}'
                    return f'({xpath})[1]'

            if parent.has_attr('role') and parent['role']:
                xpath = f'//{parent_tag}[@role="{parent["role"]}"]//{tag}'
                return f'({xpath})[1]'

            parent = parent.parent
            depth += 1

        text_content = element.get_text(strip=True)
        if text_content and len(text_content) < 50:
            ancestor = element.parent
            while ancestor and ancestor.name and ancestor.name not in ['html', 'body', '[document]']:
                ancestor_tag = ancestor.name.lower()
                if ancestor.has_attr('class') and ancestor['class']:
                    ancestor_class = ' '.join(ancestor['class'])
                    xpath = f'//{ancestor_tag}[@class="{ancestor_class}"]//{tag}[normalize-space()="{text_content}"]'
                    return f'({xpath})[1]'
                ancestor = ancestor.parent

        xpath = f'//{tag}'
        return f'({xpath})[1]'

    def _build_absolute_xpath(self, element, max_depth=20):
        """
        构建元素的 XPath 绝对路径
        :param element: BeautifulSoup 元素
        :param max_depth: 最大递归深度
        :return: XPath 绝对路径字符串
        """
        if element.name is None:
            return ''

        path_elements = []
        current_element = element
        current_depth = 0

        while current_element and current_element.name and current_depth <= max_depth:
            path_elements.insert(0, current_element)
            current_element = current_element.parent
            current_depth += 1

        xpath_parts = ['/html']

        for i, elem in enumerate(path_elements):
            if elem.name == 'html':
                continue

            if elem.name == '[document]':
                continue

            tag = elem.name.lower()

            if elem.name == 'body':
                xpath_parts.append('/body')
                continue

            parent = elem.parent
            if not parent:
                xpath_parts.append(f'/{tag}')
                continue

            siblings = [s for s in parent.children
                        if hasattr(s, 'name') and s.name == tag]

            if len(siblings) > 1:
                index = siblings.index(elem) + 1
                xpath_parts.append(f'/{tag}[{index}]')
            else:
                xpath_parts.append(f'/{tag}')

        return ''.join(xpath_parts)

    def _get_soup_from_file(self, html_file_path):
        """
        从文件读取 HTML 并解析
        :param html_file_path: HTML 文件路径
        :return: BeautifulSoup 对象
        """
        if self._html_path_cache == html_file_path and self._html_soup_cache is not None:
            return self._html_soup_cache

        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')
        self._html_soup_cache = soup
        self._html_path_cache = html_file_path

        return soup

    def generate_xpath_from_desc(self, desc_text, html_file_path=None, index=1, tag=None, p_tag=None, p_name=None, o_tag=None, o_name=None):
        """
        通过 desc 参数生成 XPath 定位
        :param desc_text: desc 参数文本
        :param html_file_path: HTML 文件路径
        :param index: 元素索引（从 1 开始）
        :param tag: HTML 标签名
        :param p_tag: 父元素标签类型
        :param p_name: 父元素类名
        :param o_tag: 祖父元素标签类型
        :param o_name: 祖父元素属性值（如 aria-label 或 class）
        :return: XPath 定位器
        """
        try:
            if html_file_path is None:
                if not desc_collector:
                    raise FileNotFoundError("未找到已保存的 HTML 文件")
                html_file_path = desc_collector[-1].get('html_path')

            if not os.path.exists(html_file_path):
                raise FileNotFoundError(f"HTML 文件不存在：{html_file_path}")

            soup = self._get_soup_from_file(html_file_path)
            target_elements = []

            # 判断 desc 是否包含@符号
            has_at_symbol = '@' in desc_text

            if has_at_symbol:
                # desc 包含@符号，只使用 tag 查找元素
                if tag:
                    tag_lower = tag.lower()
                    target_elements = soup.find_all(tag_lower)
                else:
                    # 没有指定 tag，返回所有元素
                    target_elements = soup.find_all(True)
            else:
                # desc 不包含@符号，使用原有逻辑
                desc_text_clean = desc_text.strip().strip('"').strip("'").strip()

                if tag:
                    tag_lower = tag.lower()

                    if tag_lower in ['input', 'textarea']:
                        target_elements_placeholder = soup.find_all(tag_lower, attrs={'placeholder': lambda x: x and desc_text_clean in x})
                        target_elements.extend(target_elements_placeholder)

                        target_elements_value = soup.find_all(tag_lower, attrs={'value': lambda x: x and desc_text_clean in x})
                        target_elements.extend(target_elements_value)

                    if not target_elements:
                        for element in soup.find_all(tag_lower):
                            text_content = element.get_text(strip=True)
                            if not text_content:
                                continue

                            elem_text_raw = text_content
                            elem_text_clean = elem_text_raw.strip('"').strip("'").strip()
                            elem_text_no_comment = re.sub(r'<!--.*?-->', '', elem_text_clean, flags=re.DOTALL).strip()

                            if elem_text_raw == desc_text or elem_text_clean == desc_text_clean or elem_text_no_comment == desc_text_clean:
                                target_elements.append(element)

                    if not target_elements:
                        for element in soup.find_all(tag_lower):
                            text_content = element.get_text(strip=True)
                            if not text_content:
                                continue

                            elem_text_clean = text_content.strip('"').strip("'").strip()
                            elem_text_no_comment = re.sub(r'<!--.*?-->', '', elem_text_clean, flags=re.DOTALL).strip()

                            if desc_text_clean in elem_text_clean or desc_text_clean in elem_text_no_comment:
                                target_elements.append(element)

                if not target_elements:
                    for element in soup.find_all(string=True):
                        elem_text_raw = element.strip()
                        elem_text_clean = elem_text_raw.strip('"').strip("'").strip()
                        elem_text_no_comment = re.sub(r'<!--.*?-->', '', elem_text_clean, flags=re.DOTALL).strip()

                        if elem_text_raw == desc_text or elem_text_clean == desc_text_clean or elem_text_no_comment == desc_text_clean:
                            target_elements.append(element.parent)

                if not target_elements:
                    for element in soup.find_all(string=True):
                        elem_text_clean = element.strip().strip('"').strip("'").strip()
                        elem_text_no_comment = re.sub(r'<!--.*?-->', '', elem_text_clean, flags=re.DOTALL).strip()

                        if desc_text_clean in elem_text_clean or desc_text_clean in elem_text_no_comment:
                            target_elements.append(element.parent)

                if not target_elements:
                    for btn_tag in ['button', 'a']:
                        all_buttons = soup.find_all(btn_tag)
                        for elem in all_buttons:
                            btn_text = elem.get_text(strip=True)
                            if not btn_text:
                                continue

                            btn_text_clean = btn_text.strip('"').strip("'").strip()
                            btn_text_no_comment = re.sub(r'<!--.*?-->', '', btn_text_clean, flags=re.DOTALL).strip()

                            if btn_text == desc_text or btn_text_clean == desc_text_clean or btn_text_no_comment == desc_text_clean:
                                target_elements.append(elem)
                                break
                        if target_elements:
                            break

                if not target_elements:
                    for element in soup.find_all(True):
                        text_content = element.get_text(strip=True)
                        if not text_content:
                            continue

                        text_clean = text_content.strip('"').strip("'").strip()
                        text_no_comment = re.sub(r'<!--.*?-->', '', text_clean, flags=re.DOTALL).strip()

                        if text_content == desc_text or text_clean == desc_text_clean or text_no_comment == desc_text_clean:
                            target_elements.append(element)

            if not target_elements:
                print(f"\n❌ 警告：未在 HTML 中找到包含文本 '{desc_text}' 元素" + (f" (标签名：{tag})" if tag else ""))
                return ''

            if index is not None:
                print(f"📍 找到 {len(target_elements)} 个匹配元素，需要获取第 {index} 个")

            # 构建最终结果
            indexed_xpaths = []
            for idx, elem in enumerate(target_elements, 1):
                base_xpath_raw = self._build_xpath(elem)

                # 当有多个匹配元素时，替换最外层的索引
                if len(target_elements) > 1:
                    if COMPILED_PATTERNS['xpath_index'].search(base_xpath_raw):
                        xpath_with_index = COMPILED_PATTERNS['xpath_index'].sub(f'[{idx}]', base_xpath_raw)
                    else:
                        xpath_with_index = f"({base_xpath_raw})[{idx}]"
                else:
                    xpath_with_index = base_xpath_raw

                # 如果同时有祖父元素和父元素，构建三层嵌套
                if o_tag and o_name and p_tag and p_name:
                    # 判断 o_name 是否为中文
                    is_chinese = bool(re.search(r'[\u4e00-\u9fa5]', o_name))

                    if is_chinese:
                        # 第一种场景：o_name 是中文，使用@aria-label 属性匹配
                        grandparent_xpath = f"//{o_tag}[@aria-label='{o_name}']"
                        # print(f"🔍 检测到中文 o_name: '{o_name}', 使用@aria-label 匹配")
                    else:
                        # 第二种场景：o_name 是非中文，使用@class 属性匹配
                        grandparent_xpath = f"//{o_tag}[@class='{o_name}']"
                        # print(f"🔍 检测到非中文 o_name: '{o_name}', 使用@class 匹配")

                    # 构建父元素 XPath
                    parent_xpath = f"//{p_tag}[@class='{p_name}']"

                    # 提取子元素 XPath（去掉最外层的括号和索引）
                    child_xpath = xpath_with_index
                    if child_xpath.startswith('('):
                        last_paren_pos = child_xpath.rfind(')')
                        if last_paren_pos != -1:
                            if last_paren_pos < len(child_xpath) - 1 and child_xpath[last_paren_pos + 1] == '[':
                                end_bracket_pos = child_xpath.find(']', last_paren_pos)
                                if end_bracket_pos != -1:
                                    child_xpath = child_xpath[1:last_paren_pos]
                            else:
                                if child_xpath.endswith(']'):
                                    child_xpath = child_xpath[1:-1]
                                else:
                                    child_xpath = child_xpath[1:]

                    # 组合祖父 + 父 + 子元素 XPath，并添加索引
                    full_xpath = f"({grandparent_xpath}{parent_xpath}{child_xpath})[{index}]"
                    xpath_with_index = full_xpath

                # 如果只有祖父元素，使用祖父元素定位
                elif o_tag and o_name:
                    # 判断 o_name 是否为中文
                    is_chinese = bool(re.search(r'[\u4e00-\u9fa5]', o_name))

                    if is_chinese:
                        # 第一种场景：o_name 是中文，使用@aria-label 属性匹配
                        grandparent_xpath = f"//{o_tag}[@aria-label='{o_name}']"
                        # print(f"🔍 检测到中文 o_name: '{o_name}', 使用@aria-label 匹配")
                    else:
                        # 第二种场景：o_name 是非中文，使用@class 属性匹配
                        grandparent_xpath = f"//{o_tag}[@class='{o_name}']"
                        # print(f"🔍 检测到非中文 o_name: '{o_name}', 使用@class 匹配")

                    # 提取子元素 XPath（去掉最外层的括号和索引）
                    child_xpath = xpath_with_index
                    if child_xpath.startswith('('):
                        last_paren_pos = child_xpath.rfind(')')
                        if last_paren_pos != -1:
                            if last_paren_pos < len(child_xpath) - 1 and child_xpath[last_paren_pos + 1] == '[':
                                end_bracket_pos = child_xpath.find(']', last_paren_pos)
                                if end_bracket_pos != -1:
                                    child_xpath = child_xpath[1:last_paren_pos]
                            else:
                                if child_xpath.endswith(']'):
                                    child_xpath = child_xpath[1:-1]
                                else:
                                    child_xpath = child_xpath[1:]

                    # 组合祖父 + 子元素 XPath，并添加索引
                    full_xpath = f"({grandparent_xpath}{child_xpath})[{index}]"
                    xpath_with_index = full_xpath

                # 如果只有父元素信息（没有祖父元素），使用原有逻辑
                elif p_tag and p_name:
                    parent_xpath = f"//{p_tag}[@class='{p_name}']"
                    child_xpath = xpath_with_index

                    if child_xpath.startswith('('):
                        last_paren_pos = child_xpath.rfind(')')
                        if last_paren_pos != -1:
                            if last_paren_pos < len(child_xpath) - 1 and child_xpath[last_paren_pos + 1] == '[':
                                end_bracket_pos = child_xpath.find(']', last_paren_pos)
                                if end_bracket_pos != -1:
                                    child_xpath = child_xpath[1:last_paren_pos]
                            else:
                                if child_xpath.endswith(']'):
                                    child_xpath = child_xpath[1:-1]
                                else:
                                    child_xpath = child_xpath[1:]

                    full_xpath = f"({parent_xpath}{child_xpath})[{index}]"
                    xpath_with_index = full_xpath

                indexed_xpaths.append({
                    'index': idx,
                    'xpath': xpath_with_index,
                    'element': elem
                })

            if index is not None:
                if index <= 0:
                    raise ValueError(f"index 参数必须大于 0，当前值：{index}")

                if index > len(target_elements):
                    raise IndexError(
                        f"⚠️  索引超出范围：需要第 {index} 个元素，但只找到 {len(target_elements)} 个匹配元素\n"
                        f"   desc: '{desc_text}'\n"
                        f"   tag: {tag}\n"
                        f"   HTML 文件：{html_file_path}"
                    )

                elem_info = indexed_xpaths[index - 1]
                print(f"✅ 返回第 {index} 个元素的定位：{elem_info['xpath']}")

                global _multi_element_cache
                _multi_element_cache = {
                    'desc': desc_text,
                    'tag': tag,
                    'elements': indexed_xpaths,
                    'timestamp': time.time()
                }

                return elem_info['xpath']

            first_elem_info = indexed_xpaths[0]
            xpath_to_return = first_elem_info['xpath']

            _multi_element_cache = {
                'desc': desc_text,
                'tag': tag,
                'elements': indexed_xpaths,
                'timestamp': time.time()
            }

            return xpath_to_return

        except Exception as e:
            print(f"生成定位失败：{str(e)}")
            raise

    def _find_elements_by_desc(self, soup, desc_text, index=None, html_file_path=None, tag=None):
        """
        在 HTML 中查找匹配 desc 文本的元素
        :param soup: BeautifulSoup 对象
        :param desc_text: 描述文本
        :param index: 元素索引
        :param html_file_path: HTML 文件路径
        :param tag: HTML 标签名
        :return: XPath 定位器
        """
        target_elements = []

        desc_text_clean = desc_text.strip().strip('"').strip("'").strip()

        for tag in ['input', 'textarea']:
            if tag and tag.lower() != tag:
                continue
            target_elements_placeholder = soup.find_all(tag, attrs={'placeholder': lambda x: x and desc_text_clean in x})
            target_elements.extend(target_elements_placeholder)

            target_elements_value = soup.find_all(tag, attrs={'value': lambda x: x and desc_text_clean in x})
            target_elements.extend(target_elements_value)

        if not target_elements:
            for element in soup.find_all(string=True):
                elem_text_raw = element.strip()
                elem_text_clean = elem_text_raw.strip('"').strip("'").strip()
                elem_text_no_comment = re.sub(r'<!--.*?-->', '', elem_text_clean, flags=re.DOTALL).strip()

                if elem_text_raw == desc_text or elem_text_clean == desc_text_clean or elem_text_no_comment == desc_text_clean:
                    if tag:
                        parent = element.parent
                        if parent and parent.name and parent.name.lower() == tag.lower():
                            target_elements.append(parent)
                    else:
                        target_elements.append(element.parent)

        if not target_elements and tag:
            tag_lower = tag.lower()
            for element in soup.find_all(tag_lower):
                text_content = element.get_text(strip=True)
                if not text_content:
                    continue

                elem_text_raw = text_content
                elem_text_clean = elem_text_raw.strip('"').strip("'").strip()
                elem_text_no_comment = re.sub(r'<!--.*?-->', '', elem_text_clean, flags=re.DOTALL).strip()

                if elem_text_raw == desc_text or elem_text_clean == desc_text_clean or elem_text_no_comment == desc_text_clean:
                    target_elements.append(element)

        if not target_elements:
            for element in soup.find_all(string=True):
                elem_text_clean = element.strip().strip('"').strip("'").strip()
                elem_text_no_comment = re.sub(r'<!--.*?-->', '', elem_text_clean, flags=re.DOTALL).strip()

                if desc_text_clean in elem_text_clean or desc_text_clean in elem_text_no_comment:
                    if tag:
                        parent = element.parent
                        if parent and parent.name and parent.name.lower() == tag.lower():
                            target_elements.append(parent)
                    else:
                        target_elements.append(element.parent)

        if not target_elements and tag:
            tag_lower = tag.lower()
            for element in soup.find_all(tag_lower):
                text_content = element.get_text(strip=True)
                if not text_content:
                    continue

                elem_text_clean = text_content.strip('"').strip("'").strip()
                elem_text_no_comment = re.sub(r'<!--.*?-->', '', elem_text_clean, flags=re.DOTALL).strip()

                if desc_text_clean in elem_text_clean or desc_text_clean in elem_text_no_comment:
                    target_elements.append(element)

        if not target_elements:
            button_tags = ['button', 'a']
            if tag and tag.lower() in button_tags:
                button_tags = [tag.lower()]

            for tag in button_tags:
                all_buttons = soup.find_all(tag)
                for elem in all_buttons:
                    btn_text = elem.get_text(strip=True)
                    if not btn_text:
                        continue

                    btn_text_clean = btn_text.strip('"').strip("'").strip()
                    btn_text_no_comment = re.sub(r'<!--.*?-->', '', btn_text_clean, flags=re.DOTALL).strip()

                    if btn_text == desc_text or btn_text_clean == desc_text_clean or btn_text_no_comment == desc_text_clean:
                        target_elements.append(elem)
                        break
                if target_elements:
                    break

        if not target_elements:
            for element in soup.find_all(True):
                text_content = element.get_text(strip=True)
                if not text_content:
                    continue

                text_clean = text_content.strip('"').strip("'").strip()
                text_no_comment = re.sub(r'<!--.*?-->', '', text_clean, flags=re.DOTALL).strip()

                if text_content == desc_text or text_clean == desc_text_clean or text_no_comment == desc_text_clean:
                    if tag:
                        if element.name and element.name.lower() == tag.lower():
                            target_elements.append(element)
                    else:
                        target_elements.append(element)

        if not target_elements:
            if tag:
                tag_lower = tag.lower()
                xpath = f'//{tag_lower}[normalize-space()="{desc_text_clean}"]'
            else:
                xpath = f'//*[normalize-space()="{desc_text_clean}"]'
            try:
                from selenium.webdriver.common.by import By
                elements = self.driver.find_elements(By.XPATH, xpath)
                if elements:
                    print(f"   ✅ Selenium 找到 {len(elements)} 个元素")
                    for elem in elements:
                        elem_html = elem.get_attribute('outerHTML')
                        soup_elem = BeautifulSoup(elem_html, 'html.parser')
                        if soup_elem:
                            target_elements.append(soup_elem)

                    print(f"✅ Selenium 匹配成功 - 找到 {len(target_elements)} 个元素")
            except Exception as e:
                print(f"   ⚠️  XPath 查找失败：{e}")

        if not target_elements:
            for element in soup.find_all(True):
                text_content = element.get_text(strip=True)
                if not text_content:
                    continue

                text_clean = text_content.strip('"').strip("'").strip()
                text_no_comment = re.sub(r'<!--.*?-->', '', text_clean, flags=re.DOTALL).strip()

                if text_no_comment == desc_text_clean and element.has_attr('class'):
                    class_str = ' '.join(element.get('class', []))
                    if any(keyword in class_str for keyword in ['radio', 'checkbox', 'button', 'inner']):
                        if tag:
                            if element.name and element.name.lower() == tag.lower():
                                target_elements.append(element)
                                break
                        else:
                            target_elements.append(element)
                            break

        if not target_elements:
            print(f"\n❌ 警告：未在 HTML 中找到包含文本 '{desc_text}' 元素" + (f" (标签名：{tag})" if tag else ""))
            return ''

        if index is not None:
            print(f"📍 找到 {len(target_elements)} 个匹配元素，需要获取第 {index} 个")

        indexed_xpaths = []
        for idx, elem in enumerate(target_elements, 1):
            base_xpath_raw = self._build_xpath(elem)

            if len(target_elements) > 1:
                if COMPILED_PATTERNS['xpath_index'].search(base_xpath_raw):
                    xpath_with_index = COMPILED_PATTERNS['xpath_index'].sub(f'[{idx}]', base_xpath_raw)
                else:
                    xpath_with_index = f"({base_xpath_raw})[{idx}]"
            else:
                xpath_with_index = base_xpath_raw

            indexed_xpaths.append({
                'index': idx,
                'xpath': xpath_with_index,
                'element': elem
            })

        if index is not None:
            if index <= 0:
                raise ValueError(f"index 参数必须大于 0，当前值：{index}")

            if index > len(target_elements):
                raise IndexError(
                    f"⚠️  索引超出范围：需要第 {index} 个元素，但只找到 {len(target_elements)} 个匹配元素\n"
                    f"   desc: '{desc_text}'\n"
                    f"   tag: {tag}\n"
                    f"   HTML 文件：{html_file_path}"
                )

            elem_info = indexed_xpaths[index - 1]
            print(f"✅ 返回第 {index} 个元素的定位：{elem_info['xpath']}")

            global _multi_element_cache
            _multi_element_cache = {
                'desc': desc_text,
                'tag': tag,
                'elements': indexed_xpaths,
                'timestamp': time.time()
            }

            return elem_info['xpath']

        first_elem_info = indexed_xpaths[0]
        xpath_to_return = first_elem_info['xpath']

        _multi_element_cache = {
            'desc': desc_text,
            'tag': tag,
            'elements': indexed_xpaths,
            'timestamp': time.time()
        }

        return xpath_to_return
