# Phase 9: 登录用例调通 - Context

**Gathered:** 2026-03-17
**Status:** Ready for planning

<domain>
## Phase Boundary

验证登录测试用例的端到端执行流程：从前端创建任务 → AI 执行 → 报告展示。

这是一个 **调通/验证阶段**，不开发新功能。v0.1-v0.2 已实现所有基础设施，本阶段验证它们能否协同工作完成一个简单的登录测试。

</domain>

<decisions>
## Implementation Decisions

### 测试用例格式
- 使用 **自然语言单段描述**，不拆分多个步骤字段
- 描述内容：打开页面、输入用户名、输入密码、点击登录
- 用户名和密码 **硬编码在描述中**（内部测试系统，无需环境变量）
- 示例描述格式：
  ```
  打开 https://erptest.epbox.cn/
  找到用户名输入框，输入 Y59800075
  找到密码输入框，输入 Aa123456
  点击登录按钮
  ```

### 执行环境
- ERP 环境配置 **已就绪** (ERP_BASE_URL, ERP_USERNAME, ERP_PASSWORD)
- 使用现有的 AgentService (Browser-Use + Qwen 3.5 Plus)
- max_steps 使用默认值 (20 步足够)

### 登录成功验证
- 验证方式：**URL 变化** — 登录成功后 URL 不再包含 `/login`
- 这是 AI 自动判断，无需额外配置断言
- Claude's Discretion：如果需要更精确的验证，可检查特定页面元素

### 重试机制
- 每次执行创建 **新的 Run**
- 保留所有调通尝试的记录，便于分析问题
- 不复用同一 Run ID

### 成功标准 (UAT)
登录用例调通成功需要同时满足：
1. ✅ **所有步骤成功** — 每个步骤显示成功状态
2. ✅ **截图正确保存** — 报告页面正确展示每个步骤的截图
3. ✅ **结果正确展示** — 报告页面正确展示每个步骤的执行结果
4. ✅ **登录验证通过** — AI 判断登录成功（URL 不再是登录页）

### 失败处理
- **记录问题并继续** — 每次失败记录详细日志
- 分析后修复并重试（创建新 Run）
- 发现的 Bug 记录下来，留给 Phase 11 修复

### Claude's Discretion
- 具体的 max_steps 值（使用默认 20 即可）
- 超时时间（使用系统默认）
- 如果 AI 执行不稳定，可调整描述的详细程度

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 执行引擎
- `backend/core/agent_service.py` — AgentService，Browser-Use 封装
- `backend/api/routes/runs.py` — 执行路由，SSE 事件推送

### 前端组件
- `frontend/src/components/TaskModal/TaskForm.tsx` — 任务创建表单
- `frontend/src/pages/RunMonitor.tsx` — 实时监控页面
- `frontend/src/pages/ReportDetail.tsx` — 报告详情页面

### 测试参考
- `backend/tests/test_login.py` — 现有登录测试用例参考

### 环境配置
- `.env.example` — 环境变量模板
- `backend/config/__init__.py` — 配置加载

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **TaskForm.tsx** — 任务创建表单，支持 name, description, target_url, max_steps
- **AgentService** — Browser-Use + Qwen 执行引擎，已验证可用
- **ReportService** — 报告生成，支持截图和断言结果展示
- **SSE 监控** — 实时推送执行进度

### Established Patterns
- 任务描述使用自然语言，AI 自动理解和执行
- 截图保存在 `backend/data/screenshots/`
- 报告通过 `/reports/{run_id}` 查看

### Integration Points
- 前端创建任务 → `/api/tasks` POST
- 执行任务 → `/api/runs/start` POST
- 查看报告 → `/reports/{run_id}` GET

</code_context>

<specifics>
## Specific Ideas

- 登录用例是验证整个系统最简单的场景，4 步骤，无前置条件，无 API 断言
- 如果登录用例调通失败，说明基础设施有问题，需要优先修复
- 调通后可作为其他用例的模板

</specifics>

<deferred>
## Deferred Ideas

- **Bug 修复** — 调通过程中发现的 Bug 留给 Phase 11 修复
- **销售出库用例** — 更复杂的用例（前置条件、动态数据、API 断言）在 Phase 10
- **文档指南** — Phase 12 提供 QA 填写指南

</deferred>

---

*Phase: 09-登录用例调通*
*Context gathered: 2026-03-17*
