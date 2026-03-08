# Phase 3: Agent 改造设计文档

> 创建日期: 2026-03-08
> 状态: 已批准

## 1. 概述

### 目标
将国内模型（通义千问）集成到 Browser-Use 框架，实现 AI 决策 + Playwright 执行的技术闭环。

### 方案选择
**方案 C: 混合方案** - LLM 适配器 + 自定义 System Prompt 扩展

理由：
- 通过 LLM 适配器复用 Browser-Use 的核心执行流程
- 通过 `extend_system_message` 参数注入中文化 Prompt
- 改动量可控，且保留了后续扩展的灵活性

### 测试目标
- URL: https://erptest.epbox.cn/
- 账号: Y59800075
- 密码: Aa123456

---

## 2. 模块设计

### 2.1 LLM 适配器

**文件**: `backend/llm/browser_use_adapter.py`

将国内模型适配到 Browser-Use 的 `BaseChatModel` Protocol。

```python
class BrowserUseAdapter(BaseChatModel):
    """将国内模型适配到 Browser-Use 的 BaseChatModel Protocol"""

    def __init__(self, llm: BaseLLM):
        self._llm = llm  # QwenChat 实例
        self.model = llm.model_name

    async def ainvoke(
        self,
        messages: list[BaseMessage],
        output_format: type[BaseModel] | None = None
    ) -> ChatInvokeCompletion:
        # 1. 转换消息格式 (BaseMessage → OpenAI 格式)
        # 2. 提取图像（如果有）
        # 3. 调用底层 LLM
        # 4. 解析输出为 AgentOutput 格式
        pass
```

**关键转换逻辑**:
- 消息格式: Browser-Use 使用 `BaseMessage`，QwenChat 使用 OpenAI 格式 `dict`
- 图像处理: 从消息中提取 `ContentPartImageParam`，转为 base64
- 输出解析: 将 LLM 文本输出解析为 `AgentOutput`

---

### 2.2 Prompt 模板

**文件**: `backend/agent/prompts.py`

利用 Browser-Use 的 `extend_system_message` 参数追加中文增强指令：

```python
CHINESE_ENHANCEMENT = """
## 中文页面处理增强

1. **元素识别优先级**
   - 优先使用可见文本（按钮文字、链接文字）
   - 其次使用 placeholder 属性
   - 最后使用 aria-label 或 title

2. **常见中文表单字段**
   - 用户名/账号: username, account, login
   - 密码: password, pwd, passwd
   - 登录: 登录, 登入, 确定, 提交
   - 搜索: 搜索, 查询, 检索

3. **错误处理**
   - 遇到验证码时，等待 5 秒后重试
   - 页面加载超时时，刷新页面
   - 元素未找到时，先滚动页面再查找

4. **动作输出格式**
   始终输出 JSON 格式：
   {"action": "click", "selector": "...", "value": "...", "reasoning": "..."}
"""
```

---

### 2.3 Agent 封装类

**文件**: `backend/agent/browser_agent.py`

```python
class UIBrowserAgent:
    """封装 Browser-Use Agent，集成国内模型"""

    def __init__(
        self,
        task: str,
        llm: BaseLLM,
        output_dir: str = "outputs",
    ):
        self.adapter = BrowserUseAdapter(llm)
        self.task = task
        self.output_dir = output_dir

    async def run(self) -> AgentHistoryList:
        agent = Agent(
            task=self.task,
            llm=self.adapter,
            extend_system_message=CHINESE_ENHANCEMENT,
            save_conversation_path=f"{self.output_dir}/conversations",
            max_failures=3,
        )
        return await agent.run()
```

---

### 2.4 截图和日志

**文件**: `backend/utils/logger.py`

```python
class StructuredLogger:
    """结构化日志，便于后续分析"""

    def __init__(self, output_dir: str, task_id: str):
        self.log_file = Path(output_dir) / "logs" / f"{task_id}.jsonl"

    def log_step(
        self,
        step: int,
        action: str,
        selector: str | None,
        reasoning: str,
        success: bool,
        screenshot_path: str | None = None,
        error: str | None = None,
    ):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "action": action,
            "selector": selector,
            "reasoning": reasoning,
            "success": success,
            "screenshot": screenshot_path,
            "error": error,
        }
        # 写入 JSONL 文件
```

**文件**: `backend/utils/screenshot.py`

```python
class ScreenshotManager:
    """截图文件管理"""

    def __init__(self, output_dir: str, task_id: str):
        self.screenshot_dir = Path(output_dir) / "screenshots" / task_id

    def get_path(self, step: int, suffix: str = "") -> str:
        filename = f"step_{step:03d}{suffix}.png"
        return str(self.screenshot_dir / filename)
```

---

### 2.5 验证脚本

**文件**: `backend/tests/verify_agent.py`

```python
async def verify_basic_flow():
    """验证 Agent 基础执行流程"""
    llm = QwenChat(model="qwen-vl-max")
    agent = UIBrowserAgent(
        task="打开 https://erptest.epbox.cn/ 并截图",
        llm=llm,
        output_dir="outputs/verify",
    )
    result = await agent.run()
    print(f"执行步数: {len(result.history)}")
    return result
```

**文件**: `backend/tests/test_login.py`

```python
@pytest.mark.asyncio
async def test_login_flow():
    """测试登录场景"""
    agent = UIBrowserAgent(
        task="登录 erptest.epbox.cn，账号 Y59800075，密码 Aa123456",
        llm=QwenChat(),
        output_dir="outputs/tests/login",
    )
    result = await agent.run()
    assert result.is_done
```

---

## 3. 文件结构

```
backend/
├── agent/
│   ├── __init__.py
│   ├── browser_agent.py     # Agent 封装类
│   └── prompts.py           # 中文化 Prompt
│
├── llm/
│   ├── __init__.py
│   ├── base.py              # 已有
│   ├── qwen.py              # 已有
│   ├── utils.py             # 已有
│   └── browser_use_adapter.py  # 新增 - Browser-Use 适配器
│
├── utils/
│   ├── __init__.py
│   ├── logger.py            # 新增 - 结构化日志
│   └── screenshot.py        # 新增 - 截图管理
│
├── config/
│   └── test_targets.yaml    # 测试目标配置
│
└── tests/
    ├── verify_agent.py      # Agent 基础验证
    └── test_login.py        # 登录场景测试
```

---

## 4. Phase 3 任务清单

| 任务 | 描述 | 状态 |
|------|------|------|
| 3.1 | 实现 BrowserUseAdapter 适配器 | 待完成 |
| 3.2 | 实现 UIBrowserAgent 封装类 | 待完成 |
| 3.3 | 实现中文化 Prompt 模板 | 待完成 |
| 3.4 | 实现截图和日志工具 | 待完成 |
| 3.5 | 编写验证脚本和测试用例 | 待完成 |
| 3.6 | 使用 erptest.epbox.cn 验证登录流程 | 待完成 |

---

## 5. 验收标准

- [ ] BrowserUseAdapter 能成功调用通义千问
- [ ] Agent 能完成打开页面并截图
- [ ] Agent 能完成登录场景（识别输入框、填写、点击登录）
- [ ] 每步截图保存到 outputs/screenshots/
- [ ] 执行日志保存到 outputs/logs/
