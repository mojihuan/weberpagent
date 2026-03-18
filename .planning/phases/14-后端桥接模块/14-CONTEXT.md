# Phase 14: 后端桥接模块 - Context

**Gathered:** 2026-03-17
**Status:** Ready for planning

<domain>
## Phase Boundary

创建 ExternalPreconditionBridge 模块，隔离外部项目 (webseleniumerp) 导入，提供操作码 API 端点。此阶段专注于后端桥接层实现，前端集成属于 Phase 15。

**Scope:**
- 创建 ExternalPreconditionBridge 模块，封装所有外部项目导入
- 实现 `get_available_operations()` 返回分组操作码列表
- 提供 `/api/external-operations` API 端点
- 实现操作码执行功能，与现有 PreconditionService 集成

**Out of Scope:**
- 前端操作码选择器组件（Phase 15）
- 端到端验证（Phase 16）

</domain>

<decisions>
## Implementation Decisions

### 操作码解析策略
- **解析方式**: 使用 `inspect.getsource` 解析 `PreFront.operations()` 方法源码
- **提取内容**: 操作码（如 'FA1', 'HC1'）+ 模块注释（如 '# 配件管理|配件采购'）
- **缓存策略**: 应用启动时加载一次并缓存到内存，后续请求直接返回缓存结果
- **刷新机制**: 需要重启应用才能刷新操作码列表（可接受的权衡）

### 与 PreconditionService 集成
- **集成方式**: PreconditionService 直接调用桥接模块的 `execute_operations()` 方法
- **代码生成**: 前端选择操作码后，生成 Python 代码字符串作为前置条件内容
- **生成代码模板**:
  ```python
  import sys
  sys.path.insert(0, '<WEBSERP_PATH>')

  from common.base_prerequisites import PreFront

  pre_front = PreFront()
  pre_front.operations(['FA1', 'HC1'])

  context['precondition_result'] = 'success'
  ```

### API 响应结构
- **分组方式**: 从源码注释解析模块信息（格式: `# 配件管理|配件采购|新增采购`）
- **响应结构**: 按模块分组返回
  ```json
  {
    "modules": [
      {
        "name": "配件管理 - 采购",
        "operations": [
          {"code": "FA1", "description": "新增采购单未付款入库"},
          {"code": "FA2", "description": "新增采购单未付款在路上"}
        ]
      }
    ],
    "total": 120
  }
  ```

### 错误处理策略
- **外部模块未配置/加载失败**: 返回 HTTP 503 Service Unavailable + 明确错误信息
- **操作码执行失败**: Fail-fast 模式，立即终止整个测试（与现有 PreconditionService 行为一致）
- **错误信息格式**: 清晰说明缺失项（哪个文件/目录不存在），提供修复建议

### Claude's Discretion
- 桥接模块的具体文件位置（`backend/core/` 或 `backend/services/`）
- 源码解析的正则表达式实现细节
- 模块分组的层级结构（是否支持多级分组）
- 是否需要添加操作码搜索/过滤功能

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 架构设计参考
- `.planning/research/ARCHITECTURE.md` — ExternalPreconditionBridge 架构设计、Anti-Patterns、集成检查清单
- `.planning/research/SUMMARY.md` — v0.3 架构研究总结、技术栈推荐

### 现有代码参考
- `backend/core/precondition_service.py` — 现有前置条件服务，需集成桥接模块
- `backend/config/settings.py` — 配置类，已有 `weberp_path` 字段（Phase 13 添加）
- `backend/api/routes/runs.py` — 现有 API 路由模式参考

### 前置阶段参考
- `.planning/phases/13-配置基础/13-CONTEXT.md` — Phase 13 决策（WEBSERP_PATH 配置、启动验证）

### 外部项目结构
- `webseleniumerp/common/base_prerequisites.py` — PreFront 类，operations() 方法
- `webseleniumerp/config/settings.py` — 外部项目配置（需用户创建）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/core/precondition_service.py`: PreconditionService 类 — 需集成桥接模块的 `execute_operations()`
- `backend/config/settings.py`: Settings 类 — 已有 `weberp_path` 字段
- `backend/api/routes/`: 现有 API 路由模式 — 可参考 `runs.py` 的 SSE 和错误处理模式

### Established Patterns
- **服务层模式**: `backend/core/` 目录下的服务类
- **API 路由模式**: FastAPI router + Pydantic response model
- **错误处理**: HTTPException + 明确错误信息
- **配置访问**: `get_settings()` 单例模式

### Integration Points
- `backend/core/precondition_service.py` — 需添加对外部操作码执行的支持
- `backend/api/main.py` — 需注册新的 `/external-operations` 路由
- `backend/config/settings.py` — 已有 `weberp_path` 配置

</code_context>

<specifics>
## Specific Ideas

- 源码解析应支持注释格式 `# 模块|子模块|操作描述`，提取完整层级信息
- 分组名称应清晰区分（如"配件管理 - 采购"vs"配件管理 - 库存"）
- 503 错误响应应包含 `detail` 字段，说明具体缺失项和修复步骤
- 代码生成模板应包含 `context['precondition_result'] = 'success'` 以便后续步骤引用

</specifics>

<deferred>
## Deferred Ideas

- 前端操作码选择器组件 — Phase 15
- 操作码搜索/过滤功能 — 可在 Phase 15 考虑
- 端到端验证测试 — Phase 16
- 操作码执行缓存（避免重复执行相同操作）— 未来优化

</deferred>

---
*Phase: 14-后端桥接模块*
*Context gathered: 2026-03-17*
