# Phase 16: 端到端验证 - Context

**Gathered:** 2026-03-18
**Status:** Ready for planning

<domain>
## Phase Boundary

验证完整的前置条件集成流程：用户在前端选择操作码 → 系统生成代码并执行前置条件 → 结果正确展示。同时验证各种错误场景的处理。

**In scope:**
- 使用真实 webseleniumerp 项目的后端集成测试
- 错误场景覆盖（路径未配置、路径不存在、模块导入失败、执行异常）
- 手动测试清单用于真实环境验证

**Out of scope:**
- 前端 E2E 测试（Playwright）
- Mock 模块测试
- 修改 webseleniumerp 项目代码

</domain>

<decisions>
## Implementation Decisions

### 测试范围和方式
- **使用真实项目**: 使用真实 webseleniumerp 项目进行测试，验证实际集成效果
- **后端集成测试**: 测试后端 API 端点、桥接模块、执行逻辑，无需浏览器依赖
- **完整流程测试**: 测试完整流程（选择操作码 → 生成代码 → 执行前置条件 → 结果传递），覆盖 VAL-01

### 错误场景覆盖
需覆盖以下四种错误场景：
1. **路径未配置**: WEBSERP_PATH 未配置或为空，前端显示提示信息
2. **路径不存在**: WEBSERP_PATH 指向不存在的目录或非目录文件
3. **模块导入失败**: common.base_prerequisites 导入失败，返回 HTTP 503
4. **执行异常**: PreFront.operations() 执行时抛出异常

### 验证结果记录
- **后端测试**: 使用 pytest 编写集成测试，通过/失败即验证结果
- **手动测试清单**: 创建手动测试清单文档，记录测试步骤和预期结果，用于真实环境验证

### Claude's Discretion
- 测试文件命名和位置
- 具体测试用例的断言细节
- 手动测试清单的格式

</decisions>

<specifics>
## Specific Ideas

- 测试应验证 Phase 13-15 构建的功能真正可用
- 错误场景需要清晰的用户提示，方便排查问题

</specifics>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 前置条件系统
- `backend/core/precondition_service.py` — 前置条件执行服务
- `backend/core/external_precondition_bridge.py` — 外部模块桥接
- `backend/tests/integration/test_precondition_flow.py` — 现有前置条件流程测试

### API 端点
- `backend/api/routes/external_operations.py` — 外部操作 API 端点

### 配置
- `backend/config.py` — WEBSERP_PATH 配置定义

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `external_precondition_bridge.py`: 提供操作码解析、代码生成、执行功能
- `test_precondition_flow.py`: 现有测试模式可参考（使用 tmp_path mock）
- `conftest.py`: 测试配置和 fixtures

### Established Patterns
- 后端测试使用 pytest + pytest-asyncio
- 测试文件放在 `backend/tests/integration/` 或 `backend/tests/api/`
- 使用 tmp_path fixture 创建临时测试环境

### Integration Points
- `/api/external-operations` API 端点
- `PreconditionService` 执行前置条件代码
- 前端 `OperationCodeSelector` 组件调用 API

</code_context>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 16-端到端验证*
*Context gathered: 2026-03-18*
