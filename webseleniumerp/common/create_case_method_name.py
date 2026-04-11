import re
import os
import glob
from abc import ABC, abstractmethod
from common.create_desc import generate_test_desc
from common.create_import_api_request import generate_import_files


class NameGenerator:
    """统一的名称生成器"""

    def __init__(self, random_generator=None):
        self.random_generator = random_generator

    def generate(self, length=19, prefix=''):
        """
        生成随机名称（确保字母开头）
        :param length: 随机字符串长度
        :param prefix: 前缀（如 'test_'）
        :return: 符合规范的随机字符串
        """
        if self.random_generator and hasattr(self.random_generator, 'mixed_random'):
            name = self.random_generator.mixed_random(length=length)
        else:
            import random
            import string
            first_char = random.choice(string.ascii_letters)
            rest_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=length - 1))
            name = first_char + rest_chars

        return f"{prefix}{name}"

    def generate_class_name(self, length=21):
        """生成类名（首字母大写）"""
        name = self.generate(length=length)
        return name[0].upper() + name[1:]


class BaseFileFixer(ABC):
    """文件修复器基类"""

    def __init__(self, name_generator: NameGenerator):
        self.name_gen = name_generator

    @abstractmethod
    def fix_line(self, line):
        """修复单行代码，返回 (修复后的行, 是否修复, 修复类型)"""
        pass

    def fix_content(self, content):
        """修复完整内容"""
        lines = content.split('\n')
        fixed_lines = []
        stats = {}

        for line in lines:
            fixed_line, is_fixed, fix_type = self.fix_line(line)
            if is_fixed:
                stats[fix_type] = stats.get(fix_type, 0) + 1
            fixed_lines.append(fixed_line)

        stats['total_fixes'] = sum(v for k, v in stats.items() if k != 'total_fixes')
        return '\n'.join(fixed_lines), stats

    def fix_file(self, file_path, encoding='utf-8'):
        """修复文件"""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()

            fixed_content, stats = self.fix_content(content)

            if stats['total_fixes'] > 0:
                with open(file_path, 'w', encoding=encoding) as f:
                    f.write(fixed_content)

            return stats
        except Exception as e:
            raise


class TestMethodFixer(BaseFileFixer):
    """测试方法定义修复器"""

    def __init__(self, name_generator: NameGenerator, is_base_assertions=False):
        super().__init__(name_generator)
        self.is_base_assertions = is_base_assertions

    def fix_line(self, line):
        # 模式: def (self, ...) 或 def (self): 或 def test_(self):
        if re.search(r'def \(self,', line) or re.search(r'def \(self\):', line) or re.search(r'def test_\(self\):', line):
            if self.is_base_assertions:
                random_name = self.name_gen.generate(length=6)
            else:
                random_name = self.name_gen.generate(length=20, prefix='test_')

            if re.search(r'def \(self,', line):
                fixed = re.sub(r'def \(self,', f'def {random_name}(self,', line)
            elif re.search(r'def \(self\):', line):
                fixed = re.sub(r'def \(self\):', f'def {random_name}(self):', line)
            else:
                fixed = re.sub(r'def test_\(self\):', f'def {random_name}(self):', line)

            return fixed, True, 'method_definitions_fixed'

        return line, False, None


class ApiFixer(BaseFileFixer):
    """API文件修复器（类名和方法名）"""

    def fix_line(self, line):
        # 修复类名: class (BaseApi):
        if re.search(r'class \(BaseApi\):', line):
            class_name = self.name_gen.generate_class_name(length=21)
            fixed = re.sub(r'class \(BaseApi\):', f'class {class_name}(BaseApi):', line)
            return fixed, True, 'class_names_fixed'

        # 修复方法名: def (self, ...) 或 def (self): 或 def(self):
        method_patterns = [
            (r'^(\s*)def \(self,', f'def {{}}(self,'),
            (r'^(\s*)def \(self\):', f'def {{}}(self):'),
            (r'^(\s*)def\(self\):', f'def {{}}(self):'),
        ]

        for pattern, template in method_patterns:
            match = re.search(pattern, line)
            if match:
                indent = match.group(1)
                method_name = self.name_gen.generate(length=12)
                fixed = re.sub(pattern, f'{indent}' + template.format(method_name), line)
                return fixed, True, 'method_names_fixed'

        return line, False, None


class RequestFixer(BaseFileFixer):
    """Request文件修复器（类名）"""

    def fix_line(self, line):
        if re.search(r'class \(InitializeParams\):', line):
            class_name = self.name_gen.generate_class_name(length=10)
            fixed = re.sub(r'class \(InitializeParams\):', f'class {class_name}(InitializeParams):', line)
            return fixed, True, 'class_names_fixed'

        return line, False, None


class PagesFixer(BaseFileFixer):
    """Pages文件修复器（类名）"""

    def fix_line(self, line):
        patterns = [
            (r'class \(CommonPages\):', 'CommonPages'),
            (r'class \(BaseMinium\):', 'BaseMinium'),
        ]

        for pattern, base_class in patterns:
            if re.search(pattern, line):
                class_name = self.name_gen.generate_class_name(length=11)
                fixed = re.sub(pattern, f'class {class_name}({base_class}):', line)
                return fixed, True, 'class_names_fixed'

        return line, False, None


class TestcaseClassFixer(BaseFileFixer):
    """Testcase类名修复器"""

    def fix_line(self, line):
        patterns = [
            (r'class \(BaseCase, unittest\.TestCase\):', 'BaseCase, unittest.TestCase'),
            (r'class \(MiniBaseCase\):', 'MiniBaseCase'),
        ]

        for pattern, base_class in patterns:
            if re.search(pattern, line):
                random_suffix = self.name_gen.generate(length=8)
                class_name = f'Test{random_suffix}'
                fixed = re.sub(pattern, f'class {class_name}({base_class}):', line)
                return fixed, True, 'class_names_fixed'

        return line, False, None


class DictKeyFixer(BaseFileFixer):
    """字典Key修复器基类"""

    def __init__(self, name_generator: NameGenerator, key_length, patterns):
        """
        :param name_generator: 名称生成器
        :param key_length: key的长度
        :param patterns: 匹配模式列表，每个元素是 (pattern, replacement_template) 元组
        """
        super().__init__(name_generator)
        self.key_length = key_length
        self.patterns = patterns

    def fix_line(self, line):
        for pattern, template in self.patterns:
            match = re.search(pattern, line)
            if match:
                indent = match.group(1)
                random_key = self.name_gen.generate(length=self.key_length)
                # 使用模板进行替换
                replacement = template.format(indent=indent, key=random_key)
                fixed = re.sub(pattern, replacement, line)
                return fixed, True, 'keys_fixed'

        return line, False, None


class UrlKeyFixer(DictKeyFixer):
    """URL Key修复器"""

    def __init__(self, name_generator: NameGenerator):
        patterns = [
            (r'^(\s*)"":\s*f"', r'{indent}"{key}": f"'),
            (r"^(\s*)'':\s*f'", r"{indent}'{key}': f'"),
        ]
        super().__init__(name_generator, 9, patterns)


class PrerequisitesKeyFixer(DictKeyFixer):
    """Prerequisites Key修复器"""

    def __init__(self, name_generator: NameGenerator):
        patterns = [
            (r'^(\s*)"":\s*\[self\.request\.', r'{indent}"{key}": [self.request.'),
            (r"^(\s*)'':\s*\[self\.request\.", r"{indent}'{key}': [self.request."),
        ]
        super().__init__(name_generator, 4, patterns)


class BatchProcessor:
    """批量处理器"""

    def __init__(self, directory, file_pattern='*.py', exclude_init=True):
        self.directory = directory
        self.file_pattern = file_pattern
        self.exclude_init = exclude_init

    def get_files(self):
        """获取所有需要处理的文件"""
        if not os.path.exists(self.directory):
            raise FileNotFoundError(f"目录不存在：{self.directory}")

        pattern = os.path.join(self.directory, self.file_pattern)
        files = glob.glob(pattern)

        if self.exclude_init:
            files = [f for f in files if not os.path.basename(f).startswith('__')]

        return sorted(files)

    def process(self, fixer, encoding='utf-8'):
        """批量处理文件"""
        files = self.get_files()

        if not files:
            return {'total_files': 0, 'files_processed': 0, 'total_fixes': 0}

        total_stats = {
            'total_files': len(files),
            'files_processed': 0,
            'files_with_fixes': 0,
            'total_fixes': 0
        }

        for file_path in files:
            try:
                stats = fixer.fix_file(file_path, encoding=encoding)
                total_stats['files_processed'] += 1

                if stats['total_fixes'] > 0:
                    total_stats['files_with_fixes'] += 1
                    total_stats['total_fixes'] += stats['total_fixes']

                    for key, value in stats.items():
                        if key not in ['total_fixes']:
                            total_stats[key] = total_stats.get(key, 0) + value

            except Exception as e:
                pass

        return total_stats


class CaseMethodNameGenerator:
    """
    测试用例方法名生成器（主控制器）
    统一管理各种文件修复功能
    """

    def __init__(self, random_generator=None):
        self.name_gen = NameGenerator(random_generator)
        self.testcase_dir = None
        self.api_dir = None
        self.base_url_file = None
        self.request_dir = None
        self.pages_dir = None

    def _validate_dir(self, dir_path, dir_name):
        """验证目录是否存在"""
        if not os.path.exists(dir_path):
            raise FileNotFoundError(f"{dir_name} 目录不存在：{dir_path}")

    def set_testcase_dir(self, testcase_dir):
        self._validate_dir(testcase_dir, "testcase 目录")
        self.testcase_dir = testcase_dir

    def set_api_dir(self, api_dir):
        self._validate_dir(api_dir, "api 目录")
        self.api_dir = api_dir

    def set_base_url_file(self, base_url_file):
        if not os.path.exists(base_url_file):
            raise FileNotFoundError(f"base_url.py 文件不存在：{base_url_file}")
        self.base_url_file = base_url_file

    def set_request_dir(self, request_dir):
        self._validate_dir(request_dir, "request 目录")
        self.request_dir = request_dir

    def set_pages_dir(self, pages_dir):
        self._validate_dir(pages_dir, "pages 目录")
        self.pages_dir = pages_dir

    def scan_and_fix_all_files(self, encoding='utf-8'):
        """扫描并修复所有testcase文件"""
        if not self.testcase_dir:
            raise ValueError("请先调用 set_testcase_dir() 设置 testcase 目录")

        fixer = TestMethodFixer(self.name_gen, is_base_assertions=False)
        processor = BatchProcessor(self.testcase_dir)
        return processor.process(fixer, encoding)

    def scan_and_fix_all_api_files(self, encoding='utf-8'):
        """扫描并修复所有API文件"""
        if not self.api_dir:
            raise ValueError("请先调用 set_api_dir() 设置 api 目录")

        fixer = ApiFixer(self.name_gen)
        processor = BatchProcessor(self.api_dir)
        return processor.process(fixer, encoding)

    def scan_and_fix_all_request_files(self, encoding='utf-8'):
        """扫描并修复所有Request文件"""
        if not self.request_dir:
            raise ValueError("请先调用 set_request_dir() 设置 request 目录")

        fixer = RequestFixer(self.name_gen)
        processor = BatchProcessor(self.request_dir)
        return processor.process(fixer, encoding)

    def scan_and_fix_all_pages_classes(self, encoding='utf-8'):
        """扫描并修复所有Pages文件"""
        if not self.pages_dir:
            raise ValueError("请先调用 set_pages_dir() 设置 pages 目录")

        fixer = PagesFixer(self.name_gen)
        processor = BatchProcessor(self.pages_dir)
        return processor.process(fixer, encoding)

    def scan_and_fix_all_testcase_classes(self, encoding='utf-8'):
        """扫描并修复所有testcase类名"""
        if not self.testcase_dir:
            raise ValueError("请先调用 set_testcase_dir() 设置 testcase 目录")

        fixer = TestcaseClassFixer(self.name_gen)
        processor = BatchProcessor(self.testcase_dir)
        return processor.process(fixer, encoding)

    def scan_and_fix_base_url_file(self, encoding='utf-8'):
        """修复base_url.py文件"""
        if not self.base_url_file:
            raise ValueError("请先调用 set_base_url_file() 设置 base_url.py 文件路径")

        fixer = UrlKeyFixer(self.name_gen)
        stats = fixer.fix_file(self.base_url_file, encoding)

        return stats

    def scan_and_fix_prerequisites_file(self, file_path=None, encoding='utf-8'):
        """修复base_prerequisites.py文件"""
        if file_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            file_path = os.path.join(project_root, 'common', 'base_prerequisites.py')

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"base_prerequisites.py 文件不存在：{file_path}")

        fixer = PrerequisitesKeyFixer(self.name_gen)
        stats = fixer.fix_file(file_path, encoding)

        return stats

    def fix_specific_file(self, file_path, encoding='utf-8', is_base_assertions=False):
        """修复指定的单个文件"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")

        fixer = TestMethodFixer(self.name_gen, is_base_assertions=is_base_assertions)
        return fixer.fix_file(file_path, encoding)

    def fix_specific_api_file(self, file_path, encoding='utf-8'):
        """修复指定的单个API文件"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")

        fixer = ApiFixer(self.name_gen)
        return fixer.fix_file(file_path, encoding)

    def fix_specific_request_file(self, file_path, encoding='utf-8'):
        """修复指定的单个Request文件"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")

        fixer = RequestFixer(self.name_gen)
        return fixer.fix_file(file_path, encoding)

    def fix_specific_pages_classes_file(self, file_path, encoding='utf-8'):
        """修复指定的单个Pages文件"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")

        fixer = PagesFixer(self.name_gen)
        return fixer.fix_file(file_path, encoding)

    def fix_specific_testcase_classes_file(self, file_path, encoding='utf-8'):
        """修复指定的单个testcase类名"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在：{file_path}")

        fixer = TestcaseClassFixer(self.name_gen)
        return fixer.fix_file(file_path, encoding)


# 使用示例
if __name__ == '__main__':
    from common.base_random_mixin import BaseRandomMixin

    # 初始化
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    random_generator = BaseRandomMixin()
    generator = CaseMethodNameGenerator(random_generator=random_generator)

    # 1. 修复testcase文件
    testcase_dir = os.path.join(project_root, 'testcase')
    generator.set_testcase_dir(testcase_dir)
    stats1 = generator.scan_and_fix_all_files()
    print(f"testcase方法名: 修改了 {stats1.get('total_fixes', 0)} 个")

    # 2. 修复base_assertions.py
    base_assertions_file = os.path.join(project_root, 'common', 'base_assertions.py')
    if os.path.exists(base_assertions_file):
        stats2 = generator.fix_specific_file(base_assertions_file, is_base_assertions=True)
        print(f"base_assertions.py方法名: 修改了 {stats2.get('total_fixes', 0)} 个")

    # 3. 修复API文件
    api_dir = os.path.join(project_root, 'api')
    generator.set_api_dir(api_dir)
    stats3 = generator.scan_and_fix_all_api_files()
    print(f"api类名&方法名: 修改了 {stats3.get('total_fixes', 0)} 个")

    # 4. 修复base_url.py
    base_url_file = os.path.join(project_root, 'common', 'base_url.py')
    if os.path.exists(base_url_file):
        generator.set_base_url_file(base_url_file)
        stats4 = generator.scan_and_fix_base_url_file()
        print(f"base_url.py键名: 修改了 {stats4.get('keys_fixed', 0)} 个")

    # 5. 修复Request文件
    request_dir = os.path.join(project_root, 'request')
    generator.set_request_dir(request_dir)
    stats5 = generator.scan_and_fix_all_request_files()
    print(f"Request类名: 修改了 {stats5.get('total_fixes', 0)} 个")

    # 6. 修复testcase类名
    stats6 = generator.scan_and_fix_all_testcase_classes()
    print(f"testcase类名: 修改了 {stats6.get('total_fixes', 0)} 个")

    # 7. 修复Pages文件
    pages_dir = os.path.join(project_root, 'pages')
    generator.set_pages_dir(pages_dir)
    stats7 = generator.scan_and_fix_all_pages_classes()
    print(f"Pages类名: 修改了 {stats7.get('total_fixes', 0)} 个")

    # 8. 修复base_prerequisites.py
    stats8 = generator.scan_and_fix_prerequisites_file()
    print(f"base_prerequisites.py键名: 修改了 {stats8.get('keys_fixed', 0)} 个")

    # 生成注解和导包
    generate_test_desc()
    generate_import_files()
