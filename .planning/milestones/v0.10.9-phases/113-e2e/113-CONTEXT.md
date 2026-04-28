# Phase 113: E2E 验证与回归 - Context

**Gathered:** 2026-04-28
**Status:** Ready for planning

<domain>
## Phase Boundary

全量回归测试通过 + code_generator 现有测试 docstring 更新 + 逐步代码生成端到端 Mock 集成验证 + Pydantic deprecation warning 修复。

覆盖 REQUIREMENTS: VAL-03。

不涉及：前端改动、新功能开发、真实 AI 任务执行。

</domain>

<decisions>
## Implementation Decisions

### 测试更新
- **D-01:** 更新 3 个测试文件的 docstring 注释，清除 `generate_and_save` / `_heal_weak_steps` 残留引用。测试代码本身已正确（Phase 112 已更新），仅注释过时
- **D-02:** 全量 `pytest backend/tests/` 回归通过（0 failed, 0 errors）

### E2E 集成验证
- **D-03:** 使用 httpx ASGITransport + mock LLM/agent 进程内集成测试，验证 buffer 在 runs.py 上下文中的完整流程（step_callback → buffer.append_step_async → buffer.assemble → 生成代码文件）
- **D-04:** 验证生成代码包含非空操作步骤，语法验证通过（ast.parse）

### Pydantic Warning 修复
- **D-05:** 修复 `backend/db/schemas.py` 中 `BatchResponse` 的 Pydantic deprecation warning，将 class-based `Config` 转为 `model_config = ConfigDict(...)` 风格

### Claude's Discretion
- Mock ASGI 集成测试的具体测试结构和用例组织
- 集成测试中 mock 的粒度（agent vs LLM vs 两者都 mock）
- Pydantic 修复是否需要检查其他 schemas 是否也有相同问题

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 核心源码（验证与修改目标）
- `backend/core/step_code_buffer.py` — StepCodeBuffer，集成测试的核心验证对象
- `backend/api/routes/runs.py` line 370-418 — on_step 回调和 buffer 调用点
- `backend/api/routes/runs.py` line 590-619 — 代码生成块（assemble + write 流程）
- `backend/core/code_generator.py` — generate() 方法，assemble 委托目标
- `backend/db/schemas.py` line ~317 — BatchResponse Pydantic class-based Config（修复目标）

### 测试参考
- `backend/tests/unit/test_step_code_buffer.py` — 现有 buffer 单元测试（701 行）
- `backend/tests/unit/test_code_generator.py` — docstring 需更新（266 行）
- `backend/tests/unit/test_precondition_injection.py` — docstring 需更新
- `backend/tests/unit/test_assertion_translation.py` — docstring 需更新

### 前置阶段
- `.planning/phases/111-stepcodebuffer/111-CONTEXT.md` — StepCodeBuffer 接口定义
- `.planning/phases/112-集成接入/112-CONTEXT.md` — 集成决策和 runs.py 接入方式

### 集成测试模式参考
- `backend/tests/integration/test_e2e_precondition_integration.py` — 现有 httpx ASGITransport E2E 测试模式
- `backend/tests/integration/test_api_responses.py` — API 集成测试模式

### 代码规范
- `.planning/codebase/TESTING.md` — 测试模式和 fixture 约定
- `.planning/codebase/CONVENTIONS.md` — frozen dataclass、不可变模式约定

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `httpx.AsyncClient` + `ASGITransport` — 项目已建立的进程内 E2E 测试模式，无需真实服务器
- `FastAPI dependency_overrides` — 替代 patch() 的依赖注入测试模式
- `StepCodeBuffer` — Phase 111 实现，接口完整（append_step / append_step_async / assemble）
- 现有 320 个测试用例 — 回归基线

### Established Patterns
- Mock LLM/agent 在 class level patch（`backend.core.self_healing_runner.LLMHealer`）
- frozen dataclass 不可变数据对象
- `ast.parse()` 语法验证是已有模式
- DOM 快照存于 `outputs/{run_id}/dom/step_{n}.txt`（1-indexed）
- 测试用 `tmp_path` fixture 隔离输出目录

### Integration Points
- `runs.py on_step` — 集成测试验证 buffer 在 step_callback 上下文中正确累积
- `runs.py 代码生成块` — 集成测试验证 buffer.assemble() + write 输出正确代码文件
- `agent_service.step_callback` — 集成测试需要 mock 此层

### 当前测试状态
- 320 tests collected
- 3 个文件 docstring 残留 `generate_and_save` 引用（不影响执行，需清理）
- Pydantic deprecation warning: `BatchResponse` 使用 class-based Config

</code_context>

<specifics>
## Specific Ideas

- SUCCESS CRITERIA 来自 ROADMAP.md：
  1. 全量 pytest 回归测试通过（0 failed, 0 errors）
  2. code_generator 现有测试全部更新 — docstring 注释清除 generate_and_save/_heal_weak_steps 残留
  3. AI 执行任务后生成的 Playwright 代码文件包含正确的逐步翻译结果（非空操作），语法验证通过 — 通过 Mock ASGI 集成测试验证

- 集成测试应模拟完整 runs.py 流程：创建任务 → mock agent 执行 → on_step 回调触发 buffer 累积 → 生成代码文件 → 验证输出
- Pydantic warning 修复：将 `class Config: ...` 转为 `model_config = ConfigDict(...)` 风格

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---
*Phase: 113-e2e*
*Context gathered: 2026-04-28*
