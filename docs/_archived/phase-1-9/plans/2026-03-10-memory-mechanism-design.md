# Agent 记忆机制设计文档

## 背景

当前 SimpleAgent 存在死循环问题：LLM 每次决策时只看到当前页面状态，不知道之前做了什么，容易重复执行相同动作。

虽然已有 `_build_history_context()` 方法，但只在反思（reflection）时使用，正常决策流程中没有历史上下文。

## 需求

| 维度 | 选择 |
|------|------|
| 使用场景 | 全部（决策辅助 + 失败学习 + 进度追踪） |
| 时间范围 | 短记忆（3-5 步） |
| 内容格式 | 标准版（动作 + 目标 + 思考 + 错误信息） |
| 传递方式 | User Prompt 注入 |
| 失败处理 | 主动提示（列出失败动作 + 建议替代方案） |

## 方案

**独立 Memory 模块**

新增 `memory.py` 文件，职责清晰，易于维护和扩展。

## 文件结构

```
backend/agent_simple/
├── __init__.py
├── types.py           # 现有类型（无需改动）
├── memory.py          # 🆕 记忆模块
├── perception.py      # 无需改动
├── prompts.py         # 需要修改
├── decision.py        # 需要修改
├── executor.py        # 无需改动
└── agent.py           # 需要修改
```

## Memory 模块设计

### 类定义

```python
# memory.py

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
        """添加步骤，超出容量时移除最旧的"""

    def get_recent_steps(self) -> list[Step]:
        """获取最近的步骤（最多 max_steps 个）"""

    def get_failed_actions(self) -> list[tuple[Action, str]]:
        """获取失败的动作及其错误信息"""

    def format_for_prompt(self) -> str:
        """格式化为 Prompt 文本

        输出格式：
        ## 📋 最近操作记录
        Step 1: click "登录"
          思考: ...
          结果: ✅ 成功

        ## ⚠️ 失败动作警告
        - input 目标="账号" → 元素未找到
          建议: 尝试使用 ID、placeholder 或 aria-label 定位
        """
```

### 核心方法实现思路

#### `add_step(step: Step)`

```python
def add_step(self, step: Step) -> None:
    self.steps.append(step)
    # 超出容量时移除最旧的
    if len(self.steps) > self.max_steps:
        self.steps.pop(0)
```

#### `get_failed_actions()`

```python
def get_failed_actions(self) -> list[tuple[Action, str]]:
    return [
        (step.action, step.result.error or "未知错误")
        for step in self.steps
        if not step.result.success
    ]
```

#### `format_for_prompt()`

生成三部分内容：
1. **最近操作记录** - 遍历 `self.steps`，格式化输出
2. **失败动作警告** - 从失败动作中提取，生成警告文本
3. **替代建议** - 基于失败原因生成通用建议

## Prompt 输出格式

当有历史记录时，User Prompt 格式：

```
当前任务：{task}

## 📋 最近操作记录
Step 1: click "登录"
  思考: 点击登录按钮进入登录页
  结果: ✅ 成功

Step 2: input "账号" = "test"
  思考: 输入用户名
  结果: ❌ 元素未找到

## ⚠️ 失败动作警告
- input 目标="账号" → 元素未找到
  建议: 尝试使用 ID、placeholder 或 aria-label 定位

## 当前页面
- URL: /login
- 标题: 用户登录

## 可交互元素（前 30 个）
[0] <INPUT> | ID: "account" | 占位符: "请输入账号"
...
```

当没有历史记录时（第一步）：

```
当前任务：{task}

## 📋 操作记录
（这是第一步）

## 当前页面
- URL: about:blank
...
```

## 需要修改的文件

### 1. `memory.py`（新增）

- 创建 `Memory` 类
- 实现上述方法

### 2. `prompts.py`（修改）

```python
# 修改 build_user_prompt 函数签名
def build_user_prompt(task: str, state: PageState, memory_context: str = "") -> str:
    # 在 Prompt 中注入 memory_context
```

### 3. `decision.py`（修改）

```python
# 修改 decide 方法签名
async def decide(
    self,
    task: str,
    state: PageState,
    memory: Memory | None = None,  # 新增参数
) -> Action:
    memory_context = memory.format_for_prompt() if memory else ""
    messages = build_messages(task, state, memory_context)
```

### 4. `agent.py`（修改）

```python
from backend.agent_simple.memory import Memory

class SimpleAgent:
    def __init__(self, ...):
        # 新增
        self.memory = Memory(max_steps=5)

    async def run(self) -> AgentResult:
        for step_num in range(1, self.max_steps + 1):
            # 感知
            state = await self.perception.get_state()

            # 决策（传入记忆）
            action = await self.decision.decide(self.task, state, self.memory)

            # 执行
            result = await self._execute_with_reflection(action, state, step_num)

            # 记录历史
            step = Step(...)
            self.history.append(step)
            self.memory.add_step(step)  # 🆕 同时更新记忆
```

## 调用流程

```
┌─────────────────────────────────────────────────────────┐
│                      SimpleAgent                         │
│                                                          │
│  ┌──────────┐                                            │
│  │   Loop   │                                            │
│  └────┬─────┘                                            │
│       │                                                   │
│       ▼                                                   │
│  1. perception.get_state() → PageState                   │
│       │                                                   │
│       ▼                                                   │
│  2. memory.format_for_prompt() → 历史记忆文本            │
│       │                                                   │
│       ▼                                                   │
│  3. decision.decide(task, state, memory) → Action        │
│       │                                                   │
│       ▼                                                   │
│  4. executor.execute(action) → ActionResult              │
│       │                                                   │
│       ▼                                                   │
│  5. memory.add_step(Step) → 更新记忆                     │
│       │                                                   │
│       ▼                                                   │
│  6. 检查 done → 结束或继续循环                            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 测试计划

1. **单元测试** - `test_memory.py`
   - 测试 `add_step` 容量限制
   - 测试 `get_failed_actions` 过滤
   - 测试 `format_for_prompt` 输出格式

2. **集成测试** - 修改现有 `test_agent.py`
   - 验证记忆是否正确传递给 LLM
   - 验证失败动作警告是否生效

3. **场景测试** - 运行现有登录场景
   - 对比添加记忆前后的表现
   - 记录循环次数变化

## 预期效果

| 指标 | 改进前 | 改进后（预期） |
|------|--------|----------------|
| 循环检测触发次数 | 频繁 | 显著减少 |
| 失败动作重复率 | 高 | 低 |
| 任务完成步数 | 多（因重复） | 更精简 |
| Token 消耗 | - | 略增（记忆文本） |

## 后续扩展方向

1. **长记忆** - 支持更多步骤，通过摘要压缩
2. **持久化** - 保存到文件/数据库，跨任务复用
3. **智能建议** - 基于失败模式生成更精准的替代方案
4. **跨任务记忆** - 记住常见操作模式，加速新任务
