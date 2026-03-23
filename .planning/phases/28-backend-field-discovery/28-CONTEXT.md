# Phase 28: 后端字段发现 - Context

**Gathered:** 2026-03-21
**Status:** Ready for planning

<domain>
## Phase Boundary

AST 解析 base_assertions_field.py，提供可用断言字段列表 API。此阶段专注于字段发现层实现，前端字段配置组件属于 Phase 29，执行适配层属于 Phase 30。

**Scope:**
- 使用 AST 解析 param 字典，提取所有字段（约 300 个）
- 提供 API 端点 `GET /api/external-assertions/fields`
- 字段列表包含 name, path, is_time_field, group, description
- 实现字段分组策略（从命名模式推断）
- 实现中文描述生成（关键词映射表）

**Out of Scope:**
- 前端字段配置组件（Phase 29）
- 断言执行适配层（Phase 30）
- E2E 测试（Phase 31）

</domain>

<decisions>
## Implementation Decisions

### AST 解析策略
- **D-01:** 扩展现有 `external_precondition_bridge.py`，新增 `parse_assertions_field()` 函数
- **D-02:** 使用 Python `ast` 模块解析 base_assertions_field.py，避免运行时依赖 BaseApi
- **D-03:** 解析目标：`assertive_field` 方法中的 `param = {...}` 字典，提取所有键名
- **D-04:** 与现有 `load_base_assertions_class()` 模式保持一致

### 字段分组规则
- **D-05:** 使用命名模式推断分组，规则如下：
  - `sale*` → 销售相关
  - `purchase*` → 采购相关
  - `inventory*` → 库存相关
  - `order*` → 订单相关
  - `*Time` / `*time` → 时间字段
  - `accessoryOrderInfo.*` → 配件订单嵌套字段
  - 其他 → 通用字段
- **D-06:** 不维护手动分组配置文件

### Description 生成逻辑
- **D-07:** 使用关键词映射表生成中文描述（约 50 个常用关键词）
- **D-08:** 映射表示例：
  ```python
  KEYWORD_MAPPINGS = {
      'create': '创建',
      'update': '更新',
      'delete': '删除',
      'time': '时间',
      'status': '状态',
      'order': '订单',
      'sale': '销售',
      'purchase': '采购',
      'inventory': '库存',
      # ... 约 50 个
  }
  ```
- **D-09:** 生成规则：camelCase → 分词 → 映射 → 拼接
  - `createTime` → `create` + `Time` → `创建` + `时间` → `创建时间`
  - `salesOrder` → `sales` + `Order` → `销售` + `订单` → `销售订单`
  - `statusStr` → `status` + `Str` → `状态` + `字符串` → `状态字符串`

### 时间字段识别
- **D-10:** 使用后缀匹配判断 `is_time_field`
- **D-11:** 时间字段后缀：`Time`, `time`, `Date`, `date`
- **D-12:** 示例：`createTime`, `updateTime`, `saleTime`, `orderDate` → `is_time_field: true`

### API 响应结构
- **D-13:** 复用现有分组响应格式：
  ```json
  {
    "available": true,
    "groups": [
      {
        "name": "销售相关",
        "fields": [
          {
            "name": "salesOrder",
            "path": "salesOrder",
            "is_time_field": false,
            "description": "销售订单"
          }
        ]
      }
    ],
    "total": 300
  }
  ```

### 缓存策略
- **D-14:** 与 Phase 23 一致：模块级单例 + 启动时缓存
- **D-15:** 不提供刷新端点，需重启应用刷新字段列表

### Claude's Discretion
- 关键词映射表的具体条目（约 50 个，可在实现时补充）
- 嵌套字段 path 的具体格式（如 `accessoryOrderInfo.fieldName` 或 `accessoryOrderInfo[fieldName]`）
- 边界情况处理（无法识别的字段名直接返回原名）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 架构设计参考
- `.planning/research/STACK.md` — 断言系统集成技术栈、方法签名模式
- `.planning/research/PITFALLS.md` — 断言集成陷阱、data 参数处理

### 前置阶段参考
- `.planning/phases/23-backend-assertion-discovery/23-CONTEXT.md` — Phase 23 决策（方法发现、API 格式、缓存策略）

### 现有代码参考
- `backend/core/external_precondition_bridge.py` — 现有桥接模块，需扩展支持字段解析
  - `load_base_assertions_class()` — 可复用的延迟加载模式
  - `_parse_data_options_from_source()` — 可参考的源码解析模式
- `backend/api/routes/external_assertions.py` — 现有断言 API 路由

### 外部项目结构
- `webseleniumerp/common/base_assertions_field.py` — 包含 param 字典的字段定义文件

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/core/external_precondition_bridge.py`:
  - `load_base_assertions_class()` — 延迟加载模式可复用
  - `_parse_data_options_from_source()` — 正则解析源码模式可参考
  - 单例缓存模式可直接复用
- `backend/api/routes/external_assertions.py`:
  - Pydantic 响应模型模式可复用
  - 503 错误处理模式可复用

### Established Patterns
- **源码解析**: `inspect.getsource` + 正则表达式 或 `ast` 模块
- **API 响应**: Pydantic response model + grouped list
- **错误处理**: HTTP 503 (不可用) + 明确 detail 字段
- **缓存策略**: 模块级单例 + 启动时缓存

### Integration Points
- `backend/core/external_precondition_bridge.py` — 需扩展支持 base_assertions_field.py 解析
- `backend/api/routes/external_assertions.py` — 需新增 `/fields` 端点
- `backend/api/main.py` — 路由已注册，无需修改

### 需要新增的代码
| 组件 | 目的 | 参考模式 |
|------|------|----------|
| `_load_assertions_field_file()` | 加载 base_assertions_field.py 文件 | 复用路径配置逻辑 |
| `parse_assertions_field_py()` | AST 解析 param 字典 | 新增：ast 模块解析 |
| `_infer_field_group()` | 从字段名推断分组 | 新增：命名模式匹配 |
| `_generate_field_description()` | 生成中文描述 | 新增：关键词映射 |
| `_is_time_field()` | 判断时间字段 | 新增：后缀匹配 |
| `get_assertion_fields_grouped()` | 按分组返回字段列表 | 复制 `get_assertion_methods_grouped()` |
| `/external-assertions/fields` 路由 | API 端点 | 复用现有路由文件 |

</code_context>

<specifics>
## Specific Ideas

- 关键词映射表应覆盖常见业务词汇（销售、采购、库存、订单等）
- 嵌套字段使用点分隔路径（如 `accessoryOrderInfo.imei`）
- 无法识别的字段名直接返回原名作为 description

</specifics>

<deferred>
## Deferred Ideas

- 前端字段配置组件 — Phase 29
- 断言执行适配层 — Phase 30
- E2E 测试 — Phase 31
- 手动补充字段描述 — 工作量巨大，使用自动生成
- 缓存刷新端点 — 未来优化

</deferred>

---
*Phase: 28-backend-field-discovery*
*Context gathered: 2026-03-21*
