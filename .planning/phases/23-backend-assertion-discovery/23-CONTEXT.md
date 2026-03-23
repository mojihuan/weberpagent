# Phase 23: Backend Assertion Discovery - Context

**Gathered:** 2026-03-20
**Status:** Ready for planning

<domain>
## Phase Boundary

扫描 webseleniumerp 的 base_assertions.py，提供 API 端点返回断言方法列表。此阶段专注于后端发现层实现，前端断言选择器组件属于 Phase 24，执行引擎属于 Phase 25。

**Scope:**
- 扫描 base_assertions.py 获取 PcAssert/MgAssert/McAssert 类中的断言方法
- 提取每个方法的 `data` 参数选项（从 methods 字典解析）
- 解析方法 docstring 获取 i/j/k 参数描述和可选值
- 返回 headers 可用标识符列表（main/idle/vice 等）
- 提供 API 端点 `GET /external-assertions/methods`

**Out of Scope:**
- 前端断言选择器组件（Phase 24）
- headers 标识符到实际 token 的解析（Phase 25）
- 断言执行引擎（Phase 25）
- 测试报告展示（Phase 25+）

</domain>

<decisions>
## Implementation Decisions

### data 参数发现策略
- **解析方式**: 扫描方法源码，提取 `methods = {...}` 字典的键
- **实现**: 使用 `inspect.getsource()` + 正则匹配 `methods = \{[^}]+\}` 提取键名
- **示例**: `methods = {'main': ..., 'a': ..., 'b': ...}` → 提取 `['main', 'a', 'b']`
- **缓存**: 与方法签名一起缓存

### headers 参数处理
- **Phase 23 职责**: 只返回可用标识符列表 `['main', 'idle', 'vice', 'special', 'platform', 'super', 'camera']`
- **Token 解析**: 推迟到 Phase 25 执行时，由 ExternalAssertionBridge 调用 ImportApi.headers 解析
- **硬编码列表**: headers 标识符是固定的，无需从外部模块发现

### i/j/k 参数解析深度
- **完整解析**: 将 docstring 中的选项描述解析为结构化数据
- **解析格式**: `i：订单状态 1待发货 2待取件` →
  ```json
  {
    "name": "i",
    "description": "订单状态",
    "options": [
      {"value": 1, "label": "待发货"},
      {"value": 2, "label": "待取件"}
    ]
  }
  ```
- **正则模式**: `(\d+)([^\d]+)` 匹配数字+描述组合

### 错误处理策略
- **WEBSERP_PATH 未配置**: 返回 HTTP 503 Service Unavailable + 明确错误信息
- **外部模块加载失败**: HTTP 503 + 详细错误（缺失文件/导入错误）
- **响应格式**:
  ```json
  {
    "detail": "WEBSERP_PATH not configured. Set WEBSERP_PATH in .env file."
  }
  ```

### API 响应结构
- **复用 Phase 17 格式**: 与 `/external-data-methods` 结构一致
- **响应示例**:
  ```json
  {
    "available": true,
    "headers_options": ["main", "idle", "vice", "special", "platform", "super", "camera"],
    "classes": [
      {
        "name": "PcAssert",
        "methods": [
          {
            "name": "attachment_inventory_list_assert",
            "description": "配件库存列表断言",
            "data_options": ["main", "a", "b"],
            "parameters": [
              {"name": "i", "description": "库存状态", "options": [{"value": 2, "label": "库存中"}, {"value": 1, "label": "待入库"}]}
            ]
          }
        ]
      }
    ],
    "total": 83
  }
  ```

### 缓存策略
- **方法签名**: 启动时缓存，后续请求直接返回缓存结果
- **刷新机制**: 需要重启应用才能刷新方法列表（与 Phase 17 一致）
- **不提供刷新端点**: 保持后端简单

### 搜索/过滤功能
- **后端不实现搜索**: 返回所有类和方法，前端自行实现搜索过滤
- **不支持按类名过滤**: 返回 PcAssert/MgAssert/McAssert 所有类
- **80+ 方法全部返回**: 前端可通过类名分组 + 搜索框过滤

### Claude's Discretion
- 桥接模块的具体文件位置（扩展现有 `external_precondition_bridge.py` 或新建文件）
- data 参数解析的正则表达式实现细节
- i/j/k 选项值解析的边界情况处理（如无选项描述时）
- 内部方法的过滤规则（如 `get_handle_response` 等不应暴露的方法）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 架构设计参考
- `.planning/research/ARCHITECTURE.md` — ExternalPreconditionBridge 架构设计、Anti-Patterns、集成检查清单
- `.planning/research/PITFALLS.md` — 断言集成陷阱（Pitfall A1-A5）、Headers 解析、data 参数、i/j/k 分离
- `.planning/research/STACK.md` — 断言系统集成技术栈、方法签名模式、执行流程

### 现有代码参考
- `backend/core/external_precondition_bridge.py` — 现有桥接模块，需扩展支持断言类加载
  - `load_base_params_class()` — 可复用的延迟加载模式
  - `discover_class_methods()` — 可复用的方法发现逻辑
  - `extract_method_info()` — 可复用的参数提取逻辑
  - `_parse_docstring_params()` — 可复用的 docstring 解析逻辑
- `backend/api/routes/external_data_methods.py` — API 路由模式参考
- `backend/api/routes/external_operations.py` — 503 错误处理模式参考

### 前置阶段参考
- `.planning/phases/17-后端数据获取桥接/17-CONTEXT.md` — Phase 17 决策（方法发现、API 格式、缓存策略）
- `.planning/phases/14-后端桥接模块/14-CONTEXT.md` — Phase 14 决策（桥接模块模式、错误处理）

### 外部项目结构
- `webseleniumerp/common/base_assertions.py` — PcAssert/MgAssert/McAssert 断言类
- `webseleniumerp/common/base_assert.py` — BaseAssert 基类，包含 `assert_time`/`assert_contains` 等工具方法

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/core/external_precondition_bridge.py`:
  - `configure_external_path()` — 路径配置逻辑可复用
  - `load_base_params_class()` — 延迟加载模式可复用
  - `discover_class_methods()` — 方法发现逻辑可复用
  - `extract_method_info()` — 参数提取逻辑可复用
  - `_parse_docstring_params()` — docstring 解析逻辑需扩展支持选项值解析
  - 单例缓存模式可直接复用
- `backend/api/routes/external_data_methods.py`:
  - Pydantic 响应模型模式可复用
  - 503 错误处理模式可复用

### Established Patterns
- **源码解析**: `inspect.getsource` + 正则表达式提取
- **API 响应**: Pydantic response model + grouped list
- **错误处理**: HTTP 503 (不可用) + 明确 detail 字段
- **缓存策略**: 模块级单例 + 启动时缓存
- **延迟加载**: 首次访问时加载外部模块

### Integration Points
- `backend/core/external_precondition_bridge.py` — 需扩展支持 base_assertions.py 加载
- `backend/api/main.py` — 需注册新的 `/external-assertions` 路由
- `backend/config/settings.py` — 已有 `weberp_path` 配置

### 需要新增的代码
| 组件 | 目的 | 参考模式 |
|------|------|----------|
| `load_base_assertions_class()` | 加载 PcAssert/MgAssert/McAssert | 复制 `load_base_params_class()` |
| `get_assertion_methods_grouped()` | 按类分组返回方法 | 复制 `get_data_methods_grouped()` |
| `_parse_data_options_from_source()` | 从 methods 字典提取 data 选项 | 新增：正则解析源码 |
| `_parse_param_options()` | 解析 i/j/k 选项值 | 扩展 `_parse_docstring_params()` |
| `/external-assertions/methods` 路由 | API 端点 | 复制 `/external-data-methods` |

</code_context>

<specifics>
## Specific Ideas

- data 选项解析应处理无 methods 字典的情况（默认返回 `['main']`）
- i/j/k 选项解析应支持中文冒号 `：` 和英文冒号 `:`
- headers 标识符列表是固定的：`main`, `idle`, `vice`, `special`, `platform`, `super`, `camera`
- API 响应的 `total` 字段应包含所有类的所有方法总数
- 错误信息应包含修复建议（如 "Ensure config/settings.py exists in webseleniumerp"）

</specifics>

<deferred>
## Deferred Ideas

- 前端断言选择器组件 — Phase 24
- headers 标识符到实际 token 的解析 — Phase 25
- 断言执行引擎 — Phase 25
- 断言结果存入 context — Phase 25
- E2E 测试 — Phase 26
- 单元测试覆盖 — Phase 27
- 缓存刷新端点 — 未来优化
- 按类名/方法名搜索过滤 — 前端实现

</deferred>

---
*Phase: 23-backend-assertion-discovery*
*Context gathered: 2026-03-20*
