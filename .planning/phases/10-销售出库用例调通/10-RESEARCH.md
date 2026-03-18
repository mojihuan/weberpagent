# Phase 10: 销售出库用例调通 - Research

**Researched:** 2026-03-17
**Domain:** 销售出库测试用例端到端执行（前置条件 + 动态数据 + API 断言）
**Confidence:** HIGH

## Summary

Phase 10 验证 v0.2 实现的完整功能链：前置条件系统、动态数据支持、API 断言集成。这是比 Phase 9 登录用例更复杂的场景，需要验证这些新功能能否协同工作完成一个销售出库测试流程。

**Primary recommendation:** 使用已验证的 Phase 9 登录用例模式作为模板，扩展为销售出库场景。关键验证点是前置条件执行、Jinja2 变量替换、API 断言结果的正确传递和展示。

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### 前置条件配置
- 使用 **现有 context['变量名']** 语法，不实现 self.pre 新语法
- 代码示例：`context['operations'] = get_operations(['FA1', 'HC1'])`
- ERP API 通过外部模块调用 (ERP_API_MODULE_PATH 已配置)

#### 动态数据引用
- 步骤描述中使用 **Jinja2 {{变量名}}** 语法
- 示例：`输入销售单号 {{order_no}}`
- 随机数使用全局函数：`sf_waybill()`、`random_phone()`、`random_imei()` 等

#### 数据传递
- **自动传递**：context 在 PreconditionService 和 ApiAssertionService 之间共享
- 无需显式调用传递方法

#### 用例规模
- **简版 5-8 步**：创建销售单 -> 审核 -> 出库 -> 验证
- 核心流程验证，不追求完整业务流程覆盖

#### API 断言范围
- **完整验证**：
  - 销售单号存在
  - 状态正确
  - 创建时间合理
  - 库存扣减正确
- 使用 ApiAssertionService 现有能力（时间断言、精确匹配、包含匹配）

#### 失败处理
- **Fail-fast**：任一前置条件失败，立即终止整个测试（现有行为）
- 每次执行创建新 Run，保留调通记录
- 发现的 Bug 记录，留给 Phase 11 修复

### Claude's Discretion

- 具体的销售出库步骤描述
- API 断言的具体字段名和期望值
- 截图验证点选择

### Deferred Ideas (OUT OF SCOPE)

- **self.pre 新语法** — 如需要更友好的 API，可在后续版本实现
- **完整业务流程** — 10-15 步骤的完整销售流程，可在后续扩展
- **Bug 修复** — 调通过程中发现的 Bug 留给 Phase 11 修复
- **文档指南** — Phase 12 提供 QA 填写指南

</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| SALE-01 | 用户可以在前端配置前置条件 `self.pre.operations(data=['FA1', 'HC1'])` | 使用 `context['变量名']` 语法，PreconditionService 已支持，前端 TaskForm.tsx 支持多行文本输入 |
| SALE-02 | 用户可以在步骤中使用动态数据方法 `self.copy()` 和 `self.affix()` | 使用 Jinja2 `{{变量名}}` 语法，substitute_variables() 已实现 |
| SALE-03 | 用户可以在步骤中使用随机数方法 `self.sf` | 随机数函数已注入前置条件执行环境：sf_waybill(), random_phone() 等 |
| SALE-04 | 用户可以配置 API 断言验证销售单号、状态、时间 | ApiAssertionService 支持 assert_time, assert_exact, assert_contains |
| SALE-05 | 销售出库用例可以端到端执行成功 | 参考 Phase 9 登录用例成功模式，需验证完整流程 |
| SALE-06 | 前置条件执行结果正确传递到测试步骤 | context 在服务间共享，变量替换使用 Jinja2 StrictUndefined |
| SALE-07 | API 断言结果在报告中正确展示 | ApiAssertionResults.tsx 组件已存在，ReportDetail.tsx 已集成 |

</phase_requirements>

## Standard Stack

### Core (已实现)
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| browser-use | >=0.12.2 | AI 驱动浏览器自动化 | 核心执行引擎 |
| Jinja2 | >=3.1.6 | 变量替换模板引擎 | StrictUndefined 防止静默失败 |
| FastAPI | >=0.135.1 | 后端 API 框架 | SSE 支持实时监控 |
| Pydantic | >=2.4.0 | 数据验证 | 配置和 Schema 验证 |

### Supporting (已实现)
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest | >=8.0.0 | 测试框架 | 单元测试和集成测试 |
| pytest-asyncio | >=0.24.0 | 异步测试支持 | 前置条件/断言服务测试 |
| aiosqlite | >=0.20.0 | 异步 SQLite | 数据持久化 |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| context['var'] | self.pre.var() | self.pre 语法更友好但需新实现，已推迟 |

## Architecture Patterns

### Recommended Project Structure (当前已实现)

```
backend/
├── core/
│   ├── agent_service.py       # Browser-Use Agent 封装
│   ├── precondition_service.py # 前置条件执行
│   ├── api_assertion_service.py # API 断言执行
│   ├── random_generators.py   # 随机数生成
│   └── time_utils.py          # 时间计算
├── api/routes/
│   ├── runs.py                # 执行 API (含前置条件和断言调用)
│   └── reports.py             # 报告 API
frontend/
├── src/components/
│   ├── TaskModal/TaskForm.tsx # 任务创建表单
│   └── Report/ApiAssertionResults.tsx # API 断言结果展示
└── src/pages/
    ├── RunMonitor.tsx         # 实时监控
    └── ReportDetail.tsx       # 报告详情
```

### Pattern 1: 前置条件执行流程

**What:** 前置条件通过 exec() 执行 Python 代码，结果存储在 context 中供后续使用

**When to use:** 所有需要预置数据或调用外部 API 的测试场景

**Example:**
```python
# 前置条件代码
from erp_api import get_operations
context['operations'] = get_operations(['FA1', 'HC1'])
context['order_no'] = sf_waybill()  # 随机销售单号

# 步骤描述（Jinja2 替换）
"在销售出库页面，输入销售单号 {{order_no}}"
```

**Source:** `backend/core/precondition_service.py`

### Pattern 2: API 断言执行流程

**What:** API 断言在 UI 执行完成后执行，收集所有结果但不终止执行

**When to use:** 需要验证后端数据状态的测试场景

**Example:**
```python
# API 断言代码
from erp_api import get_order_status
result = get_order_status('{{order_no}}')
assert_exact(result['status'], 'completed')
assert_time(result['created_at'])  # 时间在当前时间 +/- 60秒
```

**Source:** `backend/core/api_assertion_service.py`

### Pattern 3: Context 共享

**What:** PreconditionService 和 ApiAssertionService 共享同一个 context 字典

**When to use:** 前置条件产生的变量需要在 API 断言中使用

**Example (runs.py):**
```python
# 前置条件执行
precondition_service = PreconditionService(external_module_path=...)
# ... 执行前置条件 ...
context = precondition_service.get_context()

# API 断言执行（复用 context）
api_assertion_service = ApiAssertionService(external_module_path=...)
api_assertion_service.context = context  # 关键：复用上下文
```

**Source:** `backend/api/routes/runs.py` line 212-213

### Anti-Patterns to Avoid

- **在前置条件中使用 assert**: 会导致前置条件失败并终止整个测试
- **在 API 断言中创建新 context**: 应复用前置条件的 context
- **硬编码销售单号**: 使用 sf_waybill() 生成唯一单号
- **忽略 StrictUndefined 错误**: 未定义变量会抛出异常，这是预期行为

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| 变量替换 | 手动字符串替换 | `PreconditionService.substitute_variables()` | Jinja2 StrictUndefined 防止静默失败 |
| 随机数生成 | 自定义随机函数 | `random_generators.py` 中的函数 | 已注入执行环境 |
| 时间断言 | 手动比较时间 | `assert_time()` | 内置 +/-60秒容差 |
| 外部 API 调用 | 在步骤描述中调用 | 前置条件中调用 | 分离关注点，可重试 |

## Common Pitfalls

### Pitfall 1: 外部模块路径未配置

**What goes wrong:** 前置条件中 `from erp_api import ...` 报 ModuleNotFoundError

**Why it happens:** ERP_API_MODULE_PATH 环境变量未设置

**How to avoid:**
1. 在 .env 中设置 `ERP_API_MODULE_PATH=/path/to/erp-test-project`
2. 验证路径存在且包含 `__init__.py`

**Warning signs:** PreconditionService 日志显示 "外部模块路径不存在"

### Pitfall 2: 变量未定义错误

**What goes wrong:** 步骤描述中的 `{{order_no}}` 报 UndefinedError

**Why it happens:** 前置条件未执行或 context['order_no'] 未设置

**How to avoid:**
1. 确保前置条件代码执行成功
2. 检查前置条件结果中的 variables 字段

**Warning signs:** 日志显示 "变量未定义: order_no"

### Pitfall 3: API 断言重复执行

**What goes wrong:** API 断言被执行两次（runs.py line 216 和 line 274）

**Why it happens:** 代码中 execute_single 和 execute_all 都被调用

**How to avoid:** 这是一个已知问题，但不影响功能正确性（只是执行两次）

**Warning signs:** 日志显示相同的断言代码执行两次

### Pitfall 4: 截图 URL 构建错误

**What goes wrong:** 报告页面截图显示裂开图标

**Why it happens:** API_BASE 拼接导致 `/api/api/...` 重复

**How to avoid:** 使用 `API_BASE_FOR_IMAGES` 去除 `/api` 后缀

**Source:** Phase 9 修复，见 `frontend/src/api/reports.ts`

## Code Examples

### 销售出库用例配置示例

**前置条件代码:**
```python
# 使用外部 ERP API 模块获取操作员信息
from erp_api import get_operations
context['operations'] = get_operations(['FA1', 'HC1'])

# 生成随机销售单号
context['order_no'] = sf_waybill()
context['phone'] = random_phone()
```

**步骤描述 (Task.description):**
```
1. 打开销售出库页面
2. 选择仓库为"主仓库"
3. 输入销售单号 {{order_no}}
4. 选择操作员 {{operations[0]['name']}}
5. 点击"确认出库"按钮
6. 等待页面显示"出库成功"
```

**API 断言代码:**
```python
from erp_api import get_order
order = get_order('{{order_no}}')
# 验证销售单号存在
assert_exact(order['order_no'], '{{order_no}}')
# 验证状态正确
assert_exact(order['status'], 'completed')
# 验证创建时间合理
assert_time(order['created_at'])
```

### 前端创建任务示例

```typescript
// TaskForm.tsx 提交数据结构
const formData = {
  name: "销售出库测试用例",
  description: "1. 打开销售出库页面\n2. 输入销售单号 {{order_no}}...",
  target_url: "https://erp.example.com/sales/outbound",
  max_steps: 10,
  preconditions: [
    "context['order_no'] = sf_waybill()",
    "from erp_api import get_operations\ncontext['ops'] = get_operations(['FA1'])"
  ],
  api_assertions: [
    "from erp_api import get_order\norder = get_order('{{order_no}}')\nassert_exact(order['status'], 'completed')"
  ]
}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| self.pre 新语法 | context['变量名'] | Phase 10 设计决策 | 复用现有 exec() 机制，降低复杂度 |
| 前端硬编码断言 | API 断言代码配置 | Phase 6 | 灵活支持各种断言场景 |
| 静态测试数据 | 随机数生成 | Phase 7 | 支持并发测试，避免数据冲突 |

**Deprecated/outdated:**
- self.pre 新语法: 推迟到后续版本，使用 context 替代

## Open Questions

1. **外部 ERP API 模块具体接口**
   - What we know: 需要配置 ERP_API_MODULE_PATH
   - What's unclear: erp_api 模块的具体函数签名（get_operations, get_order 等）
   - Recommendation: 调通时需要确认实际 API 接口

2. **销售出库页面的具体 URL 和元素**
   - What we know: target_url 需要配置
   - What's unclear: 页面元素选择器、按钮文本
   - Recommendation: 调通时需要 AI 自动识别，或提供更详细的步骤描述

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 8.0.0+ |
| Config file | pyproject.toml `[tool.pytest.ini_options]` |
| Quick run command | `uv run pytest backend/tests/unit/test_precondition_service.py -v` |
| Full suite command | `uv run pytest backend/tests/ -v` |

### Phase Requirements -> Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| SALE-01 | 前置条件配置 | integration | `uv run pytest backend/tests/integration/test_precondition_flow.py -v` | Yes |
| SALE-02 | 动态数据方法 | integration | `uv run pytest backend/tests/integration/test_dynamic_data_flow.py -v` | Yes |
| SALE-03 | 随机数方法 | unit | `uv run pytest backend/tests/unit/test_random_generators.py -v` | Yes |
| SALE-04 | API 断言配置 | integration | `uv run pytest backend/tests/integration/test_api_assertion_integration.py -v` | Yes |
| SALE-05 | 端到端执行 | e2e | Manual - 需要真实 ERP 环境 | No (manual) |
| SALE-06 | 变量传递 | integration | `uv run pytest backend/tests/integration/test_precondition_flow.py::TestPreconditionFlow::test_precondition_to_ui_flow -v` | Yes |
| SALE-07 | 断言结果展示 | e2e | Manual - 前端报告页面验证 | No (manual) |

### Sampling Rate
- **Per task commit:** `uv run pytest backend/tests/unit/ -v` (快速单元测试)
- **Per wave merge:** `uv run pytest backend/tests/integration/ -v` (集成测试)
- **Phase gate:** Full suite + manual E2E verification before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `backend/tests/integration/test_sales_outbound_e2e.py` - 销售出库端到端测试 (需要真实 ERP 环境，标记为 manual)
- [ ] 前端 E2E 测试 - Playwright 测试验证报告页面 API 断言展示

**Note:** 大部分单元测试和集成测试已存在，主要缺失的是需要真实 ERP 环境的端到端测试，这部分在 Phase 10 中通过手动验证完成。

## Sources

### Primary (HIGH confidence)
- `backend/core/precondition_service.py` - 前置条件服务实现
- `backend/core/api_assertion_service.py` - API 断言服务实现
- `backend/api/routes/runs.py` - 执行流程集成
- `frontend/src/components/TaskModal/TaskForm.tsx` - 任务创建表单

### Secondary (MEDIUM confidence)
- `backend/tests/integration/test_precondition_flow.py` - 前置条件集成测试
- `backend/tests/integration/test_dynamic_data_flow.py` - 动态数据集成测试
- `backend/tests/integration/test_api_assertion_integration.py` - API 断言集成测试
- `.planning/phases/09-登录用例调通/09-VERIFICATION.md` - Phase 9 验证报告

### Tertiary (LOW confidence)
- None - 所有信息来自代码和文档

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - 代码已存在并测试
- Architecture: HIGH - Phase 9 已验证类似流程
- Pitfalls: HIGH - 基于代码分析和 Phase 9 经验

**Research date:** 2026-03-17
**Valid until:** 30 days (stable codebase)
