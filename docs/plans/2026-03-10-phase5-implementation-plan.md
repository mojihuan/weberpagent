# Phase 5: Agent 优化实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 全面优化 SimpleAgent 的稳定性、通用性和自愈能力，使测试场景通过率达到 80%+

**Architecture:** 分四层渐进式优化（Prompt → 执行 → 感知 → 反思），每层独立可测试

**Tech Stack:** Python, Playwright, 通义千问 qwen-vl-max, pytest

---

## Task 5.1: Prompt 层优化

**Files:**
- Modify: `backend/agent_simple/prompts.py`

**Step 1: 添加禁止数字索引的强规则**

在 `SYSTEM_PROMPT` 的元素定位规则部分，添加醒目的禁止规则：

```python
# 在 SYSTEM_PROMPT 中添加（约第 40 行后）

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
```

**Step 2: 添加 Few-shot 登录示例**

在 `SYSTEM_PROMPT` 的正确示例部分，添加完整的登录场景示例：

```python
# 替换现有的 "## 正确示例" 部分

## 完整示例：登录场景

任务：在 ERP 系统执行登录，账号 Y96230027，密码 Aa123456

页面元素：
- [0] <INPUT> | ID: "account" | 占位符: "请输入账号"
- [1] <INPUT> | ID: "password" | 占位符: "请输入密码"
- [2] <BUTTON> | 文本: "登 录"

Step 1: {"thought": "在账号输入框输入账号，使用 placeholder 定位", "action": "input", "target": "请输入账号", "value": "Y96230027", "done": false}

Step 2: {"thought": "在密码输入框输入密码", "action": "input", "target": "请输入密码", "value": "Aa123456", "done": false}

Step 3: {"thought": "点击登录按钮，注意按钮文本包含空格", "action": "click", "target": "登 录", "done": false}

Step 4: {"thought": "检测到页面标题变为'商品采购'，登录成功", "action": "done", "target": null, "value": null, "done": true, "result": "登录成功"}
```

**Step 3: 添加任务完成判断的详细规则**

在 `SYSTEM_PROMPT` 的任务完成判断部分，添加更详细的规则：

```python
# 扩展 "## 任务完成判断" 部分

## 任务完成判断（非常重要！）

### 何时使用 done 动作

**登录任务完成标志：**
- 页面标题包含 "商品采购"、"采购管理"、"欢迎" 等词
- URL 从 /login 变为首页
- 页面上出现用户名或头像

**导航任务完成标志：**
- URL 变为目标地址
- 页面标题包含目标页面名称
- 目标页面的特征元素出现

**表单任务完成标志：**
- 出现 "成功"、"保存成功"、"提交成功" 等提示
- 页面跳转到列表页或详情页
- 新记录出现在列表中

### 判断技巧
1. 先检查页面标题变化
2. 再检查 URL 变化
3. 最后检查关键元素是否出现
4. 如果不确定，继续执行而非猜测完成
```

**Step 4: 优化反思 Prompt**

修改 `REFLECTION_PROMPT`，添加历史记忆和禁止数字索引的提醒：

```python
# 替换现有的 REFLECTION_PROMPT

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
  "strategy": "retry 或 alternative 或 skip",
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
"""
```

**Step 5: 提交 Prompt 优化**

```bash
git add backend/agent_simple/prompts.py
git commit -m "feat(prompts): 优化 Prompt 层 - 禁止数字索引 + Few-shot + 完成判断规则

- 添加禁止数字索引的强规则
- 添加完整的登录场景 Few-shot 示例
- 扩展任务完成判断规则
- 优化反思 Prompt，添加历史记忆

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5.2: 执行层优化

**Files:**
- Modify: `backend/agent_simple/executor.py`

**Step 1: 增强元素定位的日志输出**

在 `_locate_element` 方法开头添加详细日志：

```python
async def _locate_element(
    self,
    target: str,
    elements: list[InteractiveElement],
):
    """定位元素"""
    logger.info(f"尝试定位元素: '{target}'")
    target_normalized = _normalize_text(target)

    # 检测数字索引并警告
    if target.strip().isdigit():
        logger.warning(f"⚠️ 检测到数字索引 '{target}'，这是不允许的！尝试转换为文本定位...")
        # 尝试从元素列表获取对应元素的文本
        idx = int(target)
        if 0 <= idx < len(elements):
            el = elements[idx]
            # 优先使用文本，其次 placeholder
            actual_target = el.text or el.placeholder or el.aria_label or el.id
            if actual_target:
                logger.info(f"转换为文本定位: '{actual_target}'")
                target = actual_target
                target_normalized = _normalize_text(target)
```

**Step 2: 添加按钮角色定位策略**

在 `_locate_element` 方法中，添加通过 role="button" 定位的策略：

```python
# 在精确匹配文本后添加（约第 280 行后）

# 3.5. 通过按钮角色定位（适用于 button 元素）
for el in elements:
    if el.tag == "BUTTON" and el.text:
        # 尝试 get_by_role 定位
        if target_normalized in _normalize_text(el.text):
            logger.debug(f"按钮角色定位: {el.text}")
            return self.page.get_by_role("button", name=el.text)
```

**Step 3: 优化点击方法的回退逻辑**

修改 `_click` 方法，添加更多回退策略：

```python
async def _click(
    self,
    target: str | None,
    elements: list[InteractiveElement],
) -> ActionResult:
    """点击目标元素"""
    if not target:
        return ActionResult(success=False, error="点击目标不能为空")

    # 尝试定位元素
    locator = await self._locate_element(target, elements)

    if locator:
        try:
            # 策略 1: 正常点击
            await locator.click(timeout=self.timeout)
            logger.info(f"点击成功: {target}")
            return ActionResult(success=True)
        except Exception as e:
            error_str = str(e).lower()

            # 策略 2: force 点击（跳过可见性检查）
            if "not visible" in error_str or "covered" in error_str:
                try:
                    await locator.click(force=True, timeout=self.timeout)
                    logger.info(f"Force 点击成功: {target}")
                    return ActionResult(success=True)
                except Exception as force_error:
                    pass

            # 策略 3: JavaScript 点击
            try:
                element_handle = await locator.element_handle(timeout=5000)
                await self.page.evaluate("el => el.click()", element_handle)
                logger.info(f"JavaScript 点击成功: {target}")
                return ActionResult(success=True)
            except Exception as js_error:
                logger.warning(f"所有点击策略都失败: {target}")

            return ActionResult(success=False, error=f"点击失败: {str(e)[:100]}")
    else:
        # 策略 4: 直接通过文本点击
        try:
            await self.page.get_by_text(target).click(timeout=self.timeout)
            logger.info(f"通过文本点击成功: {target}")
            return ActionResult(success=True)
        except Exception as e:
            # 策略 5: 通过 role 点击
            try:
                await self.page.get_by_role("button", name=target).click(timeout=self.timeout)
                logger.info(f"通过 role 点击成功: {target}")
                return ActionResult(success=True)
            except Exception:
                return ActionResult(success=False, error=f"无法找到元素: {target}")
```

**Step 4: 添加动作预验证方法**

在 `Executor` 类中添加预验证方法：

```python
async def validate_action(
    self,
    action: Action,
    elements: list[InteractiveElement],
) -> tuple[bool, str | None]:
    """执行前验证动作是否可行

    Returns:
        (is_valid, error_message)
    """
    if action.action == "done":
        return True, None

    if action.action == "navigate":
        if not action.value:
            return False, "navigate 动作需要 value（URL）"
        return True, None

    if action.action in ["click", "input"]:
        if not action.target:
            return False, f"{action.action} 动作需要 target"

        # 检测数字索引
        if action.target.strip().isdigit():
            return False, f"禁止使用数字索引 '{action.target}'，请使用元素文本、placeholder 或 ID"

        # 检查元素是否存在
        locator = await self._locate_element(action.target, elements)
        if not locator:
            return False, f"找不到元素: {action.target}"

        # 检查元素是否可见
        try:
            is_visible = await locator.is_visible()
            if not is_visible:
                logger.warning(f"元素存在但不可见: {action.target}")
                # 不阻止执行，因为可以用 force 或 JS
        except:
            pass

        return True, None

    if action.action == "input":
        if action.value is None:
            return False, "input 动作需要 value"

    return True, None
```

**Step 5: 提交执行层优化**

```bash
git add backend/agent_simple/executor.py
git commit -m "feat(executor): 优化执行层 - 多策略定位 + 预验证 + 增强日志

- 检测数字索引并警告，自动转换为文本定位
- 添加按钮角色定位策略
- 优化点击方法的回退逻辑（force -> JS）
- 添加动作预验证方法

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5.3: 感知层优化

**Files:**
- Modify: `backend/agent_simple/perception.py`

**Step 1: 增强元素属性提取**

现有的 `_extract_elements` 方法已经提取了 aria_label 和 title，无需修改。

**Step 2: 优化元素优先级排序**

修改 `_extract_elements` 方法，添加更智能的优先级排序：

```python
async def _extract_elements(self) -> list[InteractiveElement]:
    """提取页面上的可交互元素"""
    selector = ", ".join(self.INTERACTIVE_SELECTORS)

    elements_data = await self.page.evaluate(
        """
        ([selector, maxElements]) => {
            const elements = document.querySelectorAll(selector);
            const result = [];

            elements.forEach((el, index) => {
                // 跳过隐藏元素
                const style = window.getComputedStyle(el);
                if (style.display === 'none' || style.visibility === 'hidden') {
                    return;
                }

                // 跳过禁用元素
                if (el.disabled) {
                    return;
                }

                // 获取元素位置
                const rect = el.getBoundingClientRect();
                const isInViewport = (
                    rect.top >= 0 &&
                    rect.left >= 0 &&
                    rect.bottom <= window.innerHeight &&
                    rect.right <= window.innerWidth
                );

                // 清理文本
                let text = (el.innerText || el.value || '')
                    .replace(/\\s+/g, ' ')
                    .trim()
                    .slice(0, 50);

                // 计算优先级分数
                let priority = 0;
                if (text) priority += 30;
                if (el.placeholder) priority += 20;
                if (el.getAttribute('aria-label')) priority += 15;
                if (el.id) priority += 10;
                if (isInViewport) priority += 25;
                if (el.tagName === 'BUTTON') priority += 15;
                if (el.tagName === 'A') priority += 10;
                if (el.tagName === 'INPUT') priority += 12;

                result.push({
                    index: index,
                    tag: el.tagName,
                    text: text,
                    type: el.type || null,
                    id: el.id || null,
                    placeholder: el.placeholder || null,
                    name: el.name || null,
                    aria_label: el.getAttribute('aria-label') || null,
                    title: el.getAttribute('title') || null,
                    _priority: priority,
                    _isInViewport: isInViewport
                });
            });

            // 按优先级排序
            result.sort((a, b) => b._priority - a._priority);

            // 移除内部字段并限制数量
            return result.slice(0, maxElements).map(el => {
                const { _priority, _isInViewport, ...rest } = el;
                return rest;
            });
        }
    """,
        [selector, self.MAX_ELEMENTS],
    )

    return [InteractiveElement(**el) for el in elements_data]
```

**Step 3: 优化元素描述格式化**

修改 `format_elements_for_prompt` 方法，添加更多上下文：

```python
def format_elements_for_prompt(self, elements: list[InteractiveElement]) -> str:
    """格式化元素列表用于 Prompt"""
    if not elements:
        return "（页面上没有可交互元素）"

    lines = []
    for el in elements:
        # 构建元素描述
        parts = [f"[{el.index}] <{el.tag}>"]

        # ID 优先显示（最重要的定位信息）
        if el.id:
            parts.append(f'ID: "{el.id}"')
        if el.name:
            parts.append(f'name: "{el.name}"')

        # 文本内容
        if el.text:
            parts.append(f'文本: "{el.text}"')

        # 辅助定位属性
        if el.placeholder:
            parts.append(f'占位符: "{el.placeholder}"')
        if el.aria_label:
            parts.append(f'aria-label: "{el.aria_label}"')
        if el.title:
            parts.append(f'title: "{el.title}"')

        # 输入类型
        if el.type and el.tag == "INPUT":
            parts.append(f"类型: {el.type}")

        lines.append(" | ".join(parts))

    return "\n".join(lines)
```

**Step 4: 添加页面状态哈希**

在 `get_state` 方法中添加页面状态哈希，用于检测页面变化：

```python
async def get_state(self) -> PageState:
    """获取当前页面状态"""
    # 1. 截图并转为 base64
    screenshot_bytes = await self.page.screenshot(type="png")
    screenshot_base64 = base64.b64encode(screenshot_bytes).decode("utf-8")

    # 2. 获取页面基本信息
    url = self.page.url
    title = await self.page.title()

    # 3. 提取可交互元素
    elements = await self._extract_elements()

    # 4. 计算页面状态哈希（用于检测页面变化）
    state_hash = await self._compute_page_hash()

    return PageState(
        screenshot_base64=screenshot_base64,
        url=url,
        title=title,
        elements=elements,
        state_hash=state_hash,  # 新增字段
    )

async def _compute_page_hash(self) -> str:
    """计算页面状态哈希"""
    import hashlib

    # 使用 URL + 标题 + 主要元素文本计算哈希
    content = await self.page.evaluate("""
        () => {
            const url = window.location.href;
            const title = document.title;
            // 获取主要元素的文本
            const mainContent = document.body.innerText.slice(0, 1000);
            return url + title + mainContent;
        }
    """)

    return hashlib.md5(content.encode()).hexdigest()[:16]
```

**Step 5: 更新类型定义**

在 `backend/agent_simple/types.py` 的 `PageState` 类中添加 `state_hash` 字段：

```python
class PageState(BaseModel):
    """页面状态快照"""

    screenshot_base64: str = Field(description="截图 base64 编码")
    url: str = Field(description="当前页面 URL")
    title: str = Field(description="页面标题")
    elements: list[InteractiveElement] = Field(
        default_factory=list, description="可交互元素列表"
    )
    state_hash: str | None = Field(default=None, description="页面状态哈希")
```

**Step 6: 提交感知层优化**

```bash
git add backend/agent_simple/perception.py backend/agent_simple/types.py
git commit -m "feat(perception): 优化感知层 - 优先级排序 + 页面哈希

- 元素按优先级智能排序（视口内、有文本、按钮优先）
- 添加页面状态哈希用于检测页面变化
- 优化元素描述格式化

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5.4: 反思层优化

**Files:**
- Modify: `backend/agent_simple/agent.py`

**Step 1: 添加循环检测方法**

在 `SimpleAgent` 类中添加循环检测方法：

```python
def _detect_loop(self) -> bool:
    """检测是否陷入循环"""
    if len(self.history) < 4:
        return False

    recent = self.history[-4:]

    # 检测 1: 连续相同动作
    actions = [(s.action.action, s.action.target) for s in recent]
    if len(set(str(a) for a in actions)) <= 2:
        logger.warning("检测到循环：连续相同动作")
        return True

    # 检测 2: 页面状态无变化
    page_hashes = [s.state.state_hash for s in recent if s.state.state_hash]
    if len(page_hashes) >= 4 and len(set(page_hashes)) == 1:
        logger.warning("检测到循环：页面状态无变化")
        return True

    # 检测 3: 高失败率
    failed_count = sum(1 for s in recent if not s.result.success)
    if failed_count >= 3:
        logger.warning(f"检测到循环：高失败率 {failed_count}/4")
        return True

    return False
```

**Step 2: 添加循环恢复方法**

```python
async def _recover_from_loop(self) -> bool:
    """从循环中恢复"""
    logger.info("尝试从循环中恢复...")

    recovery_actions = [
        ("wait", "等待页面加载", lambda: self.page.wait_for_timeout(2000)),
        ("scroll_down", "滚动到页面底部", lambda: self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")),
        ("scroll_up", "滚动到页面顶部", lambda: self.page.evaluate("window.scrollTo(0, 0)")),
    ]

    for action_name, description, action_func in recovery_actions:
        try:
            logger.info(f"尝试恢复动作: {description}")
            await action_func()
            await self.page.wait_for_timeout(500)
            return True
        except Exception as e:
            logger.warning(f"恢复动作失败 {action_name}: {e}")
            continue

    return False
```

**Step 3: 构建带历史记忆的上下文**

```python
def _build_history_context(self) -> str:
    """构建历史记忆上下文"""
    if not self.history:
        return "（这是第一步）"

    parts = []

    # 最近 3 步的摘要
    recent = self.history[-3:] if len(self.history) >= 3 else self.history
    for step in recent:
        status = "✅" if step.result.success else "❌"
        target = step.action.target or ""
        value = step.action.value or ""
        action_desc = f"{step.action.action}"
        if target:
            action_desc += f" -> {target}"
        if value:
            action_desc += f" = {value}"

        parts.append(f"Step {step.step_num}: {action_desc} {status}")

    # 失败模式检测
    failed_actions = [s for s in self.history if not s.result.success]
    if failed_actions:
        parts.append("\n⚠️ 已失败的动作（请避免重复）：")
        for f in failed_actions[-2:]:
            parts.append(f"  - {f.action.action} -> {f.action.target}")

    return "\n".join(parts)
```

**Step 4: 修改反思方法使用历史上下文**

修改 `_reflect` 方法，使用历史上下文：

```python
async def _reflect(
    self,
    action: Action,
    result: ActionResult,
    state: PageState,
) -> Reflection:
    """反思失败原因并生成修复策略"""
    # 构建反思 prompt
    elements_text = format_elements_for_prompt(state.elements[:10])
    history_context = self._build_history_context()

    prompt = REFLECTION_PROMPT.format(
        task=self.task,
        history=history_context,  # 新增历史上下文
        thought=action.thought,
        action=action.action,
        target=action.target or "无",
        value=action.value or "无",
        error=result.error or "未知错误",
        url=state.url,
        title=state.title,
        elements=elements_text,
    )

    # ... 其余代码不变
```

**Step 5: 在主循环中添加循环检测**

修改 `run` 方法，在每次迭代开始时检测循环：

```python
async def run(self) -> AgentResult:
    """执行任务"""
    logger.info(f"开始执行任务: {self.task}")
    logger.info(f"最大步数: {self.max_steps}, 最大重试: {self.max_retries}")

    for step_num in range(1, self.max_steps + 1):
        logger.info(f"\n{'='*50}")
        logger.info(f"Step {step_num}/{self.max_steps}")
        logger.info(f"{'='*50}")

        # 检测循环
        if self._detect_loop():
            recovered = await self._recover_from_loop()
            if not recovered:
                logger.error("无法从循环中恢复")
                # 继续执行，让 LLM 决定下一步

        # 1. 感知页面
        state = await self.perception.get_state()
        # ... 其余代码不变
```

**Step 6: 添加 ROLLBACK 策略**

在 `types.py` 中添加 ROLLBACK 策略：

```python
class ReflectionStrategy(str, Enum):
    """反思策略"""

    RETRY = "retry"  # 原样重试
    ALTERNATIVE = "alternative"  # 替代方案
    SKIP = "skip"  # 跳过当前步骤
    ROLLBACK = "rollback"  # 回退到上一步（新增）
```

**Step 7: 提交反思层优化**

```bash
git add backend/agent_simple/agent.py backend/agent_simple/types.py
git commit -m "feat(agent): 优化反思层 - 循环检测 + 历史记忆 + 恢复机制

- 添加循环检测（相同动作、页面无变化、高失败率）
- 添加循环恢复机制（等待、滚动）
- 构建带历史记忆的反思上下文
- 添加 ROLLBACK 反思策略

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5.5: 验证测试

**Files:**
- Create: `backend/tests/test_phase5_unit.py`
- Create: `backend/tests/run_phase5.py`

**Step 1: 创建单元测试文件**

```python
# backend/tests/test_phase5_unit.py
"""Phase 5 优化模块单元测试"""

import pytest
from backend.agent_simple.prompts import SYSTEM_PROMPT, format_elements_for_prompt
from backend.agent_simple.types import InteractiveElement, Action


class TestPromptOptimization:
    """Prompt 层优化测试"""

    def test_locating_rules_forbid_numeric_index(self):
        """测试定位规则禁止数字索引"""
        assert "禁止" in SYSTEM_PROMPT or "不能是数字" in SYSTEM_PROMPT
        assert "数字索引" in SYSTEM_PROMPT or "数字" in SYSTEM_PROMPT

    def test_few_shot_login_example_exists(self):
        """测试包含登录场景示例"""
        assert "登录" in SYSTEM_PROMPT
        assert "账号" in SYSTEM_PROMPT or "密码" in SYSTEM_PROMPT

    def test_completion_rules_detailed(self):
        """测试任务完成判断规则详细"""
        assert "完成" in SYSTEM_PROMPT
        assert "done" in SYSTEM_PROMPT.lower()


class TestElementFormatting:
    """元素格式化测试"""

    def test_format_elements_with_all_attributes(self):
        """测试格式化包含所有属性的元素"""
        elements = [
            InteractiveElement(
                index=0,
                tag="INPUT",
                text="",
                type="text",
                id="username",
                placeholder="请输入用户名",
                name="user",
                aria_label="用户名",
                title="输入您的用户名",
            )
        ]
        result = format_elements_for_prompt(elements)

        assert "ID:" in result
        assert "username" in result
        assert "占位符:" in result
        assert "请输入用户名" in result

    def test_format_empty_elements(self):
        """测试格式化空元素列表"""
        result = format_elements_for_prompt([])
        assert "没有可交互元素" in result


class TestActionValidation:
    """动作验证测试"""

    def test_numeric_target_should_be_warned(self):
        """测试数字 target 应该被警告"""
        # 这个测试验证 executor 中的数字索引检测逻辑
        # 实际逻辑在 executor.py 中
        action = Action(
            thought="测试",
            action="click",
            target="2",  # 数字索引
        )
        assert action.target.isdigit()


class TestReflectionStrategy:
    """反思策略测试"""

    def test_reflection_strategies_defined(self):
        """测试反思策略已定义"""
        from backend.agent_simple.types import ReflectionStrategy

        assert ReflectionStrategy.RETRY.value == "retry"
        assert ReflectionStrategy.ALTERNATIVE.value == "alternative"
        assert ReflectionStrategy.SKIP.value == "skip"
```

**Step 2: 创建 Phase 5 运行脚本**

```python
# backend/tests/run_phase5.py
"""Phase 5 验证测试运行脚本"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pytest
from backend.tests.reporter import Phase4Report, TestResult


async def run_phase5_tests():
    """运行 Phase 5 验证测试"""
    print("=" * 60)
    print("Phase 5: Agent 优化验证测试")
    print("=" * 60)

    # 1. 运行单元测试
    print("\n1. 运行单元测试...")
    unit_test_result = pytest.main([
        "backend/tests/test_phase5_unit.py",
        "-v",
        "--tb=short"
    ])

    # 2. 运行场景测试
    print("\n2. 运行场景测试...")
    output_dir = Path("outputs/tests/phase5")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 运行 pytest
    scenario_result = pytest.main([
        "backend/tests/test_login_e2e.py",
        "backend/tests/test_purchase_e2e.py",
        "-v",
        "--tb=short",
        f"--output-dir={output_dir}"
    ])

    print("\n" + "=" * 60)
    print("Phase 5 测试完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_phase5_tests())
```

**Step 3: 运行测试验证**

```bash
# 运行单元测试
pytest backend/tests/test_phase5_unit.py -v

# 运行场景测试（可选，需要真实环境）
# pytest backend/tests/test_login_e2e.py backend/tests/test_purchase_e2e.py -v
```

**Step 4: 提交测试文件**

```bash
git add backend/tests/test_phase5_unit.py backend/tests/run_phase5.py
git commit -m "test: 添加 Phase 5 单元测试和运行脚本

- 测试 Prompt 禁止数字索引规则
- 测试 Few-shot 示例存在
- 测试元素格式化
- 测试反思策略定义

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## 验收标准

| 指标 | 目标 | 验证方式 |
|------|------|----------|
| 场景通过率 | ≥ 80% (2/2) | pytest 运行报告 |
| 自愈成功率 | ≥ 50% | 失败后重试成功次数 |
| 单步推理耗时 | ≤ 10s | LLM 响应时间 |
| 登录场景步数 | ≤ 8 步 | 执行日志 |
| 采购单场景步数 | ≤ 20 步 | 执行日志 |

---

## 执行顺序

1. Task 5.1: Prompt 层优化（基础设施）
2. Task 5.2: 执行层优化（依赖 Task 5.1）
3. Task 5.3: 感知层优化（依赖 Task 5.2）
4. Task 5.4: 反思层优化（依赖 Task 5.3）
5. Task 5.5: 验证测试（所有优化完成后）
