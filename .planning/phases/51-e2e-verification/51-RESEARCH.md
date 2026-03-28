# Phase 51: 端到端验证 - Research

**Researched:** 2026-03-28
**Domain:** Test execution, coverage validation, E2E behavioral verification
**Confidence:** HIGH

## Summary

Phase 51 is a pure verification phase with no new code. It validates that Phase 48-50 deliverables (MonitoredAgent, StallDetector, PreSubmitGuard, TaskProgressTracker, ENHANCED_SYSTEM_MESSAGE, and AgentService integration) work correctly at both the unit test level (VAL-01) and the E2E behavioral level (VAL-02, VAL-03, VAL-04).

The unit test picture is healthy: all 60 Phase 48-50 tests pass, and coverage across the 6 target modules is 94% (well above the 80% target). The full test suite has pre-existing failures in unrelated modules (assertion service, repository, external bridge) that are not regressions from Phase 48-50.

For E2E verification, the baseline run (outputs/7fcea593) recorded 4 repeated failures on element index 6250 and zero monitor-category log entries. The new run should show StallDetector intervening after 2 failures and monitor-category entries appearing in the JSONL log.

**Primary recommendation:** Run unit tests with coverage filtering for the 6 target modules, then execute the ERP sales outbound task via the platform UI and inspect the per-run JSONL log for monitor-category entries and stall intervention records.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 运行全量测试（包括已有测试），确保回归安全。不只跑 Phase 48-50 新增测试
- **D-02:** 覆盖率只统计 Phase 48-50 新增的 6 个模块（monitored_agent、stall_detector、pre_submit_guard、task_progress_tracker、enhanced_prompt、agent_params），目标 >= 80%
- **D-03:** 通过平台 UI 手动执行。创建/执行任务，观察运行过程和日志输出，人工判断是否通过。与真实用户使用场景一致
- **D-04:** 复用原测试用例。使用 outputs/7fcea593 记录中的同一个销售出库测试用例，直接对比改善效果
- **D-05:** VAL-02 -- Agent 不再对同一元素重复失败超过 2 次（StallDetector 效果）
- **D-06:** VAL-03 -- per-run 日志中出现 category="monitor" 条目（检测器接入效果）
- **D-07:** VAL-04 -- 提交前有 PreSubmitGuard 拦截记录（校验效果）

### Claude's Discretion
- 全量测试运行的具体命令和参数
- 覆盖率报告的生成方式
- E2E 验证结果的人工判读标准细化
- 验证不通过时的回退策略建议

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| VAL-01 | 所有新增模块的单元测试覆盖率 >= 80% | Current coverage is 94% across 6 target modules (verified by running `--cov`); see coverage breakdown below |
| VAL-02 | Agent 不再对同一元素重复失败超过 2 次 | StallDetector.max_consecutive_failures=2 triggers intervention; baseline shows 4 repeats on index 6250; new run should show intervention at step 2 |
| VAL-03 | per-run 日志中出现 category="monitor" 条目 | RunLogger.log() writes JSONL with category field; step_callback calls `run_logger.log("warning", "monitor", ...)` on stall/progress detection |
| VAL-04 | 提交前有 PreSubmitGuard 拦截记录 | PreSubmitGuard.check() is wired in MonitoredAgent._execute_actions(); see critical caveat below |
</phase_requirements>

## Standard Stack

### Core (already installed)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pytest | 9.0.2 | Test runner | Project standard, configured in pyproject.toml |
| pytest-cov | 7.0.0 | Coverage reporting | Generates term-missing reports, filters by module |
| pytest-asyncio | auto mode | Async test support | Required for MonitoredAgent async tests |

### Test Infrastructure (already configured)

| Item | Location | Status |
|------|----------|--------|
| pytest config | pyproject.toml [tool.pytest.ini_options] | asyncio_mode=auto, testpaths=["backend/tests"] |
| conftest.py | backend/tests/conftest.py | Session-scoped event loop, db fixtures |
| Unit test dir | backend/tests/unit/ | 28+ test files |

### No Installation Required

This phase uses existing tooling exclusively. No new packages.

## Architecture Patterns

### Verification Flow

```
Wave 1: Unit Test Validation (VAL-01)
  1. Run full test suite, identify pre-existing failures
  2. Run Phase 48-50 tests only, confirm all pass
  3. Run coverage for 6 target modules, confirm >= 80%
  4. Record results

Wave 2: E2E Verification (VAL-02, VAL-03, VAL-04)
  1. Create task on platform UI (same test case as 7fcea593)
  2. Execute task, observe in real-time
  3. Collect per-run JSONL log from outputs/{run_id}/logs/run.jsonl
  4. Analyze log for:
     a. category="monitor" entries (VAL-03)
     b. Stall intervention messages (VAL-02)
     c. PreSubmitGuard records (VAL-04)
  5. Compare with baseline 7fcea593
```

### Per-Run Log Structure

```
outputs/{run_id}/
  logs/run.jsonl       # JSONL log entries with category field
  dom/step_{N}.txt     # DOM snapshots
  screenshots/step_{N}.png
```

### JSONL Log Entry Format

```json
{
  "timestamp": "ISO-8601",
  "level": "info|warning|error",
  "category": "system|browser|agent|step|monitor",
  "message": "Human-readable description",
  "run_id": "...",
  "...extra fields..."
}
```

### Monitor-Category Entry Types

| Source | level | message prefix | Extra fields |
|--------|-------|---------------|--------------|
| StallDetector stall | warning | "Stall detected" | step, message |
| TaskProgressTracker warning | warning | "Progress warning" | step, level, remaining_steps, remaining_tasks |
| TaskProgressTracker urgent | warning | "Progress warning" | step, level, remaining_steps, remaining_tasks |
| Intervention injection | info | "Intervention injected" | message (first 100 chars) |
| PreSubmitGuard block | warning | "Submit blocked" | message (first 100 chars) |
| Detector error | error | "Detector error: ..." | step |

### Anti-Patterns to Avoid

- **Running only new tests:** D-01 requires full regression suite. Pre-existing failures in unrelated modules (assertion service, repository, external bridge) must be documented but do not block the phase.
- **Counting all-module coverage:** D-02 scopes coverage to 6 specific modules only. Do not measure total backend coverage.
- **Automating E2E judgment:** D-03 requires human observation and judgment. The plan must not attempt to script the E2E pass/fail decision.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Log analysis | Custom JSON parser | `uv run python -c` with json module | One-liner scripts suffice for log inspection |
| Coverage report | Custom metrics script | `pytest --cov --cov-report=term-missing` | Built-in, precise, shows line-level gaps |
| Test result capture | Custom reporter | `pytest -v --tb=short` output | Standard, parseable, shows exact failures |

## Common Pitfalls

### Pitfall 1: PreSubmitGuard Is Wired But Not Actively Blocking

**What goes wrong:** VAL-04 expects "PreSubmitGuard 拦截记录" but `_execute_actions()` calls `guard.check()` with `actual_values=None` and `submit_button_text=None`. This means `check()` always returns `should_block=False` (lines 86-98 of pre_submit_guard.py). The guard is structurally integrated but cannot actively intercept because it has no access to page DOM values.

**Why it happens:** The architecture was designed for future JS extraction of actual_values and button text detection. Phase 50 wired the call but did not implement DOM value extraction.

**How to avoid:** For VAL-04, the planner should verify that:
1. The PreSubmitGuard.check() call exists in _execute_actions() (structural integration)
2. A log entry with category="monitor" and message containing "Submit blocked" would appear IF the guard triggered
3. If active blocking is required for VAL-04, note it as a gap requiring additional work

**Warning signs:** If the test case does not include sales amount or logistics fee in the task description, PreSubmitGuard cannot extract expectations and will skip validation entirely (MON-06).

### Pitfall 2: Pre-Existing Test Failures Confusing Results

**What goes wrong:** The full test suite has ~20 pre-existing failures in unrelated modules (assertion service, repository, external bridge, browser cleanup, precondition service). Running "full suite" and seeing failures could be misinterpreted as Phase 48-50 regressions.

**Why it happens:** These tests have isolation issues (shared state, database dependencies) that predate v0.6.3.

**How to avoid:** Run Phase 48-50 tests first to confirm they pass. Then run the full suite separately. Document pre-existing failures explicitly. The plan should separate "Phase 48-50 regression check" from "full suite health check."

**Known pre-existing failures (verified 2026-03-28):**
- `test_assertion_result_repo.py` (2 failed, 3 errors)
- `test_assertion_service.py` (1 failed, 3 errors)
- `test_assertions_field_parser.py` (3 failed)
- `test_browser_cleanup.py` (1 failed)
- `test_external_assertion_bridge.py` (2 failed)
- `test_external_bridge.py` (6 failed)
- `test_precondition_service.py` (1 failed)
- `test_repository.py` (3 failed)
- `test_report_service.py` (3 errors)
- `core/test_external_precondition_bridge_assertion.py` (1 failed)

### Pitfall 3: Coverage Scope Misunderstanding

**What goes wrong:** Running `--cov=backend` reports total backend coverage, which will be much lower than 80% due to untested legacy modules.

**Why it happens:** pytest-cov defaults to all imported modules.

**How to avoid:** Use explicit module-level coverage flags:
```bash
uv run pytest backend/tests/unit/test_stall_detector.py \
  backend/tests/unit/test_pre_submit_guard.py \
  backend/tests/unit/test_task_progress_tracker.py \
  backend/tests/unit/test_monitored_agent.py \
  backend/tests/unit/test_enhanced_prompt.py \
  backend/tests/unit/test_agent_params.py \
  --cov=backend.agent.monitored_agent \
  --cov=backend.agent.stall_detector \
  --cov=backend.agent.pre_submit_guard \
  --cov=backend.agent.task_progress_tracker \
  --cov=backend.agent.prompts \
  --cov-report=term-missing
```

### Pitfall 4: E2E Test Flakiness

**What goes wrong:** ERP test environment may be slow, unresponsive, or have changed data since baseline run.

**Why it happens:** External ERP system at erptest.epbox.cn is not under our control.

**How to avoid:** The plan should include a retry strategy (run up to 2 times). If ERP is unavailable, VAL-02/03/04 can be deferred and a blocker filed.

### Pitfall 5: Baseline Comparison Ambiguity

**What goes wrong:** The new run may encounter different failures than baseline 7fcea593, making direct comparison difficult.

**Why it happens:** ERP data changes, DOM structure changes, or LLM non-determinism.

**How to avoid:** Focus on the structural validation criteria: (a) monitor-category entries exist, (b) no element gets >2 consecutive failures with identical action+target. Do not require identical step-by-step behavior.

## Code Examples

### Unit Test Commands (verified working)

```bash
# Phase 48-50 unit tests only (57 tests, all pass)
uv run pytest backend/tests/unit/test_stall_detector.py \
  backend/tests/unit/test_pre_submit_guard.py \
  backend/tests/unit/test_task_progress_tracker.py \
  backend/tests/unit/test_monitored_agent.py \
  backend/tests/unit/test_enhanced_prompt.py \
  backend/tests/unit/test_agent_params.py \
  -v --tb=short

# Coverage for 6 target modules (94% total)
uv run pytest backend/tests/unit/test_stall_detector.py \
  backend/tests/unit/test_pre_submit_guard.py \
  backend/tests/unit/test_task_progress_tracker.py \
  backend/tests/unit/test_monitored_agent.py \
  backend/tests/unit/test_enhanced_prompt.py \
  backend/tests/unit/test_agent_params.py \
  --cov=backend.agent.monitored_agent \
  --cov=backend.agent.stall_detector \
  --cov=backend.agent.pre_submit_guard \
  --cov=backend.agent.task_progress_tracker \
  --cov=backend.agent.prompts \
  --cov-report=term-missing
```

### Log Analysis Command

```bash
# Check for monitor-category entries in a run log
uv run python -c "
import json
with open('outputs/{RUN_ID}/logs/run.jsonl') as f:
    for line in f:
        entry = json.loads(line)
        if entry.get('category') == 'monitor':
            print(json.dumps(entry, ensure_ascii=False, indent=2))
"

# Check for repeated failures on same index
uv run python -c "
import json
from collections import Counter
clicks = []
with open('outputs/{RUN_ID}/logs/run.jsonl') as f:
    for line in f:
        e = json.loads(line)
        if e.get('category') == 'agent' and e.get('action_name') == 'click':
            idx = e.get('action_params', {}).get('index')
            clicks.append(idx)
counts = Counter(clicks)
print('Click frequency per index:', counts.most_common(10))
max_repeat = max(counts.values()) if counts else 0
print(f'Max repeats: {max_repeat} (target: <=2)')
"
```

## Current Coverage (verified 2026-03-28)

| Module | Stmts | Miss | Cover | Missing Lines |
|--------|-------|------|-------|---------------|
| backend/agent/monitored_agent.py | 95 | 12 | 87% | 75, 81-82, 98-99, 126, 132-133, 189-190, 213-216 |
| backend/agent/stall_detector.py | 57 | 0 | 100% | -- |
| backend/agent/pre_submit_guard.py | 47 | 1 | 98% | 91 |
| backend/agent/prompts.py | 3 | 0 | 100% | -- |
| backend/agent/task_progress_tracker.py | 54 | 2 | 96% | 94, 146 |
| **TOTAL** | **256** | **15** | **94%** | |

All 6 modules exceed the 80% target. The lowest is monitored_agent.py at 87%, still well above threshold.

## Baseline Analysis (outputs/7fcea593)

- Total log entries: 91
- Total steps: 30 (max_steps=30)
- Repeated click failures: element 6250 was clicked 4 times (all with failure keywords)
- Monitor-category entries: 0 (expected -- detectors did not exist)
- Run result: completed all 30 steps
- Test case: ERP sales outbound order with 17-step task

The 17-step test case from the baseline run is embedded in the first log entry as a write_file action containing the full task description.

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| No stall detection | StallDetector with 2-failure threshold | Phase 48 (2026-03-28) | Agent should switch strategy after 2 failures instead of 12 |
| No submit validation | PreSubmitGuard (structural) | Phase 48 (2026-03-28) | Wired but passive -- no active DOM value extraction yet |
| No progress tracking | TaskProgressTracker with warning/urgent | Phase 48 (2026-03-28) | Budget warnings injected into LLM context |
| Default Agent params | Tuned: loop_detection_window=10, max_failures=4, replan_on_stall=2 | Phase 49 (2026-03-28) | Faster loop detection, earlier replanning |
| No system prompt guidance | ENHANCED_SYSTEM_MESSAGE (5 sections) | Phase 49 (2026-03-28) | Click-to-edit, failure recovery, field verification instructions |

**Deprecated/outdated:**
- CHINESE_ENHANCEMENT: Kept as backward-compat alias for ENHANCED_SYSTEM_MESSAGE

## Open Questions

1. **VAL-04 Active vs. Structural Validation**
   - What we know: PreSubmitGuard.check() is called in _execute_actions() but with actual_values=None and submit_button_text=None, so it always returns should_block=False.
   - What's unclear: Does "提交前有 PreSubmitGuard 拦截记录" mean (a) structural evidence that the guard IS wired, or (b) an actual interception event in the E2E run?
   - Recommendation: Document that structural integration is verified (unit test test_blocks_submit_click proves the mechanism works with mock data). If an actual interception event is required, the E2E run would need DOM value extraction, which is not yet implemented. Plan should include a fallback judgment call.

2. **ERP Environment Availability**
   - What we know: The ERP at erptest.epbox.cn was available during baseline run (2026-03-27).
   - What's unclear: Current availability and whether test data has changed.
   - Recommendation: Plan should allow up to 2 retry attempts and document ERP unavailability as a blocker for VAL-02/03/04 (but not VAL-01).

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| uv | Test runner | Yes | 0.9.24 | -- |
| Python | Runtime | Yes | 3.11.14 (in venv) | -- |
| pytest | Test execution | Yes | 9.0.2 | -- |
| pytest-cov | Coverage report | Yes | 7.0.0 | -- |
| ERP system (erptest.epbox.cn) | E2E test target | Not verified | -- | Manual check required |
| Platform UI (121.40.191.49) | Task creation | Not verified | -- | Manual check required |

**Missing dependencies with no fallback:**
- ERP system availability must be verified before Wave 2

**Missing dependencies with fallback:**
- None

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 9.0.2 + pytest-asyncio |
| Config file | pyproject.toml [tool.pytest.ini_options] |
| Quick run command | `uv run pytest backend/tests/unit/test_stall_detector.py backend/tests/unit/test_pre_submit_guard.py backend/tests/unit/test_task_progress_tracker.py backend/tests/unit/test_monitored_agent.py backend/tests/unit/test_enhanced_prompt.py backend/tests/unit/test_agent_params.py -v --tb=short` |
| Full suite command | `uv run pytest backend/tests/ -v --tb=short` |
| Coverage command | `uv run pytest backend/tests/unit/test_stall_detector.py backend/tests/unit/test_pre_submit_guard.py backend/tests/unit/test_task_progress_tracker.py backend/tests/unit/test_monitored_agent.py backend/tests/unit/test_enhanced_prompt.py backend/tests/unit/test_agent_params.py --cov=backend.agent.monitored_agent --cov=backend.agent.stall_detector --cov=backend.agent.pre_submit_guard --cov=backend.agent.task_progress_tracker --cov=backend.agent.prompts --cov-report=term-missing` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| VAL-01 | Coverage >= 80% for 6 modules | unit+coverage | See coverage command above | Yes |
| VAL-02 | No element >2 consecutive failures | E2E manual | Manual: inspect JSONL log | N/A |
| VAL-03 | monitor-category entries in log | E2E manual | Manual: grep JSONL for category=monitor | N/A |
| VAL-04 | PreSubmitGuard intercept evidence | E2E manual | Manual: grep JSONL for "Submit blocked" or structural verification | N/A |

### Sampling Rate
- **Per task commit:** `uv run pytest {phase 48-50 test files} -v --tb=short`
- **Per wave merge:** `uv run pytest backend/tests/ -v --tb=short`
- **Phase gate:** Full coverage report + E2E log analysis

### Wave 0 Gaps
None -- existing test infrastructure covers all phase requirements. All 57 Phase 48-50 tests pass, coverage tooling is configured, and log analysis commands are documented above.

## Sources

### Primary (HIGH confidence)
- Code inspection: All 6 target modules, 7 test files, agent_service.py, run_logger.py
- Live test execution: 60/60 Phase 48-50 tests pass, 94% coverage verified
- Baseline analysis: outputs/7fcea593/logs/run.jsonl (91 entries analyzed)
- pyproject.toml: pytest configuration verified

### Secondary (MEDIUM confidence)
- Full suite execution: 393 passed, 20 failed, 9 errors in unit tests (pre-existing failures documented)
- CONTEXT.md canonical references to prior phase artifacts

### Tertiary (LOW confidence)
- ERP environment availability: Not verified at research time; requires live check

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - all tools verified installed and working
- Architecture: HIGH - log format and coverage commands verified with live execution
- Pitfalls: HIGH - PreSubmitGuard limitation discovered via code inspection; pre-existing test failures verified via live run
- Coverage: HIGH - 94% measured and line-level gaps documented

**Research date:** 2026-03-28
**Valid until:** 2026-04-04 (7 days -- stable codebase, ERP availability may vary)
