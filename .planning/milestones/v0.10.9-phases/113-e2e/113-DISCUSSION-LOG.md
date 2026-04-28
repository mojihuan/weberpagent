# Phase 113: E2E 验证与回归 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-28
**Phase:** 113-e2e
**Areas discussed:** 测试更新策略, E2E 验证深度, 回归范围与基准

---

## 测试更新策略

| Option | Description | Selected |
|--------|-------------|----------|
| 仅更新 docstring 注释即可 | docstring 不影响测试执行，非必须 | |
| 更新 docstring + 验证全量回归通过 | 清除残留引用 + 确认全量通过 | ✓ |
| You decide | Claude 自行决定 | |

**User's choice:** 更新 docstring + 验证全量回归通过
**Notes:** 3 个文件（test_precondition_injection.py, test_assertion_translation.py, test_code_generator.py）只是 docstring 注释过时，测试代码已在 Phase 112 更新完毕。无实际调用已删除方法。

---

## E2E 验证深度

| Option | Description | Selected |
|--------|-------------|----------|
| Mock ASGI 集成测试 | httpx ASGITransport + mock LLM/agent，项目已有此模式 | ✓ |
| Buffer 单元级验证 | 模拟 step_callback 调用 buffer，覆盖范围窄 | |
| 真实 AI 任务端到端 | 最全面但依赖 ERP + LLM API + 耗时长 | |

**User's choice:** Mock ASGI 集成测试
**Notes:** 项目已建立 httpx ASGITransport + dependency_overrides 模式，快速可靠无需外部依赖。

---

## 回归范围与基准

| Option | Description | Selected |
|--------|-------------|----------|
| 仅 backend pytest | 全量通过即可，Pydantic warning 不处理 | |
| backend + 修复 Pydantic warning | 转为 ConfigDict 风格 | ✓ |

**User's choice:** backend + 修复 Pydantic warning
**Notes:** BatchResponse 在 backend/db/schemas.py line ~317 使用 class-based Config，需转为 model_config = ConfigDict(...) 风格。

---

## Claude's Discretion

- Mock ASGI 集成测试的具体测试结构和用例组织
- 集成测试中 mock 的粒度
- Pydantic 修复是否需要检查其他 schemas

## Deferred Ideas

None — discussion stayed within phase scope
