# Agent 记忆机制实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 为 SimpleAgent 添加记忆机制，让 LLM 在决策时能看到最近操作历史，避免重复动作和死循环。

**Architecture:** 新增独立 Memory 模块（`memory.py`），修改 `prompts.py`、`decision.py`、`agent.py` 将记忆上下文注入到 User Prompt 中。

**Tech Stack:** Python, Pydantic, pytest

---

## Task 1: 创建 Memory 模块单元测试

**Files:**
- Create: `backend/tests/test_memory.py`

**Step 1: Write the failing test**

```python
"""Memory 模块单元测试"""

import pytest
from backend.agent_simple.memory import Memory
from backend.agent_simple.types import (
    Action,
    ActionResult,
    PageState,
    Step,
)


def make_step(step_num: int, action: str, target: str, success: bool, error: str = None) -> Step:
    """创建测试用 Step 对象"""
    return Step(
        step_num=step_num,
        state=PageState(
            screenshot_base64="test",
            url="https://example.com",
            title="Test Page",
        ),
        action=Action(
            thought=f"执行 {action}",
            action=action,
            target=target,
            value=None,
            done=False,
        ),
        result=ActionResult(
            success=success,
            error=error,
        ),
    )


class TestMemoryAddStep:
    """测试 add_step 方法"""

    def test_add_step_empty(self):
        """测试向空记忆添加步骤"""
        memory = Memory(max_steps=5)
        step = make_step(1, "click", "登录", True)

        memory.add_step(step)

        assert len(memory.steps) == 1
        assert memory.steps[0] == step

    def test_add_step_respects_max_steps(self):
        """测试容量限制：超过 max_steps 时移除最旧的"""
        memory = Memory(max_steps=3)

        for i in range(1, 6):
            memory.add_step(make_step(i, "click", f"按钮{i}", True))

        assert len(memory.steps) == 3
        assert memory.steps[0].step_num == 3  # 最旧的是第 3 步
        assert memory.steps[-1].step_num == 5  # 最新的是第 5 步


class TestMemoryGetFailedActions:
    """测试 get_failed_actions 方法"""

    def test_get_failed_actions_empty(self):
        """测试空记忆返回空列表"""
        memory = Memory()
        assert memory.get_failed_actions() == []

    def test_get_failed_actions_filters_success(self):
        """测试过滤成功动作"""
        memory = Memory()
        memory.add_step(make_step(1, "click", "登录", True))
        memory.add_step(make_step(2, "input", "账号", False, "元素未找到"))
        memory.add_step(make_step(3, "click", "提交", True))

        failed = memory.get_failed_actions()

        assert len(failed) == 1
        action, error = failed[0]
        assert action.action == "input"
        assert action.target == "账号"
        assert error == "元素未找到"

    def test_get_failed_actions_multiple(self):
        """测试多个失败动作"""
        memory = Memory()
        memory.add_step(make_step(1, "click", "A", False, "错误1"))
        memory.add_step(make_step(2, "input", "B", False, "错误2"))

        failed = memory.get_failed_actions()

        assert len(failed) == 2


class TestMemoryFormatForPrompt:
    """测试 format_for_prompt 方法"""

    def test_format_empty_memory(self):
        """测试空记忆的输出"""
        memory = Memory()
        result = memory.format_for_prompt()

        assert "这是第一步" in result

    def test_format_with_steps(self):
        """测试有步骤时的输出格式"""
        memory = Memory()
        memory.add_step(make_step(1, "click", "登录", True))
        memory.add_step(make_step(2, "input", "账号", False, "元素未找到"))

        result = memory.format_for_prompt()

        # 检查操作记录
        assert "Step 1" in result
        assert "click" in result
        assert "登录" in result
        assert "✅" in result

        # 检查失败警告
        assert "⚠️" in result or "失败" in result
        assert "元素未找到" in result

    def test_format_includes_suggestions(self):
        """测试失败动作包含替代建议"""
        memory = Memory()
        memory.add_step(make_step(1, "input", "账号", False, "元素未找到"))

        result = memory.format_for_prompt()

        assert "建议" in result or "ID" in result or "placeholder" in result


**Step 2: Run test to verify it fails**

Run: `cd /Users/huhu/project/weberpagent && python -m pytest backend/tests/test_memory.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'backend.agent_simple.memory'"

---

## Task 2: 实现 Memory 模块

**Files:**
- Create: `backend/agent_simple/memory.py`

**Step 1: Write minimal implementation**

```python
"""记忆模块 - 存储最近 N 步的操作历史，用于 LLM 决策上下文"""

from backend.agent_simple.types import Step, Action


class Memory:
    """短记忆模块 - 存储最近 N 步的操作历史"""

    def __init__(self, max_steps: int = 5):
        """初始化记忆模块

        Args:
            max_steps: 最大记忆步数，默认 5 步
        """
        self.max_steps = max_steps
        self.steps: list[Step] = []

    def add_step(self, step: Step) -> None:
        """添加步骤，超出容量时移除最旧的

        Args:
            step: 要添加的步骤记录
        """
        self.steps.append(step)
        # 超出容量时移除最旧的
        if len(self.steps) > self.max_steps:
            self.steps.pop(0)

    def get_recent_steps(self) -> list[Step]:
        """获取最近的步骤（最多 max_steps 个）

        Returns:
            最近步骤列表
        """
        return self.steps.copy()

    def get_failed_actions(self) -> list[tuple[Action, str]]:
        """获取失败的动作及其错误信息

        Returns:
            列表，每项为 (Action, 错误信息) 元组
        """
        return [
            (step.action, step.result.error or "未知错误")
            for step in self.steps
            if not step.result.success
        ]

    def format_for_prompt(self) -> str:
        """格式化为 Prompt 文本

        Returns:
            格式化的记忆文本，包含操作记录和失败警告
        """
        if not self.steps:
            return "## 📋 操作记录\n（这是第一步）"

        parts = []

        # 1. 最近操作记录
        parts.append("## 📋 最近操作记录")
        for step in self.steps:
            status = "✅ 成功" if step.result.success else f"❌ {step.result.error or '失败'}"

            # 动作描述
            action_desc = f"{step.action.action}"
            if step.action.target:
                action_desc += f" \"{step.action.target}\""
            if step.action.value:
                action_desc += f" = \"{step.action.value}\""

            parts.append(f"Step {step.step_num}: {action_desc}")
            parts.append(f"  思考: {step.action.thought}")
            parts.append(f"  结果: {status}")

        # 2. 失败动作警告
        failed_actions = self.get_failed_actions()
        if failed_actions:
            parts.append("\n## ⚠️ 失败动作警告")
            for action, error in failed_actions:
                target_desc = f"目标=\"{action.target}\"" if action.target else ""
                parts.append(f"- {action.action} {target_desc} → {error}")
                parts.append(f"  建议: {self._generate_suggestion(error)}")

        return "\n".join(parts)

    def _generate_suggestion(self, error: str) -> str:
        """根据错误信息生成替代建议

        Args:
            error: 错误信息

        Returns:
            建议文本
        """
        error_lower = error.lower()

        if "元素未找到" in error or "not found" in error_lower:
            return "尝试使用 ID、placeholder、aria-label 或 name 属性定位"
        elif "超时" in error or "timeout" in error_lower:
            return "等待页面加载完成后再操作，或使用 wait 动作"
        elif "不可见" in error or "not visible" in error_lower:
            return "先滚动页面使元素可见，或展开隐藏的菜单"
        elif "被禁用" in error or "disabled" in error_lower:
            return "检查是否需要先完成前置操作"
        else:
            return "尝试换一种定位方式或操作顺序"

**Step 2: Run test to verify it passes**

Run: `cd /Users/huhu/project/weberpagent && python -m pytest backend/tests/test_memory.py -v`
Expected: All tests PASS

**Step 3: Commit**

```bash
git add backend/agent_simple/memory.py backend/tests/test_memory.py
git commit -m "feat(agent): 添加 Memory 记忆模块

- 支持短记忆（3-5 步）
- 格式化为 Prompt 文本
- 失败动作主动提示

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: 更新 __init__.py 导出 Memory

**Files:**
- Modify: `backend/agent_simple/__init__.py`

**Step 1: Add Memory to exports**

```python
"""自研简化版 Agent 模块"""

from backend.agent_simple.types import (
    Action,
    ActionResult,
    PageState,
    AgentResult,
    Step,
    Reflection,
    ReflectionStrategy,
    InteractiveElement,
    ActionType,
)
from backend.agent_simple.memory import Memory
from backend.agent_simple.perception import Perception
from backend.agent_simple.decision import Decision
from backend.agent_simple.executor import Executor
from backend.agent_simple.agent import SimpleAgent

__all__ = [
    "Action",
    "ActionResult",
    "PageState",
    "AgentResult",
    "Step",
    "Reflection",
    "ReflectionStrategy",
    "InteractiveElement",
    "ActionType",
    "Memory",
    "Perception",
    "Decision",
    "Executor",
    "SimpleAgent",
]
```

**Step 2: Verify import works**

Run: `cd /Users/huhu/project/weberpagent && python -c "from backend.agent_simple import Memory; print('OK')"`
Expected: "OK"

**Step 3: Commit**

```bash
git add backend/agent_simple/__init__.py
git commit -m "feat(agent): 导出 Memory 类

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 4: 修改 prompts.py 支持记忆上下文

**Files:**
- Modify: `backend/agent_simple/prompts.py`

**Step 1: Update build_user_prompt function signature**

找到 `build_user_prompt` 函数（约第 349 行），修改签名和实现：

```python
def build_user_prompt(task: str, state: PageState, memory_context: str = "") -> str:
    """构建用户提示词

    Args:
        task: 任务描述
        state: 页面状态
        memory_context: 记忆上下文（由 Memory.format_for_prompt() 生成）

    Returns:
        用户提示词字符串
    """
    elements_text = format_elements_for_prompt(state.elements[:30])

    # 判断页面状态
    page_status = ""
    if "百度搜索" in state.title or "wd=" in state.url or "q=" in state.url:
        page_status = "\n⚠️ 当前页面似乎是搜索结果页，如果任务是搜索，可能已完成！"
    elif state.url == "about:blank":
        page_status = "\n⚠️ 当前是空白页，需要先导航到目标网站。"

    # 构建完整 Prompt
    return f"""当前任务：{task}

{memory_context}

## 当前页面
- URL: {state.url}
- 标题: {state.title}{page_status}

## 可交互元素（前 30 个）
{elements_text}

## 提示
1. 先判断任务是否已完成（检查标题、URL）
2. 如果已完成，使用 done 动作标记完成
3. 如果未完成，选择合适的元素进行操作
4. 优先使用 ID 定位元素
5. ⚠️ 不要重复已失败的动作

请分析页面截图和元素列表，决定下一步动作。只输出 JSON 格式的动作。"""
```

**Step 2: Update build_messages function**

找到 `build_messages` 函数（约第 387 行），修改签名：

```python
def build_messages(task: str, state: PageState, memory_context: str = "") -> list[dict]:
    """构建发送给 LLM 的消息列表

    Args:
        task: 任务描述
        state: 页面状态
        memory_context: 记忆上下文

    Returns:
        OpenAI 格式的消息列表
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(task, state, memory_context)},
    ]
```

**Step 3: Verify syntax**

Run: `cd /Users/huhu/project/weberpagent && python -c "from backend.agent_simple.prompts import build_messages; print('OK')"`
Expected: "OK"

**Step 4: Commit**

```bash
git add backend/agent_simple/prompts.py
git commit -m "feat(agent): prompts 支持记忆上下文

- build_user_prompt 增加 memory_context 参数
- build_messages 传递记忆上下文

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 5: 修改 decision.py 接收 Memory 参数

**Files:**
- Modify: `backend/agent_simple/decision.py`

**Step 1: Add Memory import and update decide method**

```python
"""LLM 决策模块 - 调用模型生成动作"""

import json
import logging
import re
from backend.llm.base import BaseLLM
from backend.agent_simple.types import Action, PageState
from backend.agent_simple.prompts import build_messages

# 新增导入
from backend.agent_simple.memory import Memory

logger = logging.getLogger(__name__)


class Decision:
    """LLM 决策模块

    负责调用 LLM 并解析输出为结构化动作
    """

    def __init__(self, llm: BaseLLM):
        """初始化决策模块

        Args:
            llm: LLM 实例（支持 vision 的模型）
        """
        self.llm = llm

    async def decide(
        self,
        task: str,
        state: PageState,
        memory: Memory | None = None,  # 新增参数
    ) -> Action:
        """根据页面状态决定下一步动作

        Args:
            task: 任务描述
            state: 当前页面状态
            memory: 记忆模块（可选）

        Returns:
            Action: 解析后的动作对象
        """
        # 1. 获取记忆上下文
        memory_context = memory.format_for_prompt() if memory else ""

        # 2. 构建消息（传入记忆上下文）
        messages = build_messages(task, state, memory_context)

        # 3. 构建图像 URL（data URI 格式）
        if state.screenshot_base64 and len(state.screenshot_base64) > 100:
            image_url = f"data:image/png;base64,{state.screenshot_base64}"
            images = [image_url]
        else:
            logger.warning("截图无效，LLM 将仅基于 DOM 信息决策")
            images = []

        logger.info(f"调用 LLM 决策，模型: {self.llm.model_name}")

        # 4. 调用 LLM
        response = await self.llm.chat_with_vision(
            messages=messages,
            images=images,
        )

        logger.info(f"LLM 原始输出: {response.content[:200]}...")

        # 5. 解析输出
        action = self._parse_action(response.content)

        logger.info(f"解析后的动作: {action.action}, 目标: {action.target}")

        return action

    # ... _parse_action 和 _extract_json 方法保持不变
```

**Step 2: Verify syntax**

Run: `cd /Users/huhu/project/weberpagent && python -c "from backend.agent_simple.decision import Decision; print('OK')"`
Expected: "OK"

**Step 3: Commit**

```bash
git add backend/agent_simple/decision.py
git commit -m "feat(agent): decision 模块接收 Memory 参数

- decide 方法新增 memory 参数
- 将记忆上下文传递给 LLM

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 6: 修改 agent.py 集成 Memory

**Files:**
- Modify: `backend/agent_simple/agent.py`

**Step 1: Add Memory import and initialization**

在文件顶部添加导入：

```python
from backend.agent_simple.memory import Memory
```

在 `__init__` 方法中添加 Memory 初始化：

```python
def __init__(
    self,
    task: str,
    llm: BaseLLM,
    page: Page,
    output_dir: str = "outputs",
    max_steps: int = 20,
    max_retries: int = 3,
    timeout: int = 60000,
):
    # ... 现有代码 ...

    # 执行历史
    self.history: list[Step] = []

    # 🆕 记忆模块
    self.memory = Memory(max_steps=5)
```

**Step 2: Update run method to pass memory to decision**

在 `run` 方法中，修改决策调用：

```python
async def run(self) -> AgentResult:
    # ... 现有代码 ...

    for step_num in range(1, self.max_steps + 1):
        # ... 日志和循环检测代码 ...

        # 1. 感知页面
        state = await self.perception.get_state()

        # 2. LLM 决策（传入记忆）
        action = await self.decision.decide(self.task, state, self.memory)  # 🆕 传入 memory

        # 3. 执行动作（带反思重试）
        result = await self._execute_with_reflection(action, state, step_num)

        # 4. 记录历史
        step = Step(
            step_num=step_num,
            state=state,
            action=action,
            result=result,
        )
        self.history.append(step)
        self.memory.add_step(step)  # 🆕 同时更新记忆

        # ... 后续代码不变 ...
```

**Step 3: Verify syntax**

Run: `cd /Users/huhu/project/weberpagent && python -c "from backend.agent_simple.agent import SimpleAgent; print('OK')"`
Expected: "OK"

**Step 4: Commit**

```bash
git add backend/agent_simple/agent.py
git commit -m "feat(agent): SimpleAgent 集成 Memory 模块

- 初始化 Memory 实例
- 决策时传入记忆
- 每步更新记忆

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 7: 集成测试验证

**Files:**
- Run: 现有 Agent 测试

**Step 1: Run existing agent test**

Run: `cd /Users/huhu/project/weberpagent && python -m pytest backend/tests/test_agent.py -v -s`
Expected: 测试运行，观察日志中是否有记忆上下文

**Step 2: Manual verification with test script**

创建简单验证脚本 `backend/tests/test_memory_integration.py`:

```python
"""记忆模块集成测试"""

import asyncio
from backend.agent_simple.memory import Memory
from backend.agent_simple.types import Step, Action, ActionResult, PageState


async def test_memory_integration():
    """测试记忆模块在模拟流程中的表现"""
    memory = Memory(max_steps=5)

    # 模拟登录流程
    steps = [
        Step(
            step_num=1,
            state=PageState(screenshot_base64="", url="https://example.com/login", title="登录"),
            action=Action(thought="点击登录", action="click", target="登录", done=False),
            result=ActionResult(success=True),
        ),
        Step(
            step_num=2,
            state=PageState(screenshot_base64="", url="https://example.com/login", title="登录"),
            action=Action(thought="输入账号", action="input", target="账号", value="test", done=False),
            result=ActionResult(success=False, error="元素未找到"),
        ),
        Step(
            step_num=3,
            state=PageState(screenshot_base64="", url="https://example.com/login", title="登录"),
            action=Action(thought="用 ID 输入账号", action="input", target="account", value="test", done=False),
            result=ActionResult(success=True),
        ),
    ]

    for step in steps:
        memory.add_step(step)

    # 打印格式化的记忆
    print("\n" + "=" * 60)
    print("记忆上下文输出:")
    print("=" * 60)
    print(memory.format_for_prompt())
    print("=" * 60)

    # 验证
    assert len(memory.steps) == 3
    assert len(memory.get_failed_actions()) == 1

    failed_actions = memory.get_failed_actions()
    assert failed_actions[0][0].target == "账号"
    assert "元素未找到" in failed_actions[0][1]

    print("\n✅ 集成测试通过!")


if __name__ == "__main__":
    asyncio.run(test_memory_integration())
```

Run: `cd /Users/huhu/project/weberpagent && python -m backend.tests.test_memory_integration`
Expected: 输出记忆上下文，测试通过

**Step 3: Final commit**

```bash
git add backend/tests/test_memory_integration.py
git commit -m "test(agent): 添加记忆模块集成测试

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 8: 更新调优文档

**Files:**
- Modify: `docs/3_agent调优.md`

**Step 1: Add tuning record**

在调优记录表格中添加新条目：

| 时间 | 触发原因 | 调优经过 | 调优结果 | 下一步建议 |
|------|----------|----------|----------|------------|
| 2026-03-10 | Agent 陷入死循环，AI 看不到历史操作 | 新增 Memory 模块，在 User Prompt 中注入最近 3-5 步操作记录和失败警告 | 待验证 | 如果 Token 消耗过高，可考虑压缩记忆格式 |

**Step 2: Commit**

```bash
git add docs/3_agent调优.md
git commit -m "docs: 记录记忆机制调优

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Summary

| Task | Description | Files |
|------|-------------|-------|
| 1 | 创建 Memory 单元测试 | `backend/tests/test_memory.py` |
| 2 | 实现 Memory 模块 | `backend/agent_simple/memory.py` |
| 3 | 更新模块导出 | `backend/agent_simple/__init__.py` |
| 4 | 修改 prompts 支持记忆 | `backend/agent_simple/prompts.py` |
| 5 | 修改 decision 接收 Memory | `backend/agent_simple/decision.py` |
| 6 | 修改 agent 集成 Memory | `backend/agent_simple/agent.py` |
| 7 | 集成测试验证 | `backend/tests/test_memory_integration.py` |
| 8 | 更新调优文档 | `docs/3_agent调优.md` |

**预计耗时:** 1-2 小时

