# Phase 121: 死代码清理 - Context

**Gathered:** 2026-04-29
**Status:** Ready for planning

<domain>
## Phase Boundary

删除 backend/ 和 frontend/src/ 中所有未使用的 import、函数、变量、废弃模块文件。顺手修复 2 个 undefined name（ChatOpenAI、ContextWrapper）。

覆盖 REQUIREMENTS: DEAD-01, DEAD-02, DEAD-03, DEAD-04。

不涉及：webseleniumerp/ 目录、新增功能、命名规范化（Phase 123）、重复逻辑合并（Phase 122）。

</domain>

<decisions>
## Implementation Decisions

### 验证策略
- **D-01:** 删除后验证 FastAPI 正常启动 + 关键 API 端点冒烟测试（GET /tasks、GET /runs 等）。比 Phase 120 更严格，确保无运行时 500 错误。

### Undefined Name 修复
- **D-02:** 顺手修复 2 个 undefined name（非死代码，是潜在 bug）：
  - `backend/llm/factory.py:163` — `ChatOpenAI` 在 except 块中使用但仅在 try 块中 import
  - `backend/core/external_precondition_bridge.py:1275` — `ContextWrapper` 使用但从未 import
  这些不是死代码但清理过程中自然会遇到，顺手修比另开 phase 高效。

### 废弃模块删除
- **D-03:** 删除以下完全无引用的模块文件：
  - `backend/agent/browser_agent.py` — legacy UIBrowserAgent（已被 MonitoredAgent 替代）
  - `backend/agent/proxy_agent.py` — legacy ProxyBrowserAgent（同上）
  - `backend/storage/run_store.py` — 无任何文件引用
  - `backend/storage/task_store.py` — 无任何文件引用
  - `backend/storage/__init__.py` — 目录内唯一剩余文件
  - **整个 `backend/storage/` 目录删除**（只有上述 3 个文件，全部无引用）

### 清理范围
- **D-04:** 范围限定为 `backend/` + `frontend/src/`。**不包括** `webseleniumerp/`（外部项目）。

### Claude's Discretion
- 未使用 import 的具体删除顺序和批次划分
- 前端 TypeScript 未使用 export 的检测方式（ts-prune / ESLint / 手动）
- API 冒烟测试选择哪些端点
- 是否分 2 个 plan（backend 先行 + frontend 后行）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 死代码检测基准
- pyflakes 扫描结果 — 以下文件的 ~35+ 个警告（未使用 import、未使用变量、重复 import 等）：
  - `backend/llm/factory.py` — LLMConfig 未使用 import + ChatOpenAI undefined name
  - `backend/llm/base.py` — typing.Any 未使用
  - `backend/core/agent_service.py` — f-string missing placeholders
  - `backend/core/step_code_buffer.py` — pathlib.Path 未使用
  - `backend/core/precondition_service.py` — UndefinedError 未使用 + loop 变量未使用
  - `backend/core/external_precondition_bridge.py` — ContextWrapper undefined name
  - `backend/core/code_generator.py` — 4 处 f-string missing placeholders
  - `backend/config/validators.py` — importlib.util 未使用
  - `backend/utils/screenshot.py` — datetime 未使用
  - `backend/agent/proxy_agent.py` — typing.Any 未使用
  - `backend/agent/browser_agent.py` — typing.Any 未使用
  - `backend/agent/dom_patch.py` — 2 处 global 变量未赋值
  - `backend/storage/task_store.py` — Task 重复 import + 未使用
  - `backend/storage/run_store.py` — Run/Step/RunResult 重复 import + 未使用
  - `backend/api/main.py` — backend.db.models 未使用
  - `backend/api/routes/external_assertions.py` — Optional 未使用
  - `backend/api/routes/runs.py` — ReportRepository + TokenFetchError 未使用
  - `backend/api/routes/external_data_methods.py` — typing.Any 未使用

### 废弃模块文件（待删除）
- `backend/agent/browser_agent.py` — legacy UIBrowserAgent，0 引用
- `backend/agent/proxy_agent.py` — legacy ProxyBrowserAgent，0 引用
- `backend/storage/run_store.py` — 0 引用
- `backend/storage/task_store.py` — 0 引用
- `backend/storage/__init__.py` — 目录删除时一并移除
- `backend/agent/__init__.py` — 包含已注释的 UIBrowserAgent 导出，需更新

### 不可破坏的运行时依赖（Phase 120 已确认）
- `backend/api/routes/runs.py` — 代码执行功能依赖 pytest，不可破坏
- `backend/core/auth_service.py` — 依赖 httpx，不可破坏
- `backend/core/code_generator.py` — 生成 pytest 格式代码，不可破坏

### 前端参考
- `frontend/src/types/index.ts` — 54 个 export，部分可能未使用
- 所有 frontend 组件目录均有引用（BatchProgress、Dashboard、ImportModal、Report、RunMonitor、shared、TaskDetail、TaskList、TaskModal）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- pyflakes — 已安装，可直接用于 Python 死代码检测
- 前端可用 ts-prune 或 ESLint no-unused-vars 检测 TypeScript 死代码

### Established Patterns
- Phase 120 的 delete-first 策略 — 先删文件，再清理引用
- Phase 120 的回归验证模式 — FastAPI 启动检查
- `backend/agent/__init__.py` 已有注释说明 UIBrowserAgent 被注释原因

### Integration Points
- `backend/api/main.py` — FastAPI app entry，删除未使用 import 时注意保留所有 router 注册
- `backend/agent/__init__.py` — 删除 browser_agent/proxy_agent 后需更新此文件
- `backend/api/routes/runs.py` — 最复杂的路由文件，删除 import 时需格外小心
- `frontend/src/App.tsx` — 前端入口，所有页面路由注册

### 关键风险点
- **重复 import 删除顺序** — storage/*.py 有 import-then-redefine 模式，需先确认 redefine 后的用法
- **f-string missing placeholders** — 可能是 bug 而非死代码，需要逐一检查是刻意为之还是遗漏
- **dom_patch.py global 变量** — `global` 声明但未赋值，可能是条件性赋值，需仔细确认

</code_context>

<specifics>
## Specific Ideas

- 成功标准：
  1. `pyflakes backend/` 零警告（所有 Python 文件）
  2. 不存在未被调用的函数或方法
  3. 不存在未引用的模块级变量或常量
  4. browser_agent.py、proxy_agent.py、storage/ 目录完全删除
  5. ChatOpenAI 和 ContextWrapper undefined name 已修复
  6. FastAPI 应用正常启动
  7. 关键 API 端点冒烟测试通过（GET /tasks、GET /runs 等）
  8. 前端 TypeScript 未使用 export 已清理

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---
*Phase: 121-dead-code-cleanup*
*Context gathered: 2026-04-29*
