# 简化版 Agent 设计文档

## 1. 背景

### 问题

Browser-Use 框架与国产模型存在兼容性问题：

| 模型 | 问题 |
|------|------|
| Azure OpenAI | 内容过滤器触发（jailbreak 检测）|
| DeepSeek | 无法输出复杂的 AgentOutput JSON Schema |
| 通义千问 | 无法输出 action 字段 |

### 解决方案

**自己实现简化版 Agent**，核心代码约 200-300 行。

---

## 2. 架构设计

### 2.1 整体流程

```
┌─────────────────────────────────────────────────────────────┐
│                      SimpleAgent                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ 感知模块  │───▶│ 决策模块  │───▶│ 执行模块  │              │
│  │Perception│    │ Decision │    │ Executor │              │
│  └──────────┘    └──────────┘    └──────────┘              │
│       │              │               │                      │
│       ▼              ▼               ▼                      │
│  ┌─────────────────────────────────────────────┐           │
│  │              循环控制 (Loop Controller)       │           │
│  └─────────────────────────────────────────────┘           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 模块职责

| 模块 | 文件 | 职责 |
|------|------|------|
| **Perception** | `perception.py` | 获取截图、提取可交互元素、构建页面描述 |
| **Decision** | `decision.py` | 调用 LLM、解析输出、生成动作 |
| **Executor** | `executor.py` | 执行 Playwright 动作（click/input/navigate） |
| **Agent** | `agent.py` | 主循环、状态管理、错误处理 |
| **Prompts** | `prompts.py` | Prompt 模板，针对国产模型优化 |

---

## 3. 核心设计

### 3.1 简化的输出格式

**Browser-Use 的复杂格式**（国产模型难以输出）：
```json
{
  "action": [
    {
      "click": {"index": 14, "num_clicks": 1},
      "interacted_element": {...}
    }
  ]
}
```

**我们简化后的格式**：
```json
{
  "thought": "分析当前页面，发现需要切换到密码登录",
  "action": "click",
  "target": "密码登录",
  "value": null,
  "done": false
}
```

### 3.2 支持的动作类型

| 动作 | 参数 | 示例 |
|------|------|------|
| `navigate` | url | `{"action": "navigate", "url": "https://..."}` |
| `click` | target | `{"action": "click", "target": "登录按钮"}` |
| `input` | target, value | `{"action": "input", "target": "用户名", "value": "admin"}` |
| `wait` | - | `{"action": "wait"}` |
| `done` | result | `{"action": "done", "done": true, "value": "登录成功"}` |

### 3.3 元素定位策略

**优先级**：
1. **文本匹配** - 通过按钮/输入框的文本内容定位
2. **CSS 选择器** - 通过 id/class/data 属性定位
3. **索引定位** - 通过可交互元素列表的索引定位

---

## 4. Prompt 设计

### 4.1 系统提示词

```
你是一个浏览器自动化助手，负责执行用户指定的网页操作任务。

当前任务：{task}

你可以执行以下动作：
- navigate: 打开网页，参数为 url
- click: 点击元素，参数为 target（元素的文本或描述）
- input: 输入文本，参数为 target 和 value
- wait: 等待页面加载
- done: 任务完成，参数为 result（完成说明）

输出格式（JSON）：
{
  "thought": "你的思考过程",
  "action": "动作类型",
  "target": "目标元素描述（click/input 时需要）",
  "value": "输入值（input 时需要）",
  "done": false
}

任务完成后设置 done: true。
```

### 4.2 用户提示词模板

```
当前页面状态：
{page_description}

可交互元素：
{interactive_elements}

请分析页面状态，决定下一步动作。
```

---

## 5. 代码实现

### 5.1 目录结构

```
backend/agent_simple/
├── __init__.py
├── agent.py          # SimpleAgent 主类
├── perception.py     # 页面感知
├── decision.py       # LLM 决策
├── executor.py       # 动作执行
├── prompts.py        # Prompt 模板
└── types.py          # 类型定义
```

### 5.2 核心类设计

```python
# agent.py
class SimpleAgent:
    def __init__(self, task: str, llm: BaseLLM, page: Page):
        self.task = task
        self.llm = llm
        self.page = page
        self.perception = Perception(page)
        self.decision = Decision(llm)
        self.executor = Executor(page)
        self.history: list[Step] = []
        self.max_steps = 20

    async def run(self) -> AgentResult:
        for step_num in range(self.max_steps):
            # 1. 感知页面
            state = await self.perception.get_state()

            # 2. LLM 决策
            action = await self.decision.decide(
                task=self.task,
                state=state,
                history=self.history
            )

            # 3. 执行动作
            result = await self.executor.execute(action)

            # 4. 记录历史
            self.history.append(Step(state, action, result))

            # 5. 检查完成
            if action.done:
                return AgentResult(success=True, result=action.value)

        return AgentResult(success=False, error="超过最大步数")
```

### 5.3 感知模块

```python
# perception.py
class Perception:
    async def get_state(self) -> PageState:
        # 1. 截图
        screenshot = await self.page.screenshot()

        # 2. 获取可交互元素
        elements = await self.page.evaluate("""
            () => {
                const interactive = [];
                document.querySelectorAll('button, a, input, select, textarea, [onclick], [role="button"]')
                    .forEach((el, i) => {
                        interactive.push({
                            index: i,
                            tag: el.tagName,
                            text: el.innerText?.slice(0, 50),
                            type: el.type,
                            id: el.id,
                            class: el.className
                        });
                    });
                return interactive;
            }
        """)

        return PageState(screenshot=screenshot, elements=elements)
```

### 5.4 决策模块

```python
# decision.py
class Decision:
    async def decide(self, task, state, history) -> Action:
        # 构建 prompt
        messages = self._build_messages(task, state, history)

        # 调用 LLM
        response = await self.llm.chat_with_vision(
            messages=messages,
            images=[state.screenshot_base64]
        )

        # 解析输出
        return self._parse_action(response.content)
```

### 5.5 执行模块

```python
# executor.py
class Executor:
    async def execute(self, action: Action) -> ActionResult:
        if action.type == "navigate":
            await self.page.goto(action.url)
        elif action.type == "click":
            await self._click_element(action.target)
        elif action.type == "input":
            await self._input_text(action.target, action.value)
        elif action.type == "wait":
            await self.page.wait_for_timeout(1000)

    async def _click_element(self, target: str):
        # 优先通过文本定位
        try:
            await self.page.get_by_text(target).click()
        except:
            # fallback: 通过索引定位
            await self.page.evaluate(f"document.querySelectorAll('[data-idx]')[{target}].click()")
```

---

## 6. 与 Browser-Use 对比

| 特性 | Browser-Use | 简化版 Agent |
|------|-------------|--------------|
| 代码量 | ~10000+ 行 | ~300 行 |
| 输出格式 | 复杂 AgentOutput | 简单 JSON |
| 元素定位 | 多种策略 | 文本 + 索引 |
| 错误恢复 | 复杂机制 | 简单重试 |
| 国产模型兼容 | ❌ 不兼容 | ✅ 优化适配 |
| 自愈能力 | 较强 | 基础 |

---

## 7. 实施计划

### Phase 3.2-3.7 任务拆分

| 任务 | 预计时间 | 产出 |
|------|----------|------|
| 3.2 设计简化版 Agent 架构 | 0.5 天 | 本文档 |
| 3.3 实现页面感知模块 | 0.5 天 | `perception.py` |
| 3.4 实现 LLM 决策模块 | 0.5 天 | `decision.py`, `prompts.py` |
| 3.5 实现动作执行模块 | 0.5 天 | `executor.py` |
| 3.6 实现循环控制模块 | 0.5 天 | `agent.py` |
| 3.7 验证基础执行流程 | 0.5 天 | 测试通过 |

**总计：2-3 天**

---

## 8. 验收标准

1. **登录场景** - 能完成完整的登录流程（切换 tab → 输入 → 点击登录）
2. **输出正确** - LLM 能稳定输出正确格式的 JSON
3. **截图完整** - 每步都有截图记录
4. **日志清晰** - 每步的 thought/action/result 都有记录

---

## 9. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 元素定位失败 | 动作无法执行 | 多种定位策略 fallback |
| LLM 输出格式错误 | 无法解析动作 | 添加格式修复逻辑 |
| 页面加载慢 | 超时 | 增加等待机制 |

---

## 10. 后续扩展

1. **增强定位** - 添加更多元素定位策略
2. **自愈能力** - 失败后自动分析原因并重试
3. **多标签页** - 支持多标签页操作
4. **数据提取** - 支持从页面提取数据
