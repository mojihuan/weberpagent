# Phase 52: Prompt 增强 — 键盘操作 - Research

**Researched:** 2026-03-30
**Domain:** browser-use send_keys API + ENHANCED_SYSTEM_MESSAGE prompt engineering
**Confidence:** HIGH

## Summary

Phase 52 的核心任务是在 `ENHANCED_SYSTEM_MESSAGE` 中添加第 6 段键盘操作指导，让 Qwen 3.5 Plus LLM 知道何时以及如何使用 browser-use 的 `send_keys` 动作。关键发现：browser-use 的 `SendKeysAction` 注册时 description 为空字符串，意味着 LLM 无法从动作描述中了解 `send_keys` 的用途，必须通过 prompt 指导。`send_keys` 的底层实现通过 CDP `Input.dispatchKeyEvent` 完成，支持键别名（ctrl/esc/enter 等）和组合键（`+` 分隔符）。

**Primary recommendation:** 在 `prompts.py` 的 `ENHANCED_SYSTEM_MESSAGE` 末尾追加约 5-7 行的键盘操作段落，使用场景-动作对格式，覆盖 Enter 搜索触发、Escape 关闭弹窗、Control+a 全选覆盖三种场景。粘贴操作不使用 Ctrl+V。

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 场景-动作对格式。每条规则以"场景 → 动作"形式描述
- **D-02:** 作为 ENHANCED_SYSTEM_MESSAGE 的第 6 段落添加，保留现有 5 段不变
- **D-03:** 中文撰写，与现有 prompt 风格一致
- **D-04:** 总长度增量控制在 10 行以内，避免 prompt 过长影响 Qwen 遵守率
- **D-05:** 采用"先全选再覆盖"模式。用 send_keys('Control+a') 全选输入框内容，再用 input action 输入新值覆盖。不依赖系统剪贴板状态
- **D-06:** 不指导 Agent 使用 send_keys('Control+v') 粘贴操作
- **D-07:** 仅搜索触发式场景。当输入框是搜索框时，输入完成后用 send_keys('Enter') 触发搜索
- **D-08:** 仅关闭弹窗场景。日期选择器、下拉弹窗等遮挡元素出现时，用 send_keys('Escape') 关闭
- **D-09:** 使用采购单场景验证
- **D-10:** 结构 + 关键词检查测试
- **D-11:** Plan 52-01 为 prompt 修改，Plan 52-02 为 ERP 场景验证

### Claude's Discretion
- ENHANCED_SYSTEM_MESSAGE 键盘操作段落的具体措辞
- 测试用例的具体关键词列表
- 验证步骤的具体 ERP 操作流程

### Deferred Ideas (OUT OF SCOPE)
None
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| KB-01 | Agent 能执行 Ctrl+V 粘贴操作，将剪贴板内容粘贴到输入框 | D-05/D-06 决定不使用 Ctrl+V，改用 Control+a 全选 + input 覆盖策略。prompt 中指导"需清空输入框 → send_keys('Control+a') 全选后 input 新值" |
| KB-02 | Agent 能在输入框中按回车键触发搜索/确认 | send_keys('Enter') 通过 CDP dispatchKeyEvent 实现，包含 char 事件触发 keypress listeners（行 2482-2489）。prompt 中指导"搜索框输入后 → send_keys('Enter') 触发搜索" |
| KB-03 | Agent 能按 ESC 键关闭弹窗 | send_keys('Escape') 或 send_keys('Esc') 均可通过别名映射生效（行 2390-2391）。prompt 中指导"弹窗遮挡 → send_keys('Escape') 关闭" |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| browser-use (installed) | (local .venv) | Agent 框架，提供 send_keys 动作 | 项目核心依赖，已集成 |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest | (existing) | 单元测试 | 验证 prompt 关键词和结构 |

**No new dependencies required.** This phase is purely prompt text modification and test extension.

## Architecture Patterns

### Current ENHANCED_SYSTEM_MESSAGE Structure
```
ENHANCED_SYSTEM_MESSAGE (prompts.py, lines 9-34)
  ## 1. 表格编辑模式         (lines 10-13)
  ## 2. 失败恢复强制规则      (lines 15-20)
  ## 3. 字段填写后验证        (lines 22-24)
  ## 4. 提交前校验            (lines 26-28)
  ## 5. 元素识别与表单策略     (lines 30-33)
  ## 6. [NEW] 键盘操作        (to be added, ~5-7 lines)
```

### Pattern: Scene-Action Pairs (D-01)
**What:** Each rule written as "场景描述 → 动作指令" format
**When to use:** All keyboard operation guidance in the new paragraph
**Example:**
```
搜索框输入后 → send_keys('Enter')触发搜索
日期选择器遮挡 → send_keys('Escape')关闭
需清空输入框 → send_keys('Control+a')全选后 input 新值
```

### Pattern: Keyword-based Test Assertions (D-10)
**What:** Test checks for presence of key terms, not exact strings
**When to use:** Extending test_enhanced_prompt.py
**Example:**
```python
def test_contains_keyboard_operation_keywords(self):
    lower = ENHANCED_SYSTEM_MESSAGE.lower()
    assert "send_keys" in lower
    assert "enter" in lower
    assert "escape" in lower
    assert "control" in lower
```

### Anti-Patterns to Avoid
- **Overly detailed key syntax instructions:** Qwen 3.5 Plus follows concise instructions better. Keep each rule to one line.
- **Teaching Ctrl+V paste:** D-06 explicitly forbids this. The clipboard content is unpredictable in headless browser mode.
- **Using send_keys for text input:** Text input should use the `input` action, not `send_keys`. send_keys is for special keys and shortcuts only.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Keyboard event dispatch | Custom CDP key dispatch calls | browser-use `send_keys` action | Already handles key aliases, modifier bitmask, keyDown/keyUp sequencing, and Enter char event |
| Key name normalization | Custom key name mapping | browser-use built-in aliases (ctrl/esc/enter/etc) | 21 aliases already supported in default_action_watchdog.py lines 2376-2401 |
| Input field clearing | Custom clear logic | Control+a + input overwrite (D-05) | browser-use already has triple-click+Delete and Ctrl+A+Backspace strategies, but prompt guidance should use the simpler Control+a + input approach |

**Key insight:** The send_keys action has a robust CDP implementation. The problem is not the action's capability but the LLM's awareness of when and how to use it, because the action description is empty.

## Common Pitfalls

### Pitfall 1: send_keys Description is Empty
**What goes wrong:** browser-use registers `send_keys` with description `''` (empty string) in `tools/service.py:1377`. The LLM sees `send_keys: . (keys=str ...)` in its action prompt, which gives no guidance on when to use it.
**Why it happens:** browser-use intentionally leaves this blank for framework users to customize via prompts.
**How to avoid:** ENHANCED_SYSTEM_MESSAGE must explicitly teach the LLM about send_keys usage scenarios.
**Warning signs:** Agent never uses send_keys in its actions; Agent tries to use evaluate JS for keyboard operations instead.

### Pitfall 2: Ctrl+V Unreliability in Headless Browser
**What goes wrong:** `send_keys('Control+v')` dispatches the keyboard shortcut but the clipboard may be empty or contain unexpected content in headless Chromium.
**Why it happens:** Headless browser has no system clipboard integration; clipboard state depends on prior copy operations that may not have happened.
**How to avoid:** D-05/D-06: Use Control+a to select all + input new value. Never instruct Ctrl+V.
**Warning signs:** Agent attempts paste and gets empty or wrong values in the field.

### Pitfall 3: Prompt Length Degradation
**What goes wrong:** Adding too many instructions causes Qwen 3.5 Plus to ignore or partially follow the prompt.
**Why it happens:** Longer prompts dilute attention; Phase 49 D-01 established that Qwen 3.5 Plus follows concise instructions better.
**How to avoid:** D-04 limits the addition to 10 lines. Keep the keyboard section to 5-7 lines maximum.
**Warning signs:** Agent stops following earlier prompt sections (e.g., click-to-edit pattern).

### Pitfall 4: Enter Key for Form Submission
**What goes wrong:** Agent presses Enter to submit a form instead of clicking the submit button, causing unexpected behavior.
**Why it happens:** Prompt doesn't distinguish between "search trigger" and "form submission" scenarios.
**How to avoid:** D-07 restricts Enter usage to search trigger scenarios only. Explicitly state "不用于表单提交" in the prompt.
**Warning signs:** Agent presses Enter on a form and it submits prematurely or triggers wrong behavior.

### Pitfall 5: ESC Key Overuse
**What goes wrong:** Agent tries to dismiss confirmation dialogs or cancel operations with Escape instead of handling them properly.
**Why it happens:** Prompt is too broad about when to use Escape.
**How to avoid:** D-08 restricts Escape to closing overlay elements (date pickers, dropdown popups) only.
**Warning signs:** Agent dismisses important confirmation dialogs that need explicit Accept/Cancel clicks.

## Code Examples

### SendKeysAction Definition (browser-use source)
```python
# Source: .venv/.../browser_use/tools/views.py:123-124
class SendKeysAction(BaseModel):
    keys: str = Field(description='keys (Escape, Enter, PageDown) or shortcuts (Control+o)')
```

### send_keys Action Registration (browser-use source)
```python
# Source: .venv/.../browser_use/tools/service.py:1376-1393
@self.registry.action(
    '',  # Empty description -- LLM sees no guidance
    param_model=SendKeysAction,
)
async def send_keys(params: SendKeysAction, browser_session: BrowserSession):
    try:
        event = browser_session.event_bus.dispatch(SendKeysEvent(keys=params.keys))
        await event
        await event.event_result(raise_if_any=True, raise_if_none=False)
        memory = f'Sent keys: {params.keys}'
        msg = f'⌨️  {memory}'
        logger.info(msg)
        return ActionResult(extracted_content=memory, long_term_memory=memory)
    except Exception as e:
        logger.error(f'Failed to dispatch SendKeysEvent: {type(e).__name__}: {e}')
        error_msg = f'Failed to send keys: {str(e)}'
        return ActionResult(error=error_msg)
```

### Key Alias Mapping (browser-use source)
```python
# Source: .venv/.../browser_use/browser/watchdogs/default_action_watchdog.py:2376-2401
key_aliases = {
    'ctrl': 'Control', 'control': 'Control',
    'alt': 'Alt', 'option': 'Alt',
    'meta': 'Meta', 'cmd': 'Meta', 'command': 'Meta',
    'shift': 'Shift',
    'enter': 'Enter', 'return': 'Enter',
    'tab': 'Tab', 'delete': 'Delete', 'backspace': 'Backspace',
    'escape': 'Escape', 'esc': 'Escape',
    'space': ' ',
    'up': 'ArrowUp', 'down': 'ArrowDown', 'left': 'ArrowLeft', 'right': 'ArrowRight',
    'pageup': 'PageUp', 'pagedown': 'PageDown', 'home': 'Home', 'end': 'End',
}
```

### Existing Test Pattern (to extend)
```python
# Source: backend/tests/unit/test_enhanced_prompt.py
class TestEnhancedPrompt:
    def test_contains_click_to_edit_keywords(self):
        """PRM-01: Must contain click-to-edit guidance with key terms."""
        lower = ENHANCED_SYSTEM_MESSAGE.lower()
        assert "click" in lower
        assert "td" in lower
        assert "input" in lower
        assert "edit" in lower

    def test_line_count_under_60(self):
        """D-01: ENHANCED_SYSTEM_MESSAGE must be under 60 lines."""
        lines = ENHANCED_SYSTEM_MESSAGE.strip().splitlines()
        assert len(lines) <= 60
```

### Prompt Addition Pattern (recommended)
```python
# Target location: backend/agent/prompts.py, ENHANCED_SYSTEM_MESSAGE
# After line 33 (end of section 5), add:

## 6. 键盘操作
搜索框输入后 → send_keys('Enter') 触发搜索，不用于表单提交。
日期选择器或弹窗遮挡 → send_keys('Escape') 关闭。
需清空输入框 → send_keys('Control+a') 全选后用 input 输入新值覆盖。
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual event_bus.on() registration | Auto-registration via attach_to_session() | browser-use refactor | All on_XxxEvent handlers are automatically discovered and registered; the commented-out lines in session.py:1642 are legacy code |
| CHINESE_ENHANCEMENT as separate constant | Merged into ENHANCED_SYSTEM_MESSAGE | Phase 49 | Single source of truth for agent prompt; CHINESE_ENHANCEMENT is now an alias |

**Note on session.py commented-out lines:** The `event_bus.on(SendKeysEvent, ...)` lines at `session.py:1642` are commented out because `attach_to_session()` at `session.py:1645` automatically discovers all `on_EventName` methods via introspection and registers them. The `on_SendKeysEvent` handler is fully functional.

## Open Questions

1. **Qwen 3.5 Plus send_keys compliance rate**
   - What we know: Phase 49 established that Qwen 3.5 Plus follows concise instructions well. The send_keys action is available but has empty description.
   - What's unclear: Whether Qwen will reliably use send_keys when instructed via prompt. This can only be validated by Plan 52-02 (ERP scenario testing).
   - Recommendation: Keep keyboard prompt section concise (5-7 lines), use exact action name `send_keys` and parameter format in examples.

2. **Control+a reliability on Ant Design inputs**
   - What we know: browser-use already uses Ctrl+A + Backspace as a fallback clearing strategy (default_action_watchdog.py lines 1409-1457).
   - What's unclear: Whether the "select all + overwrite with input" approach works reliably for all Ant Design input types.
   - Recommendation: This should be validated in Plan 52-02 ERP scenario testing.

## Environment Availability

Step 2.6: SKIPPED (no external dependencies beyond existing project code and installed browser-use package)

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest with pytest-asyncio |
| Config file | pyproject.toml [tool.pytest.ini_options] |
| Quick run command | `uv run pytest backend/tests/unit/test_enhanced_prompt.py -x -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| KB-01 | Prompt contains keyboard clear/overwrite keywords (Control+a, input) | unit | `uv run pytest backend/tests/unit/test_enhanced_prompt.py::TestEnhancedPrompt::test_contains_keyboard_operation_keywords -x` | Wave 0 |
| KB-02 | Prompt contains Enter key guidance | unit | `uv run pytest backend/tests/unit/test_enhanced_prompt.py::TestEnhancedPrompt::test_contains_keyboard_operation_keywords -x` | Wave 0 |
| KB-03 | Prompt contains Escape key guidance | unit | `uv run pytest backend/tests/unit/test_enhanced_prompt.py::TestEnhancedPrompt::test_contains_keyboard_operation_keywords -x` | Wave 0 |
| (structural) | Prompt line count stays within limit | unit | `uv run pytest backend/tests/unit/test_enhanced_prompt.py::TestEnhancedPrompt::test_line_count_under_60 -x` | Exists (may need threshold update) |
| (integration) | Agent executes keyboard ops in ERP | manual | Plan 52-02 ERP scenario test | N/A |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_enhanced_prompt.py -x -v`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `test_contains_keyboard_operation_keywords` — new test method in existing file
- [ ] `test_line_count_under_60` — may need threshold adjustment if current line count + new section exceeds 60 (current: 25 lines + 5-7 new = ~32 lines, well within 60)

## Sources

### Primary (HIGH confidence)
- `.venv/.../browser_use/tools/views.py` — SendKeysAction model definition (keys parameter)
- `.venv/.../browser_use/tools/service.py` — send_keys action registration and implementation (lines 1376-1393)
- `.venv/.../browser_use/browser/watchdogs/default_action_watchdog.py` — on_SendKeysEvent handler with key aliases (lines 2371-2490)
- `.venv/.../browser_use/browser/session.py` — attach_to_session() auto-registration mechanism (line 1645)
- `.venv/.../browser_use/browser/watchdog_base.py` — attach_to_session() introspection-based handler registration (lines 243-263)
- `backend/agent/prompts.py` — Current ENHANCED_SYSTEM_MESSAGE (5 paragraphs, 25 lines)
- `backend/tests/unit/test_enhanced_prompt.py` — Existing test patterns

### Secondary (MEDIUM confidence)
- `.planning/phases/49-prompt-optimization/49-CONTEXT.md` — Phase 49 prompt design decisions (concise style, 60-line limit, Chinese language)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new dependencies, purely prompt modification
- Architecture: HIGH — send_keys API fully traced through source code, handler registration confirmed
- Pitfalls: HIGH — empty description confirmed by source code, headless clipboard issue is well-known
- Prompt effectiveness: MEDIUM — depends on Qwen 3.5 Plus compliance, needs Plan 52-02 validation

**Research date:** 2026-03-30
**Valid until:** 2026-04-30 (stable — no external API dependencies)
