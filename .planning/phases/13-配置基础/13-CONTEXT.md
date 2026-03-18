# Phase 13: 配置基础 - Context

**Gathered:** 2026-03-17
**Status:** Ready for planning

<domain>
## Phase Boundary

配置 WEBSERP_PATH 环境变量，提供 webseleniumerp 配置文档。这是基础设施配置阶段，专注于环境变量设置和验证，不涉及业务功能变更。

**Scope:**
- 添加 WEBSERP_PATH 环境变量配置
- 实现启动时配置验证
- 提供 webseleniumerp 的 config/settings.py 配置文档

**Out of Scope:**
- ExternalPreconditionBridge 模块实现（Phase 14）
- 前端操作码选择器（Phase 15）
- 端到端验证（Phase 16）

</domain>

<decisions>
## Implementation Decisions

### 验证时机
- **系统启动时验证**（fail-fast 策略）
- 在 FastAPI startup event 中执行验证
- 配置错误时直接阻止启动，确保问题在第一时间暴露

### 验证内容
启动时全面验证以下内容：
1. **路径存在** — WEBSERP_PATH 指向的目录存在
2. **base_prerequisites.py 存在** — 核心前置条件文件存在
3. **config/settings.py 存在** — webseleniumerp 配置文件存在（该文件在 .gitignore 中，需用户创建）
4. **可导入性** — 模块可以成功导入（浅尝验证，不执行代码）

### 文档位置
- 在 **README.md** 中添加"webseleniumerp 配置"章节
- 提供完整的 config/settings.py 模板
- 包含 DATA_PATHS 配置示例

### 错误处理策略
- **启动失败 + 明确错误信息**
- 打印具体缺失项（哪个文件/目录不存在）
- 提供修复建议（如何创建 config/settings.py）
- 使用 exit code 1 退出进程

### Claude's Discretion
- 验证函数的具体实现位置（backend/config/ 或 backend/services/）
- 错误信息的具体格式和文案
- 是否需要 logging vs print

</decisions>

<canonical_refs>
## Canonical References

### 配置模式参考
- `backend/config/settings.py` — 现有 Pydantic Settings 配置模式
- `.env.example` — 环境变量模板格式
- `.planning/phases/01-foundation-fixes/01-CONTEXT.md` — Phase 1 配置决策

### 外部项目结构
- `webseleniumerp/base_prerequisites.py` — 前置条件基类
- `webseleniumerp/config/settings.py` — 外部项目配置（需用户创建）

### 研究文档
- `.planning/research/SUMMARY.md` — v0.3 架构研究总结
- `.planning/research/ARCHITECTURE.md` — ExternalPreconditionBridge 架构设计

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `backend/config/settings.py`: Pydantic Settings 类 — 可直接添加 weberp_path 字段
- `.env.example`: 环境变量模板 — 可添加 WEBSERP_PATH 示例
- FastAPI startup event: 现有启动生命周期钩子 — 可添加验证逻辑

### Established Patterns
- **配置加载**: Pydantic BaseSettings + lru_cache 单例
- **环境变量命名**: 小写下划线格式（如 erp_api_module_path）
- **验证模式**: 可参考 Phase 5 的 ERP_API_MODULE_PATH 配置

### Integration Points
- `backend/api/main.py` — FastAPI 应用入口，startup event 挂载点
- `backend/config/settings.py` — 配置类，添加 weberp_path 字段
- `.env.example` — 添加 WEBSERP_PATH 配置示例

</code_context>

<specifics>
## Specific Ideas

- 错误信息应该清晰指出缺失的文件/目录，并提供创建命令示例
- 验证逻辑应该轻量，不执行实际的前置条件代码
- config/settings.py 模板应该包含 DATA_PATHS 配置（webseleniumerp 必需）

</specifics>

<deferred>
## Deferred Ideas

- ExternalPreconditionBridge 模块实现 — Phase 14
- 前端操作码选择器组件 — Phase 15
- 操作码执行和结果展示 — Phase 16

</deferred>

---
*Phase: 13-配置基础*
*Context gathered: 2026-03-17*
