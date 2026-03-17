# Phase 6: 接口断言集成 - Context

**Gathered:** 2026-03-16
**Status:** Ready for planning

<domain>
## Phase Boundary

支持通过 API 调用验证测试结果。用户可以在测试用例中定义 API 断言，进行时间断言（±1 分钟范围）和数据断言（精确/包含匹配），断言结果展示在测试报告中。

**包含：** 断言语法设计、BaseAssert 类移植、时间断言实现、断言结果报告集成
**不包含：** 前置条件系统（Phase 5）、动态数据生成（Phase 7）、UI 测试执行（已有）

</domain>

<decisions>
## Implementation Decisions

### 集成方式
- **移植现有 BaseAssert 类** - 将现有项目的 BaseAssert 类移植到 aiDriveUITest
- 复用现有的多层封装设计（查询层 → 数据层 → 断言层 → 报告层）

### 断言语法格式
- **Python 代码格式** - 与前置条件一致，用户直接写 Python 代码
- 通过 `context['变量名']` 存储结果，支持 Jinja2 变量替换
- 示例：
  ```python
  from api.api_purchase import PurchaseOrderListApi
  api = PurchaseOrderListApi()
  result = api.get_order({{order_id}})
  assert result['status'] == 'success'
  ```

### 前端位置
- **独立输入区域** - 在任务编辑页增加「接口断言」输入区域
- 与「前置条件」、「测试步骤」分开显示

### 执行时机
- **UI 测试完成后执行**
- 执行顺序：前置条件 → UI 测试 → 接口断言 → 生成报告

### 上下文复用
- **可以引用前置条件变量** - 接口断言代码可以引用前置条件中存储的变量
- 使用 `{{order_id}}` 语法引用，与 Jinja2 一致

### 断言类型支持
- **精确匹配** - `status == 'success'`
- **包含匹配** - `name contains '测试'`
- **时间断言** - 时间字段在当前时间 ±1 分钟范围内
- **小数近似** - `1.23 ≈ 1.24`（误差范围内）

### 多字段断言处理
- **合并为一条记录** - 所有字段断言结果合并为一条记录
- 显示各字段通过/失败状态

### 时间断言范围
- **固定 ±1 分钟** - 简单直接，不提供配置选项
- 与 API 返回的时间字段比较

### 错误信息展示
- **简洁模式** - 只显示不匹配的字段和预期/实际值对比
- 方便维护和定位问题

### 报告展示
- **独立区域显示** - 在测试报告中新增「接口断言」区域
- 与 UI 断言分开显示，便于区分

### BaseAssert 类设计（多层封装）
- **第一层**：查询列表 API 获取数据
- **第二层**：数据封装（中间文件）
- **第三层**：断言判断逻辑（时间、模糊匹配、精确匹配、小数等）
- **预定义字段名**：左边实际结果，右边预期结果
- **最后一层**：处理多个字段断言匹配，打印结果

### Claude's Discretion
- 具体的 BaseAssert 类移植实现细节
- 前端接口断言输入组件样式（是否用 Monaco Editor）
- 小数近似的默认误差范围（如 0.01 或 0.001）
- 断言执行错误处理逻辑

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 现有断言系统
- `backend/core/assertion_service.py` - 现有 UI 断言服务，可参考断言执行模式
- `backend/db/models.py` - Assertion/AssertionResult 模型，需要扩展支持新断言类型
- `backend/core/report_service.py` - 报告服务，需要集成接口断言结果

### 前置条件系统（Phase 5）
- Phase 5 CONTEXT.md - 前置条件执行机制、变量替换、exec() 模式
- `ERP_API_MODULE_PATH` 环境变量配置

### 现有代码参考
- `frontend/src/pages/TaskEdit.tsx` - 任务编辑页，需要添加接口断言输入区域
- `backend/api/routes/tasks.py` - 任务 API，需要保存接口断言数据

### 外部依赖
- 现有项目 `BaseAssert` 类 - 需要移植的断言封装类

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `AssertionService` - 可扩展支持新的断言类型（api_call, time_check, data_match）
- `AssertionResult` 模型 - 已有 status, message, actual_value 字段，可直接使用
- `ReportService` - 可扩展汇总接口断言结果
- Phase 5 的 `exec()` 执行机制 - 可复用于接口断言代码执行
- Phase 5 的 Jinja2 变量替换 - 可复用于 `{{变量名}}` 替换

### Established Patterns
- Python 代码格式 + exec() 执行（来自 Phase 5）
- Jinja2 变量替换（来自 Phase 5）
- FastAPI + Pydantic for API layer
- SQLAlchemy async for database
- SSE for real-time updates
- React + TypeScript + Tailwind for frontend

### Integration Points
- 任务编辑页: `frontend/src/pages/TaskEdit.tsx` - 添加接口断言输入区域
- 任务模型: `backend/db/models.py` - 可能需要新增 api_assertions 字段
- 断言服务: `backend/core/assertion_service.py` - 扩展支持接口断言类型
- 执行服务: `backend/core/agent_service.py` - 集成接口断言执行（UI 测试后）
- 报告服务: `backend/core/report_service.py` - 汇总接口断言结果

</code_context>

<specifics>
## Specific Ideas

- 接口断言输入区域支持代码高亮（与前置条件一致）
- 断言失败时显示：字段名 | 预期值 | 实际值 | 状态
- 时间断言语法：`assert_time(response['create_time'])` 自动比较当前时间 ±1 分钟
- 小数近似语法：`assert_decimal(response['amount'], 100.00, tolerance=0.01)`

</specifics>

<deferred>
## Deferred Ideas

None — 讨论保持在 Phase 范围内

</deferred>

---

*Phase: 06-接口断言集成*
*Context gathered: 2026-03-16*
