# Phase 111: StepCodeBuffer 核心实现 - Research

**Researched:** 2026-04-28
**Domain:** 逐步代码翻译缓冲区，累积 TranslatedAction 并组装完整测试文件
**Confidence:** HIGH

## Summary

StepCodeBuffer 是一个独立的数据结构，在 agent 执行过程中逐步累积翻译后的操作，替代当前 PlaywrightCodeGenerator.generate_and_save() 的"事后批量翻译"模式。它封装了三个核心行为：同步单步翻译（append_step）、异步弱步骤修复（append_step_async）、最终组装（assemble）。

研究基于对现有 ActionTranslator、PlaywrightCodeGenerator、LLMHealer、LocatorChainBuilder 四个核心模块的完整源码分析。所有被复用的 API 签名、数据结构、文件路径约定均已验证，不存在接口不兼容或路径假设错误的风险。

**Primary recommendation:** 新建 `backend/core/step_code_buffer.py`，内部组合 ActionTranslator + LLMHealer + PlaywrightCodeGenerator，使用 frozen dataclass StepRecord 包装翻译结果。assemble() 委托给 PlaywrightCodeGenerator.generate() 实现最大化复用。

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 新建 `StepRecord` frozen dataclass，包装 `TranslatedAction` + `wait_before: str` + `step_index: int`。不修改现有 TranslatedAction
- Buffer 内部存储为 `list[StepRecord]`，step_index 自动递增
- **D-02:** Buffer 构造时接收 `base_dir` 和 `run_id`，`append_step_async()` 从磁盘读取 DOM 快照文件（`{base_dir}/{run_id}/dom/step_{n}.txt`）
- **D-03:** LLM 修复采用同步阻塞模式 -- `append_step_async()` 调用 `LLMHealer.heal()` 并等待结果
- **D-04:** `_derive_wait()` 的操作耗时由调用方通过 `duration: float | None = None` 参数传入
- **D-05:** `assemble()` 委托给现有 `PlaywrightCodeGenerator.generate()` 组装完整测试文件
- **D-06:** `wait_before` 等待代码作为独立的 `TranslatedAction` 插入到主操作 action 之前

### Claude's Discretion
- StepRecord 的具体字段命名和默认值
- `_derive_wait()` 的 navigate 操作检测逻辑（action_type 判断）
- `append_step_async()` 内部错误处理和 fallback 策略
- Buffer 的构造函数签名细节（哪些参数必选 vs 可选）
- 单元测试文件组织和覆盖粒度
- LLM 配置传递方式（llm_config 参数 vs 全局配置）

### Deferred Ideas (OUT OF SCOPE)
None
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| CODEGEN-01 | append_step() 同步翻译单步操作，复用 ActionTranslator，存储 TranslatedAction + wait_before + step_index | ActionTranslator.translate() 接受 dict 返回 TranslatedAction (line 64); StepRecord frozen dataclass 包装结果; _derive_wait() 生成 wait_before 字符串 |
| CODEGEN-02 | append_step_async() 检测弱步骤，即时调用 LLMHealer 修复 | LLMHealer.heal() 是 async (line 191); 弱步骤检测复用 LocatorChainBuilder.extract() 返回值长度; DOM 路径 {base_dir}/{run_id}/dom/step_{n}.txt (1-indexed) |
| CODEGEN-03 | _derive_wait() 智能等待推导 -- navigate/耗时/click 三策略 | ActionTranslator._identify_action_type() 提取 action_type; duration 参数由调用方传入 (D-04); wait TranslatedAction 构造方式参考 _translate_wait() |
| CODEGEN-04 | assemble() 组装完整测试文件 | PlaywrightCodeGenerator.generate() 接受 list[TranslatedAction] + precondition_config + assertions_config (line 39); StepRecord 展平为 TranslatedAction 列表 |
| VAL-01 | 单元测试覆盖 append 同步/异步、wait 推导、assemble 组装、空 buffer、语法验证 | pytest + pytest-asyncio (auto mode); 现有 test_code_generator.py 测试模式参考; TranslatedAction fixture 构造方式已记录 |
</phase_requirements>

## Standard Stack

### Core (全部复用现有，无新依赖)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| dataclasses (stdlib) | Python 3.11+ | StepRecord frozen dataclass | 项目约定: frozen dataclass 用于不可变数据对象 |
| ast (stdlib) | Python 3.11+ | 语法验证 | PlaywrightCodeGenerator.validate_syntax() 已使用此模式 |
| pathlib (stdlib) | Python 3.11+ | DOM 快照文件读取 | 现有代码一致使用 Path |
| logging (stdlib) | Python 3.11+ | 日志记录 | 全项目统一 |

### 复用的项目内部模块

| Module | Purpose | How Used |
|--------|---------|----------|
| backend.core.action_translator | ActionTranslator.translate() 翻译操作 | append_step() 调用 translate(action_dict) 获取 TranslatedAction |
| backend.core.action_translator | ActionTranslator._identify_action_type() | _derive_wait() 中识别 navigate/click 等操作类型 |
| backend.core.locator_chain_builder | LocatorChainBuilder.extract() | append_step_async() 判断定位器数量 <=1 |
| backend.core.llm_healer | LLMHealer.heal() | append_step_async() 调用修复弱步骤 |
| backend.core.code_generator | PlaywrightCodeGenerator.generate() | assemble() 委托组装完整测试文件 |
| backend.core.healer_error | HealerError | LLM 修复代码中的异常引用 |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| 委托 generate() | 自己实现组装逻辑 | 委托减少约 200 行重复代码，但依赖 PlaywrightCodeGenerator 接口稳定。已锁定 D-05 |
| frozen dataclass | attrs 或 pydantic | 项目约定 dataclass; 无验证需求不需要 pydantic 开销 |

**Installation:**
无新依赖。所有模块已存在于项目中。

## Architecture Patterns

### Recommended Project Structure
```
backend/core/
    step_code_buffer.py     # StepCodeBuffer + StepRecord（新建）
    action_translator.py    # 复用，不修改
    code_generator.py       # 复用，不修改（Phase 112 简化）
    llm_healer.py           # 复用，不修改
    locator_chain_builder.py # 复用，不修改
    healer_error.py         # 复用，不修改

backend/tests/unit/
    test_step_code_buffer.py  # VAL-01 单元测试（新建）
```

### Pattern 1: StepRecord Frozen Dataclass
**What:** 不可变数据容器，包装翻译结果 + 等待策略 + 步骤序号
**When to use:** 每次调用 append_step() / append_step_async() 产生一条
**Example:**
```python
from dataclasses import dataclass
from backend.core.action_translator import TranslatedAction

@dataclass(frozen=True)
class StepRecord:
    """单步翻译结果（不可变）"""
    action: TranslatedAction  # 翻译后的 Playwright 代码
    wait_before: str          # 等待代码字符串，空字符串表示无等待
    step_index: int           # 步骤序号（自动递增）
```

### Pattern 2: _derive_wait 策略分发
**What:** 根据 action_type 和 duration 生成等待代码
**When to use:** append_step() 内部调用，为每步生成 wait_before
**Example:**
```python
def _derive_wait(self, action_type: str, duration: float | None = None) -> str:
    """根据操作类型和耗时推导等待代码"""
    if action_type == "navigate":
        return '    page.wait_for_load_state("networkidle")'
    if duration is not None and duration > 0.8:
        return f"    page.wait_for_timeout({int(duration * 1000)})"
    if action_type == "click":
        return "    page.wait_for_timeout(300)"
    return ""
```

### Pattern 3: append_step_async 弱步骤修复
**What:** 检测弱步骤后同步调用 LLMHealer，将修复结果合并到 StepRecord
**When to use:** 需要即时修复的步骤（elem=None 或 <=1 locator）
**Example:**
```python
async def append_step_async(self, action_dict: dict, duration: float | None = None) -> None:
    """翻译并尝试修复弱步骤"""
    action_type = ActionTranslator._identify_action_type(action_dict)
    translated = self._translator.translate(action_dict)

    # 弱步骤检测
    if action_type in ("click", "input") and self._is_weak(action_dict, action_type):
        # 从磁盘读取 DOM 快照
        dom_path = Path(self._base_dir) / self._run_id / "dom" / f"step_{self._next_index + 1}.txt"
        if dom_path.exists():
            dom_content = dom_path.read_text(encoding="utf-8")
            failed_locators = self._get_failed_locators(action_dict, action_type)
            action_params = action_dict.get(action_type, {})
            result = await self._healer.heal(action_type, failed_locators, dom_content, action_params)
            if result.success:
                translated = self._translator.translate_with_llm(action_dict, result.code_snippet)

    wait_before = self._derive_wait(action_type, duration)
    record = StepRecord(action=translated, wait_before=wait_before, step_index=self._next_index)
    self._records.append(record)
    self._next_index += 1
```

### Pattern 4: assemble 委托组装
**What:** 将 StepRecord 列表展平为 TranslatedAction 列表，委托给 PlaywrightCodeGenerator
**When to use:** agent 执行结束后，调用一次生成完整测试文件
**Example:**
```python
def assemble(
    self,
    run_id: str,
    task_name: str,
    task_id: str,
    precondition_config: dict | None = None,
    assertions_config: list[dict] | None = None,
) -> str:
    """组装完整测试文件"""
    flat_actions: list[TranslatedAction] = []
    for record in self._records:
        if record.wait_before:
            flat_actions.append(TranslatedAction(
                code=record.wait_before,
                action_type="wait",
                is_comment=False,
                has_locator=False,
            ))
        flat_actions.append(record.action)
    return self._generator.generate(
        run_id=run_id,
        task_name=task_name,
        task_id=task_id,
        actions=flat_actions,
        precondition_config=precondition_config,
        assertions_config=assertions_config,
    )
```

### Anti-Patterns to Avoid

- **不要在 StepRecord 中存储 action_dict 原始数据:** action_dict 可能很大（含 interacted_element 完整 DOM 信息），翻译后只保留 TranslatedAction 即可。存储原始数据会浪费内存且违反不可变原则
- **不要让 append_step 修改已有 StepRecord:** frozen dataclass 保证不可变，所有修改通过创建新 record 并追加到列表完成
- **不要在 Buffer 内部做文件写入:** Buffer 只负责翻译和组装字符串，文件写入留给调用方（Phase 112 的 runs.py）
- **不要修改 PlaywrightCodeGenerator 的 generate() 签名:** D-05 明确委托关系，保持 generate() 不变

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| 操作翻译 | 自己写 action_dict -> Playwright 代码映射 | ActionTranslator.translate() | 已处理 10 种操作类型 + 边界 case |
| 弱步骤修复 | 自己实现 DOM 解析 + LLM 调用 | LLMHealer.heal() | 已有 DOM 截断、超时保护、语法验证 |
| 定位器提取 | 自己解析 interacted_element 属性 | LocatorChainBuilder.extract() | 已有 6 种定位器策略 + 优先级排序 |
| 测试文件组装 | 自己拼接 import/header/body | PlaywrightCodeGenerator.generate() | 已有条件 import、logging、healer 初始化 |
| 语法验证 | 自己写 Python 解析器 | ast.parse() (via generator.validate_syntax()) | 已有验证模式，assemble 结果可直接验证 |

**Key insight:** StepCodeBuffer 本质是一个"编排器"而非"翻译器"。它的价值在于逐步累积的时序控制，不在翻译逻辑本身。所有翻译、修复、组装工作都委托给现有模块。

## Common Pitfalls

### Pitfall 1: DOM 快照步骤索引 1-indexed vs 0-indexed
**What goes wrong:** Buffer 内部 step_index 是 0-indexed（从 0 开始），但 DOM 文件命名是 1-indexed（step_1.txt, step_2.txt）
**Why it happens:** run_logger.log_browser_state() 使用 `step_{step}.txt` 其中 step 从 1 开始；_heal_weak_steps() 使用 `step_{i + 1}.txt`（i 是 0-indexed 的列表索引）
**How to avoid:** append_step_async() 读取 DOM 时使用 `step_{self._next_index + 1}.txt`
**Warning signs:** FileNotFoundError 或 DOM 内容与步骤不匹配

### Pitfall 2: wait_before 作为 TranslatedAction 的 action_type 选择
**What goes wrong:** 如果 wait_before 的 action_type 与前后步骤相同，_build_body() 不会在它们之间插入空行分隔
**Why it happens:** PlaywrightCodeGenerator._build_body() 的逻辑是"不同操作类型之间插入空行"
**How to avoid:** wait_before TranslatedAction 使用 action_type="wait"，与 navigate/click/input 不同，自然获得空行分隔
**Warning signs:** 生成的代码中等待语句与操作挤在一起无分隔

### Pitfall 3: append_step_async 中 _identify_action_type 是静态方法
**What goes wrong:** 直接调用 `self._translator._identify_action_type(action)` 可行但访问了私有方法
**Why it happens:** _identify_action_type 被定义为 @staticmethod 但命名带下划线前缀
**How to avoid:** 两种方案：(A) 在 Buffer 中复制类型识别逻辑（简单但重复）；(B) 调用静态方法（已有先例：_heal_weak_steps 在 code_generator.py line 206 中直接调用）。推荐方案 B，与现有代码一致
**Warning signs:** 无直接警告，但需注意如果 ActionTranslator 更改了类型识别逻辑，Buffer 也会受影响

### Pitfall 4: LLMHealer.heal() 是 async，append_step_async 也是 async
**What goes wrong:** 如果测试中忘记 mock LLMHealer.heal()，单元测试会尝试真实 LLM 调用
**Why it happens:** pytest-asyncio 的 auto mode 会自动处理 async 函数，但不会阻止真实网络调用
**How to avoid:** 单元测试中统一 mock LLMHealer 构造函数或 heal 方法，使用 `unittest.mock.AsyncMock`
**Warning signs:** 测试超时或需要 API key

### Pitfall 5: 空 buffer 的 assemble() 行为
**What goes wrong:** 空 buffer（无 StepRecord）调用 assemble() 时，generate() 收到空 actions 列表，生成只有 header + import + def 但无函数体的测试文件
**Why it happens:** PlaywrightCodeGenerator._build_body([]) 返回空字符串
**How to avoid:** 这是预期行为（ast.parse 仍然通过），但应在文档中明确说明空 buffer 返回的是有效的空测试函数
**Warning signs:** 无——这是正确的边界行为

## Code Examples

Verified patterns from project source code:

### 构造 TranslatedAction（用于 wait_before 插入）
```python
# Source: backend/core/action_translator.py line 533-540
TranslatedAction(
    code=f"    page.wait_for_timeout({ms})",
    action_type="wait",
    is_comment=False,
    has_locator=False,
)
```

### LLMHealer.heal() 调用签名
```python
# Source: backend/core/llm_healer.py line 191-208
result = await healer.heal(
    action_type=action_type,       # str: "click" or "input"
    failed_locators=failed_locators,  # tuple[str, ...]
    dom_snapshot=dom_content,       # str: DOM 快照文本
    action_params=action_params,    # dict: 操作参数
)
# result.success: bool
# result.code_snippet: str (Playwright 代码)
```

### 弱步骤检测模式
```python
# Source: backend/core/code_generator.py line 214-225
elem = action.get("interacted_element")
needs_healing = False
failed_locators: tuple[str, ...] = ()

if elem is None:
    needs_healing = True
else:
    locators = translator._chain_builder.extract(elem, action_type)
    if len(locators) <= 1:
        needs_healing = True
        failed_locators = tuple(locators)
```

### PlaywrightCodeGenerator.generate() 签名
```python
# Source: backend/core/code_generator.py line 39-47
def generate(
    self,
    run_id: str,
    task_name: str,
    task_id: str,
    actions: list[TranslatedAction],
    precondition_config: dict | None = None,
    assertions_config: list[dict] | None = None,
) -> str:
```

### ast.parse 语法验证
```python
# Source: backend/core/code_generator.py line 418-424
@staticmethod
def validate_syntax(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| 批量事后翻译 generate_and_save() | 逐步即时翻译 append_step() | Phase 111 | 翻译结果实时可用，弱步骤可即时修复 |
| _heal_weak_steps() 批量修复 | append_step_async() 逐步即时修复 | Phase 111 | 修复时 DOM 上下文更新鲜 |
| generate_and_save() 内部完成所有工作 | assemble() 委托 generate() | Phase 111 | Buffer 关注累积逻辑，组装交给专业模块 |

**Deprecated/outdated:**
- _heal_weak_steps()（Phase 112 后可移除，Phase 111 保留不改动）

## Open Questions

1. **append_step_async 是否需要 run_in_executor 包装同步操作?**
   - What we know: D-03 明确"同步阻塞模式"，heal() 本身是 async（内部有 asyncio.wait_for）
   - What's unclear: "同步阻塞"是指从调用者视角看（调用后等待结果），还是指用同步代码实现
   - Recommendation: heal() 本身已经是 async，append_step_async() 用 await 调用即可。不需要 run_in_executor。"同步阻塞模式"的意思是不做批量/后台处理，而是逐步等待结果

2. **StepRecord 是否需要额外字段存储 LLM 修复状态?**
   - What we know: TranslatedAction 已经包含了修复后的代码（通过 translate_with_llm 生成）
   - What's unclear: 是否需要标记某条 record 经过 LLM 修复（用于调试/日志）
   - Recommendation: 可在 Claude's Discretion 中决定。最小化方案不加，通过 logging 在修复时记录即可。如果需要追踪，可在 StepRecord 加 `healed: bool = False`

## Environment Availability

> Phase 111 无外部新依赖。所有依赖均为项目已有模块。

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | 运行时 | Yes | 3.14.3 | -- |
| uv | 包管理 | Yes | 0.9.24 | -- |
| pytest | 测试框架 | Yes | >=8.0.0 | -- |
| pytest-asyncio | 异步测试 | Yes | >=0.24.0 | -- |

**Missing dependencies with no fallback:** None

**Missing dependencies with fallback:** None

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.x + pytest-asyncio (auto mode) |
| Config file | pyproject.toml [tool.pytest.ini_options] |
| Quick run command | `uv run pytest backend/tests/unit/test_step_code_buffer.py -v` |
| Full suite command | `uv run pytest backend/tests/unit/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CODEGEN-01 | append_step() 同步翻译存储 StepRecord | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_append_step -v` | Wave 0 创建 |
| CODEGEN-01 | append_step() 自动递增 step_index | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_append_step_increments_index -v` | Wave 0 创建 |
| CODEGEN-01 | append_step() 多步累积 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_append_multiple_steps -v` | Wave 0 创建 |
| CODEGEN-02 | append_step_async() 检测弱步骤 elem=None | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_async_heals_weak_step_no_elem -v` | Wave 0 创建 |
| CODEGEN-02 | append_step_async() 检测 <=1 locator | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_async_heals_weak_step_single_locator -v` | Wave 0 创建 |
| CODEGEN-02 | append_step_async() DOM 快照读取 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_async_reads_dom_snapshot -v` | Wave 0 创建 |
| CODEGEN-02 | append_step_async() 修复失败 fallback | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_async_heal_failure_fallback -v` | Wave 0 创建 |
| CODEGEN-03 | _derive_wait() navigate 策略 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_derive_wait_navigate -v` | Wave 0 创建 |
| CODEGEN-03 | _derive_wait() duration >800ms 策略 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_derive_wait_long_duration -v` | Wave 0 创建 |
| CODEGEN-03 | _derive_wait() click 策略 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_derive_wait_click -v` | Wave 0 创建 |
| CODEGEN-03 | _derive_wait() 其他操作无等待 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_derive_wait_no_wait -v` | Wave 0 创建 |
| CODEGEN-04 | assemble() 组装完整测试文件 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_assemble_complete -v` | Wave 0 创建 |
| CODEGEN-04 | assemble() 语法验证通过 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_assemble_syntax_valid -v` | Wave 0 创建 |
| CODEGEN-04 | assemble() 空 buffer 边界 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::test_assemble_empty_buffer -v` | Wave 0 创建 |
| VAL-01 | append_step 同步翻译完整覆盖 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py -k append_step -v` | Wave 0 创建 |
| VAL-01 | wait 推导 3 种策略覆盖 | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py -k derive_wait -v` | Wave 0 创建 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_step_code_buffer.py -v`
- **Per wave merge:** `uv run pytest backend/tests/unit/ -v`
- **Phase gate:** `uv run pytest backend/tests/ -v` (全量回归)

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_step_code_buffer.py` -- covers VAL-01 (all test cases above)
- [ ] `backend/core/step_code_buffer.py` -- the implementation itself (Wave 0 creates both)

*(Existing test infrastructure: pytest + pytest-asyncio already configured, conftest.py fixtures available)*

## Sources

### Primary (HIGH confidence)
- `backend/core/action_translator.py` -- TranslatedAction 定义 (line 20-28), translate() (line 64), translate_with_llm() (line 106), _identify_action_type() (line 155)
- `backend/core/code_generator.py` -- PlaywrightCodeGenerator.generate() (line 39-123), _heal_weak_steps() (line 181-258), validate_syntax() (line 418-424)
- `backend/core/llm_healer.py` -- LLMHealer.heal() (line 191-292), LLMHealResult (line 89-107)
- `backend/core/locator_chain_builder.py` -- LocatorChainBuilder.extract() (line 45-123)
- `backend/utils/run_logger.py` -- DOM 快照保存路径约定 (line 88-92)
- `.planning/codebase/CONVENTIONS.md` -- frozen dataclass 约定、中文注释约定

### Secondary (MEDIUM confidence)
- `backend/tests/unit/test_code_generator.py` -- 测试 fixture 和 mock 模式参考
- `backend/core/healer_error.py` -- HealerError 异常定义
- `backend/api/routes/runs.py` line 372 -- on_step callback 签名（Phase 112 集成参考）

### Tertiary (LOW confidence)
- None -- 所有研究基于直接源码阅读

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - 全部复用现有模块，源码已完整阅读
- Architecture: HIGH - 现有代码模式清晰，CONTEXT.md 锁定了关键设计决策
- Pitfalls: HIGH - 基于 _heal_weak_steps() 已有实现的已知问题分析
- Integration points: HIGH - generate() 签名、heal() 签名、DOM 路径均已验证

**Research date:** 2026-04-28
**Valid until:** 2026-05-28 (stable -- no external dependency changes expected)
