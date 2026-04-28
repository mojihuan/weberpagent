# 逐步代码生成设计

**日期:** 2026-04-28
**状态:** Approved

## 问题

当前代码生成流程是"事后一次性翻译"——agent 全部执行完后，`PlaywrightCodeGenerator.generate_and_save()` 遍历所有 `model_actions()` 批量翻译为 Playwright 代码。问题：

1. **定位器脆弱** — 绝对 XPath (`html/body/div[1]/...`) 在 ERP 系统中几乎 100% 会变
2. **缺少等待策略** — agent 执行时有真实浏览器等待，生成代码只有固定 `wait_for_timeout`
3. **上下文丢失** — 弱步骤事后修复时 DOM 快照可能已过时
4. **自愈重试超时** — 生成的代码 pytest 执行时定位器全部失败，3 次自愈全部超时

## 方案：逐步即时生成

**核心改动：** 代码翻译从"agent 完成后批量翻译"改为"每步成功后即时翻译"。

### 三阶段流程

```
阶段 1: Agent 执行（不变）
  → 每步 step_callback 捕获 DOM + interacted_element + action
  → 新增：StepCodeBuffer.append_step() 即时翻译
  → 新增：智能等待推导
  → agent 全部完成

阶段 2: 组装文件（简化）
  → 前置条件代码 + buffer.steps + 断言代码
  → 写入 .py 文件

阶段 3: Self-healing 验证（不变）
  → SelfHealingRunner.run() 作为最终兜底
```

### 新增组件

#### StepCodeBuffer（新文件 `backend/core/step_code_buffer.py`）

逐步代码缓冲区，在 step_callback 中逐条追加。

```python
@dataclass
class BufferedStep:
    action: TranslatedAction
    wait_before: str | None  # 自动推导的等待代码
    step_index: int

class StepCodeBuffer:
    """逐步代码缓冲区——在 step_callback 中即时翻译每步操作。

    替代 PlaywrightCodeGenerator._heal_weak_steps() 的批量修复逻辑，
    改为每步即时翻译，DOM 上下文最新，修复成功率更高。
    """

    steps: list[BufferedStep]
    _translator: ActionTranslator
    _llm_snippets: dict[int, str]  # 即时 LLM 修复结果缓存

    def append_step(
        self,
        action: dict,
        step_index: int,
        elapsed_ms: int = 0,
        prev_action_type: str | None = None,
    ) -> None:
        """翻译单个操作并追加到缓冲区。

        1. 识别弱步骤（elem=None 或 <=1 locator）
        2. 弱步骤即时 LLM 修复（用当前 DOM 快照）
        3. 翻译为 Playwright 代码
        4. 推导等待代码
        5. 追加到缓冲区
        """

    def _derive_wait(
        self,
        elapsed_ms: int,
        prev_action_type: str | None,
    ) -> str | None:
        """根据实际耗时推导等待代码。

        | 条件                         | 插入代码                                              |
        |------------------------------|------------------------------------------------------|
        | 上一步是 navigate            | page.wait_for_load_state("networkidle", timeout=10000) |
        | 步骤间耗时 > 800ms           | page.wait_for_timeout(elapsed_ms)                    |
        | 上一步是 click（菜单展开）    | page.wait_for_timeout(300)                           |
        """

    def assemble(
        self,
        header: str,
        precondition: str | None,
        assertions: str | None,
    ) -> str:
        """组装完整测试文件内容。"""
```

### 数据流

```
step_callback (runs.py)
    │
    ├── 现有：DOM 快照 + 截图 → Step DB + SSE
    │
    └── 新增：buffer.append_step(action, step_index, elapsed_ms)
          │
          ├── ActionTranslator.translate_with_llm(action)
          │     复用现有翻译逻辑
          │
          ├── 弱步骤即时 LLM 修复（替代 _heal_weak_steps）
          │     DOM 是最新的，修复成功率高
          │
          ├── _derive_wait(elapsed_ms, prev_action_type)
          │     智能等待推导
          │
          └── 追加到 buffer.steps

agent 完成后 (runs.py)
    │
    └── buffer.assemble(header, precondition, assertions)
          → 写入 .py 文件
          → SelfHealingRunner.run() 验证
```

### 智能等待策略

根据 agent 实际执行数据推导等待代码，替代固定的 `wait_for_timeout`：

| 条件 | 插入代码 |
|---|---|
| 上一步是 `navigate` | `page.wait_for_load_state("networkidle", timeout=10000)` |
| 步骤间耗时 > 800ms | `page.wait_for_timeout(实际耗时ms)` |
| 上一步是 `click`（可能是菜单展开） | `page.wait_for_timeout(300)` |

### 错误处理

- **翻译失败** → 生成占位符注释 `# TODO: 翻译失败 step_N`，不阻塞 agent
- **弱步骤 LLM 修复失败** → 保留占位符，记录 warning
- **Self-healing** → 保持不变，作为最终兜底

### 改动范围

| 文件 | 改动类型 | 说明 |
|---|---|---|
| `backend/core/step_code_buffer.py` | **新增** | 逐步代码缓冲区 |
| `backend/api/routes/runs.py` | 修改 | step_callback 增加 buffer.append_step() |
| `backend/core/code_generator.py` | 简化 | 保留 generate() 用于组装，去掉 _heal_weak_steps |

### 不改动

- `action_translator.py` — 完全复用
- `locator_chain_builder.py` — 完全复用
- `agent_service.py` — 完全复用
- `self_healing_runner.py` — 保持不变
- `llm_healer.py` — 保持不变（被 StepCodeBuffer 即时调用）

## 预期收益

1. **定位器更可靠** — 每步有最新 DOM 上下文，弱步骤即时修复
2. **等待更智能** — 根据实际耗时推导，不再依赖固定 timeout
3. **问题更早发现** — 翻译失败立即知道，不用等到 pytest 才发现
4. **代码更简洁** — 去掉 _heal_weak_steps 的批量修复逻辑
