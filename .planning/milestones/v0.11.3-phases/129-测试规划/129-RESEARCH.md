# Phase 129: 测试规划 - Research

**Researched:** 2026-05-04
**Domain:** Test scenario derivation from code review findings; test prioritization methodology
**Confidence:** HIGH

## Summary

Phase 129 is a review-only phase that reads ~390 findings from Phase 125-128 (backend core: 32 actionable, API layer: 78, frontend: 95, code quality: 81) and identifies which findings would benefit from automated test protection. The output is a prioritized test scenario list in `129-FINDINGS.md`, not test code.

The project currently has zero test coverage -- the test suite was deleted in Phase 120 (v0.11.0) and never rebuilt. pytest, pytest-asyncio, and pytest-playwright dependencies exist in `pyproject.toml`, but there is no `conftest.py`, no `backend/tests/` directory, and no frontend test framework. Seven E2E spec files exist using Playwright but use conditional skip patterns and flexible assertions.

The core methodology for this phase is: (1) filter Phase 125-128 findings for testability (would a test catch regression?), (2) classify by test type (unit/integration/E2E), (3) score by ROI (severity x regression_risk / implementation_cost), (4) organize in the FINDINGS format matching Phase 125-128. The 5 systemic patterns from Phase 128 (CP-1 through CP-5) are high-ROI integration test candidates because they span multiple modules and are most vulnerable to regression during refactoring.

**Primary recommendation:** Use a structured filter-classify-score pipeline. First filter findings where automated tests provide genuine regression protection (not findings fixable by one-time code changes). Then classify remaining findings into test types per D-03 (backend unit > backend integration > frontend component > E2E). Score by ROI using severity from the original findings, estimated regression risk, and implementation cost. The output should map each test scenario to its source finding(s) so the future test implementation milestone can trace back to the original review rationale.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** 严重程度驱动排序 -- 按 Phase 125-128 发现的严重程度 (Critical > High > Medium > Low) 排序测试场景优先级。直接保护最高风险区域
- **D-02:** 从审查发现推导 -- 不是独立做边界分析，而是从 390 条审查发现中筛选「写测试能防回归」的部分。不需要覆盖全部发现，只识别有回归保护价值的场景
- **D-03:** 后端优先 -- 按后端单元测试 -> 后端集成测试 -> 前端组件测试 -> E2E 补充的顺序组织。后端无测试保护、风险最高，优先建立基线
- **D-04:** E2E 现有覆盖补充 -- 已有 7 个 E2E spec 文件，识别缺失的 E2E 场景但不作为重点
- **D-05:** 仅输出清单 -- Phase 129 是 review-only，不写测试代码、不设计 fixtures/mocks、不创建测试基础设施
- **D-06:** 延续 FINDINGS 格式 -- 输出到 `129-FINDINGS.md`，与 Phase 125-128 保持格式一致。按严重程度分级、分层组织
- **D-07:** 每个测试场景包含：场景名称、描述、对应审查发现引用（如 "See 125-FINDINGS.md #BD-08"）、推荐测试类型（unit/integration/e2e）、优先级
- **D-08:** 建议延续 3-plan 结构：
  - **Plan 1 (129-01):** 汇总分析 -- 读取 125-128 FINDINGS，筛选可测试验证的发现，按严重程度排序
  - **Plan 2 (129-02):** 后端测试场景详列 -- 对后端 Critical/High 发现推导具体测试场景（单元 + 集成）
  - **Plan 3 (129-03):** 前端 + E2E 测试场景 + 总结 -- 前端和 E2E 补充场景 + 最终统计

### Claude's Discretion
- 每条发现是否「适合写测试」的判断标准
- 后端单元测试与集成测试的边界划分
- E2E 缺失场景的具体优先级排序
- 最终统计数据和分组方式

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| TEST-01 | 识别关键测试缺失 -- 哪些核心业务流程缺少测试保护、高 ROI 测试场景 | The 5 systemic patterns (CP-1~CP-5), high/critical findings from 125-128, and TESTING.md recommended additions provide the raw material. This research defines the filter-classify-score methodology for identifying which findings map to high-ROI test scenarios. |
| TEST-02 | 识别边界情况覆盖不足 -- 边界值、异常路径、竞态条件、超时场景 | Phase 125-128 findings explicitly document boundary conditions (dual stall detection, precondition failure skipping started event, corrective evaluate detection, etc.). The methodology classifies these into test types: boundary value tests, error path tests, race condition tests, timeout tests. |
</phase_requirements>

## Standard Stack

### Core (Test Framework -- already in pyproject.toml)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pytest | 8.0.0+ | Python test framework | Industry standard for Python testing; already configured in pyproject.toml |
| pytest-asyncio | 0.24.0+ | Async test support | Required for all backend tests (FastAPI + SQLAlchemy async); already in pyproject.toml |
| pytest-playwright | 0.7.0+ | Browser automation in tests | Required for E2E tests; already in pyproject.toml |

### Supporting (Dev Dependencies)
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest-timeout | 2.4.0+ | Test execution timeout | Prevent hanging tests, especially for async/integration tests |
| pytest-html | 4.0.0+ | HTML test reports | Test result visualization |
| @playwright/test | ^1.51.1 | E2E test framework | Frontend E2E tests; already configured in e2e/playwright.config.ts |

### Not Yet Present (Future Implementation Milestone)
| Library | Purpose | When to Use |
|---------|---------|-------------|
| pytest-cov | Coverage reporting | Implementation phase, not this phase |
| pytest-mock | Enhanced mocking | Implementation phase, for LLM/browser mocks |
| vitest + testing-library | Frontend unit tests | Implementation phase; not configured yet |

**Note:** This phase does NOT install or configure anything. The standard stack is listed for reference -- the planner needs to know what will be available during the future test implementation milestone.

## Architecture Patterns

### Recommended Test Organization (for future implementation)

```
backend/tests/
  conftest.py                    # Shared fixtures (db_session, mock_llm, client)
  unit/
    test_stall_detector.py       # Unit tests for pure logic modules
    test_task_progress_tracker.py
    test_action_utils.py
    test_time_utils.py
    test_random_generators.py
    test_cache_service.py
    test_schemas.py              # Pydantic validation
    test_excel_parser.py
    test_error_utils.py
    test_action_translator.py
    test_step_code_buffer.py
  integration/
    test_repository.py           # CRUD with in-memory SQLite
    test_run_pipeline.py         # Pipeline stage integration
    test_agent_service.py        # Agent lifecycle with mocks
    test_event_manager.py        # SSE pub/sub lifecycle
    test_assertion_service.py    # Assertion evaluation
    test_precondition_service.py # Precondition execution
    test_code_generator.py       # Code generation pipeline
    test_api_routes.py           # FastAPI TestClient
  e2e/
    (existing e2e/tests/ directory)

frontend/src/
  __tests__/                     # (future, no framework configured yet)
```

### Pattern 1: Filter-Classify-Score Pipeline (this phase's methodology)

**What:** A three-stage pipeline to derive test scenarios from review findings.

**Stage 1 -- Filter:** Read each finding from 125-128. Ask: "If this bug reappeared after a refactor, would an automated test catch it?" If yes, the finding is testable. Findings that are one-time fixes (unused imports, naming issues, dead code removal) do NOT need tests -- they are already fixed and won't regress.

**Stage 2 -- Classify:** For each testable finding, determine the test type:
- **Unit test:** Pure logic, no external dependencies. Examples: StallDetector.check(), TaskProgressTracker.update_from_evaluation(), Excel parser, Pydantic schema validation.
- **Integration test:** Requires database, API, or mock of external services. Examples: Repository CRUD, pipeline stage orchestration, SSE event flow, assertion evaluation.
- **E2E test:** Requires full stack running. Examples: User workflows currently covered by existing specs.

**Stage 3 -- Score:** Rate each scenario by ROI:
- **ROI = Severity x Regression_Risk / Implementation_Cost**
- Severity: Directly from the finding's severity rating (Critical=4, High=3, Medium=2, Low=1)
- Regression Risk: How likely is this to regress after code changes? (High for mutable state, shared instances, cross-module coupling; Low for isolated pure functions)
- Implementation Cost: How hard to write the test? (Low for pure functions, Medium for DB tests, High for async/browser-dependent tests)

**When to use:** This is the primary methodology for this phase.

### Pattern 2: Systemic Pattern Test Derivation

**What:** The 5 systemic patterns from Phase 128 (CP-1 through CP-5) are cross-module issues that are especially high-value for testing.

| Pattern | Test Type | Key Scenario |
|---------|-----------|-------------|
| CP-1 Memory leak (unbounded growth) | Integration | Verify cleanup() is called after run completion; verify _events is empty; verify useRunStream arrays are bounded |
| CP-2 Error handling at boundaries | Unit + Integration | Test SSE publish with broken subscriber; test JSON.parse with malformed event; test event_manager.publish with queue error |
| CP-3 Installed-but-unused | Manual verification | Document that StructuredLogger/React Query have zero consumers; not a test scenario but a finding |
| CP-4 Blocking in async context | Integration | Test save_screenshot does not block event loop; test subprocess.run does not block concurrent requests |
| CP-5 Mutable state coupling | Unit + Integration | Test that context mutation in external assertions does not leak to variable_map; test that setState callbacks produce correct state |

### Pattern 3: Finding-to-Test Mapping Rules

**What:** Rules for determining which findings are worth protecting with tests.

**Worth a test (HIGH regression protection value):**
- Correctness bugs with specific input/output expectations (dual stall detection, assertion stub, IndexError in multi-action)
- Error handling gaps (SSE stream, JSON.parse, publish failures)
- State mutation leaks (context mutation, variable_map filter)
- Race conditions (heartbeat task overwrite, batch partial creation)
- Performance regressions with measurable thresholds (blocking I/O, wait times)

**NOT worth a test (fix once, won't regress):**
- Unused imports (ruff catches these)
- Naming issues (l -> loc, Optional -> pipe syntax)
- Dead code removal (PreSubmitGuard dead code, response.py unused helpers)
- Missing type annotations
- Documentation issues

**Borderline (judge per case):**
- Architecture issues (coupling, god-module) -- test the behavior, not the architecture
- Security issues (path traversal, CORS) -- integration test with specific attack payloads
- Configuration issues (hardcoded DEBUG) -- test that settings control behavior

### Anti-Patterns to Avoid
- **Testing implementation details:** Tests should verify observable behavior (output, state, side effects), not internal method calls or variable names.
- **Testing dead code:** PreSubmitGuard's core logic is unreachable -- no point testing it until the caller is fixed. Mark as "not testable until fix."
- **Testing third-party library behavior:** Don't test that Pydantic validates correctly; test that YOUR schemas define the right constraints.
- **Counting findings instead of test scenarios:** One finding may produce 0 test scenarios (dead code) or 5 (complex pipeline stage with multiple failure modes).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Test result formatting | Custom markdown generator | Direct FINDINGS format (severity + category + description + recommendation) | Consistency with 125-128 format; D-06 mandate |
| ROI scoring system | Complex weighted algorithm | Simple severity x regression_risk / cost formula | Transparent and defensible; complexity not warranted for a review phase |
| Test type classification | Machine learning or NLP | Manual judgment per finding with documented criteria | Human judgment catches nuances (e.g., "this looks like a unit test but actually needs browser mocks") |

**Key insight:** This phase is analysis work, not implementation. The don't-hand-roll items are about not over-engineering the analysis methodology.

## Common Pitfalls

### Pitfall 1: Confusing "finding" with "test scenario"
**What goes wrong:** Treating every finding as needing a test. Many findings are one-time fixes (unused imports, naming) that won't regress.
**Why it happens:** Natural tendency to achieve complete coverage of input data.
**How to avoid:** Apply the filter rule: "If this is already fixed and cannot regress, it does not need a test." Dead code removal, import cleanup, and naming fixes are one-time improvements.
**Warning signs:** Test scenario count approaches finding count (~390). Realistic ratio is 20-30%.

### Pitfall 2: Ignoring the "testability prerequisite" gap
**What goes wrong:** Creating test scenarios for bugs that require a code fix first. For example, PreSubmitGuard's core logic is unreachable (actual_values is always None). You cannot test the guard's behavior until the caller is fixed.
**Why it happens:** The finding describes a real bug, but the fix is a prerequisite for testing.
**How to avoid:** Tag test scenarios as "requires fix first" vs. "testable now." The planner should separate these -- "requires fix first" scenarios belong in a post-fix milestone.
**Warning signs:** Test scenario describes testing code that is currently unreachable.

### Pitfall 3: Over-indexing on unit tests at the expense of integration coverage
**What goes wrong:** Writing unit test scenarios for every pure function while missing the high-value integration paths (pipeline stages, SSE flow, batch execution).
**Why it happens:** Unit tests are easier to describe and cheaper to implement.
**How to avoid:** Per D-03, prioritize by test type. But within each priority tier, weight integration tests higher because they catch cross-module regressions that unit tests miss. The 5 systemic patterns (CP-1~CP-5) are all integration-level concerns.
**Warning signs:** 80%+ of test scenarios are unit tests for utility functions.

### Pitfall 4: Creating vague test scenarios that cannot be implemented
**What goes wrong:** Writing "test the pipeline" without specifying what input, what expected output, what mock setup.
**Why it happens:** Review-level analysis may not drill down to implementation specifics.
**How to avoid:** Per D-07, each test scenario must have: name, description, source finding reference, recommended test type, priority. The description should include enough specificity (what to assert, what to mock) that a future implementer can write the test without re-reading the finding.
**Warning signs:** Test scenario description is shorter than 2 sentences.

### Pitfall 5: Duplicating findings across plans
**What goes wrong:** The same finding appears in Plan 1 (summary analysis), Plan 2 (backend detail), and Plan 3 (final summary), creating confusion about which plan "owns" the test scenario.
**Why it happens:** 3-plan structure with summary + detail + summary creates overlap.
**How to avoid:** Plan 1 produces the filtered list. Plan 2 expands backend scenarios. Plan 3 expands frontend/E2E scenarios. The final summary in Plan 3 is a statistical rollup, not a re-listing.
**Warning signs:** A finding is described with test scenarios in multiple plans.

### Pitfall 6: Missing the E2E gap analysis
**What goes wrong:** Focusing entirely on backend unit/integration tests and forgetting to identify gaps in the existing 7 E2E spec files.
**Why it happens:** E2E is explicitly lower priority per D-04.
**How to avoid:** Dedicate a section to E2E gaps. The existing E2E tests cover happy paths. Missing E2E scenarios include: error path flows (failed preconditions, assertion failures), batch execution monitoring, external module integration, and the stop-run flow.
**Warning signs:** No E2E gap section in the output.

## Code Examples

### Example: Finding-to-Test-Scenario Derivation (this phase's output format)

```markdown
### [TS-BE-01] StallDetector double-invocation causes premature stall intervention
- **Severity:** High (from 125-FINDINGS BD-08, 128-FINDINGS BD-08)
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P1 agent_service.py:340-347
- **Description:** Verify that calling `StallDetector.check()` with consecutive failure
  records triggers `should_intervene=True` at the correct threshold (not at half threshold).
  Test with: (1) N failures recorded once -> assert intervention at N. (2) N failures
  recorded twice (simulating dual invocation) -> assert intervention at N/2 (demonstrating
  the bug). (3) Mixed success/failure -> assert correct reset behavior.
- **Priority:** P0 -- protects a High-severity correctness bug with high regression risk
- **Mock requirements:** None (pure logic, no external dependencies)
- **Implementation cost:** Low
```

### Example: Integration Test Scenario from Systemic Pattern

```markdown
### [TS-BE-15] EventManager cleanup prevents memory leak across multiple runs
- **Severity:** High (from CP-1, 125-FINDINGS P2 event_manager.py:27)
- **Test Type:** Integration
- **Source Finding:** See 125-FINDINGS.md P2 event_manager.py:27; 128-FINDINGS CP-1
- **Description:** (1) Subscribe to a run, publish events, verify cleanup(run_id) removes
  all stored events. (2) Run full pipeline (mocked agent), verify cleanup is called in
  _finalize_run. (3) Verify heartbeat task is cancelled and removed after cleanup.
  (4) Verify re-subscribe does not leak previous heartbeat task.
- **Priority:** P0 -- systemic pattern, protects long-running server stability
- **Mock requirements:** Mock agent execution, real EventManager instance
- **Implementation cost:** Medium
```

### Example: Testability Prerequisite Tag

```markdown
### [TS-BE-XX] PreSubmitGuard blocks submit when actual values differ from expected
- **Severity:** High (from 125-FINDINGS P1 monitored_agent.py:113-114)
- **Test Type:** Unit
- **Source Finding:** See 125-FINDINGS.md P1 monitored_agent.py:113-114
- **Description:** Test PreSubmitGuard.check() with actual_values != expected_values
  verifies should_block=True. Test with matching values -> should_block=False.
- **Priority:** DEFERRED -- requires code fix first (wire up DOM value extraction in MonitoredAgent)
- **Mock requirements:** None (pure logic)
- **Implementation cost:** Low (test), High (fix prerequisite)
- **Note:** Test scenario is valid but the feature is currently dead code. Cannot be tested until the caller provides non-None actual_values.
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual test scenario brainstorming | Review-driven test derivation | This project's approach | Grounded in actual findings, not hypothetical risk |
| Severity-only prioritization | ROI scoring (severity x risk / cost) | Industry best practice | More nuanced; avoids over-investing in easy but low-risk tests |
| Unit test first | Integration test first for risk | Recent shift (2024+) | Cross-module bugs are harder to catch with unit tests alone |

**Outdated approaches to avoid:**
- Code coverage percentage as primary goal (without context, 80% coverage of utility functions provides less protection than 20% coverage of pipeline integration paths)
- Test-per-function mapping (not every function needs its own test; focus on behavior boundaries)

## Open Questions

1. **What is the expected test scenario count?**
   - What we know: ~390 findings, estimated 20-30% testability rate = ~80-120 scenarios
   - What's unclear: Whether the planner should aim for a specific target or let the filter drive the count
   - Recommendation: Let the filter drive. The 20-30% estimate is a sanity check, not a target. If the count is below 40 or above 150, re-examine the filtering criteria.

2. **Should "requires fix first" scenarios be included in the output?**
   - What we know: Several High findings involve dead code or unreachable paths (PreSubmitGuard, assertion_service stub)
   - What's unclear: Whether to include these as "deferred" test scenarios or exclude them entirely
   - Recommendation: Include with a "DEFERRED" tag and a "requires fix first" note. The future milestone needs to know what tests to write after fixing the underlying bugs.

3. **Should E2E gap scenarios reference the existing 7 spec files specifically?**
   - What we know: Existing E2E tests use conditional skip and flexible assertions (documented anti-patterns in TESTING.md)
   - What's unclear: Whether E2E gap scenarios should also recommend fixing existing test anti-patterns
   - Recommendation: Focus on missing E2E scenarios (new tests needed). Note existing test anti-patterns as informational, not as test scenarios. Fixing existing test quality is a separate concern.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python 3.11+ | Backend test execution (future) | Python 3.14.3 | 3.14.3 | -- |
| uv | Package management | uv 0.9.24 | 0.9.24 | -- |
| npm | Frontend tooling | npm 10.9.4 | 10.9.4 | -- |
| pytest | Test runner (future) | In pyproject.toml | 8.0.0+ | -- |
| Playwright | E2E tests | Configured | ^1.51.1 | -- |

**Missing dependencies with no fallback:** None -- this phase requires no external tools beyond reading files.

**Missing dependencies with fallback:** N/A -- this is a review-only phase with no execution requirements.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | N/A -- this phase produces test scenarios, not test code |
| Config file | N/A |
| Quick run command | N/A |
| Full suite command | N/A |

### Phase Requirements to Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| TEST-01 | Identify missing test coverage for core business flows | Manual review | `Read 125-128 FINDINGS.md` | Input files exist |
| TEST-02 | Identify boundary value, error path, race condition gaps | Manual review | `Read 125-128 FINDINGS.md` | Input files exist |

### Sampling Rate
- **Per task commit:** Verify output file 129-FINDINGS.md has expected sections
- **Per wave merge:** Cross-reference output scenarios against input finding counts
- **Phase gate:** Success criteria from ROADMAP.md verified in 129-FINDINGS.md

### Wave 0 Gaps
None -- this phase requires no test infrastructure. It reads findings and produces a scenario document.

## Sources

### Primary (HIGH confidence)
- Phase 125-FINDINGS.md -- 32 actionable findings (backend core logic)
- Phase 126-FINDINGS.md -- 78 actionable findings (API layer + security)
- Phase 127-FINDINGS.md -- 95 actionable findings (frontend)
- Phase 128-FINDINGS.md -- 81 actionable findings (code quality + 5 systemic patterns)
- TESTING.md -- Current test strategy, E2E structure, coverage gaps, recommended test additions
- 129-CONTEXT.md -- Locked decisions (D-01 through D-08), scope, canonical references

### Secondary (MEDIUM confidence)
- CLAUDE.md -- Project conventions, testing commands, known pitfalls
- pyproject.toml -- Test dependency versions confirmed (pytest, pytest-asyncio, pytest-playwright)
- ROADMAP.md -- Phase 129 definition, success criteria, requirements mapping

### Tertiary (LOW confidence)
- None -- all findings are from verified project documentation

## Key Data for Planning

### Input Summary (what Plan 1 reads)

| Source | Actionable Findings | Critical | High | Medium | Low |
|--------|-------------------|----------|------|--------|-----|
| Phase 125 (backend core) | 32 | 0 | 2 | 14 | 16 |
| Phase 126 (API layer) | 78 | 0 | 2 | 27 | 49 |
| Phase 127 (frontend) | 95 | 0 | 3 | 34 | 58 |
| Phase 128 (code quality) | 81 | 0 | 14 | 38 | 29 |
| **Total** | **~286** | **0** | **~21** | **~113** | **~152** |

Note: "Actionable" excludes N/A and verified-correct entries. Total actionable ~286 out of ~390 total entries. The actual count the planner works with is the actionable subset.

### High-ROI Test Candidates (pre-identified)

**Backend Unit Tests (P0 -- High severity + pure logic):**
1. StallDetector.check() -- dual invocation bug (125-P1 agent_service.py:340-347)
2. assertion_service.check_element_exists -- stub always returns True (125-P2 assertion_service.py:88-110)
3. step_code_buffer._is_corrective_evaluate -- detection gap (125-P1 step_code_buffer.py:227-257)
4. code_generator._substitute_variables -- false match risk (125-P1 code_generator.py:241-242)
5. task_progress_tracker.update_from_evaluation -- loose keyword matching (125-P3 task_progress_tracker.py:149-152)
6. External assertion summary context mutation (125-Cross-4, 126-DD-pipe-04)
7. test_flow_service._shift_step_numbers -- boundary values (125-P2 test_flow_service.py:174-193)

**Backend Integration Tests (P0 -- Systemic patterns):**
1. CP-1: EventManager lifecycle (publish -> subscribe -> cleanup -> verify empty)
2. CP-2: SSE error handling (broken subscriber -> publish -> verify no crash)
3. CP-4: Blocking I/O in async (save_screenshot -> verify concurrent tasks not blocked)
4. Pipeline precondition failure -> missing "started" event (125-P1 run_pipeline.py:499-500, 126-DD-pipe-03)
5. Batch execution partial creation (126-DD-batch-03)
6. Stop run does not cancel agent (126-DD-runs-10)
7. Heartbeat task leak on re-subscribe (125-P2 event_manager.py:84-85)

**Frontend Component Tests (P1):**
1. useRunStream JSON.parse error handling (127-DD-USE-01)
2. useRunStream unbounded array growth (127-SSE-4)
3. TaskForm stale data on mode switch (127-DD-TF-01)
4. client.ts retry toast persistence (127-DD-CLI-03)
5. DataMethodSelector empty-to-0 conversion (127-DD-DMS-01)

**E2E Gap Scenarios (P2):**
1. Precondition failure flow (task with bad precondition -> verify error state)
2. Assertion failure flow (task with failing assertion -> verify report)
3. Batch execution monitoring (create batch -> monitor progress -> verify all runs)
4. Stop run flow (start run -> stop -> verify agent stops -- currently broken, DD-runs-10)
5. External module integration (create task with external data method -> verify execution)

### Findings NOT Worth Test Scenarios
- Unused imports (125-P1 run_pipeline.py:7,14,19,29)
- Naming issues (125-P3 action_translator.py:378 E741)
- Dead code documentation (125-P3 pre_submit_guard.py:109-114)
- print() in lifespan (126-DD-main-06)
- __init__.py incomplete exports (126-P3-init-01)
- Response format inconsistency (126-API-08)
- StructuredLogger unused (128-BD-33)
- LLMFactory bypassed (128-BD-31)

These are fix-once issues with near-zero regression risk.

## Metadata

**Confidence breakdown:**
- Methodology (filter-classify-score): HIGH -- standard approach, well-documented
- Finding counts: HIGH -- directly from verified FINDINGS files
- Testability assessment: HIGH -- derived from reading actual findings
- ROI estimates: MEDIUM -- judgment-based, may vary by implementer
- E2E gap analysis: MEDIUM -- based on existing spec files, not full coverage analysis

**Research date:** 2026-05-04
**Valid until:** 2026-06-04 (stable -- findings are historical, methodology is timeless)
