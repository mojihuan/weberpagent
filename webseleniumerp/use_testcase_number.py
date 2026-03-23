import re
from pathlib import Path
from collections import Counter

try:
    from config.settings import DATA_PATHS

    CLEAR_ALL_TESTCASE_NUMBERS = DATA_PATHS.get('testcase_numbers', False)
except ImportError:
    CLEAR_ALL_TESTCASE_NUMBERS = False
    print("警告: 未找到 config/settings.py 配置文件，使用默认值 (False)")


def get_all_testcase_numbers(all_contents):
    """从所有内容中提取所有测试用例编号"""
    all_matches = []
    for content in all_contents:
        matches = re.findall(r'T\d{8}', content)
        all_matches.extend(matches)
    return all_matches


def find_next_global_testcase_number(all_contents):
    """查找所有文件中当前最大的用例编号，返回下一个编号"""
    all_matches = get_all_testcase_numbers(all_contents)

    if all_matches:
        numbers = [int(match[1:]) for match in all_matches]
        return max(numbers) + 1
    else:
        return 1


def check_duplicate_numbers(content, file_path):
    """检查是否有重复的用例编号"""
    matches = re.findall(r'T\d{8}', content)

    if matches:
        count = Counter(matches)
        duplicates = {num: cnt for num, cnt in count.items() if cnt > 1}

        if duplicates:
            print(f"  ⚠️  {file_path}: ", end="")
            for num, cnt in duplicates.items():
                print(f"{num}({cnt}次) ", end="")
            print()
            return True
    return False


def find_test_methods_without_numbers(content):
    """查找没有编号的测试方法"""
    pattern = r'^(\s*)(def\s+test_\w+\s*\([^)]*\)\s*:)(\s*\n\s*)("""\[([^\]]+)\]([^\"]*?)(?<!T\d{8}))"""\s*\n'
    return re.findall(pattern, content, re.MULTILINE)


def remove_all_testcase_numbers(content):
    """移除所有测试用例编号"""
    pattern = r'-T\d{8}'
    updated_content = re.sub(pattern, '', content)

    # 清理可能产生的多余符号
    updated_content = re.sub(r'(-\s*""")', '"""', updated_content)
    updated_content = re.sub(r'"""\s*-\s*"""', '"""', updated_content)
    updated_content = re.sub(r'(\s+)-(\s+)', r'\1\2', updated_content)

    return updated_content


def process_single_file(file_path, global_next_number=None, used_numbers=None, clear_only=False):
    """处理单个测试文件，根据模式清除或添加编号"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if clear_only:
        cleared_content = remove_all_testcase_numbers(content)
        if cleared_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleared_content)
            print(f"  ✓ 已清除 {file_path.name} 中的编号")
            return cleared_content, 1
        else:
            return content, 0

    else:  # 添加模式
        methods_without_numbers = find_test_methods_without_numbers(content)
        if not methods_without_numbers:
            return content, 0

        check_duplicate_numbers(content, file_path.name)

        pattern = r'^(\s*)(def\s+test_\w+\s*\([^)]*\)\s*:)(\s*\n\s*)("""\[([^\]]+)\]([^\"]*?)(?<!T\d{8}))"""\s*\n'
        current_number = global_next_number[0]

        def add_number_if_missing(match):
            nonlocal current_number
            full_indent, func_def, newline_indent, full_docstring, action_part = \
                match.group(1), match.group(2), match.group(3), match.group(4), match.group(5)

            if not re.search(r'T\d{8}', full_docstring) and not re.search(r'-T\d{8}$', full_docstring.strip()):
                while f'T{current_number:08d}' in used_numbers:
                    current_number += 1

                new_docstring = f'{full_docstring}-T{current_number:08d}"""'
                used_numbers.add(f'T{current_number:08d}')

                current_number += 1
                return f"{full_indent}{func_def}{newline_indent}{new_docstring}\n"

            return match.group(0)

        updated_content = re.sub(pattern, add_number_if_missing, content, flags=re.MULTILINE)
        processed_count = current_number - global_next_number[0]

        if processed_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"  ✓ {file_path.name}: 添加了 {processed_count} 个编号 (T{global_next_number[0]:08d}-T{current_number-1:08d})")
        else:
            print(f"  → {file_path.name}: 无需添加编号")

        global_next_number[0] = current_number
        return updated_content, processed_count


def process_all_test_files(testcase_dir, clear_only=CLEAR_ALL_TESTCASE_NUMBERS):
    """处理testcase目录下所有test*.py文件"""
    testcase_path = Path(testcase_dir)
    if not testcase_path.exists():
        print(f"❌ 错误: 目录不存在 - {testcase_dir}")
        return

    test_files = list(testcase_path.glob('test*.py'))
    print(f"📁 扫描目录: {testcase_dir} (找到 {len(test_files)} 个文件)")

    if clear_only:
        print("🧹 清除模式")
        total_cleared = 0
        for file_path in test_files:
            cleared_count = process_single_file(file_path, clear_only=True)[1]
            total_cleared += cleared_count
        print(f"  ✓ 共清除 {total_cleared} 个编号")
        return total_cleared

    else:
        print("🏷️  添加模式")
        # 读取所有文件内容
        file_content_pairs = [(file_path, file_path.read_text(encoding='utf-8')) for file_path in test_files]
        all_contents = [content for _, content in file_content_pairs]

        # 初始化全局编号
        global_start_number = find_next_global_testcase_number(all_contents)
        print(f"  📌 起始编号: T{global_start_number:08d}")

        global_next_number = [global_start_number]
        all_existing_numbers = get_all_testcase_numbers(all_contents)
        used_numbers = set(all_existing_numbers)
        print(f"  📊 已存在编号: {len(used_numbers)} 个")

        total_processed = 0
        files_need_processing = 0

        for file_path, content in file_content_pairs:
            methods_without_numbers = find_test_methods_without_numbers(content)
            has_duplicates = check_duplicate_numbers(content, file_path.name)

            if methods_without_numbers or has_duplicates:
                files_need_processing += 1
                _, processed_count = process_single_file(
                    file_path, global_next_number, used_numbers.copy()
                )
                total_processed += processed_count

        final_number = global_next_number[0] - 1 if global_next_number[0] > global_start_number else global_start_number - 1
        print(f"  ✅ 处理完成: {total_processed} 个用例, {files_need_processing} 个文件")
        if total_processed > 0:
            print(f"  🏷️  最后编号: T{final_number:08d}")
        return total_processed


def check_all_duplicates(testcase_dir):
    """检查所有文件中的重复编号"""
    testcase_path = Path(testcase_dir)
    if not testcase_path.exists():
        print(f"❌ 错误: 目录不存在 - {testcase_dir}")
        return

    test_files = list(testcase_path.glob('test*.py'))

    all_numbers = {}
    duplicate_numbers = set()

    for file_path in test_files:
        content = file_path.read_text(encoding='utf-8')
        matches = re.findall(r'T\d{8}', content)

        for match in matches:
            if match in all_numbers:
                all_numbers[match].append(file_path.name)
                duplicate_numbers.add(match)
            else:
                all_numbers[match] = [file_path.name]

    if duplicate_numbers:
        print(f"  ⚠️  重复编号: {len(duplicate_numbers)} 个", end="")
        for num in sorted(list(duplicate_numbers)[:3]):  # 只显示前3个
            files = all_numbers[num]
            print(f" | {num}: {len(files)}个文件", end="")
        if len(duplicate_numbers) > 3:
            print(f" ... 还有 {len(duplicate_numbers)-3} 个", end="")
        print()
        return True
    else:
        print(f"  ✓ 无重复编号 ({len(test_files)} 个文件)")
        return False


def main():
    """主函数，执行用例编号清除或添加"""
    testcase_dirs = [
        r'D:\webseleniumerp\testcase',
        # 可以添加更多目录
    ]

    mode_str = "清除所有编号" if CLEAR_ALL_TESTCASE_NUMBERS else "添加缺失编号"
    print(f"⚙️  配置模式: {mode_str}")
    print("-" * 60)

    # 检查所有目录的重复编号
    print("🔍 检查重复编号:")
    for testcase_dir in testcase_dirs:
        check_all_duplicates(testcase_dir)

    # 处理所有目录
    print("\n🔄 开始处理:")
    total_processed = 0
    for i, testcase_dir in enumerate(testcase_dirs, 1):
        print(f"\n{i}. 处理目录:")
        processed = process_all_test_files(testcase_dir, clear_only=CLEAR_ALL_TESTCASE_NUMBERS)
        total_processed += processed

    if not CLEAR_ALL_TESTCASE_NUMBERS:
        print(f"\n✅ 主处理完成 (共处理 {total_processed} 个用例)")
        print("-" * 60)
        print("🔍 处理后再次检查重复编号:")
        for testcase_dir in testcase_dirs:
            check_all_duplicates(testcase_dir)

    print(f"\n🎉 所有测试用例编号处理完成！(总计: {total_processed} 个用例)")


if __name__ == "__main__":
    main()
