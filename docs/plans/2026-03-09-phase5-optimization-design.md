# Phase 5: Agent 优化阶段设计文档

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 全面优化 SimpleAgent 的稳定性、通用性和自愈能力，使测试场景通过率达到 80%+，自愈成功率达到 50%+

**Architecture:** 分四层渐进式优化（Prompt → 执行 → 感知 → 反思），每层独立可测试，为未来扩展预留空间

**Tech Stack:** Python, Playwright, 通义千问 qwen-vl-max

---

## 1. 背景分析

### Phase 4 测试结果

| 场景 | 结果 | 步数 | 耗时 | 错误 |
|------|------|------|------|------|
| 登录场景 | ❌ | 10 | 628s | 超过最大步数 |
| 新增采购单 | ❌ | 25 | 607s | 超过最大步数 |

### 核心问题

| 问题 | 表现 | 影响 |
|------|------|------|
| LLM 数字索引 | 输出 `target: "2"` 而非元素文本 | 元素定位失败 |
| 导航检测 | 侧边栏点击后菜单未展开 | 陷入循环 |
| 反思失效 | 修复后下一步又重复错误 | 无法自愈 |
| 完成判断 | 无法准确判断任务完成 | 超时失败 |

---

## 2. 优化架构

```
┌─────────────────────────────────────────┐
│            反思层优化                    │  ← 第 4 层（最高）
│  • 多策略反思（retry/alternative/skip） │
│  • 历史记忆增强                          │
│  • 循环检测和自动恢复                    │
├─────────────────────────────────────────┤
│            感知层优化                    │  ← 第 3 层
│  • 增强元素属性提取                      │
│  • 文本清理和标准化                      │
│  • 元素优先级排序                        │
├─────────────────────────────────────────┤
│            执行层优化                    │  ← 第 2 层
│  • 多策略元素定位                        │
│  • JavaScript 回退机制                  │
│  • 动作预验证                            │
├─────────────────────────────────────────┤
│            Prompt 层优化                 │  ← 第 1 层（基础）
│  • 禁止数字索引                          │
│  • Few-shot 示例                        │
│  • 任务完成判断规则                      │
└─────────────────────────────────────────┘
```

---

## 3. 任务清单

### Task 5.1: Prompt 层优化

**Files:**
- Modify: `backend/agent_simple/prompts.py`

**优化内容:**

#### 3.1.1 强制定位规则

```python
LOCATING_RULES = """
⚠️ 元素定位规则（必须遵守）：
1. target 必须是元素的文本内容，不能是数字索引
   ✅ 正确: "target": "密码登录"
   ❌ 错误: "target": "2" 或 "target": "第2个"

2. 如果元素没有文本，使用 placeholder、aria-label 或 title 属性
   ✅ 正确: "target": "请输入密码"
   ❌ 错误: "target": "input_1"

3. 文本应精确匹配页面上显示的内容
   ✅ 正确: "target": "登 录"（如果页面有空格）
   ❌ 错误: "target": "登录"（页面实际是 "登 录"）
"""
```

#### 3.1.2 Few-shot 示例

```python
FEW_SHOT_EXAMPLES = """
示例 1 - 登录场景：
页面元素: [账号输入框(placeholder: 请输入账号), 密码输入框(placeholder: 请输入密码), 登录按钮]
任务: 输入账号 test_user，输入密码 123456，点击登录

Step 1: {"thought": "需要先在账号输入框输入账号", "action": "input", "target": "请输入账号", "value": "test_user"}
Step 2: {"thought": "然后在密码输入框输入密码", "action": "input", "target": "请输入密码", "value": "123456"}
Step 3: {"thought": "最后点击登录按钮", "action": "click", "target": "登录"}
Step 4: {"thought": "检测到欢迎信息，登录成功", "action": "done"}

示例 2 - 表单填写：
页面元素: [下拉选择框(请选择类型), 名称输入框, 提交按钮]
任务: 选择类型为"手机"，填写名称为"测试设备"

Step 1: {"thought": "先选择设备类型", "action": "click", "target": "请选择类型"}
Step 2: {"thought": "从下拉菜单选择手机", "action": "click", "target": "手机"}
Step 3: {"thought": "填写设备名称", "action": "input", "target": "名称", "value": "测试设备"}
Step 4: {"thought": "点击提交", "action": "click", "target": "提交"}
Step 5: {"thought": "表单提交成功，出现新记录", "action": "done"}
"""
```

#### 3.1.3 任务完成判断规则

```python
COMPLETION_RULES = """
任务完成判断规则：
1. done 动作必须基于明确的页面变化证据
2. 完成证据类型：
   - 出现新的成功提示（"成功"、"完成"、"保存成功"）
   - 出现目标元素（如新记录、新页面）
   - 页面 URL 变化到预期地址
3. 如果不确定是否完成，继续执行而非猜测完成
4. 完成后简要说明完成依据
"""
```

---

### Task 5.2: 执行层优化

**Files:**
- Modify: `backend/agent_simple/executor.py`

**优化内容:**

#### 3.2.1 多策略元素定位

```python
async def locate_element(self, target: str) -> Locator | None:
    """多策略定位元素，按优先级尝试"""
    strategies = [
        # 策略 1: 精确文本匹配（button role）
        lambda t: self.page.get_by_role("button", name=t),

        # 策略 2: 精确文本匹配（通用）
        lambda t: self.page.locator(f"text={t}"),

        # 策略 3: 包含文本（模糊匹配）
        lambda t: self.page.locator(f"text=/{t}/i"),

        # 策略 4: placeholder 属性
        lambda t: self.page.locator(f"[placeholder*={t}i]"),

        # 策略 5: aria-label 属性
        lambda t: self.page.locator(f"[aria-label*={t}i]"),

        # 策略 6: title 属性
        lambda t: self.page.locator(f"[title*={t}i]"),

        # 策略 7: name 属性
        lambda t: self.page.locator(f"[name*={t}i]"),

        # 策略 8: ID 包含
        lambda t: self.page.locator(f"[id*={t}i]"),
    ]

    for strategy in strategies:
        try:
            locator = strategy(target)
            if await locator.count() > 0:
                return locator.first
        except:
            continue

    return None
```

#### 3.2.2 JavaScript 回退机制

```python
async def click(self, target: str) -> ActionResult:
    """点击元素，带 JS 回退"""
    element = await self.locate_element(target)
    if not element:
        return ActionResult(success=False, error=f"找不到元素: {target}")

    try:
        # 尝试标准点击
        await element.click(timeout=5000)
        return ActionResult(success=True)
    except Exception as e:
        # 回退到 JavaScript 点击
        try:
            await element.evaluate("el => el.click()")
            return ActionResult(success=True, message="使用 JS 点击成功")
        except Exception as js_error:
            return ActionResult(success=False, error=f"点击失败: {e}, JS回退也失败: {js_error}")

async def input_text(self, target: str, value: str) -> ActionResult:
    """输入文本，带 JS 回退"""
    element = await self.locate_element(target)
    if not element:
        return ActionResult(success=False, error=f"找不到元素: {target}")

    try:
        # 尝试标准输入
        await element.fill(value, timeout=5000)
        return ActionResult(success=True)
    except Exception as e:
        # 回退到 JavaScript 输入
        try:
            await element.evaluate(f"el => {{ el.value = '{value}' }}")
            await element.evaluate("el => el.dispatchEvent(new Event('input', { bubbles: true }))")
            return ActionResult(success=True, message="使用 JS 输入成功")
        except Exception as js_error:
            return ActionResult(success=False, error=f"输入失败: {e}, JS回退也失败: {js_error}")
```

#### 3.2.3 动作预验证

```python
async def validate_action(self, action: str, target: str) -> bool:
    """执行前验证动作是否可行"""
    if action == "done":
        return True

    if action in ["click", "input", "select"]:
        element = await self.locate_element(target)
        if not element:
            return False
        # 检查是否可见可交互
        return await element.is_visible()

    return True
```

---

### Task 5.3: 感知层优化

**Files:**
- Modify: `backend/agent_simple/perception.py`

**优化内容:**

#### 3.3.1 增强元素属性提取

```python
async def extract_interactive_elements(self) -> list[dict]:
    """提取可交互元素，包含更多属性"""
    elements = await self.page.evaluate("""
        () => {
            const results = [];
            const selectors = [
                'button', 'a', 'input', 'select', 'textarea',
                '[role="button"]', '[onclick]', '[tabindex]'
            ];
            const interactive = document.querySelectorAll(selectors.join(', '));

            interactive.forEach((el, index) => {
                const text = (el.innerText || el.textContent || '').trim();
                const ariaLabel = el.getAttribute('aria-label') || '';
                const title = el.getAttribute('title') || '';
                const placeholder = el.getAttribute('placeholder') || '';
                const name = el.getAttribute('name') || '';
                const id = el.getAttribute('id') || '';
                const type = el.getAttribute('type') || el.tagName.toLowerCase();

                const rect = el.getBoundingClientRect();
                const isVisible = rect.width > 0 && rect.height > 0;

                results.push({
                    index,
                    text,
                    ariaLabel,
                    title,
                    placeholder,
                    name,
                    id,
                    type,
                    isVisible,
                    rect: { x: rect.x, y: rect.y, width: rect.width, height: rect.height }
                });
            });

            return results;
        }
    """)
    return elements
```

#### 3.3.2 文本清理和标准化

```python
def format_element_description(self, element: dict) -> str:
    """生成元素的标准化描述"""
    parts = []

    # 主文本（清理多余空白）
    if element.get('text'):
        text = ' '.join(element['text'].split())
        if text:
            parts.append(text)

    # 辅助属性（用方括号标记）
    if element.get('ariaLabel'):
        parts.append(f"[aria:{element['ariaLabel']}]")

    if element.get('placeholder'):
        parts.append(f"[placeholder:{element['placeholder']}]")

    if element.get('title'):
        parts.append(f"[title:{element['title']}]")

    return ' '.join(parts) if parts else f"[{element.get('type', 'unknown')}]"
```

#### 3.3.3 元素优先级排序

```python
def prioritize_elements(self, elements: list[dict]) -> list[dict]:
    """按交互优先级排序"""
    def priority_score(el):
        score = 0

        # 可见元素优先
        if el.get('isVisible'):
            score += 100

        # 有文本内容优先
        if el.get('text') and len(el['text'].strip()) > 0:
            score += 50

        # 按类型加权
        type_weights = {
            'button': 30,
            'a': 25,
            'input': 20,
            'select': 20,
            'textarea': 15
        }
        score += type_weights.get(el.get('type'), 10)

        # 视口内优先
        rect = el.get('rect', {})
        if 0 <= rect.get('x', 0) < 1920 and 0 <= rect.get('y', 0) < 1080:
            score += 20

        return score

    return sorted(elements, key=priority_score, reverse=True)
```

---

### Task 5.4: 反思层优化

**Files:**
- Modify: `backend/agent_simple/agent.py`
- Modify: `backend/agent_simple/prompts.py`

**优化内容:**

#### 3.4.1 多策略反思

```python
class ReflectionStrategy(Enum):
    RETRY = "retry"              # 原样重试
    ALTERNATIVE = "alternative"  # 替代方案
    SKIP = "skip"                # 跳过当前步骤
    ROLLBACK = "rollback"        # 回退到上一步

def analyze_failure(self, error: str, action: Action, history: list) -> ReflectionStrategy:
    """分析失败原因，选择反思策略"""

    error_lower = error.lower()

    # 元素定位失败 → 尝试替代方案
    if "not found" in error_lower or "timeout" in error_lower or "找不到" in error_lower:
        return ReflectionStrategy.ALTERNATIVE

    # 页面未变化 → 可能需要等待或滚动
    if "no change" in error_lower or "无变化" in error_lower:
        return ReflectionStrategy.RETRY

    # 重复相同动作超过3次 → 跳过
    recent_actions = [h.action for h in history[-5:]]
    same_action_count = sum(1 for a in recent_actions
                           if a.action == action.action and a.target == action.target)
    if same_action_count >= 3:
        return ReflectionStrategy.SKIP

    return ReflectionStrategy.RETRY
```

#### 3.4.2 历史记忆增强

```python
def build_context_with_memory(self, history: list) -> str:
    """构建带记忆的上下文"""
    memory_parts = []

    # 最近3步的摘要
    recent = history[-3:] if len(history) >= 3 else history
    for step in recent:
        status = '✅' if step.success else '❌'
        memory_parts.append(
            f"步骤{step.step_num}: {step.action.action} -> {step.action.target or step.action.value} {status}"
        )

    # 失败模式检测
    failed_actions = [s for s in history if not s.success]
    if failed_actions:
        memory_parts.append("\n⚠️ 注意 - 以下动作失败了，请避免重复：")
        for f in failed_actions[-2:]:
            memory_parts.append(f"  - {f.action.action} -> {f.action.target}")

    return "\n".join(memory_parts)
```

#### 3.4.3 循环检测和自动恢复

```python
def detect_loop(self, history: list) -> bool:
    """检测是否陷入循环"""
    if len(history) < 4:
        return False

    recent = history[-4:]

    # 检测连续相同动作
    actions = [(s.action.action, s.action.target) for s in recent]
    if len(set(actions)) <= 2:
        return True

    # 检测页面无变化（如果有页面状态哈希）
    page_states = [s.page_state_hash for s in recent if hasattr(s, 'page_state_hash') and s.page_state_hash]
    if len(page_states) >= 4 and len(set(page_states)) == 1:
        return True

    return False

async def recover_from_loop(self) -> bool:
    """从循环中恢复"""
    recovery_actions = [
        ("wait", "等待页面加载"),
        ("scroll", "滚动到页面底部"),
    ]

    for action_type, description in recovery_actions:
        try:
            if action_type == "wait":
                await self.page.wait_for_timeout(2000)
            elif action_type == "scroll":
                await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            return True
        except:
            continue

    return False
```

#### 3.4.4 反思 Prompt 优化

```python
REFLECTION_PROMPT = """
之前的动作失败了，请分析原因并调整策略：

失败的动作: {failed_action}
失败原因: {error_message}

历史记录:
{history_summary}

⚠️ 反思规则：
1. 如果元素定位失败，尝试使用不同的定位方式（如 placeholder、aria-label）
2. 如果点击后页面无变化，可能需要先展开菜单或滚动页面
3. 如果重复相同动作失败，请尝试跳过或换一种方式
4. 禁止输出数字索引，必须使用元素的文本内容

请输出修正后的动作（JSON格式）：
{{"thought": "...", "action": "...", "target": "...", "value": "..."}}
"""
```

---

### Task 5.5: 验证测试

**Files:**
- Create: `backend/tests/test_phase5_unit.py`
- Modify: `backend/tests/run_phase4.py` → `run_phase5.py`

**测试策略:**

#### 3.5.1 单元测试

```python
# test_phase5_unit.py

import pytest
from backend.agent_simple.perception import Perception
from backend.agent_simple.executor import Executor
from backend.agent_simple.prompts import build_system_prompt

class TestPromptOptimization:
    def test_locating_rules_in_prompt(self):
        """测试定位规则是否包含在 Prompt 中"""
        prompt = build_system_prompt("测试任务")
        assert "target 必须是元素的文本内容" in prompt
        assert "不能是数字索引" in prompt

    def test_few_shot_examples_in_prompt(self):
        """测试 Few-shot 示例是否包含"""
        prompt = build_system_prompt("登录")
        assert "示例" in prompt

class TestPerceptionOptimization:
    @pytest.mark.asyncio
    async def test_extract_aria_label(self, page):
        """测试提取 aria-label 属性"""
        perception = Perception(page)
        # ... 测试逻辑

    def test_prioritize_elements(self):
        """测试元素优先级排序"""
        # ... 测试逻辑

class TestExecutorOptimization:
    @pytest.mark.asyncio
    async def test_multi_strategy_locate(self, page):
        """测试多策略定位"""
        executor = Executor(page)
        # ... 测试逻辑

    @pytest.mark.asyncio
    async def test_js_fallback_click(self, page):
        """测试 JS 点击回退"""
        # ... 测试逻辑

class TestReflectionOptimization:
    def test_analyze_failure_strategy(self):
        """测试失败分析策略选择"""
        # ... 测试逻辑

    def test_detect_loop(self):
        """测试循环检测"""
        # ... 测试逻辑
```

#### 3.5.2 场景验证

复用 Phase 4 的测试用例：
- `test_login_e2e.py` - 登录场景
- `test_purchase_e2e.py` - 采购单场景

#### 3.5.3 验收标准

| 指标 | 目标 | 验证方式 |
|------|------|----------|
| 场景通过率 | ≥ 80% (2/2) | pytest 运行报告 |
| 自愈成功率 | ≥ 50% | 失败后重试成功次数 / 总失败次数 |
| 单步推理耗时 | ≤ 10s | LLM 响应时间统计 |
| 截图完整率 | 100% | 每步截图检查 |
| 登录场景步数 | ≤ 8 步 | 执行日志 |
| 采购单场景步数 | ≤ 20 步 | 执行日志 |

---

## 4. 预期效果

### 优化前后对比

| 指标 | 优化前 | 优化后目标 |
|------|--------|------------|
| 登录场景步数 | 10 (超时) | ≤ 8 |
| 采购单场景步数 | 25 (超时) | ≤ 20 |
| 场景通过率 | 0% | ≥ 80% |
| 自愈成功率 | 0% | ≥ 50% |
| 元素定位成功率 | ~60% | ≥ 90% |

### 关键改进点

1. **Prompt 层**：LLM 输出更规范，减少数字索引错误
2. **执行层**：多策略定位 + JS 回退，提高定位成功率
3. **感知层**：更完整的元素信息，更好的优先级
4. **反思层**：智能反思策略 + 循环检测，避免陷入死循环

---

## 5. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| LLM 仍输出数字索引 | 定位失败 | 多次强调 + Few-shot + 反思修正 |
| 页面结构变化 | 定位失败 | 多策略定位 + JS 回退 |
| 网络延迟 | 超时失败 | 增加超时时间 + 重试机制 |
| 模型理解偏差 | 动作错误 | Few-shot 示例 + 反思修正 |

---

## 6. 后续扩展

Phase 5 完成后，可考虑：
1. **Phase 6**：增加更多测试场景（搜索、报表等）
2. **Phase 7**：性能优化（缓存、并行执行）
3. **Phase 8**：CI/CD 集成
