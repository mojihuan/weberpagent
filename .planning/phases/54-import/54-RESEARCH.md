# Phase 54: 文件导入 - Research

**Researched:** 2026-03-31
**Domain:** browser-use file upload mechanism, Agent parameter configuration, ENHANCED_SYSTEM_MESSAGE prompt extension
**Confidence:** HIGH

## Summary

Phase 54 adds file upload capability to the AI Agent by leveraging browser-use's built-in `upload_file(index, path)` action. The implementation requires two code changes: (1) populating `available_file_paths` with test file paths from `data/test-files/` when creating the MonitoredAgent, and (2) adding a Section 8 to ENHANCED_SYSTEM_MESSAGE guiding the Agent to use `upload_file` instead of `click` for file inputs. browser-use internally blocks `click` on file input elements and requires the dedicated `upload_file` action, which uses CDP's `DOM.setFileInputFiles` under the hood.

The `available_file_paths` parameter flows from `Agent.__init__()` through to the `upload_file` action handler via dependency injection. The action handler validates the file path is in the whitelist, checks the file exists and is non-empty, then finds the nearest file input element near the target index and uses CDP to set the file. The LLM sees available files in an `<available_file_paths>` XML tag in the agent state.

**Primary recommendation:** Pass absolute file paths from `data/test-files/` as `available_file_paths` to MonitoredAgent (which passes through to browser-use Agent via `**kwargs`). Add a concise Section 8 to ENHANCED_SYSTEM_MESSAGE with scene-action pairs and a negation instruction about not clicking file inputs.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 测试用 Excel 和图片文件预先放置在服务器 `data/test-files/` 目录下，不需要 API 动态传入
- **D-02:** Agent 服务启动时扫描 `data/test-files/` 目录，将所有文件路径自动加入 `available_file_paths` 白名单。新增测试文件无需改代码
- **D-03:** 修改 `agent_service.py`，在创建 MonitoredAgent 时传入 `available_file_paths` 参数，值为扫描 `data/test-files/` 得到的文件路径列表
- **D-04:** 添加 ENHANCED_SYSTEM_MESSAGE 第 8 段（文件上传），指导 Agent 遇到文件上传场景时使用 `upload_file` action 而非 `click`
- **D-05:** 场景-动作对格式，与 Phase 52/53 段落风格一致
- **D-06:** 中文撰写，增量控制在 10 行以内
- **D-07:** Excel 导入使用采购单导入页面验证（IMP-01）
- **D-08:** 图片上传使用商品管理中的商品图片上传功能验证（IMP-02）
- **D-09:** 两个 Plan。Plan 54-01: 基础设施（test-files 目录 + available_file_paths + prompt 第 8 段 + 测试），Plan 54-02: ERP 场景验证
- **D-10:** 结构 + 关键词检查。测试 ENHANCED_SYSTEM_MESSAGE 包含文件上传关键词，不检查具体措辞

### Claude's Discretion
- ENHANCED_SYSTEM_MESSAGE 文件上传段落的具体措辞
- 测试用例的具体关键词列表
- `data/test-files/` 目录下需要准备的具体测试文件名和内容
- 验证步骤的具体 ERP 操作流程
- `available_file_paths` 扫描逻辑的具体实现

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| IMP-01 | Agent 能触发文件上传对话框并上传 Excel 文件完成数据导入 | browser-use `upload_file(index, path)` action with CDP `DOM.setFileInputFiles`; `available_file_paths` whitelist; Section 8 prompt guidance; Excel test file in `data/test-files/` |
| IMP-02 | Agent 能触发文件上传并上传图片文件 | Same mechanism as IMP-01; image test file in `data/test-files/`; Agent must locate file input element near upload button |
</phase_requirements>

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| browser-use | installed (.venv) | Provides `upload_file` action via `UploadFileAction(index, path)` | Built-in file upload mechanism using CDP, no alternative needed |
| openpyxl | 3.1.5 | Create test Excel files programmatically | Already available via uv; lightweight XLSX creation |
| Pillow | 12.1.0 | Create test image files programmatically | Already available via uv; lightweight PNG/JPG creation |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pathlib | stdlib | Scan `data/test-files/` directory for file paths | D-02 directory scanning at service startup |
| os.path | stdlib | File existence and size validation | Verify test files are non-empty |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Programmatic file creation | Static committed test files | Static files are simpler but may corrupt in git; programmatic creation via openpyxl/Pillow guarantees correctness |

## Architecture Patterns

### Recommended Project Structure
```
data/
├── screenshots/       # existing
└── test-files/        # NEW - test files for upload
    ├── import.xlsx    # Excel import test file (created by test fixture or manually)
    └── product.jpg    # Image upload test file (created by test fixture or manually)

backend/
├── agent/
│   ├── prompts.py              # MODIFY - add Section 8 to ENHANCED_SYSTEM_MESSAGE
│   └── ...
├── core/
│   └── agent_service.py        # MODIFY - scan data/test-files/ and pass available_file_paths
└── tests/
    └── unit/
        └── test_enhanced_prompt.py  # MODIFY - add file upload keyword assertions
```

### Pattern 1: available_file_paths Injection
**What:** browser-use Agent accepts `available_file_paths: list[str]` at construction time. The list is passed to the `upload_file` action handler via dependency injection. The LLM sees these paths in an `<available_file_paths>` XML tag in the agent state context.
**When to use:** Every Agent instantiation that needs file upload capability.
**Flow:**
```
agent_service.py scans data/test-files/
  -> list of absolute paths
  -> passed as available_file_paths kwarg to MonitoredAgent
    -> passes through **kwargs to browser_use.Agent.__init__
      -> self.available_file_paths = [...]
        -> injected into upload_file action handler
        -> formatted as <available_file_paths> in LLM context
```
**Example:**
```python
# agent_service.py
from pathlib import Path

def scan_test_files() -> list[str]:
    """Scan data/test-files/ for uploadable files."""
    test_dir = Path("data/test-files")
    if not test_dir.exists():
        return []
    return [str(f.resolve()) for f in test_dir.iterdir() if f.is_file()]

# In run_with_streaming():
file_paths = scan_test_files()
agent = MonitoredAgent(
    task=actual_task,
    llm=llm,
    browser_session=browser_session,
    available_file_paths=file_paths,  # NEW
    extend_system_message=ENHANCED_SYSTEM_MESSAGE,
    # ... other params
)
```

### Pattern 2: Scene-Action Pair Prompt (Section 8)
**What:** Follow Phase 52/53 pattern: concise Chinese instructions with scene-action pairs and negation instructions, under 10 lines.
**When to use:** Adding ENHANCED_SYSTEM_MESSAGE Section 8 for file upload guidance.
**Example:**
```python
## 8. 文件上传
遇到导入/上传按钮打开文件选择时 → 不要 click file input 元素（会被拦截），用 upload_file(index, '文件路径') 上传。
文件路径从 <available_file_paths> 中选择匹配类型的文件。上传后等待文件名显示确认成功。
不要尝试 click type="file" 的 input 元素，也不要用 evaluate 模拟文件选择。
```

### Pattern 3: Keyword-Based Test (D-10)
**What:** Test ENHANCED_SYSTEM_MESSAGE contains key terms without exact string matching, plus line count constraint.
**When to use:** Verifying prompt content additions.
**Example:**
```python
def test_contains_file_upload_keywords(self):
    """IMP-01~02: Must contain file upload guidance with key terms."""
    lower = ENHANCED_SYSTEM_MESSAGE.lower()
    assert "upload_file" in lower
    assert "file input" in lower or "文件上传" in ENHANCED_SYSTEM_MESSAGE
    assert "文件上传" in ENHANCED_SYSTEM_MESSAGE

def test_file_upload_section_line_count(self):
    """D-06: File upload section must not exceed 10 lines."""
    lines = ENHANCED_SYSTEM_MESSAGE.splitlines()
    section_start = None
    section_end = None
    for i, line in enumerate(lines):
        if line.strip().startswith("## 8."):
            section_start = i
        elif section_start is not None and line.strip().startswith("## "):
            section_end = i
            break
    assert section_start is not None, "Section '## 8.' not found"
    end = section_end if section_end is not None else len(lines)
    section_lines = [l for l in lines[section_start:end] if l.strip()]
    assert len(section_lines) <= 10
```

### Anti-Patterns to Avoid
- **Clicking file input elements:** browser-use's click handler (default_action_watchdog.py:348-354) explicitly detects file input elements and returns `validation_error` instead of executing the click. The Agent must use `upload_file` action.
- **Empty test files:** browser-use validates file size > 0 bytes before upload (service.py:782-785). Test files must have actual content.
- **Relative file paths:** browser-use's upload_file checks paths against `available_file_paths` list (service.py:748). If paths don't match exactly, upload fails. Use absolute paths (`Path.resolve()`) consistently.
- **Passing available_file_paths to wrong layer:** Must go to `Agent.__init__` (or `MonitoredAgent` which passes through `**kwargs`), not as a parameter to tools or controller directly.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| File input interaction | Custom CDP file upload code | browser-use `upload_file(index, path)` action | browser-use already implements CDP `DOM.setFileInputFiles`, path validation, element searching, and error handling |
| File path whitelist | Custom security layer | browser-use `available_file_paths` parameter | Built-in whitelist enforcement in action handler (service.py:748) |
| Finding file input elements near buttons | Custom DOM traversal | browser-use `find_file_input_near_element()` | Built-in BFS search up parent tree and descendants (service.py:796-818) |

**Key insight:** browser-use has a complete file upload pipeline -- whitelist validation, existence check, empty-file check, element proximity search, and CDP upload. The only thing needed is providing the whitelist and prompting the Agent correctly.

## Common Pitfalls

### Pitfall 1: Click on File Input Blocked
**What goes wrong:** Agent tries to `click(index)` on a file input element, which browser-use blocks with `validation_error`.
**Why it happens:** browser-use's click handler explicitly checks `is_file_input(element_node)` and returns an error (watchdog:350-354).
**How to avoid:** Section 8 prompt must contain strong negation instruction: "do NOT click file input elements, use upload_file instead."
**Warning signs:** Agent step returns validation_error mentioning "file upload dialog."

### Pitfall 2: File Path Not in Whitelist
**What goes wrong:** `upload_file` fails with "File path X is not available" error.
**Why it happens:** The path provided to the action does not exactly match an entry in `available_file_paths`. Common when using relative paths vs absolute paths.
**How to avoid:** Always use `Path.resolve()` to get absolute paths when scanning `data/test-files/`. Ensure the same absolute path format is used throughout.
**Warning signs:** Agent step returns error with "not available" and suggests adding to `available_file_paths`.

### Pitfall 3: Empty Test File
**What goes wrong:** Upload fails with "File X is empty (0 bytes)" error.
**Why it happens:** Test file was created but not written with content, or was corrupted.
**How to avoid:** When creating test files programmatically, write actual data (at minimum one cell in Excel, at minimum 1x1 pixel in image). Validate files after creation.
**Warning signs:** Agent step returns error mentioning "empty" or "0 bytes."

### Pitfall 4: Agent Cannot Find File Input Element
**What goes wrong:** `upload_file` reports "Element with index X does not exist" or cannot find a file input near the target.
**Why it happens:** The index provided is not pointing to a file input or an element near one. ERP upload buttons may not be directly adjacent to the hidden file input in the DOM.
**How to avoid:** Agent should first click the "import" or "upload" button to trigger the file input, then identify the file input's index from the updated DOM snapshot, then use `upload_file`. The prompt should guide this two-step flow.
**Warning signs:** Agent repeatedly tries upload_file with wrong indices, or tries to click the file input directly.

### Pitfall 5: Test Files Missing on Server
**What goes wrong:** `scan_test_files()` returns empty list, no files available for upload.
**Why it happens:** `data/test-files/` directory doesn't exist on server, or files weren't deployed.
**How to avoid:** Create test files as part of Plan 54-01. Ensure `.gitignore` doesn't exclude `data/test-files/`. Consider programmatic creation via test fixtures or a setup script.
**Warning signs:** `available_file_paths` is empty; Agent has no files to reference.

## Code Examples

### browser-use UploadFileAction Model
```python
# Source: .venv/.../browser_use/tools/views.py:127-129
class UploadFileAction(BaseModel):
    index: int
    path: str
```

### browser-use upload_file Action Handler (Key Validation Logic)
```python
# Source: .venv/.../browser_use/tools/service.py:743-785
async def upload_file(
    params: UploadFileAction, browser_session: BrowserSession,
    available_file_paths: list[str], file_system: FileSystem
):
    # Step 1: Whitelist check
    if params.path not in available_file_paths:
        # ... fallback checks for downloaded files and file_system
        # If all fail, returns error

    # Step 2: File existence and size check (local browser only)
    if browser_session.is_local:
        if not os.path.exists(params.path):
            return ActionResult(error=f'File {params.path} does not exist')
        if os.path.getsize(params.path) == 0:
            return ActionResult(error=f'File {params.path} is empty (0 bytes)')

    # Step 3: Find element by index, then find nearby file input
    selector_map = await browser_session.get_selector_map()
    node = selector_map[params.index]
    # ... BFS search for file input near element
```

### browser-use Click Block on File Input
```python
# Source: .venv/.../browser_use/browser/watchdogs/default_action_watchdog.py:350-354
if self.browser_session.is_file_input(element_node):
    msg = f'Index {index_for_logging} - has an element which opens file upload dialog. To upload files please use a specific function to upload files'
    return {'validation_error': msg}
```

### available_file_paths in LLM Context
```python
# Source: .venv/.../browser_use/agent/prompts.py:348-350
if self.available_file_paths:
    available_file_paths_text = '\n'.join(self.available_file_paths)
    agent_state += f'<available_file_paths>{available_file_paths_text}\nUse with absolute paths</available_file_paths>\n'
```

### Existing MonitoredAgent Kwargs Passthrough
```python
# Source: backend/agent/monitored_agent.py:38-47
class MonitoredAgent(Agent):
    def __init__(self, *, stall_detector=None, pre_submit_guard=None,
                 task_progress_tracker=None, run_logger=None, **kwargs):
        super().__init__(**kwargs)  # available_file_paths passes through here
        # ...
```

### Existing Agent Construction in agent_service.py
```python
# Source: backend/core/agent_service.py:349-364
agent = MonitoredAgent(
    task=actual_task,
    llm=llm,
    browser_session=browser_session,
    max_actions_per_step=5,
    register_new_step_callback=step_callback,
    extend_system_message=ENHANCED_SYSTEM_MESSAGE,
    loop_detection_window=10,
    max_failures=4,
    planning_replan_on_stall=2,
    enable_planning=True,
    stall_detector=stall_detector,
    pre_submit_guard=pre_submit_guard,
    task_progress_tracker=task_progress_tracker,
    run_logger=run_logger,
)
# NOTE: available_file_paths is NOT currently passed -- this is the gap to fill
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| N/A (new feature) | browser-use `upload_file` action with CDP | browser-use 0.3.x+ | Native file upload support without custom CDP code |

**No deprecated items in this phase** -- file upload is a new capability being added to the Agent.

## Open Questions

1. **Test file deployment to server**
   - What we know: Server at 121.40.191.49, project at `/root/project/weberpagent/`. Test files need to be at `data/test-files/` on the server.
   - What's unclear: Whether test files should be committed to git (tracked) or created programmatically on server startup (ephemeral).
   - Recommendation: Create test files programmatically using openpyxl and Pillow as part of a setup utility. This avoids binary file git issues and ensures files are always valid. Alternatively, commit small binary files -- both approaches are viable.

2. **ERP import page flow specifics**
   - What we know: 采购单导入页面 has an "import" button (D-07). 商品管理 has image upload (D-08).
   - What's unclear: Exact DOM structure of the import button and whether clicking it reveals a hidden file input, or if the file input is already visible in DOM.
   - Recommendation: Plan 54-02 (ERP verification) should first explore the page DOM to understand the upload flow before writing verification steps.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| openpyxl | Excel test file creation | Available (uv) | 3.1.5 | -- |
| Pillow | Image test file creation | Available (uv) | 12.1.0 | -- |
| browser-use | upload_file action | Available (.venv) | installed | -- |
| Server filesystem | data/test-files/ storage | Available | -- | -- |

**Missing dependencies with no fallback:**
- None -- all dependencies available.

**Missing dependencies with fallback:**
- None.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest |
| Config file | pyproject.toml (project root) |
| Quick run command | `uv run pytest backend/tests/unit/test_enhanced_prompt.py -x -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| IMP-01 | ENHANCED_SYSTEM_MESSAGE contains file upload keywords (upload_file, file input) | unit | `uv run pytest backend/tests/unit/test_enhanced_prompt.py::TestEnhancedPrompt::test_contains_file_upload_keywords -x` | Wave 0 (extend existing) |
| IMP-01 | Section 8 line count <= 10 | unit | `uv run pytest backend/tests/unit/test_enhanced_prompt.py::TestEnhancedPrompt::test_file_upload_section_line_count -x` | Wave 0 (extend existing) |
| IMP-02 | Same prompt covers image upload | unit | Covered by IMP-01 keywords test | -- |
| IMP-01 | scan_test_files() returns files from data/test-files/ | unit | `uv run pytest backend/tests/unit/test_agent_service.py -x -k scan_test_files` | Wave 0 (new) |
| IMP-01 | available_file_paths passed to MonitoredAgent | integration | `uv run pytest backend/tests/ -x -k agent_service` | Wave 0 (extend existing or new) |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/test_enhanced_prompt.py -x -v`
- **Per wave merge:** `uv run pytest backend/tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `test_contains_file_upload_keywords` -- covers IMP-01/02 prompt keywords
- [ ] `test_file_upload_section_line_count` -- covers D-06 line constraint
- [ ] `test_scan_test_files` or equivalent -- covers D-02 directory scanning
- [ ] Test files in `data/test-files/` -- physical test assets (Excel + image)

## Sources

### Primary (HIGH confidence)
- `.venv/.../browser_use/tools/views.py:127-129` -- UploadFileAction model definition
- `.venv/.../browser_use/tools/service.py:743-818` -- upload_file action implementation with whitelist, validation, element search
- `.venv/.../browser_use/browser/watchdogs/default_action_watchdog.py:348-354` -- click file input block
- `.venv/.../browser_use/browser/watchdogs/default_action_watchdog.py:2576-2612` -- on_UploadFileEvent CDP upload
- `.venv/.../browser_use/agent/service.py:173,251-252,304` -- Agent.__init__ available_file_paths parameter
- `.venv/.../browser_use/agent/prompts.py:348-350` -- available_file_paths LLM context injection
- `backend/agent/prompts.py` -- existing 7-section ENHANCED_SYSTEM_MESSAGE (45 lines)
- `backend/core/agent_service.py` -- current MonitoredAgent construction (no available_file_paths yet)
- `backend/agent/monitored_agent.py` -- **kwargs passthrough to browser-use Agent
- `backend/tests/unit/test_enhanced_prompt.py` -- existing test patterns

### Secondary (MEDIUM confidence)
- `.planning/phases/52-prompt/52-CONTEXT.md` -- Phase 52 keyboard prompt pattern reference
- `.planning/phases/53-prompt/53-CONTEXT.md` -- Phase 53 table prompt pattern reference

### Tertiary (LOW confidence)
- None -- all findings verified against source code.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH -- all libraries already installed, verified via uv pip list
- Architecture: HIGH -- traced complete data flow from agent_service.py through browser-use Agent to action handler to CDP
- Pitfalls: HIGH -- verified against browser-use source code (click block, path validation, empty file check)
- Prompt pattern: HIGH -- follows established Phase 52/53 pattern with known constraints

**Research date:** 2026-03-31
**Valid until:** 2026-04-30 (stable -- browser-use file upload mechanism unlikely to change)
