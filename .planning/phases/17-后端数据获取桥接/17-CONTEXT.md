# Phase 17: 后端数据获取桥接 - Context

**Gathered:** 2026-03-18
**Status:** Ready for planning

<domain>
## Phase Boundary

扫描 webseleniumerp 的 base_params.py 中的查询方法，提供 API 端点让用户可以获取方法列表和执行结果。此阶段专注于后端桥接层实现，前端数据选择器组件属于 Phase 18。

**Scope:**
- 扫描 base_params.py 获取所有公开查询方法
- 提供数据获取方法列表 API（按类分组，包含完整签名信息）
- 执行数据获取方法并返回 JSON 结果
- 与现有 ExternalPreconditionBridge 模块集成

**Out of Scope:**
- 前端数据选择器组件（Phase 18）
- 字段提取路径配置（Phase 18）
- 前置条件代码生成（Phase 19）

</domain>

<decisions>
## Implementation Decisions

### 方法解析策略
- **解析方式**: 使用 `inspect.getsource` + 正则解析，复用 Phase 14 模式
- **扫描范围**: 扫描所有公开方法（不以 `_` 开头），不仅限于 `xxx_data()` 方法
- **参数类型**: 推断参数类型信息（从类型注解或默认值）
- **签名信息**: 包含参数名、类型、是否必需、默认值

### API 响应结构
- **分组方式**: 按类名分组（如 BaseParams, InventoryParams 等）
- **响应结构**:
  ```json
  {
    "available": true,
    "classes": [
      {
        "name": "BaseParams",
        "methods": [
          {
            "name": "inventory_list_data",
            "description": "获取库存列表",
            "parameters": [
              {"name": "i", "type": "int", "required": false, "default": 0},
              {"name": "j", "type": "int", "required": false, "default": 10}
            ]
          }
        ]
      }
    ],
    "total": 25
  }
  ```
- **执行响应**: 直接返回 JSON 数据结果，字段提取在前端/测试执行时处理

### 执行与错误处理
- **执行方式**: 在桥接模块中实现 `execute_data_method()`，直接调用 base_params.py 的方法
- **超时策略**: 30 秒超时（与 PreconditionService 一致）
- **错误处理**: 返回 HTTP 200 + 错误信息字段，便于前端展示和重试
  ```json
  {
    "success": false,
    "error": "参数 i 必须为整数",
    "error_type": "ParameterError"
  }
  ```

### 缓存策略
- **方法签名**: 启动时缓存，后续请求直接返回缓存结果
- **执行结果**: 不缓存，每次调用都重新执行（确保数据最新）
- **刷新机制**: 仅通过重启应用刷新缓存（与 Phase 14 一致）

### Claude's Discretion
- API 端点命名（`/external-data-methods` 或 `/data-methods`）
- 桥接模块的文件位置（复用 `external_precondition_bridge.py` 或新建文件）
- 参数类型推断的具体实现（优先使用类型注解，其次从默认值推断）
- 是否需要添加方法搜索/过滤功能

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 架构设计参考
- `.planning/research/ARCHITECTURE.md` — ExternalPreconditionBridge 架构设计、Anti-Patterns、集成检查清单

### 现有代码参考
- `backend/core/external_precondition_bridge.py` — 现有桥接模块，需扩展支持数据获取方法
- `backend/api/routes/external_operations.py` — 现有 API 路由模式参考
- `backend/core/precondition_service.py` — 前置条件服务，30 秒超时模式

### 前置阶段参考
- `.planning/phases/14-后端桥接模块/14-CONTEXT.md` — Phase 14 决策（操作码解析、API 模式、错误处理）

### 外部项目结构
- `webseleniumerp/common/base_params.py` — 查询方法类，包含 xxx_data() 方法

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/core/external_precondition_bridge.py`:
  - `configure_external_path()` — 路径配置逻辑可复用
  - `load_pre_front_class()` — 延迟加载模式可复用
  - `_parse_operations_from_source()` — 源码解析模式可复用
  - 单例缓存模式可直接复用
- `backend/api/routes/external_operations.py`:
  - Pydantic 响应模型模式可复用
  - 503 错误处理模式可复用

### Established Patterns
- **源码解析**: `inspect.getsource` + 正则表达式提取
- **API 响应**: Pydantic response model + grouped list
- **错误处理**: HTTP 503 (不可用) / HTTP 200 + error field (执行失败)
- **缓存策略**: 模块级单例 + 启动时缓存

### Integration Points
- `backend/core/external_precondition_bridge.py` — 需扩展支持 base_params.py 加载
- `backend/api/main.py` — 需注册新的数据获取方法路由
- `backend/config/settings.py` — 已有 `weberp_path` 配置

</code_context>

<specifics>
## Specific Ideas

- API 端点命名建议: `/external-data-methods` (与 `/external-operations` 保持一致)
- 方法分组应清晰展示类名，便于用户理解方法来源
- 参数签名信息应包含 `required` 字段，前端可据此标记必填项
- 执行失败时返回 `error_type` 字段，便于前端区分参数错误和系统错误

</specifics>

<deferred>
## Deferred Ideas

- 前端数据选择器组件 — Phase 18
- 字段提取路径配置 — Phase 18
- 前置条件代码生成 — Phase 19
- 数据缓存机制（避免重复查询）— v2 需求
- 方法搜索/过滤功能 — 可在 Phase 18 考虑

</deferred>

---
*Phase: 17-后端数据获取桥接*
*Context gathered: 2026-03-18*
