"""子 Agent Prompt 模板 - CodeGenerator、CodeReviewer、CodeOptimizer"""

import random
import string
from datetime import datetime, timedelta

from backend.agent_simple.types import InteractiveElement


# ============================================================
# 字段数据生成规则
# ============================================================

FIELD_GENERATION_RULES = """## 字段数据生成规则

### 1. 手机号（phone/mobile/tel）
- 格式：138 开头，共 11 位数字
- 示例：13812345678, 13887654321
- 生成方式：`138` + 8 位随机数字

### 2. 邮箱（email/mail）
- 格式：test_{random}@example.com
- 示例：test_a7x9k@example.com, test_user123@example.com
- 生成方式：`test_` + 6 位随机字母数字 + `@example.com`

### 3. 姓名（name/username/realname）
- 中文姓名：随机中文姓名
- 示例：张三, 李明, 王芳
- 常见姓氏：王李张刘陈杨赵黄周吴
- 常见名字：明华强芳敏静伟丽刚平建军

### 4. 日期（date/birthday/createdate）
- 日期范围：今天或未来 30 天内
- 格式：YYYY-MM-DD 或根据页面要求
- 示例：2024-01-15, 2024-02-20

### 5. 金额（amount/price/money）
- 范围：10.00 - 10000.00
- 格式：保留两位小数
- 示例：128.50, 999.00, 5000.00

### 6. 地址（address/location）
- 格式：省市区 + 详细地址
- 示例：北京市朝阳区建国路88号院5号楼
- 常见城市：北京、上海、广州、深圳、杭州

### 7. 身份证号（idcard/id_number）
- 格式：18 位数字，最后一位可能是 X
- 示例：110101199001011234
- 注意：生成合法格式的测试身份证号

### 8. 数量（quantity/num/count）
- 范围：1 - 100
- 示例：5, 10, 50

### 9. 验证码（code/captcha/verifycode）
- 格式：4-6 位数字或字母
- 示例：1234, AB5678

### 10. 通用文本
- 无特定规则时，根据字段名语义生成合理值
- 例如：description -> "测试描述内容", remark -> "备注信息"

### 混合生成策略
- 优先级：字段规则 > 字段名语义 > 随机值
- 对于未知字段，根据 placeholder 提示生成
- 保持数据一致性（如：省市匹配）
"""


def _generate_random_suffix(length: int = 6) -> str:
    """生成随机后缀"""
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=length))


def _format_elements(elements: list[InteractiveElement]) -> str:
    """格式化元素列表用于 Prompt

    Args:
        elements: 可交互元素列表

    Returns:
        格式化后的字符串
    """
    if not elements:
        return "（页面上没有可交互元素）"

    lines = []
    for el in elements:
        parts = [f"[{el.index}] <{el.tag}>"]

        if el.id:
            parts.append(f'ID: "{el.id}"')
        if el.name:
            parts.append(f'name: "{el.name}"')
        if el.text:
            parts.append(f'文本: "{el.text}"')
        if el.placeholder:
            parts.append(f'占位符: "{el.placeholder}"')
        if el.aria_label:
            parts.append(f'aria-label: "{el.aria_label}"')
        if el.type and el.tag == "INPUT":
            parts.append(f"类型: {el.type}")

        lines.append(" | ".join(parts))

    return "\n".join(lines)


# ============================================================
# 代码生成 Prompt
# ============================================================

CODE_GENERATOR_SYSTEM = """你是一个 Playwright 代码生成专家，负责根据任务描述生成表单填写的 Playwright 代码。

## 输出要求

你必须输出一个 JSON 对象，格式如下：
```json
{
  "code": "async def fill_form(page) -> None:\\n    ...",
  "description": "代码功能描述",
  "field_values": {
    "字段名": "生成的值",
    ...
  }
}
```

## 代码规范

1. 函数签名必须是 `async def fill_form(page) -> None:`
2. 使用 Playwright async API
3. 使用 try-except 处理可能的错误
4. 添加适当的等待（page.wait_for_*）
5. 添加注释说明关键步骤

## 选择器优先级

1. ID 选择器：`page.locator('#id')`
2. name 属性：`page.locator('[name="xxx"]')`
3. placeholder：`page.locator('[placeholder="xxx"]')`
4. 文本：`page.get_by_text('xxx')`
5. 组合选择器：`page.locator('tag[attr="value"]')`

## 常用操作示例

### 文本输入框
```python
await page.locator('#username').fill('test_user')
await page.locator('[name="password"]').fill('Test@123')
```

### ⚠️ 下拉选择框（重要！）
下拉框不能用 `.fill()` 方法！必须使用点击选项或 select_option。

#### 方式1：点击打开下拉 + 点击选项（适用于自定义下拉框）
```python
# 步骤1：点击打开下拉框
await page.locator('[placeholder="请选择供应商"]').click()
# 步骤2：等待下拉选项出现
await page.wait_for_timeout(500)
# 步骤3：点击目标选项
await page.get_by_text('供应商A', exact=True).click()
```

#### 方式2：使用 select_option（适用于原生 <select> 元素）
```python
await page.locator('select#type').select_option('value1')
await page.locator('select[name="status"]').select_option(label='启用')
```

#### 方式3：带搜索功能的下拉框
```python
# 点击打开下拉框
await page.locator('.el-select').click()
# 在搜索框中输入关键字
await page.locator('.el-input__inner').fill('关键字')
# 等待过滤结果
await page.wait_for_timeout(300)
# 点击匹配的选项
await page.get_by_text('目标选项').click()
```

### 点击操作
```python
await page.get_by_text('提交').click()
await page.locator('#submit-btn').click()
```

### 等待操作
```python
await page.wait_for_load_state('networkidle')
await page.wait_for_selector('.success-message')
```

### 复选框/单选框
```python
await page.locator('#agree').check()
await page.locator('#gender-male').check()
```

## ❌ 常见错误

### 错误：对下拉框使用 fill()
```python
# ❌ 错误：下拉框不支持 fill()
await page.locator('[placeholder="请选择"]').fill('选项值')

# ✅ 正确：先点击打开下拉，再点击选项
await page.locator('[placeholder="请选择"]').click()
await page.get_by_text('选项值').click()
```
"""


def build_code_generator_prompt(
    task: str,
    elements: list[InteractiveElement],
    page_url: str,
) -> list[dict]:
    """构建代码生成 Prompt

    Args:
        task: 任务描述
        elements: 可交互元素列表
        page_url: 当前页面 URL

    Returns:
        OpenAI 格式的消息列表
    """
    elements_text = _format_elements(elements)

    user_prompt = f"""## 任务

{task}

## 页面信息

- URL: {page_url}
- 元素总数: {len(elements)}

## 可交互元素

{elements_text}

{FIELD_GENERATION_RULES}

## 要求

1. 根据任务描述，识别需要填写的表单字段
2. 按照字段生成规则，生成合理的测试数据
3. 生成完整的 `async def fill_form(page)` 函数
4. 处理各种表单控件（输入框、下拉选择、日期选择器等）
5. 添加适当的错误处理和等待

请输出 JSON 格式的结果，不要输出其他内容。"""

    return [
        {"role": "system", "content": CODE_GENERATOR_SYSTEM},
        {"role": "user", "content": user_prompt},
    ]


# ============================================================
# 代码审查 Prompt
# ============================================================

CODE_REVIEWER_SYSTEM = """你是一个 Playwright 代码审查专家，负责检查生成的代码质量和安全性。

## 审查维度

### 1. 安全性检查
- 无硬编码敏感信息（密码、API Key）
- 无 SQL 注入风险
- 无 XSS 漏洞

### 2. 选择器有效性
- 选择器是否稳定可靠
- 是否有更好的选择器替代方案
- 是否存在选择器冲突

### 3. 逻辑完整性
- 是否处理了所有必要字段
- 是否有适当的等待逻辑
- 是否有错误处理

### 4. API 正确性
- Playwright API 使用是否正确
- 异步操作是否正确使用 await
- 参数传递是否正确

## 输出格式

你必须输出一个 JSON 对象：
```json
{
  "approved": true/false,
  "issues": [
    {
      "severity": "CRITICAL/HIGH/MEDIUM/LOW",
      "line": 10,
      "message": "问题描述"
    }
  ],
  "suggestions": [
    "改进建议1",
    "改进建议2"
  ]
}
```

## 严重级别定义

| 级别 | 说明 | 示例 |
|------|------|------|
| CRITICAL | 必须修复，否则无法运行 | 语法错误、API 误用 |
| HIGH | 强烈建议修复 | 选择器不稳定、缺少错误处理 |
| MEDIUM | 建议修复 | 代码风格、缺少注释 |
| LOW | 可选优化 | 性能优化、代码简化 |

## 审查标准

- CRITICAL/HIGH 问题存在时，approved = false
- 仅 MEDIUM/LOW 问题存在时，approved = true（附带建议）
"""


def build_code_reviewer_prompt(
    code: str,
    elements: list[InteractiveElement],
) -> list[dict]:
    """构建代码审查 Prompt

    Args:
        code: 待审查的代码
        elements: 页面可交互元素列表

    Returns:
        OpenAI 格式的消息列表
    """
    elements_text = _format_elements(elements)

    user_prompt = f"""## 待审查代码

```python
{code}
```

## 页面元素参考

{elements_text}

## 审查要求

1. 检查代码是否使用了正确的选择器（优先使用 ID）
2. 检查是否正确处理了各种表单控件
3. 检查是否有适当的等待和错误处理
4. 检查 API 使用是否正确
5. 提出改进建议

请输出 JSON 格式的审查结果，不要输出其他内容。"""

    return [
        {"role": "system", "content": CODE_REVIEWER_SYSTEM},
        {"role": "user", "content": user_prompt},
    ]


# ============================================================
# 代码优化 Prompt
# ============================================================

CODE_OPTIMIZER_SYSTEM = """你是一个 Playwright 代码优化专家，负责根据审查意见或执行错误优化代码。

## 优化原则

### 1. 选择器优化
- 优先使用 ID 选择器
- 避免使用脆弱的 CSS 选择器
- 使用 Playwright 推荐的定位方法

### 2. 稳定性优化
- 添加适当的等待机制
- 使用 try-except 处理异常
- 添加重试逻辑

### 3. 可读性优化
- 添加清晰的注释
- 合理的代码结构
- 有意义的变量名

### 4. 错误修复
- 根据执行错误信息定位问题
- 修复语法错误
- 修复 API 使用错误

## 输出格式

你必须输出一个 JSON 对象：
```json
{
  "code": "优化后的完整代码",
  "description": "优化说明",
  "changes": [
    "修改1：xxx",
    "修改2：xxx"
  ]
}
```
"""


def build_code_optimizer_prompt(
    code: str,
    issues: list[dict] | None,
    elements: list[InteractiveElement],
    execution_error: str | None = None,
) -> list[dict]:
    """构建代码优化 Prompt

    Args:
        code: 原始代码
        issues: 审查问题列表
        elements: 页面可交互元素列表
        execution_error: 执行错误信息（可选）

    Returns:
        OpenAI 格式的消息列表
    """
    elements_text = _format_elements(elements)

    # 格式化问题列表
    issues_text = ""
    if issues:
        issues_text = "## 审查问题\n\n"
        for issue in issues:
            severity = issue.get("severity", "MEDIUM")
            line = issue.get("line", "?")
            message = issue.get("message", "")
            issues_text += f"- [{severity}] 行 {line}: {message}\n"

    # 执行错误信息
    error_text = ""
    if execution_error:
        error_text = f"""## 执行错误

```
{execution_error}
```

请根据错误信息修复代码问题。
"""

    user_prompt = f"""## 原始代码

```python
{code}
```

## 页面元素参考

{elements_text}

{issues_text}
{error_text}
## 优化要求

1. 解决所有 CRITICAL 和 HIGH 级别的问题
2. 修复执行错误（如果有）
3. 优化选择器以提高稳定性
4. 保持代码功能不变
5. 输出完整的优化后代码

请输出 JSON 格式的优化结果，不要输出其他内容。"""

    return [
        {"role": "system", "content": CODE_OPTIMIZER_SYSTEM},
        {"role": "user", "content": user_prompt},
    ]


# ============================================================
# 辅助函数
# ============================================================

def generate_field_value(field_name: str, field_type: str | None = None) -> str:
    """根据字段名生成测试数据

    Args:
        field_name: 字段名称
        field_type: 字段类型（可选）

    Returns:
        生成的测试数据
    """
    field_lower = field_name.lower()

    # 手机号
    if any(kw in field_lower for kw in ["phone", "mobile", "tel", "手机"]):
        return f"138{random.randint(10000000, 99999999)}"

    # 邮箱
    if any(kw in field_lower for kw in ["email", "mail", "邮箱"]):
        return f"test_{_generate_random_suffix()}@example.com"

    # 姓名
    if any(kw in field_lower for kw in ["name", "username", "姓名", "真实姓名"]):
        surnames = "王李张刘陈杨赵黄周吴"
        names = "明华强芳敏静伟丽刚平建军国"
        return random.choice(surnames) + random.choice(names)

    # 日期
    if any(kw in field_lower for kw in ["date", "日期", "birthday", "出生"]):
        future_date = datetime.now() + timedelta(days=random.randint(0, 30))
        return future_date.strftime("%Y-%m-%d")

    # 金额
    if any(kw in field_lower for kw in ["amount", "price", "money", "金额", "价格"]):
        return f"{random.uniform(10, 10000):.2f}"

    # 地址
    if any(kw in field_lower for kw in ["address", "地址", "location"]):
        cities = [
            ("北京市", "朝阳区", "建国路88号院"),
            ("上海市", "浦东新区", "陆家嘴金融中心"),
            ("广州市", "天河区", "体育西路103号"),
            ("深圳市", "南山区", "科技园南路"),
        ]
        city = random.choice(cities)
        return f"{city[0]}{city[1]}{city[2]}{random.randint(1, 100)}号"

    # 数量
    if any(kw in field_lower for kw in ["quantity", "num", "count", "数量"]):
        return str(random.randint(1, 100))

    # 身份证
    if any(kw in field_lower for kw in ["idcard", "id_number", "身份证"]):
        return f"110101{random.randint(19900101, 20051231)}{random.randint(100, 999)}"

    # 默认：生成随机字符串
    return f"test_{_generate_random_suffix(4)}"