# CLAUDE.md

## 项目概述

AI 驱动的 UI 自动化测试平台，让 QA 用自然语言编写测试用例，AI 自动执行并生成报告。

核心流程：自然语言描述 → AI 决策(browser-use + Qwen) → Playwright 执行

用户通过前端界面创建测试任务（支持 Excel 导入），描述测试步骤后由 AI agent 自动驱动浏览器执行，
实时展示执行过程，最后生成包含截图和断言结果的测试报告，同时输出可复用的 Playwright 测试代码。

| 层级 | 技术 |
|------|------|
| 前端 | React 19.2, TypeScript 5.9, Vite 7.3, Tailwind CSS 4.2 |
| 后端 | Python 3.11+, FastAPI, Pydantic, SQLAlchemy |
| AI 引擎 | Browser-Use 0.12+, Qwen 3.5 Plus (阿里云 DashScope) |
| 浏览器自动化 | Playwright (Chromium) |
| 通信 | REST API + SSE (Server-Sent Events) |
| 数据库 | SQLite (aiosqlite, 异步) |
| 包管理 | uv (Python), npm (Node.js) |

## 架构关键决策

### browser-use CDP 限制

browser-use 通过 CDP 协议控制浏览器，Playwright 的 locator 和 keyboard API 不可用。
所有 DOM 交互必须用 `page.evaluate()` + `page.mouse` 替代：
- 查找元素 → `page.evaluate(() => document.querySelector(...))`
- 输入文本 → `page.evaluate(() => element.value = ...)`
- 点击操作 → `page.mouse.click(x, y)`

dom_patch.py 对 browser-use 内部类做猴子补丁以修正元素检测，升级 browser-use 时必须验证补丁兼容性。

### 多阶段执行管道

`backend/api/routes/run_pipeline.py` 编排完整的测试执行流程：

1. **preconditions** — 执行前置条件（准备测试数据、登录等）
2. **agent run** — AI agent 驱动浏览器执行测试步骤
3. **assertions** — 执行断言验证
4. **codegen** — 将 agent 动作转换为 Playwright 测试代码
5. **report** — 生成测试报告

每个阶段通过 EventManager 推送 SSE 事件，前端实时展示进度。

### SSE 实时推送

EventManager 单例管理 SSE 订阅，前端 `useRunStream` hook 消费事件流。
运行状态、步骤进度、日志、截图均通过 SSE 实时推送到前端，无需轮询。

### 代码生成管道

agent 动作经过多级转换生成可复用的 Playwright 测试代码：
- agent 动作 → ActionTranslator 转换为 Playwright 原子操作
- CodeGenerator 组装完整测试文件（含 import、fixture、test function）
- 生成的代码包含嵌入式登录、前置条件调用和断言
- `get_data()` 调用通过 `_get_data` helper 保留在生成代码中

### 外部项目集成

通过 external_module_loader 动态加载 webseleniumerp 模块：
- 支持 `get_data()` 等外部方法调用，将结果注入前置条件和断言
- external_method_discovery 扫描并缓存外部模块的方法签名
- _module_map 通过 JSON 文件缓存避免每次扫描（优化前 32s → 缓存后即时加载）

## 目录结构约定

```
backend/
  api/routes/    — 每个 domain 一个路由文件（tasks.py, runs.py, reports.py...）
  agent/         — AI 浏览器自动化层（MonitoredAgent, detectors, prompts）
  core/          — 业务服务（agent_service, code_generator, precondition_service...）
  llm/           — LLM 抽象层（factory, config, openai）
  db/            — 数据库（models, repository, schemas, database）
  config/        — 配置（settings.py 用 Pydantic BaseSettings）
  utils/         — 工具类（logger, excel_parser, screenshot）

frontend/src/
  pages/         — 页面组件（Dashboard, Tasks, RunMonitor, Reports...）
  components/    — 按功能分组（RunMonitor/, Report/, TaskDetail/...）
  hooks/         — 自定义 hooks（useRunStream, useTasks, useReports）
  api/           — API 客户端（client.ts + 每个 domain 一个文件）
  types/         — TypeScript 类型定义（index.ts 统一导出）
```

路由约定：新增 domain 时，后端在 `api/routes/` 添加路由文件并在 `api/routes/__init__.py` 注册，
前端在 `api/` 添加对应 API 文件，`types/index.ts` 添加类型定义。

## 代码规范

- **Python**: ruff (line-length=100, target=py311)，类型注解用 `str | None`（不用 Optional）
- **TypeScript**: strict mode, `verbatimModuleSyntax`, `erasableSyntaxOnly`（不用 enum）
- **API 响应格式**:
  ```json
  {"success": true, "data": {...}}
  {"success": false, "error": {"code": "...", "message": "..."}}
  ```
- **数据库**: SQLAlchemy async + aiosqlite, Repository 模式, ID 用 `uuid4().hex[:8]`
- **前端状态**: TanStack React Query (server state) + useState (local state)，无 Redux
- **异步优先**: 所有 DB/IO 操作用 async/await，同步阻塞操作用 `run_in_executor`
- **日志**: 使用 `backend/utils/logger.py` 的 get_logger，不直接用 print/logging

## 开发命令

```bash
# 启动后端（端口 11002）
uv run uvicorn backend.api.main:app --port 11002

# 启动前端（端口 11001，自动代理 /api → 11002）
cd frontend && npm run dev

# 测试
uv run pytest backend/tests/ -v

# Lint
uv run ruff check backend/
cd frontend && npm run lint

# 部署到服务器（121.40.191.49）
# Docker 部署: docker compose up -d --build
# 快速启动: 参见 docs/deployment.md
```

前端开发时 Vite 配置了 proxy，`/api` 请求自动转发到后端 11002 端口，无需 CORS 配置。

## 已知陷阱

- **exec() 执行用户代码**: PreconditionService 用 exec() 执行前置条件代码，单用户场景可接受，多用户部署需沙箱化
- **browser-use monkey-patch**: dom_patch.py 猴子补丁 browser-use 内部类，升级 browser-use 时必须验证补丁兼容性
- **UUID 主键碰撞**: 8 位 hex 主键约 40 亿种可能，生产环境有碰撞风险
- **LLM 双配置源**: settings.py（.env 文件）和 llm/config.py（YAML 文件）两套配置，修改时需注意一致性
- **手动数据库迁移**: init_db() 中手动 ALTER TABLE，无迁移版本追踪，每次启动都执行所有检查
- **表格 input 检测**: ERP 表格中的 input 元素 placeholder 匹配不可靠，需用结构化检测策略定位
- **多 action 丢失**: agent 单次返回多个 action 时需确保全部处理，否则后续 fill 等操作会丢失
