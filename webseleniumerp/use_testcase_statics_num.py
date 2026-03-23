# -*- coding: utf-8 -*-

import os
import re


TESTCASE_DIR = os.path.abspath(os.path.join(os.getcwd(), 'testcase'))
print('--dir;', TESTCASE_DIR)


def get_test_files():
    """获取 testcase 目录下的所有测试文件
    Returns: list: 测试文件列表（排除以__开头的文件）
    """
    if not os.path.exists(TESTCASE_DIR):
        return []
    return [item for item in os.listdir(TESTCASE_DIR)
            if item.endswith('.py') and not item.startswith('__') and os.path.isfile(os.path.join(TESTCASE_DIR, item))]


def process_test_files():
    """处理测试文件，提取装饰器统计用例编号
    """
    api_num = 0
    ui_num = 0
    all_num = 0

    test_files = get_test_files()

    for file_item in test_files:
        file_item_path = os.path.join(TESTCASE_DIR, file_item)
        try:
            with open(file_item_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # 使用正则表达式查找所有 @BaseCase.auto 装饰器
                pattern = r"@BaseCase\.auto\(['\"](.*?)['\"]\)"
                matches = re.findall(pattern, content)

                for type_str in matches:
                    if type_str == 'api':
                        api_num += 1
                    elif type_str == 'ui':
                        ui_num += 1
                    else:
                        all_num += 1

        except Exception as e:
            print(f"处理文件 {file_item_path} 时出错: {e}")

    # 使用格式化字符串避免类型转换问题
    print(f'api数量:{api_num}, ui数量:{ui_num}, all数量:{all_num}')
    total = api_num + ui_num + all_num * 2
    print(f'累计总数: {total}')
    return api_num, ui_num, all_num


def main():
    test_files = get_test_files()
    print('---test files:', test_files)
    process_test_files()


# 主程序入口
if __name__ == "__main__":
    main()
