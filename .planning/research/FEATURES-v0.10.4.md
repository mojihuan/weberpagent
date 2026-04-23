# Feature Research: v0.10.4 Playwright Code Verification and Task Management UI

**Domain:** AI-driven UI test automation platform -- Playwright code lifecycle integration
**Researched:** 2026-04-23
**Confidence:** HIGH (existing codebase well-understood, standard UI patterns)

## Existing Infrastructure (Already Built)

These features exist and the new features build directly on them:

| Existing Feature | Location | Relevance to v0.10.4 |
|-----------------|----------|---------------------|
| Playwright code generation | `backend/core/code_generator.py` | Generates pytest files saved to `outputs/` |
| SelfHealingRunner (pytest subprocess) | `backend/core/self_healing_runner.py` | Already runs pytest via subprocess with timeout, retry, LLM repair |
| Run.generated_code_path | `backend/db/models.py:71` | DB column storing path to generated test file |
| Run.healing_status / healing_attempts | `backend/db/models.py:73-75` | DB columns tracking code verification status |
| SSE execution monitoring | `backend/api/routes/runs.py` | Real-time event streaming for run progress |
| Task status: draft/ready | `backend/db/models.py:26` | Current two-value status field |
| TaskTable + TaskRow components | `frontend/src/components/TaskList/` | Table with columns: name, URL, status, steps, actions |
| StatusBadge component | `frontend/src/components/shared/StatusBadge.tsx` | Centralized status display with color config |
| Modal patterns | ConfirmModal, ImageViewer, ImportModal | Reusable modal architecture already established |
| Task CRUD API | `backend/api/routes/tasks.py` | REST endpoints for task operations |

## Feature Landscape

### Table Stakes (Users Expect These)

Features QA testers assume exist when they see "generated Playwright code" in the UI.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Task list "code" column** (UI-01) | After code generation runs, users need to see which tasks have usable code at a glance without drilling into each task | LOW | Add column to TaskTable with icon/badge. Requires backend endpoint or field to expose "has code" status per task |
| **View generated code** (UI-02) | Once code exists, viewing it is the natural next action. Users expect to see the Playwright pytest code in context | LOW | Read-only modal/panel. Code already exists on filesystem at `Run.generated_code_path`. New API endpoint to read file content, new React modal component with syntax highlighting |
| **Run code button** (UI-03) | The entire point of generating code is to re-execute it. Users expect a button to trigger this | MEDIUM | SelfHealingRunner already does subprocess pytest. Reuse its infrastructure but expose as standalone endpoint. Need async execution + status feedback (SSE or polling) |
| **Task status "success"** (STATUS-01) | When code runs successfully, the task status should reflect this. Without it, users cannot distinguish verified vs unverified tasks | LOW | Extend Task.status from `{draft, ready}` to `{draft, ready, success}`. Requires DB migration, schema update, StatusBadge update |

### Differentiators (Competitive Advantage)

Features that go beyond basic expectations and add real value.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Inline code execution feedback** | Show real-time pytest output (pass/fail per test, error summary) directly in the code viewer, not just a status badge | MEDIUM | Could reuse SSE pattern from run monitoring. Show stdout/stderr in a collapsible panel below the code |
| **Code status badge on task row** | Color-coded indicator (green=verified, yellow=unverified, red=failed, gray=no code) gives instant visual status across all tasks | LOW | Derive from latest Run's healing_status + generated_code_path. No new DB columns needed |

### Anti-Features (Commonly Requested, Often Problematic)

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| **In-place code editing** | "Let me fix the generated code directly" | Breaks the AI-driven workflow. Edits get overwritten on next run. Creates divergence between AI understanding and actual code | Keep read-only viewer. Use SelfHealingRunner LLM repair for fixes. If manual edit needed, download the file and edit locally |
| **Full IDE in browser** | "VS Code-like experience for test code" | Massive dependency (Monaco Editor ~5MB), complex integration, scope creep beyond QA tester needs | Syntax-highlighted read-only viewer with line numbers. Copy-to-clipboard for external editing |
| **Automatic task.status = success on healing pass** | "No manual step needed" | Healing can pass with flaky results. Auto-promoting hides uncertainty. Task status should be a deliberate QA decision | Show healing status prominently, let user confirm "mark as verified" manually |
| **Code execution on every run completion** | "Always verify after agent execution" | SelfHealingRunner already runs post-execution (lines 496-534 in runs.py). Re-running on every view is wasteful and slow. Creates noise when debugging | Run code on explicit user action only. Cache execution results. Show latest result in UI |

## Feature Dependencies

```
[Backend: Code content API endpoint]
    |
    v
[Frontend: Code viewer modal]  ──requires──>  [Frontend: Task list "code" column]
                                                      |
                                                      v
                                               [Frontend: Status badge extension]
                                                      |
                                                      v
[Backend: Task status = success]  <──depends on──>  [Frontend: Run code button]
         |
         v
[Backend: Standalone pytest execution endpoint]  ──reuses──>  [SelfHealingRunner]

[Backend: "has code" field on task response]  ──enhances──>  [Task list "code" column]
```

### Dependency Notes

- **Code viewer requires code content API**: The frontend needs a new endpoint `GET /tasks/{task_id}/code` or `GET /runs/{run_id}/code` that reads the generated file from disk and returns its content. Cannot show code without this.
- **Task status = success depends on run code button**: The "success" status only makes sense after the user has verified code execution. Without the run code button, there is no verification action to trigger the status change.
- **"Has code" field enhances task list**: The task list column needs to know whether any run for that task has generated code. This requires either a computed field (join query) or a denormalized field on the Task model.
- **Run code reuses SelfHealingRunner**: The existing `SelfHealingRunner.run()` method handles subprocess pytest execution, storage_state injection, timeout, and LLM repair. The new endpoint should instantiate and call it directly rather than reimplementing.
- **StatusBadge extension is additive**: Adding "success" to the existing StatusBadge config is a single-line change that does not break existing status rendering.

## Detailed Feature Specifications

### UI-01: Task List "Code" Column

**What it shows:** An icon or badge indicating whether the task has usable generated Playwright code.

**Implementation approach:**
- Backend: Add a computed field `has_code: bool` to the task list response. Query: check if any Run for this task has a non-null `generated_code_path` and file exists at that path.
- Simpler alternative: Add `has_code` as a denormalized boolean on the Task model, updated when code generation completes. This avoids N+1 file existence checks on list queries.
- Frontend: Add a column header "Code" between "Steps" and "Actions". Each row shows a small icon: checkmark (green) if has_code=true, dash (gray) if has_code=false.

**Backend query pattern:**
```python
# In TaskRepository.list()
from sqlalchemy import exists
subquery = select(
    Run.task_id,
    func.max(Run.generated_code_path).label('latest_code_path')
).group_by(Run.task_id).subquery()
# Join to determine has_code per task
```

**Complexity estimate:** LOW. One DB field + one table column.

### UI-02: View Generated Code (Read-Only Code Viewer)

**What it shows:** A modal or side panel displaying the Playwright pytest code with syntax highlighting and line numbers.

**Implementation approach:**

Backend:
- New endpoint: `GET /api/tasks/{task_id}/code` returns the content of the latest generated test file for that task.
- Logic: Find the most recent Run with a non-null `generated_code_path`, read the file, return as plain text with appropriate content-type.
- Response shape: `{ code: string, language: "python", run_id: string, generated_at: datetime, healing_status: string }`

Frontend:
- New component: `CodeViewerModal` following the existing modal pattern (see ConfirmModal, ImageViewer).
- Syntax highlighting: Add `react-syntax-highlighter` (Prism variant) as a dependency. It supports Python, has line numbers, and matches VS Code dark theme style.
- Props: `open`, `onClose`, `code`, `language`, `healingStatus`.
- Layout: Dark background modal with code block, header showing task name and healing status badge, copy-to-clipboard button.

**Why `react-syntax-highlighter` over alternatives:**
- `prism-react-renderer`: Lighter, but fewer built-in themes and less flexible styling.
- `shiki`: Better accuracy (uses VS Code grammars) but requires async WASM loading and is heavier.
- Plain `<pre>`: No syntax highlighting, defeats the purpose of a code viewer.
- `react-syntax-highlighter` is the right balance: simple API, zero config, Python support, 10+ built-in themes, line numbers built in.

**Complexity estimate:** LOW-MEDIUM. New dependency + new component + new endpoint, but straightforward patterns.

### UI-03: Run Code Button

**What it does:** Triggers pytest execution of the generated Playwright code and reports results back to the user.

**Implementation approach:**

Backend:
- New endpoint: `POST /api/tasks/{task_id}/run-code` (or `POST /api/runs/{run_id}/replay-code`).
- Logic: Locate the latest generated test file for the task. Instantiate SelfHealingRunner and call its `run()` method with the test file path and login_role from the task.
- Async execution: Use `BackgroundTasks` (same pattern as agent execution in runs.py). Return immediately with a run_code_id for status tracking.
- Status tracking: Either reuse SSE event_manager or use simple polling with a new status field.

Frontend:
- New button in TaskRow actions area (alongside existing Play, Edit, Delete, Report buttons). Icon: `Terminal` or `Code` from lucide-react.
- On click: Open the CodeViewerModal first (so user sees what will run), with a "Run" button inside the modal.
- During execution: Show loading spinner on the Run button, display progress text ("Running pytest... attempt 1/3").
- On completion: Show result (pass/fail) in the modal. If passed, offer "Mark task as verified" action.

**Key design decision -- button location:**
Place "Run code" inside the CodeViewerModal, NOT as a separate action button on the task row. Rationale:
1. User should see the code before running it (informed action).
2. Reduces button clutter on the task row (already has 4 buttons).
3. The code viewer becomes the central hub for code-related actions.
4. Matches user mental model: see code -> decide to run -> see result.

**Complexity estimate:** MEDIUM. Reuses SelfHealingRunner but needs new endpoint, async status feedback, and frontend execution state management.

### STATUS-01: Task Status Extension to "success"

**What changes:** The Task.status field gains a new value "success" (in addition to "draft" and "ready").

**Implementation approach:**

Backend:
- Update `TaskUpdate.status` validation regex: `^(draft|ready|success)$` (currently `^(draft|ready)$`).
- Add "success" to `StatusBadge` config in `frontend/src/components/shared/StatusBadge.tsx`.
- No DB migration needed -- the status column is already `String(20)`, which accepts any string value.

**When status becomes "success":**
- NOT automatic. User explicitly triggers "Mark as verified" after confirming code runs successfully.
- The action is available in the CodeViewerModal after a successful pytest run.
- Implementation: `PATCH /api/tasks/{task_id}` with `{ status: "success" }` using existing update endpoint.

**Guard rails:**
- Only allow transition to "success" if the task has at least one run with healing_status = "passed".
- This prevents marking tasks as verified without actual code verification.

**Complexity estimate:** LOW. Minimal schema change, reuse existing update endpoint.

### CODE-01: Playwright Code Verification (Backend)

**What it ensures:** The generated Playwright pytest code can run independently and pass for the corresponding test task.

**Current state analysis:**
- Code generation already happens (code_generator.py, line 481-493 in runs.py).
- SelfHealingRunner already executes the generated code post-run (lines 496-534 in runs.py).
- Healing result (pass/fail/skip) is already stored in Run.healing_status.

**What needs to happen:**
1. **Verification on demand**: The "Run code" button triggers re-execution of the latest generated code. This is a fresh pytest run, not a cached result.
2. **Verification result visibility**: The healing_status on the Run model already captures this. The frontend needs to display it clearly.
3. **Storage state injection**: SelfHealingRunner already handles this (conftest.py generation, storage_state.json). No changes needed.

**Potential issues:**
- Generated code file may have been deleted (cleanup, disk space). Backend should check file existence before attempting execution.
- Login credentials may have changed since code was generated. Re-fetch token each time (SelfHealingRunner already does this).
- Playwright browser may need updating. Already handled by `uv run pytest` which uses the project's Playwright.

**Complexity estimate:** LOW. Most infrastructure exists. Need to expose it via new endpoint.

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Task list "code" column (UI-01) | HIGH -- instant visibility | LOW -- one field + one column | P1 |
| Task status "success" (STATUS-01) | HIGH -- workflow completion | LOW -- status regex + badge config | P1 |
| View code modal (UI-02) | HIGH -- essential for code interaction | LOW-MEDIUM -- new dep + component + endpoint | P1 |
| Run code button (UI-03) | HIGH -- core verification action | MEDIUM -- new endpoint + async feedback + state | P1 |
| Code status badge on task row | MEDIUM -- visual enhancement | LOW -- derive from existing data | P2 |
| Inline execution feedback | MEDIUM -- better UX for debugging | MEDIUM -- SSE integration in modal | P2 |

**Priority key:**
- P1: Must have -- these four features form a complete code verification workflow
- P2: Should have -- enhance the P1 features, add after core flow works

## Implementation Order Recommendation

Based on dependencies and complexity:

1. **STATUS-01** (Task status = success) -- 30 min
   - Rationale: Simplest change, unlocks the workflow concept. No dependencies.
   - Changes: Backend regex, frontend StatusBadge config, TypeScript type.

2. **UI-01** (Task list "code" column) -- 1-2 hours
   - Rationale: Requires backend field addition and frontend table column. Independent of code viewer.
   - Changes: Backend computed field or denormalized column, TaskResponse schema, TaskTable column, TaskRow cell.

3. **UI-02** (View code modal) -- 2-3 hours
   - Rationale: New dependency + component + endpoint. Foundation for run code button.
   - Changes: `npm install react-syntax-highlighter`, new `GET /tasks/{id}/code` endpoint, new `CodeViewerModal` component.

4. **UI-03** (Run code button) -- 3-4 hours
   - Rationale: Depends on code viewer modal for placement. Reuses SelfHealingRunner.
   - Changes: New `POST /tasks/{id}/run-code` endpoint, async status feedback, Run button in CodeViewerModal, success -> status promotion.

5. **CODE-01** (Backend verification) -- Implicit
   - Rationale: Already implemented via SelfHealingRunner. The "run code" endpoint (step 4) is the integration point.

## Competitor Feature Analysis

| Feature | TestRail | Sauce Labs | Playwright Test UI | Our Approach |
|---------|----------|------------|-------------------|--------------|
| Code visibility | File attachment view | Test script viewer | Built-in trace viewer | Syntax-highlighted modal |
| Code execution | External CI trigger | Cloud execution | `npx playwright test` | Subprocess pytest via SelfHealingRunner |
| Task status tracking | Test case status lifecycle | Pass/fail/skip | Built-in reporter | draft -> ready -> success (explicit verification) |
| Code verification | Manual review | Automated retry | Built-in retries | LLM repair + retry (SelfHealingRunner) |

## Key Design Decisions

1. **Denormalized `has_code` on Task vs. computed at query time:** Prefer computed query. The task list is already a join query, adding a subquery for "latest run has code" is efficient enough. Avoids sync bugs between Run updates and Task field.

2. **Code viewer as modal vs. side panel:** Modal. The task list page is the primary workspace. A side panel would reduce list visibility. Modal follows existing patterns (ImageViewer, ConfirmModal).

3. **"Run code" inside modal vs. separate button:** Inside modal. User sees code before running. Reduces task row clutter. Creates natural code-centric interaction flow.

4. **Manual vs. automatic status promotion:** Manual with guard. User explicitly marks "verified" after seeing code run successfully. Guard: only allow if healing_status = "passed". Prevents false confidence from flaky passes.

5. **`react-syntax-highlighter` vs. `prism-react-renderer`:** `react-syntax-highlighter` for simplicity. More built-in themes, simpler API (`<SyntaxHighlighter language="python">{code}</SyntaxHighlighter>`), zero configuration. For a read-only viewer, the bundle size difference (approx 200KB vs 50KB) is acceptable.

## Sources

- Codebase analysis: `backend/core/self_healing_runner.py`, `backend/api/routes/runs.py`, `backend/db/models.py`
- Frontend patterns: `frontend/src/components/shared/`, `frontend/src/components/TaskList/`
- [react-syntax-highlighter](https://www.npmjs.com/package/react-syntax-highlighter) -- npm registry
- [Reddit: Best library for highlighting code blocks in React](https://www.reddit.com/r/reactjs/comments/1ln31zd/whats_the_best_library_for_highlighting_code/) -- community consensus
- [TestRail Code-first workflow](https://support.testrail.com/hc/en-us/articles/12609674354068-Code-first-workflow) -- competitor reference for code verification patterns
- [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) -- existing async execution pattern in the codebase

---
*Feature research for: v0.10.4 Playwright Code Verification and Task Management Integration*
*Researched: 2026-04-23*
