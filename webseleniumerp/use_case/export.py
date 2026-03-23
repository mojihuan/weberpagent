# export.py
import json
from openpyxl import load_workbook

# ==============================
# 1. 从 JSON 文件加载测试用例数据
# ==============================
def load_test_cases():
    """从 export.json 加载测试用例"""
    try:
        with open('export.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ 找不到 export.json 文件，请确保文件存在")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON 格式错误: {e}")
        return []

# ==============================
# 2. 读取现有Excel文件，并追加数据
# ==============================
file_path = r'D:\yongli.xlsx'
workbook = load_workbook(file_path)
sheet = workbook.active

# 获取表头（第一行）用于对齐列
headers = [cell.value for cell in sheet[1]]

# 找出各字段对应的列索引
col_map = {}
for idx, header in enumerate(headers):
    col_map[header] = idx + 1

# ==============================
# 3. 写入新用例数据
# ==============================
test_cases = load_test_cases()
for case in test_cases:
    row_data = []
    for header in headers:
        value = case.get(header, "")
        row_data.append(value)
    sheet.append(row_data)

# ==============================
# 4. 保存文件
# ==============================
try:
    workbook.save(file_path)
    print("✅ 测试用例已成功插入 Excel 文件！")
except PermissionError:
    print("❌ 文件被占用，请关闭 WPS/Excel 后重试！")
except Exception as e:
    print(f"❌ 保存失败：{e}")
