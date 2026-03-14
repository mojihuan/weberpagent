# Phase 1: Foundation Fixes - Context

**Gathered:** 2026-03-14
**Status:** Ready for planning
**Revised:** 2026-03-14 (removed retry mechanism to future phase)

<domain>
## Phase Boundary

这 phase 专注于技术基础设施层面的修复， 不涉及业务功能变更。

</domain>

<decisions>
## Implementation Decisions

### 环境配置
- **文件结构**: 单文件 `.env` (git 忽略本地 `.env 文件)
- **开发/生产区分**: 通过注释区分，开发时使用默认值， 生产时需要取消注释并修改值
- **格式**: `KEY=VALUE` 格式，  - 后端: `DASHSCOPE_API_KEY`, `OPENAI_API_KEY`, `ERP_BASE_URL`, `ERP_USERNAME`
  `ERP_PASSWORD`
  - 前端: `VITE_API_BASE` (Vite 环境变量)
  - `.env.example` 提供示例，  - 本地开发无需 `.env` 文件 (直接使用默认值)

- **决策理由**: 简化配置管理，  鷭开发生产环境切换成本，  .env 文件统一管理所有环境变量

### API 响应格式
- **成功响应**: `{success: true, data: T, meta?: {page: number, total: number}}`
- **错误响应**: HTTP 状态码 + 结构化错误体
  ```json
  {
    "success": false,
    "error": {
      "code": "ERROR_CODE",
      "message": "Human readable error message",
      "request_id": "UUID for debugging",
      "stack": "Optional: stack trace for debugging"
    }
  }
  ```
- **HTTP 状态码**: 400 (Bad Request), 404 (Not Found), 500 (Internal Server Error)
- **决策理由**: 结构化错误体便于前端统一处理和 提供调试信息 (request_id)
  HTTP 状态码让前端可以根据状态码进行分支处理

### 异步数据库模式
- **引擎**: aiosqlite async engine
- **连接池**: 5 个连接 (开发环境足够)
- **会话管理**: 每个请求创建新会话
- **决策理由**: SQLite 是文件数据库， 连接池开销小， 5 个连接足够开发环境使用

### LLM 确定性配置
- **temperature**: 0 (确保确定性)
- **无缓存**: 每次任务重新计算
- **决策理由**: 测试需要确定性， temperature=0 确保相同输入产生相同结果

### 浏览器清理
- **模式**: try/finally 确保清理
- **错误日志**: 记录到日志文件
- **决策理由**: 浏览器异常可能导致内存泄漏， try/finally 确保资源释放

</decisions>

<specifics>
## Specific Ideas

- 使用 Python 3.11 + FastAPI 最佳实践
- SQLite async patterns 参考 aiosqlite 官方文档
- LLM temperature=0 参考 OpenAI/Anthropic 文档

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/db/database.py`: 现有 async engine 实现
- `backend/api/main.py`: FastAPI 应用框架
- `pydantic`: 数据验证

### Established Patterns
- Repository pattern for data 访问
- FastAPI BackgroundTasks for 异步任务
- SSE for 实时通信

### Integration Points
- 配置集中在 `.env` 和 `config.py`
- API 响应在 `routes/` 中间件
- 数据库在 `backend/db/` 层

</code_context>

<deferred>
## Deferred Ideas

### LLM 重试机制 (Deferred to Phase 3)
- **原计划**: 指数退避重试， 最多 3 次
- **延期原因**:
  1. 重试机制需要更复杂的错误处理逻辑
  2. 需要区分可重试错误 (网络超时) 和不可重试错误 (认证失败)
  3. Phase 1 专注于基础设施稳定性， 重试是增强功能
- **移至**: Phase 3 Service Layer Restoration (SVC-04)
- **实现位置**: `backend/llm/factory.py` 的 `create_llm()` 或 AgentService 包装器

</deferred>

---
*Phase: 01-foundation-fixes*
*Context gathered: 2026-03-14*
*Last revised: 2026-03-14*
