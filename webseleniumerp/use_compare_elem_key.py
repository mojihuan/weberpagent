import os
import re
import ast

"""元素定位排查 pages 页面是否有被使用，并自动清理未使用的 key"""


# 步骤一：从 element_positioning.py 提取所有层级下的所有 key
def extract_all_keys_from_py(file_path):
    all_keys = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 使用 AST 解析 Python 文件中的字典
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            var_name = target.id
                            if isinstance(node.value, ast.Dict):
                                # 提取字典中的 key
                                keys = {ast.literal_eval(key) for key in node.value.keys}
                                all_keys[var_name] = keys
        return all_keys
    except Exception as e:
        print(f"读取 Python 文件出错: {e}")
        return all_keys


# 步骤二：扫描 pages/* 下的 .py 文件，查找使用的 key
def find_used_keys_in_pages(pages_dir, all_sub_keys):
    used_keys = set()
    for root, _, files in os.walk(pages_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for key in all_sub_keys:
                            # 匹配单词边界，避免部分匹配
                            if re.search(r"\b" + re.escape(key) + r"\b", content):
                                used_keys.add(key)
                except Exception as e:
                    print(f"读取文件 {file_path} 出错: {e}")
    return used_keys


# 步骤三：删除未使用的 key-value 行（优化版）
def remove_unused_keys_from_file(file_path, unused_keys):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # 构建新的文件内容
        new_lines = []
        for line in lines:
            stripped_line = line.strip()
            # 跳过注释和空行
            if stripped_line.startswith("#") or not stripped_line:
                new_lines.append(line)
                continue

            # 匹配 key: value 格式的行（支持多种格式）
            match = re.match(r'^\s*"([^"]+)"\s*:\s*(.*?),?\s*$', line)
            if match:
                key = match.group(1)
                if key not in unused_keys:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        print(f"✅ 已成功删除未使用的 key，共删除 {len(unused_keys)} 项。")
    except Exception as e:
        print(f"❌ 删除未使用的 key 失败: {e}")


# 主程序逻辑
if __name__ == "__main__":
    elem_file = "common/element_positioning.py"
    pages_dir = "D:/webseleniumerp/pages"

    # 提取所有顶层 key 及其子 key
    all_keys_dict = extract_all_keys_from_py(elem_file)

    # 合并所有子 key 用于检查使用情况
    all_sub_keys = set()
    for sub_keys in all_keys_dict.values():
        all_sub_keys.update(sub_keys)

    used_keys = find_used_keys_in_pages(pages_dir, all_sub_keys)

    print("✅ 顶层 key 数量:", len(all_keys_dict))
    print("✅ 所有子 key 数量:", len(all_sub_keys))
    print("🔍 被使用的子 key 数量:", len(used_keys))

    total_unused = 0
    has_unused = False
    unused_keys_list = []

    print("\n📌 各顶层 key 下的未使用子 key:")
    for top_key, sub_keys in all_keys_dict.items():
        unused_sub_keys = sub_keys - used_keys
        total_unused += len(unused_sub_keys)

        if unused_sub_keys:
            has_unused = True
            print(f"\n📁 {top_key} (未使用: {len(unused_sub_keys)}/{len(sub_keys)}):")
            for key in sorted(unused_sub_keys):
                print(f"   - {key}")
                unused_keys_list.append(key)
        else:
            print(f"\n✅ {top_key} (全部已使用: {len(sub_keys)}/{len(sub_keys)})")

    if not has_unused:
        print("\n🎉 所有子 key 都已被使用，无需清理。")
    else:
        # 自动删除未使用的 key
        remove_unused_keys_from_file(elem_file, unused_keys_list)
