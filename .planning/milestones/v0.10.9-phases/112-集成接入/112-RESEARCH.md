# Phase 112: 集成接入 - Research

**Researched:** 2026-04-28
**Domain:** Python async integration (FastAPI closures, step callback wiring)
**Confidence:** HIGH

## Summary

Phase 112 将 Phase 111 实现的 StepCodeBuffer 接入 runs.py 的 step_callback 和代码生成块。核心改动有三个：(1) runs.py 在 on_step 闭包外创建 buffer 实例，每步调用 buffer.append_step_async；(2) runs.py 代码生成块用 buffer.assemble() + Path.write_text() 替换 generate_and_save()；(3) code_generator.py 删除 generate_and_save() 和 _heal_weak_steps() 方法。

关键约束：on_step 回调签名需要扩展以接收 action_dict，agent_service.step_callback 需要在调用 on_step 时传递 action_dict。DOM 快照时序已确认安全——run_logger.log_browser 在 step_callback 前段执行，on_step 调用时 DOM 文件已写入磁盘。duration 参数从 step_stats_json 中解析（当前 step_stats.duration_ms 始终为 0，但 JSON 结构可扩展）。

**Primary recommendation:** 按时序顺序实施：(1) 扩展 on_step 签名 + agent_service 传 action_dict；(2) 创建 buffer 实例 + 闭包捕获；(3) 替换代码生成块；(4) 删除 generate_and_save 和 _heal_weak_steps；(5) 更新测试。

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** runs.py 中 on_step 闭包外创建 StepCodeBuffer 实例，通过闭包捕获传给 on_step。扩展 on_step 回调签名，增加 `action_dict: dict | None = None` 参数。agent_service 的 step_callback 调用 on_step 时传递 action_dict。Buffer 构造参数：`base_dir="outputs"`, `run_id=run_id`, `llm_config=get_code_gen_llm_config()`
- **D-02:** 统一使用 `append_step_async`（含弱步骤即时 LLM 修复）。DOM 快照在 step_callback 前段已写入（run_logger.log_browser），on_step 调用时 DOM 文件已存在，append_step_async 可正常读取。duration 参数从 step_stats 中提取（agent_service 已有 step_stats_data）
- **D-03:** 删除 `generate_and_save()` 方法和 `_heal_weak_steps()` 方法。runs.py 代码生成块改为 `buffer.assemble()` + 手动写文件（`Path.write_text`）。`generate()` 方法保留不变（assemble 内部委托调用）。现有 `generate_and_save` 测试更新：移除或改为测试 assemble + write 流程
- **D-04:** 单元级 buffer 集成测试 -- 构造模拟 step_callback 上下文直接调用 buffer.append_step_async，验证累积和组装。不启动真实 HTTP 服务器

### Claude's Discretion
- on_step 签名扩展的具体参数名和顺序
- action_dict 为空或 None 时的 fallback 处理
- duration 从 step_stats_json 解析的具体逻辑
- 文件写入目录创建逻辑
- 测试文件组织

### Deferred Ideas (OUT OF SCOPE)
None
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| INTEG-01 | runs.py step_callback 传递 action_dict 给 buffer.append_step()，每步即时翻译 | on_step 签名需新增 action_dict 参数，agent_service.step_callback line 587-590 需传 action_dict。action_dict 已在 step_callback line 456 解析为 first_action.model_dump()。on_step 是 async 闭包，append_step_async 是 async 方法，await 调用即可 |
| INTEG-02 | runs.py 代码生成块替换为 buffer.assemble() + import/header 组装 + 文件写入 | 当前 generate_and_save 在 line 607-615。替换为 buffer.assemble(run_id, task_name, task_id, precondition_config, assertions_config) + Path(output_dir).write_text(content)。output_dir = Path("outputs") / run_id / "generated" |
| INTEG-03 | code_generator.py 去掉 _heal_weak_steps，generate_and_save 接受 list[TranslatedAction] 预翻译结果直接组装输出 | 删除 line 125-179 (generate_and_save) 和 line 181-258 (_heal_weak_steps)。generate() 保留不变。test_code_generator.py 中 test_healing_failure_preserves_original 和 test_generate_and_save_validates_before_write 需移除或重写 |
| VAL-02 | 集成测试验证 buffer 在 step_callback 上下文中累积步骤，弱步骤异步修复正常触发 | 构造模拟 step_callback 上下文：创建 buffer + DOM 文件 + mock LLMHealer，调用 append_step_async 多次，验证 records 累积和 assemble 结果。不启动真实 HTTP 服务器（per D-04） |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| FastAPI | project-existing | Web framework, on_step is async closure in route handler | Existing project infrastructure |
| pytest | >=8.0.0 | Test framework | Project standard |
| pytest-asyncio | >=0.24.0 | Async test support (asyncio_mode = "auto") | Required for append_step_async testing |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| unittest.mock | stdlib | AsyncMock, MagicMock, patch | All test mocking |
| ast | stdlib | Syntax validation of generated code | Verifying assemble() output |
| pathlib.Path | stdlib | File write operations | Replacing generate_and_save file write |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| append_step_async | append_step (sync) | D-02 locks in async; sync is simpler but loses LLM healing |

**Installation:**
No new packages required. All dependencies are existing project dependencies.

## Architecture Patterns

### Recommended Modification Points

```
runs.py modification flow:
1. Before on_step definition (line ~370): Create buffer instance
2. Inside on_step closure (after line 418): Call buffer.append_step_async
3. Replace code generation block (line 590-619): buffer.assemble() + write
4. Extend on_step signature: add action_dict parameter

agent_service.py modification flow:
1. Extend on_step Callable type hint (line 345)
2. Pass action_dict to on_step call (line 587-590)
```

### Pattern 1: Buffer Instance Creation Before Closure
**What:** Create StepCodeBuffer before on_step closure, capture via closure
**When to use:** on_step needs buffer access for every step
**Example:**
```python
# runs.py, before on_step definition (~line 370)
from backend.core.step_code_buffer import StepCodeBuffer

buffer = StepCodeBuffer(
    base_dir="outputs",
    run_id=run_id,
    llm_config=get_code_gen_llm_config(),
)

async def on_step(step: int, action: str, reasoning: str,
                  screenshot_path: str | None,
                  step_stats_json: str | None = None,
                  action_dict: dict | None = None):
    nonlocal step_count, global_seq
    # ... existing logic ...

    # New: append step to buffer (per D-02)
    if action_dict is not None:
        duration = None
        if step_stats_json:
            try:
                stats = json.loads(step_stats_json)
                duration = stats.get("duration_ms", 0) / 1000.0
            except (json.JSONDecodeError, TypeError):
                pass
        try:
            await buffer.append_step_async(action_dict, duration=duration)
        except Exception as e:
            logger.error(f"[{run_id}] buffer append 失败（非阻塞）: {e}")
```

### Pattern 2: Code Generation Block Replacement
**What:** Replace generate_and_save with buffer.assemble() + write
**When to use:** Post-execution code generation
**Example:**
```python
# runs.py, replacing line 590-619
try:
    from pathlib import Path as PathLib
    precondition_config = (
        {"target_url": effective_target_url}
        if effective_target_url else None
    )
    assertions_config = None
    if run and run.task and run.task.assertions:
        assertions_config = [
            {"type": a.type, "expected": a.expected, "name": a.name}
            for a in run.task.assertions
        ]
    content = buffer.assemble(
        run_id=run_id,
        task_name=task_name,
        task_id=task_id,
        precondition_config=precondition_config,
        assertions_config=assertions_config,
    )
    output_dir = PathLib("outputs") / run_id / "generated"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"test_{run_id}.py"
    output_path.write_text(content, encoding="utf-8")
    code_path = str(output_path)
    await run_repo.update_generated_code_path(run_id, code_path)
    logger.info(f"[{run_id}] 生成 Playwright 代码: {code_path}")
except Exception as e:
    logger.error(f"[{run_id}] 代码生成失败（非阻塞）: {e}")
```

### Pattern 3: agent_service on_step Signature Extension
**What:** Add action_dict to on_step call
**When to use:** step_callback passes action_dict to on_step
**Example:**
```python
# agent_service.py, line 587-590 modification
# Current:
#   await on_step(step, action, reasoning, screenshot_path, step_stats_json)
# New:
action_dict_data = action_dict if 'action_dict' in locals() else None
if asyncio.iscoroutinefunction(on_step):
    await on_step(step, action, reasoning, screenshot_path, step_stats_json,
                  action_dict=action_dict_data)
else:
    on_step(step, action, reasoning, screenshot_path, step_stats_json,
            action_dict=action_dict_data)
```

### Anti-Patterns to Avoid
- **Blocking buffer.append in step_callback:** append_step_async is awaitable; forgetting await will cause unhandled coroutine warning and no translation
- **Capturing mutable action_dict reference:** action_dict is already a fresh dict from model_dump(), but if captured by reference in a loop it could mutate -- pass it directly
- **Deleting generate() instead of generate_and_save():** generate() is used internally by assemble() and must be preserved (per D-03)
- **Creating buffer inside on_step closure:** Must be outside to accumulate across steps

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| File syntax validation | Custom Python syntax checker | ast.parse() | Already used in code_generator.validate_syntax() |
| Weak step detection | New weak step logic | StepCodeBuffer._is_weak_step() | Already implemented and tested in Phase 111 |
| Action translation | New translation logic | ActionTranslator.translate() | Already integrated in StepCodeBuffer |
| Test file assembly | Custom string concatenation | buffer.assemble() + PlaywrightCodeGenerator.generate() | Already handles imports, header, precondition, assertions |

**Key insight:** Phase 112 is purely a wiring/integration phase. All core logic (translation, healing, wait derivation, assembly) exists in Phase 111's StepCodeBuffer. This phase connects the pipes.

## Common Pitfalls

### Pitfall 1: DOM Snapshot 1-Indexed vs 0-Indexed Mismatch
**What goes wrong:** step_code_buffer uses `self._next_index + 1` for DOM path (1-indexed), but on_step receives `step` from agent_service which is also 1-indexed. The buffer's internal `_next_index` starts at 0 and increments after each append.
**Why it happens:** Two different numbering systems -- buffer's step_index is 0-indexed, DOM files are 1-indexed, agent's step parameter is 1-indexed.
**How to avoid:** Buffer already handles this correctly in append_step_async: `dom_path = ... / f"step_{self._next_index + 1}.txt"`. The on_step `step` parameter is not used by buffer; buffer uses its own internal counter. No action needed, just be aware.
**Warning signs:** If buffer fails to find DOM files, check if DOM path matches step numbering.

### Pitfall 2: action_dict is Already model_dump()'d
**What goes wrong:** agent_service.step_callback already converts first_action to action_dict via `first_action.model_dump(exclude_none=True, mode='json')`. Passing the raw agent_output.action[0] instead would break ActionTranslator.
**Why it happens:** Misunderstanding the data flow -- action_dict is already a dict, not an ActionModel.
**How to avoid:** Pass the already-extracted action_dict directly to on_step. Do NOT re-extract from agent_output.
**Warning signs:** ActionTranslator crashes with "dict has no attribute model_dump".

### Pitfall 3: Forgetting await on append_step_async
**What goes wrong:** Calling `buffer.append_step_async(action_dict, duration)` without `await` returns a coroutine object that is never awaited -- no translation happens, no error is raised, but buffer remains empty.
**Why it happens:** on_step is already async, but in the heat of integration it is easy to forget await.
**How to avoid:** Always use `await buffer.append_step_async(...)`. Add a comment: `# Must await -- async for LLM healing`.
**Warning signs:** buffer.records is empty after all steps, assemble() produces empty function body.

### Pitfall 4: on_step Signature Breaking agent_service
**What goes wrong:** Adding `action_dict` as a positional parameter changes the Callable type hint and breaks agent_service's call site at line 587-590.
**Why it happens:** agent_service calls `on_step(step, action, reasoning, screenshot_path, step_stats_json)` with positional args.
**How to avoid:** Add `action_dict: dict | None = None` as a keyword-only parameter at the end. The existing call works unchanged; new code passes action_dict as keyword arg.
**Warning signs:** TypeError: on_step() got an unexpected keyword argument 'action_dict'.

### Pitfall 5: duration_ms Always 0 in Current step_stats
**What goes wrong:** step_stats.duration_ms is hardcoded to 0 in agent_service.py line 495. Passing 0 to buffer's _derive_wait means duration-based wait strategy never triggers.
**Why it happens:** Timing wrapper has not been implemented yet -- the comment says "Will be updated if timing wrapper exists".
**How to avoid:** Accept that duration will be None or 0 for now. The click default (300ms) and navigate (wait_for_load_state) strategies still work. Duration > 800ms strategy is future enhancement. Parse safely: `duration = stats.get("duration_ms", 0) / 1000.0 if stats.get("duration_ms", 0) > 0 else None`.
**Warning signs:** No wait_for_timeout(long_ms) in generated code for slow operations.

### Pitfall 6: generate_and_save Test Breakage
**What goes wrong:** test_code_generator.py has 2 tests (test_healing_failure_preserves_original, test_generate_and_save_validates_before_write) that call generate_and_save(). Deleting the method breaks these tests.
**Why it happens:** Tests test the old API that is being removed.
**How to avoid:** Per D-03, remove or rewrite these tests. The generate() method tests (test_generate_complete_file, test_fallback_complete_file_parses, etc.) remain valid since generate() is preserved.
**Warning signs:** Import errors or AttributeError for generate_and_save in test suite.

## Code Examples

Verified patterns from source code analysis:

### action_dict Extraction in agent_service (already exists)
```python
# Source: backend/core/agent_service.py line 454-461
if hasattr(agent_output, "action") and agent_output.action:
    first_action = agent_output.action[0]
    action_dict = first_action.model_dump(exclude_none=True, mode='json')
    if action_dict:
        action_name = list(action_dict.keys())[0]
        action_params = action_dict[action_name]
        action = f"{action_name}: {action_params}" if action_params else action_name
```

### on_step Current Call Site in agent_service
```python
# Source: backend/core/agent_service.py line 586-590
step_stats_json = step_stats_data["value"]
if asyncio.iscoroutinefunction(on_step):
    await on_step(step, action, reasoning, screenshot_path, step_stats_json)
else:
    on_step(step, action, reasoning, screenshot_path, step_stats_json)
```

### Current Code Generation Block (to be replaced)
```python
# Source: backend/api/routes/runs.py line 590-619
try:
    from backend.core.code_generator import PlaywrightCodeGenerator
    code_generator = PlaywrightCodeGenerator()
    _precondition_config = (
        {"target_url": effective_target_url} if effective_target_url else None
    )
    _assertions_config = None
    if run and run.task and run.task.assertions:
        _assertions_config = [
            {"type": a.type, "expected": a.expected, "name": a.name}
            for a in run.task.assertions
        ]
    code_path = await code_generator.generate_and_save(
        run_id=run_id, task_name=task_name, task_id=task_id,
        agent_history=result, llm_config=get_code_gen_llm_config(),
        precondition_config=_precondition_config,
        assertions_config=_assertions_config,
    )
    await run_repo.update_generated_code_path(run_id, code_path)
except Exception as e:
    logger.error(f"[{run_id}] 代码生成失败（非阻塞）: {e}")
```

### StepCodeBuffer Constructor (Phase 111)
```python
# Source: backend/core/step_code_buffer.py line 48-62
def __init__(self, *, base_dir: str = "", run_id: str = "",
             llm_config: dict | None = None) -> None:
    self._records: list[StepRecord] = []
    self._next_index: int = 0
    self._translator = ActionTranslator()
    self._generator = PlaywrightCodeGenerator()
    self._chain_builder = LocatorChainBuilder()
    self._base_dir = base_dir
    self._run_id = run_id
    self._llm_config = llm_config or {}
```

### Integration Test Pattern (simulated step_callback context)
```python
# Pattern for VAL-02 integration tests
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from backend.core.step_code_buffer import StepCodeBuffer

@pytest.mark.asyncio
async def test_buffer_accumulates_in_callback_context(tmp_path):
    """VAL-02: buffer accumulates steps in simulated step_callback context."""
    run_id = "integ_test"
    buffer = StepCodeBuffer(
        base_dir=str(tmp_path),
        run_id=run_id,
        llm_config={"model": "test"},
    )
    # Create DOM snapshot (simulating run_logger.log_browser)
    dom_dir = tmp_path / run_id / "dom"
    dom_dir.mkdir(parents=True)
    (dom_dir / "step_1.txt").write_text("<html><button id='btn'>Click</button></html>")
    (dom_dir / "step_2.txt").write_text("<html><input id='name' /></html>")

    # Simulate step_callback step 1: navigate
    navigate_dict = {"navigate": {"url": "https://example.com"}}
    await buffer.append_step_async(navigate_dict)

    # Simulate step_callback step 2: click (weak step with healing)
    click_dict = {"click": {"index": 5}, "interacted_element": None}
    with patch("backend.core.step_code_buffer.LLMHealer") as MockHealer:
        mock_instance = MockHealer.return_value
        mock_instance.heal = AsyncMock(return_value=MagicMock(
            success=True, code_snippet="page.locator('#btn').click()",
            raw_response="", locator="page.locator('#btn')",
        ))
        with patch.object(buffer._translator, "translate_with_llm",
                          return_value=MagicMock(code="    page.locator('#btn').click()",
                                                 action_type="click", is_comment=False,
                                                 has_locator=True)):
            await buffer.append_step_async(click_dict)

    # Verify accumulation
    assert len(buffer.records) == 2
    assert buffer.records[0].action.action_type == "navigate"
    assert buffer.records[1].action.action_type == "click"

    # Verify assembly
    content = buffer.assemble(run_id, "集成测试", "task1")
    assert "def test_" in content
    ast.parse(content)
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| generate_and_save (post-hoc batch) | buffer.append_step_async (per-step即时) | Phase 111/112 | LLM healing uses fresh DOM, better locator quality |
| _heal_weak_steps batch in code_generator | append_step_async inline healing in StepCodeBuffer | Phase 111 | Healing happens per-step with latest DOM context |

**Deprecated/outdated:**
- `PlaywrightCodeGenerator.generate_and_save()`: Deleted in this phase. File write moves to runs.py
- `PlaywrightCodeGenerator._heal_weak_steps()`: Deleted in this phase. Healing moves to StepCodeBuffer.append_step_async()

## Open Questions

1. **Duration parsing from step_stats_json**
   - What we know: step_stats.duration_ms is currently hardcoded to 0 in agent_service.py line 495
   - What's unclear: Whether a timing wrapper will be added before Phase 112
   - Recommendation: Parse defensively -- `duration = stats.get("duration_ms", 0) / 1000.0` with a guard for 0 values. If duration_ms is 0, pass None to buffer so _derive_wait uses type-based defaults.

2. **on_step Callable type hint in agent_service.py**
   - What we know: Current signature is `Callable[[int, str, str, str | None], Any]` (line 345)
   - What's unclear: Whether extending it with `action_dict: dict | None = None` keyword arg needs type hint change
   - Recommendation: Change to `Callable[..., Any]` or use `Protocol` for clarity. Since on_step is already used with keyword arg `step_stats_json`, the existing Callable hint is already loose enough.

## Environment Availability

Step 2.6: SKIPPED (no external dependencies identified -- all changes are code-only, using existing project packages)

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest >=8.0.0 + pytest-asyncio >=0.24.0 |
| Config file | pyproject.toml [tool.pytest.ini_options], asyncio_mode = "auto" |
| Quick run command | `uv run pytest backend/tests/unit/test_step_code_buffer.py backend/tests/unit/test_code_generator.py -v -x` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| INTEG-01 | on_step receives action_dict and calls buffer.append_step_async | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::TestIntegration -x` | Wave 0 |
| INTEG-02 | Code generation block uses buffer.assemble() + write | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::TestIntegration::test_assemble_write -x` | Wave 0 |
| INTEG-03 | generate_and_save and _heal_weak_steps removed, generate() preserved | unit | `uv run pytest backend/tests/unit/test_code_generator.py -x` | Update existing |
| VAL-02 | Buffer accumulates in step_callback context, weak step healing works | unit | `uv run pytest backend/tests/unit/test_step_code_buffer.py::TestIntegration -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_step_code_buffer.py backend/tests/unit/test_code_generator.py -v -x`
- **Per wave merge:** `uv run pytest backend/tests/unit/ -v`
- **Phase gate:** `uv run pytest backend/tests/ -v` (full suite green)

### Wave 0 Gaps
- [ ] `backend/tests/unit/test_step_code_buffer.py` -- add TestIntegration class with VAL-02 tests
- [ ] `backend/tests/unit/test_code_generator.py` -- remove test_healing_failure_preserves_original and test_generate_and_save_validates_before_write (methods being deleted per D-03)

## Sources

### Primary (HIGH confidence)
- Source code analysis: `backend/core/step_code_buffer.py` (248 lines) -- Phase 111 implementation
- Source code analysis: `backend/core/code_generator.py` (425 lines) -- deletion targets
- Source code analysis: `backend/api/routes/runs.py` (lines 370-418 on_step, lines 590-619 code gen block)
- Source code analysis: `backend/core/agent_service.py` (lines 393-590 step_callback, lines 341-350 run_with_streaming signature)
- CONTEXT.md Phase 112 -- locked decisions D-01 through D-04

### Secondary (MEDIUM confidence)
- Phase 111 CONTEXT.md -- StepCodeBuffer design decisions
- `backend/tests/unit/test_step_code_buffer.py` -- existing buffer unit test patterns
- `backend/tests/unit/test_code_generator.py` -- existing code gen test patterns

### Tertiary (LOW confidence)
- None

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - all dependencies are existing project packages, no new libraries
- Architecture: HIGH - all source files read and analyzed, modification points identified precisely
- Pitfalls: HIGH - 6 concrete pitfalls identified from source code analysis
- Integration test: HIGH - test pattern established from existing test_step_code_buffer.py

**Research date:** 2026-04-28
**Valid until:** 2026-05-28 (stable codebase, no external dependency changes)
