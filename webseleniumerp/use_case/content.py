# content.py
import json
import re

# 读取 content.txt 文件
file_path = r'/common/functional_use_cases/content.txt'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 存储所有用例
test_cases = []

for line in lines:
    line = line.strip()

    # 跳过空行
    if not line:
        continue

    # 按 Tab 分割字段
    parts = line.split('\t')

    # 确保有三个部分
    if len(parts) != 3:
        print(f"❌ 无法解析行: {line}")
        continue

    # 提取各部分信息
    module_part = parts[0].strip()
    steps_part = parts[1].strip()
    result_part = parts[2].strip()

    # 解析测试模块（去除序号）
    module_match = re.match(r'^\d+\.\s+测试模块：(.+)$', module_part)
    if not module_match:
        print(f"❌ 无法解析测试模块: {module_part}")
        continue

    test_module = module_match.group(1).strip()

    # 解析测试步骤（去除"测试步骤："前缀）
    steps_match = re.match(r'^测试步骤：(.+)$', steps_part)
    if not steps_match:
        print(f"❌ 无法解析测试步骤: {steps_part}")
        continue

    test_steps = steps_match.group(1).strip()

    # 解析预期结果（去除"预期结果："前缀）
    result_match = re.match(r'^预期结果：(.+)$', result_part)
    if not result_match:
        print(f"❌ 无法解析预期结果: {result_part}")
        continue

    expected_result = result_match.group(1).strip()

    # 构造用例对象
    new_case = {
        "序号": "",
        "功能模块*": "客服系统",
        "用例名称*": test_module,
        "用例编号": "",
        "维护人": "mojihuan",
        "用例类型": "功能测试",
        "优先级": "P1",
        "前置条件": "",
        "备注": "",
        "步骤描述": test_steps,
        "预期结果": expected_result,
        "评审结论": "待评审"
    }

    test_cases.append(new_case)

# 写入 export.json
output_file = r'/common/functional_use_cases/export.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(test_cases, f, ensure_ascii=False, indent=2)

print("✅ 已成功将 content.txt 文件转换为 export.json！")
print(f"总共处理了 {len(test_cases)} 条测试用例")
