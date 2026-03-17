# Phase 5: 前置条件系统 - Context

**Gathered:** 2026-03-16
**Status:** Ready for planning

<domain>
## Phase Boundary

支持 API 方式执行前置条件，快速造数据。用户可以在测试用例中定义前置条件步骤，通过 API 调用执行（不启动浏览器），支持复用现有项目的 API 封装方法，结果可传递给后续测试步骤。

**包含：** 前置条件语法设计、API 调用框架集成、现有项目方法复用、结果传递机制
**不包含：** UI 测试执行（已有）、接口断言（Phase 6）、动态数据生成（Phase 7）

</domain>

<decisions>
## Implementation Decisions

### 语法识别方式
- **分离的输入字段** - 前端提供独立的「前置条件」输入区域，与「测试步骤」分开
- 用户无需特殊标记，系统自动识别前置条件区域

### 前置条件语法格式
- **Python 代码格式** - 用户直接写 Python 代码调用 API
- 通过 `context['变量名']` 存储结果供后续引用
- 示例：
  ```python
  from api.api_purchase import PurchaseOrderListApi
  api = PurchaseOrderListApi()
  order = api.create_order()
  context['order_id'] = order['id']
  ```

### API 模块集成
- **Python 模块导入** - 复用现有三层架构（request/ → api/ → common/base_api.py）
- **环境变量配置** - 通过 `.env` 或 `settings.py` 配置现有项目路径
- 现有 BaseApi 类能力：request_handle, get_response_data, get_token, headers 等

### 数据传递机制
- **变量替换** - 结果存入 `{{变量名}}` 格式
- UI 测试步骤中用 `{{order_id}}` 引用前置条件结果
- **用户显式命名** - 变量名由用户在代码中指定，如 `context['order_id']`

### 结果存储
- **内存上下文** - 仅存储到内存，本次执行过程中可引用
- 不持久化到数据库，每次执行重新生成

### 多步骤前置条件
- **独立输入项** - 每个前置条件是独立的输入框，可添加/删除
- 按顺序依次执行

### 执行展示
- **合并到步骤列表** - 与 UI 步骤一起展示，有「前置条件」标签区分
- 用户可在执行监控中看到前置条件执行进度

### 失败处理
- **立即终止** - 前置条件失败则整个测试终止，标记为失败
- 不重试，直接报告错误

### 代码执行
- **直接执行** - 使用 exec() 执行用户代码，依赖环境隔离和用户信任
- **30 秒超时** - 单个前置条件默认 30 秒超时

### 前端位置
- **任务编辑页新增字段** - 在任务编辑页增加「前置条件」输入区域

### Claude's Discretion
- 具体数据库模型设计（Precondition 表是否需要）
- 前端组件布局细节
- 执行错误消息格式
- 代码编辑器样式（是否用 Monaco Editor）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 现有 API 架构
- 现有项目 `api/` 目录 - API 接口层封装
- 现有项目 `common/base_api.py` - BaseApi 基类
- 现有项目 `common/base_url.py` - URL 管理和环境配置
- 现有项目 `request/` 目录 - 请求参数构建层

### 现有代码参考
- `backend/core/agent_service.py` - Agent 执行服务，可参考执行模式
- `backend/db/models.py` - 数据模型，可能需要扩展
- `frontend/src/pages/TaskEdit.tsx` - 任务编辑页，需要添加前置条件字段

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `AgentService` - 可参考 run_with_streaming 的回调模式
- `Task/Run/Step` 模型 - 可能需要新增 Precondition 模型或扩展 Step 类型
- `create_llm()` - LLM 创建工厂，前置条件不需要 LLM
- `EventManager` - SSE 事件推送，可用于前置条件执行进度

### Established Patterns
- FastAPI + Pydantic for API layer
- SQLAlchemy async for database
- SSE for real-time updates
- React + TypeScript + Tailwind for frontend

### Integration Points
- 任务编辑页: `frontend/src/pages/TaskEdit.tsx` - 添加前置条件输入
- 任务 API: `backend/api/routes/tasks.py` - 保存前置条件数据
- 执行服务: `backend/core/agent_service.py` - 集成前置条件执行
- SSE 事件: `backend/core/event_manager.py` - 推送前置条件执行进度

</code_context>

<specifics>
## Specific Ideas

- 前置条件输入区域支持代码高亮（Monaco Editor 或简单 textarea）
- 前置条件执行结果在步骤列表显示为「前置条件」类型
- 变量替换语法：`{{变量名}}` 与 Jinja2 一致
- 环境变量名：`ERP_API_MODULE_PATH` 指定现有项目路径

</specifics>

<deferred>
## Deferred Ideas

None — 讨论保持在 Phase 范围内

</deferred>

---

*Phase: 05-前置条件系统*
*Context gathered: 2026-03-16*
