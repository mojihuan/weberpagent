# Phase 3: Service Layer Restoration - Context

**Gathered:** 2026-03-14
**Status:** Ready for planning

<domain>
## Phase Boundary

恢复服务层核心功能 — 断言评估服务、报告生成服务、SSE 心跳机制、LLM 重试机制。确保 AI 执行流程的完整性和可靠性。

**包含：** AssertionService 适配 ORM、ReportService 新建、SSE heartbeat、LLM retry
**不包含：** 前端显示（Phase 4）、新断言类型扩展（仅添加 element_exists）

</domain>

<decisions>
## Implementation Decisions

### 断言结果存储流程

- **返回类型**：AssertionService 返回 `AssertionResult` ORM 对象（非 dict）
- **存储位置**：服务内存储 — AssertionService 接收 run_id，内部调用 AssertionResultRepository
- **失败详情**：message 字段记录详细失败原因，如 "URL 不包含 'dashboard'，实际为 'login'"
- **断言类型**：
  - `url_contains`（已有）— 检查 URL 是否包含期望字符串
  - `text_exists`（已有）— 检查页面是否包含期望文本
  - `no_errors`（已有）— 检查执行是否无错误
  - `element_exists`（新增）— 检查页面元素是否存在（CSS 选择器）
- **执行策略**：所有断言独立执行，无依赖关系，执行完成后统一检查
- **断言层级**：Task 级别（Phase 2 已确定）

### 报告生成服务设计

- **服务结构**：新建 `ReportService` 类，与 AssertionService/AgentService 平级
- **生成时机**：任务执行完成后自动生成，用户无需手动操作
- **报告内容**：
  - 基础统计（通过/失败状态、步骤数、耗时）
  - 步骤详情（每个步骤的信息和截图链接）
  - 断言结果（每个断言的结果和失败原因）
  - 错误信息（执行过程中的错误和堆栈）
- **断言展示**：显示通过率百分比
- **报告特性**：不可变，不支持重新生成

### SSE 心跳实现

- **心跳间隔**：20 秒
- **事件格式**：SSE 注释格式（`:heartbeat`），浏览器 EventSource 自动忽略
- **超时检测**：只发送心跳，不检测客户端超时断开（依赖 TCP 层）

### LLM 重试机制

- **重试策略**：指数退避（1s → 2s → 4s）
- **最大重试次数**：3 次
- **可重试错误**：
  - 网络超时
  - 速率限制（429/503）
  - 响应格式错误
- **不可重试错误**：
  - 认证失败
  - 配额不足
  - API Key 无效
- **实现位置**：LLM Factory 层（`backend/llm/factory.py` 的 `create_llm()` 函数）
- **日志记录**：详细日志（每次重试记录错误类型、等待时间、重试次数）

### Claude's Discretion

- AssertionService 具体方法签名设计
- ReportService 内部方法组织
- SSE 心跳在 EventManager 中的具体实现方式
- LLM 重试装饰器/包装函数的具体实现

</decisions>

<specifics>
## Specific Ideas

- 断言失败消息参考：`"URL 不包含 'dashboard'，实际为 'login'"`
- 报告通过率显示格式：`"通过率: 75% (3/4)"`
- 心跳格式：`:heartbeat` 单行注释
- 重试日志格式：`"LLM 调用失败，1/3 次重试，等待 1s，错误: TimeoutError"`

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/core/assertion_service.py`：现有断言服务逻辑，返回 dict 需要适配
- `backend/core/agent_service.py`：Agent 服务封装，已使用 create_llm()
- `backend/core/event_manager.py`：SSE 事件管理器，需要添加心跳功能
- `backend/llm/factory.py`：LLM 工厂，create_llm() 函数需要添加重试逻辑
- `backend/db/repository.py`：ReportRepository 已存在，可复用
- `backend/api/routes/reports.py`：报告路由，部分逻辑可提取到 ReportService

### Established Patterns
- Repository pattern for data access
- Service layer pattern (AssertionService, AgentService)
- FastAPI BackgroundTasks for async tasks
- SSE for real-time communication
- try/finally for cleanup logging

### Integration Points
- 新服务添加到 `backend/core/` 目录
- AssertionService 需要导入 AssertionResult 模型（Phase 2 创建）
- ReportService 需要调用 RunRepository、StepRepository、AssertionResultRepository
- EventManager 需要添加心跳定时任务
- create_llm() 需要包装重试逻辑

### 已实现功能（无需修改）
- ✓ 截图文件存储（`backend/data/screenshots/`）
- ✓ 断言验证逻辑（`check_url_contains`, `check_text_exists`, `check_no_errors`）
- ✓ 报告数据模型（`Report` ORM）
- ✓ LLM temperature=0 配置

</code_context>

<deferred>
## Deferred Ideas

None — 讨论保持在 Phase 范围内

</deferred>

---

*Phase: 03-service-layer-restoration*
*Context gathered: 2026-03-14*
