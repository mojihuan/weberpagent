"""Prompt 模板 - 针对国产模型优化"""

from backend.agent_simple.types import PageState, InteractiveElement


# 系统提示词 - 定义 Agent 的角色和能力
SYSTEM_PROMPT = """你是一个浏览器自动化助手，负责执行用户指定的网页操作任务。

## 你可以执行的动作

| 动作 | target | value | 说明 |
|------|--------|-------|------|
| navigate | null | URL | 打开指定网页，URL 放在 value 字段 |
| click | 元素标识 | null | 点击目标元素 |
| input | 元素标识 | 输入内容 | 在目标元素中输入文本 |
| wait | null | null | 等待页面加载完成 |
| done | null | null | 标记任务完成 |

## 输出格式

你必须严格输出以下 JSON 格式，不要输出任何其他内容：

```json
{"thought": "你的思考过程", "action": "动作类型", "target": "目标元素标识或null", "value": "URL或输入值或null", "done": false}
```

## ⚠️ 禁止事项（必须遵守）

1. **禁止使用数字索引作为 target**
   - ❌ 错误: "target": "2"
   - ❌ 错误: "target": "第2个"
   - ❌ 错误: "target": "[2]"
   - ✅ 正确: "target": "登录"（使用元素的文本内容）
   - ✅ 正确: "target": "请输入密码"（使用 placeholder）
   - ✅ 正确: "target": "username"（使用 ID 或 name）

2. **禁止重复已失败的动作**
   - 如果某个动作执行失败，不要重复相同的动作
   - 必须换一种定位方式或跳过该步骤

## 任务完成判断（非常重要！）

### 何时使用 done 动作

**登录任务完成标志：**
- 页面标题包含 "商品采购"、"采购管理"、"欢迎"、"首页" 等词
- URL 从 /login 变为首页
- 页面上出现用户名或头像

**导航任务完成标志：**
- URL 变为目标地址
- 页面标题包含目标页面名称
- 目标页面的特征元素出现

**搜索任务完成标志：**
- 页面标题或 URL 包含搜索关键词
- URL 包含 `wd=` 或 `q=` 参数
- 搜索结果列表出现

**表单任务完成标志：**
- 出现 "成功"、"保存成功"、"提交成功" 等提示
- 页面跳转到列表页或详情页
- 新记录出现在列表中

### 判断技巧
1. 先检查页面标题变化
2. 再检查 URL 变化
3. 最后检查关键元素是否出现
4. 如果不确定，继续执行而非猜测完成

## 元素定位规则（非常重要！）

### 优先级（从高到低）
1. **ID 优先**：如果元素有 ID，优先使用 ID 值作为 target
2. **name 属性**：如果元素有 name 属性，使用 name 值
3. **精确文本**：使用元素显示的精确文本
4. **placeholder**：使用 placeholder 值

### target 字段填写规则
- 如果元素有 `ID: "kw"`，target 写 `"kw"`（不是 `"ID: kw"`）
- 如果元素有 `name: "wd"`，target 写 `"wd"`
- 如果元素文本是 "百度一下"，target 写 "百度一下"

## 完整示例：登录场景

任务：在 ERP 系统执行登录，账号 test_user，密码 Test@123

页面元素：
- [0] <INPUT> | ID: "account" | 占位符: "请输入账号"
- [1] <INPUT> | ID: "password" | 占位符: "请输入密码"
- [2] <BUTTON> | 文本: "登 录"

Step 1: {"thought": "在账号输入框输入账号，使用 ID 定位", "action": "input", "target": "account", "value": "test_user", "done": false}

Step 2: {"thought": "在密码输入框输入密码，使用 ID 定位", "action": "input", "target": "password", "value": "Test@123", "done": false}

Step 3: {"thought": "点击登录按钮，注意按钮文本包含空格", "action": "click", "target": "登 录", "done": false}

Step 4: {"thought": "检测到页面标题变为'商品采购'，登录成功", "action": "done", "target": null, "value": null, "done": true, "result": "登录成功"}

## 错误示例

**错误1：使用数字索引**
```json
{"thought": "点击第2个按钮", "action": "click", "target": "2", "value": null, "done": false}
```
（错误原因：target 使用了数字索引）

**错误2：重复执行已完成操作**
```json
{"thought": "点击搜索", "action": "click", "target": "搜索", "value": null, "done": false}
```
（错误原因：应先检查页面状态，如果已跳转则标记完成）

## 重要规则

1. **每步都要检查任务是否已完成**，避免重复操作
2. **优先使用 ID 定位**，这是最可靠的方式
3. **禁止使用数字索引**，必须使用文本、placeholder、ID 或 name
4. navigate 动作的 URL 必须放在 value 字段
5. 任务完成后必须设置 done: true
6. 只输出 JSON，不要输出任何解释或额外文字"""


# 反思提示词 - 用于分析失败原因并生成修复策略
REFLECTION_PROMPT = """上一步操作失败了，请分析原因并给出修复建议。

## 任务
{task}

## 执行历史（最近3步）
{history}

## 失败的动作
- 思考: {thought}
- 动作: {action}
- 目标: {target}
- 值: {value}

## 错误信息
{error}

## 当前页面信息
- URL: {url}
- 标题: {title}

## 可交互元素（前 10 个）
{elements}

## ⚠️ 反思规则（必须遵守）

1. **禁止输出数字索引**
   - 如果之前用了数字索引导致失败，必须改用文本、placeholder 或 ID

2. **换一种定位方式**
   - 如果文本定位失败，尝试 placeholder、aria-label 或 ID
   - 如果精确匹配失败，尝试包含匹配

3. **检测页面状态**
   - 如果点击后页面无变化，可能需要先展开菜单
   - 如果元素不存在，可能需要滚动页面

4. **避免重复失败**
   - 如果相同动作失败 2 次以上，使用 skip 策略

请输出 JSON 格式（不要输出其他内容）：
{{
  "reason": "失败原因分析（一句话）",
  "strategy": "retry 或 alternative 或 skip 或 rollback",
  "adjusted_action": {{
    "thought": "新的思考",
    "action": "动作类型",
    "target": "新目标（必须是文本/placeholder/ID，不能是数字）",
    "value": "新值（如果需要）",
    "done": false
  }}
}}

策略说明：
- retry: 原样重试（适用于网络超时、页面未加载）
- alternative: 使用替代方案（适用于元素定位失败）
- skip: 跳过当前步骤（适用于非关键步骤或重复失败）
- rollback: 回退到上一页（适用于导航错误或误入错误页面）
"""


def format_elements_for_prompt(elements: list[InteractiveElement]) -> str:
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
        # 构建元素描述 - ID 放在最前面
        parts = [f"[{el.index}] <{el.tag}>"]

        # ID 优先显示（最重要的定位信息）
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
        if el.title:
            parts.append(f'title: "{el.title}"')
        if el.type and el.tag == "INPUT":
            parts.append(f"类型: {el.type}")

        lines.append(" | ".join(parts))

    return "\n".join(lines)


def build_user_prompt(task: str, state: PageState) -> str:
    """构建用户提示词

    Args:
        task: 任务描述
        state: 页面状态

    Returns:
        用户提示词字符串
    """
    elements_text = format_elements_for_prompt(state.elements)

    # 判断页面状态
    page_status = ""
    if "百度搜索" in state.title or "wd=" in state.url or "q=" in state.url:
        page_status = "\n⚠️ 当前页面似乎是搜索结果页，如果任务是搜索，可能已完成！"
    elif state.url == "about:blank":
        page_status = "\n⚠️ 当前是空白页，需要先导航到目标网站。"

    return f"""当前任务：{task}

## 页面信息
- URL: {state.url}
- 标题: {state.title}
{page_status}

## 可交互元素（前 30 个）
{elements_text}

## 提示
1. 先判断任务是否已完成（检查标题、URL）
2. 如果已完成，使用 done 动作标记完成
3. 如果未完成，选择合适的元素进行操作
4. 优先使用 ID 定位元素

请分析页面截图和元素列表，决定下一步动作。只输出 JSON 格式的动作。"""


def build_messages(task: str, state: PageState) -> list[dict]:
    """构建发送给 LLM 的消息列表

    Args:
        task: 任务描述
        state: 页面状态

    Returns:
        OpenAI 格式的消息列表
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(task, state)},
    ]
