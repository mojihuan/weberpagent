# Phase 7: 动态数据支持 - Context

**Gathered:** 2026-03-17
**Status:** Ready for planning

<domain>
## Phase Boundary

支持随机数生成、动态数据获取和数据缓存。让用户可以在测试用例中生成测试数据（SF 物流单号、手机号、IMEI 等）、从 API 获取动态数据、跨步骤缓存数据供后续复用、支持时间计算（now ± N 分钟）。

**包含：** 随机数生成器移植、动态数据获取机制、数据缓存系统、时间计算工具
**不包含：** 前置条件执行（Phase 5 已实现）、接口断言（Phase 6 已实现）、UI 测试执行（已有）

</domain>

<decisions>
## Implementation Decisions

### 随机数生成器
- **移植现有 BaseRandomMixin 类** - 从现有项目移植到 aiDriveUITest
- **支持的随机数据类型：**
  - SF 物流单号生成
  - 11 位中国手机号生成
  - IMEI 设备识别码生成
  - 可扩展机制（用户可添加自定义生成器）
- **调用语法：** 函数调用方式，在前置条件中通过 `context['变量名'] = sf_waybill()` 存储
- **示例：**
  ```python
  # 在前置条件中生成随机数据
  context['order_no'] = sf_waybill()
  context['phone'] = random_phone()
  context['imei'] = random_imei()
  ```

### 动态数据获取
- **获取时机：** 仅在前置条件阶段获取动态数据
- **API 来源：** 复用现有项目的 API 封装层（api/ 目录），通过 ERP_API_MODULE_PATH 环境变量配置
- **列表数据处理：** 用户自行在代码中处理，如 `context['first_order'] = orders[0]`
- **示例：**
  ```python
  # 在前置条件中从 API 获取数据
  from api.api_purchase import PurchaseOrderListApi
  api = PurchaseOrderListApi()
  orders = api.list_orders(status='pending')
  context['order_id'] = orders[0]['id']
  ```

### 数据缓存机制
- **缓存范围：** 单次运行（Run），数据存储在内存 context 中
- **生命周期：** 仅在当前 Run 执行期间有效，不持久化到数据库
- **跨步骤传递：** 顺序传递 context（前置条件 → UI 测试 → 接口断言）
- **变量引用：** 使用 `{{变量名}}` 语法在后续步骤中引用（Jinja2）

### 时间计算工具
- **调用语法：** 函数调用方式，在前置条件中通过 `context['时间变量'] = time_now(±N)` 存储
- **输出格式：** datetime 字符串格式（如 `2026-03-17 10:30:00`）
- **支持操作：**
  - `time_now()` - 获取当前时间
  - `time_now(+N)` - 当前时间 + N 分钟
  - `time_now(-N)` - 当前时间 - N 分钟
- **示例：**
  ```python
  # 在前置条件中计算时间
  context['current_time'] = time_now()
  context['expire_time'] = time_now(+30)  # 30 分钟后
  context['start_time'] = time_now(-5)    # 5 分钟前
  ```

### Claude's Discretion
- BaseRandomMixin 类的具体实现细节
- 时间计算工具的具体函数名（如 time_now 或其他）
- 随机生成器的具体函数名（如 sf_waybill、random_phone 等）
- 可扩展机制的实现方式（如配置文件或代码注册）
- 前端是否需要展示动态数据生成日志

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 前置条件系统（Phase 5）
- `.planning/phases/05-前置条件系统/05-CONTEXT.md` - 前置条件执行机制、exec() 模式、context 存储模式
- `backend/core/precondition_service.py` - 前置条件执行服务，需要集成随机数和时间计算函数

### 接口断言系统（Phase 6）
- `.planning/phases/06-接口断言集成/06-CONTEXT.md` - 接口断言执行机制、context 传递模式
- `backend/core/api_assertion_service.py` - 接口断言服务，需要接收前置条件的 context

### 现有 API 架构
- 现有项目 `api/` 目录 - API 接口层封装
- 现有项目 `common/base_api.py` - BaseApi 基类
- `ERP_API_MODULE_PATH` 环境变量 - 外部 API 模块路径配置

### 外部依赖
- 现有项目 `BaseRandomMixin` 类 - 需要移植的随机数生成器基类

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `PreconditionService` - 前置条件执行服务，需要在 `_setup_execution_env()` 中添加随机数和时间计算函数
- `ApiAssertionService` - 接口断言服务，已经支持 context 传递
- `ERP_API_MODULE_PATH` 环境变量 - 已配置，可直接复用
- Jinja2 变量替换 - 已实现，可在 UI 测试步骤和接口断言中引用 context 变量

### Established Patterns
- Python 代码格式 + exec() 执行（来自 Phase 5）
- `context['变量名']` 存储结果（来自 Phase 5）
- Jinja2 变量替换 `{{变量名}}`（来自 Phase 5/6）
- 30 秒超时（来自 Phase 5/6）
- FastAPI + Pydantic for API layer
- SQLAlchemy async for database

### Integration Points
- 前置条件服务: `backend/core/precondition_service.py` - 集成随机数生成器和时间计算函数
- 执行环境: `_setup_execution_env()` 方法 - 添加新的辅助函数
- 执行流程: `agent_service.py` - 确保顺序传递 context（前置 → UI → 断言）

</code_context>

<specifics>
## Specific Ideas

- 随机数生成器函数名建议：`sf_waybill()`, `random_phone()`, `random_imei()`
- 时间计算函数名建议：`time_now(offset_minutes=0)` 或 `get_time(±N)`
- 可扩展机制：支持在 `ERP_API_MODULE_PATH` 中定义自定义生成器
- 前端展示：在执行监控中显示动态数据生成日志

</specifics>

<deferred>
## Deferred Ideas

None — 讨论保持在 Phase 范围内

</deferred>

---

*Phase: 07-动态数据支持*
*Context gathered: 2026-03-17*
