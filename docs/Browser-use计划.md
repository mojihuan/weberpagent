# Browser-Use Restart 主计划

> **单一真实来源 (SSOT)** - 本文档是 Browser-Use 重新集成项目的总纲
>
> 最后更新：2026-03-12
> 状态：🔄 进行中

---

## 📋 项目概览

### 目标
构建 **AI + Playwright UI 自动化测试平台**，使用 Browser-Use + OpenAI/DeepSeek 实现 ERP 系统自动化测试。

### 核心价值
| 价值点 | 说明 |
|--------|------|
| 🤖 AI 驱动 | 自然语言描述测试任务，AI 自动决策执行 |
| 🔄 实时反馈 | SSE 推送执行进度、截图、AI 推理过程 |
| ✅ 双重断言 | AI 判断 + 代码断言双重验证 |
| 🎯 优先场景 | 登录/认证流程优先 |

### 技术栈
| 层级 | 技术 |
|------|------|
| 前端 | React 18 + TypeScript + Vite 5 + Tailwind CSS + SSE |
| 后端 | Python + FastAPI + browser-use + langchain-openai |
| LLM | DeepSeek（优先）/ GPT-4o（备选） |
| 浏览器 | Playwright + Chromium |
| 存储 | SQLite + JSON 文件 |

---

## 🗺️ 阶段总览

### 整体时间线

```
Phase 0 ──▶ Phase 1 ──▶ Phase 2 ──▶ Phase 3 ──▶ Phase 4 ──▶ Phase 5
 环境准备     代码归档     依赖更新    核心服务     API开发     前后端联调
   │            │            │           │           │           │
   ▼            ▼            ▼           ▼           ▼           ▼
  0.5h         2h          0.5h        2h          2h          1h
                                                        │
                                                        ▼
                                              Phase 6 ──▶ Phase 7
                                               登录验证     文档收尾
                                                  │           │
                                                  ▼           ▼
                                                 1h         0.5h

总计：约 9.5 小时
```

### 阶段状态表

| Phase | 名称 | 状态 | 预计 | 关键交付物 | 阻塞项 |
|-------|------|:----:|:----:|-------------|--------|
| 0 | 环境准备 | ⬜ | 0.5h | `.env` 配置、依赖安装 | - |
| 1 | 代码归档 | ⬜ | 2h | `_archived/` 目录结构 | - |
| 2 | 依赖更新 | ⬜ | 0.5h | `pyproject.toml` 更新 | Phase 1 |
| 3 | 核心服务 | ⬜ | 2h | LLM工厂、Agent服务、断言服务 | Phase 2 |
| 4 | API 开发 | ⬜ | 2h | FastAPI 路由、SSE 推送 | Phase 3 |
| 5 | 前后端联调 | ⬜ | 1h | CORS、Mock 移除 | Phase 4 |
| 6 | 登录验证 | ⬜ | 1h | ERP 登录测试通过 | Phase 5 |
| 7 | 文档收尾 | ⬜ | 0.5h | CLAUDE.md、主计划更新 | Phase 6 |

### 状态图例
- ⬜ 未开始
- 🔄 进行中
- ✅ 已完成
- ⚠️ 有风险
- ❌ 已阻塞

---

## 🎯 关键决策

### 决策记录

| # | 决策点 | 决策内容 | 理由 | 日期 |
|---|--------|----------|------|------|
| D1 | LLM 选择 | DeepSeek 优先，GPT-4o 备选 | 成本低，中文能力强 | 2026-03-12 |
| D2 | 架构模式 | browser-use 原生 API，最小封装 | 减少维护负担，官方支持 | 2026-03-12 |
| D3 | 历史代码 | 归档到 `_archived/`，不删除 | 保留参考价值 | 2026-03-12 |
| D4 | 实时推送 | SSE 而非 WebSocket | 简单、单向、足够 | 2026-03-12 |
| D5 | 断言方式 | AI 断言 + 代码断言双重验证 | 互补，更可靠 | 2026-03-12 |
| D6 | 存储方案 | SQLite + JSON 文件 | 轻量、无需额外服务 | 2026-03-12 |

### 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    前端 (React + Vite)                       │
│   Dashboard / Tasks / RunMonitor / Reports                  │
│   ────────────────────────────────────────────────          │
│   EventSource ← SSE 实时推送                                │
└─────────────────────┬───────────────────────────────────────┘
                      │ REST + SSE
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI 后端                              │
├─────────────────────────────────────────────────────────────┤
│  路由层                                                      │
│  ├── /api/tasks      任务 CRUD                              │
│  ├── /api/runs       执行管理 + SSE                         │
│  ├── /api/reports    报告查看                               │
│  └── /api/config     配置管理                               │
├─────────────────────────────────────────────────────────────┤
│  核心层                                                      │
│  ├── AgentService    browser-use 封装                       │
│  ├── LLMFactory      DeepSeek/GPT-4o 工厂                   │
│  └── AssertionService 断言服务                              │
├─────────────────────────────────────────────────────────────┤
│  数据层                                                      │
│  ├── TaskStore       任务存储 (JSON)                        │
│  ├── RunStore        执行记录 (JSON)                        │
│  └── screenshots/    截图存储                               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              browser-use Agent (原生)                        │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐             │
│   │  感知    │───▶│  决策    │───▶│  执行    │             │
│   │ Browser  │    │ LLM      │    │Playwright│             │
│   └──────────┘    └──────────┘    └──────────┘             │
└─────────────────────────────────────────────────────────────┘
```

### 目录结构

```
backend/
├── api/
│   ├── main.py              # FastAPI 入口
│   ├── routes/              # 路由模块
│   │   ├── tasks.py
│   │   └── runs.py
│   └── schemas/             # Pydantic 模型
│       └── index.py
├── core/
│   ├── agent_service.py     # browser-use 封装
│   ├── llm_factory.py       # LLM 工厂
│   └── assertion_service.py # 断言服务
├── storage/
│   ├── task_store.py        # 任务存储
│   └── run_store.py         # 执行记录存储
├── _archived/               # 归档代码
│   ├── agent_simple/
│   ├── llm/
│   └── proxy/
└── tests/
    └── test_login.py        # 登录测试
```

---

## 📦 Phase 0: 环境准备

### 目标
确保开发环境就绪，依赖正确安装。

### 任务清单
| # | 任务 | 状态 | 命令/文件 |
|---|------|:----:|-----------|
| 0.1 | 安装 Python 依赖 | ⬜ | `uv sync` |
| 0.2 | 安装 Playwright 浏览器 | ⬜ | `playwright install chromium` |
| 0.3 | 配置环境变量 | ⬜ | `.env` |
| 0.4 | 验证 LLM 连接 | ⬜ | `uv run python -c "from langchain_openai import ChatOpenAI; ..."` |

### 验收标准
- [ ] `uv sync` 无错误
- [ ] `playwright install chromium` 成功
- [ ] `.env` 包含 `DEEPSEEK_API_KEY` 或 `OPENAI_API_KEY`
- [ ] LLM 连接测试返回有效响应

### 预计时间
0.5 小时

---

## 📦 Phase 1: 代码归档

### 目标
将历史代码归档到 `_archived/` 目录，保持代码库整洁。

### 任务清单
| # | 任务 | 状态 | 文件/目录 |
|---|------|:----:|-----------|
| 1.1 | 创建归档目录结构 | ⬜ | `backend/_archived/{agent_simple,llm,proxy,tests}/` |
| 1.2 | 归档 SimpleAgent | ⬜ | `backend/agent_simple/*` → `_archived/agent_simple/` |
| 1.3 | 归档 LLM 适配器 | ⬜ | `qwen.py, deepseek.py, azure_openai.py` → `_archived/llm/` |
| 1.4 | 归档代理服务 | ⬜ | `backend/proxy/*` → `_archived/proxy/` |
| 1.5 | 归档旧测试脚本 | ⬜ | `run_validation*.py` → `_archived/tests/` |
| 1.6 | 添加归档说明 | ⬜ | 各目录 `__init__.py` 添加注释 |

### 验收标准
- [ ] `backend/_archived/` 包含 4 个子目录
- [ ] `backend/` 根目录无 `agent_simple/`、`proxy/`
- [ ] 归档文件顶部有 `⚠️ 已归档` 注释
- [ ] `git status` 显示移动操作

### 依赖
无

### 预计时间
2 小时

---

## 📦 Phase 2: 依赖更新

### 目标
更新 `pyproject.toml`，确保 browser-use 和 langchain-openai 正确配置。

### 任务清单
| # | 任务 | 状态 | 文件/命令 |
|---|------|:----:|-----------|
| 2.1 | 更新依赖清单 | ⬜ | `pyproject.toml` |
| 2.2 | 同步依赖 | ⬜ | `uv sync` |
| 2.3 | 验证导入 | ⬜ | `from browser_use import Agent; from langchain_openai import ChatOpenAI` |

### 关键依赖
```toml
dependencies = [
    "browser-use>=0.12.0",
    "langchain-openai>=0.3.0",
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "playwright>=1.40.0",
    "sqlalchemy>=2.0.0",
    "aiosqlite>=0.20.0",
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "pyyaml>=6.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
]
```

### 验收标准
- [ ] `uv sync` 无错误
- [ ] 导入测试返回 "OK"

### 依赖
Phase 1 完成

### 预计时间
0.5 小时

---

## 📦 Phase 3: 核心服务开发

### 目标
构建 LLM 工厂、Agent 服务和断言服务。

### 任务清单
| # | 任务 | 状态 | 文件 |
|---|------|:----:|------|
| 3.1 | 创建 LLM 工厂 | ⬜ | `backend/core/llm_factory.py` |
| 3.2 | 创建 Agent 服务 | ⬜ | `backend/core/agent_service.py` |
| 3.3 | 创建断言服务 | ⬜ | `backend/core/assertion_service.py` |
| 3.4 | 编写单元测试 | ⬜ | `backend/tests/test_core_services.py` |

### 关键接口

```python
# LLM 工厂
class LLMFactory:
    @staticmethod
    def create(config: LLMConfig) -> ChatOpenAI: ...
    @staticmethod
    def create_with_fallback(primary, fallback) -> ChatOpenAI: ...

# Agent 服务
class AgentService:
    async def run_with_streaming(task, on_step, max_steps) -> AgentHistoryList: ...
    async def run_simple(task, max_steps) -> AgentHistoryList: ...

# 断言服务
class AssertionService:
    def check_url_contains(history, expected) -> bool: ...
    def check_text_exists(history, expected) -> bool: ...
    def run_all_assertions(history, assertions) -> dict: ...
```

### 验收标准
- [ ] LLM 工厂支持 DeepSeek 和 OpenAI 切换
- [ ] Agent 服务能执行简单任务（如打开网页）
- [ ] 断言服务能检测 URL 和文本
- [ ] 单元测试覆盖率 ≥ 80%

### 依赖
Phase 2 完成

### 预计时间
2 小时

---

## 📦 Phase 4: API 路由开发

### 目标
构建 FastAPI 路由层，实现任务管理和 SSE 实时推送。

### 任务清单
| # | 任务 | 状态 | 文件 |
|---|------|:----:|------|
| 4.1 | 创建数据模型 | ⬜ | `backend/api/schemas/index.py` |
| 4.2 | 创建任务存储 | ⬜ | `backend/storage/task_store.py` |
| 4.3 | 创建执行存储 | ⬜ | `backend/storage/run_store.py` |
| 4.4 | 创建任务路由 | ⬜ | `backend/api/routes/tasks.py` |
| 4.5 | 创建执行路由（含 SSE） | ⬜ | `backend/api/routes/runs.py` |
| 4.6 | 创建 FastAPI 入口 | ⬜ | `backend/api/main.py` |

### API 端点

```
任务管理
  GET    /api/tasks           # 列表
  POST   /api/tasks           # 创建
  GET    /api/tasks/{id}      # 详情
  PUT    /api/tasks/{id}      # 更新
  DELETE /api/tasks/{id}      # 删除

执行管理
  POST   /api/runs            # 创建执行记录
  GET    /api/runs            # 执行列表
  GET    /api/runs/{id}       # 执行详情
  POST   /api/runs/{id}/execute  # 执行并返回 SSE 流
  POST   /api/runs/{id}/stop  # 停止执行
```

### 验收标准
- [ ] `uv run uvicorn backend.api.main:app` 启动成功
- [ ] `/docs` 显示 Swagger UI
- [ ] `/api/tasks` CRUD 操作正常
- [ ] `/api/runs/{id}/execute` 返回 SSE 流

### 依赖
Phase 3 完成

### 预计时间
2 小时

---

## 📦 Phase 5: 前后端联调

### 目标
前端移除 Mock 数据，对接真实后端 API。

### 任务清单
| # | 任务 | 状态 | 文件 |
|---|------|:----:|------|
| 5.1 | 配置 CORS | ⬜ | `backend/api/main.py` |
| 5.2 | 创建 API 客户端 | ⬜ | `frontend/src/api/client.ts` |
| 5.3 | 移除 Mock 数据 | ⬜ | `frontend/src/api/mock*.ts` |
| 5.4 | 对接任务 API | ⬜ | `frontend/src/pages/Tasks/` |
| 5.5 | 对接执行 API + SSE | ⬜ | `frontend/src/pages/RunMonitor/` |

### 验收标准
- [ ] 前端任务列表显示真实数据
- [ ] 创建任务后后端返回 ID
- [ ] 执行任务时 SSE 实时推送步骤
- [ ] 截图正确显示

### 依赖
Phase 4 完成

### 预计时间
1 小时

---

## 📦 Phase 6: 登录验证

### 目标
完成 ERP 登录场景的端到端测试。

### 任务清单
| # | 任务 | 状态 | 文件/操作 |
|---|------|:----:|-----------|
| 6.1 | 配置测试目标 | ⬜ | `.env` 中 ERP_BASE_URL/USERNAME/PASSWORD |
| 6.2 | 创建登录任务 | ⬜ | POST `/api/tasks` |
| 6.3 | 执行登录测试 | ⬜ | POST `/api/runs/{id}/execute` |
| 6.4 | 验证断言结果 | ⬜ | 检查 ai_assertion + code_assertion |
| 6.5 | 保存截图 | ⬜ | `screenshots/` 目录 |

### 测试任务描述

```
登录 ERP 系统：
1. 打开登录页面
2. 如果显示手机验证码登录，点击切换到"密码登录"
3. 输入用户名和密码
4. 点击登录按钮
5. 确认登录成功（页面跳转或显示欢迎信息）
```

### 断言配置

```json
[
  {"name": "URL跳转正确", "type": "url_contains", "expected": "/dashboard"},
  {"name": "无执行错误", "type": "no_errors", "expected": true}
]
```

### 验收标准
- [ ] 登录任务执行成功
- [ ] SSE 推送显示每一步骤
- [ ] 截图保存到 `screenshots/`
- [ ] 双重断言全部通过

### 依赖
Phase 5 完成

### 预计时间
1 小时

---

## 📦 Phase 7: 文档收尾

### 目标
更新项目文档，确保后续开发有清晰的参考。

### 任务清单
| # | 任务 | 状态 | 文件 |
|---|------|:----:|------|
| 7.1 | 更新 CLAUDE.md | ⬜ | `CLAUDE.md` |
| 7.2 | 更新主计划状态 | ⬜ | 本文档（标记完成状态） |
| 7.3 | 创建 Git Tag | ⬜ | `git tag v0.1.0-browser-use-restart` |
| 7.4 | 归档旧计划文档 | ⬜ | `docs/_archived/phase-1-9/` |

### 验收标准
- [ ] CLAUDE.md 反映最新架构
- [ ] 所有 Phase 标记 ✅
- [ ] Git Tag 创建成功

### 依赖
Phase 6 完成

### 预计时间
0.5 小时

---

## 🚨 风险清单

| # | 风险 | 等级 | 缓解措施 | 状态 |
|---|------|:----:|----------|:----:|
| R1 | DeepSeek API 不稳定 | 🔴 高 | 自动切换到 GPT-4o 备选 | ⬜ |
| R2 | SSE 连接中断 | 🟡 中 | 前端实现重连机制 | ⬜ |
| R3 | browser-use 版本更新导致 API 变化 | 🟡 中 | 锁定版本号，定期检查更新日志 | ⬜ |
| R4 | ERP 登录页面变化 | 🟡 中 | 任务描述保持通用，避免硬编码选择器 | ⬜ |
| R5 | 截图存储空间不足 | 🟢 低 | 定期清理，限制保留天数 | ⬜ |
| R6 | LLM Token 消耗过大 | 🟡 中 | 设置 max_steps 限制，监控用量 | ⬜ |

### 等级图例
- 🔴 高：可能阻塞项目
- 🟡 中：需要关注
- 🟢 低：可接受

---

## 📝 变更日志

| 日期 | 变更内容 | 影响范围 |
|------|----------|----------|
| 2026-03-12 | 创建主计划文档 | 初始化 |

---

## 🔗 相关文档

### 设计文档
| 文档 | 路径 | 说明 |
|------|------|------|
| 架构设计 | `docs/plans/2026-03-12-browser-use-restart-design.md` | 详细技术架构 |
| 实施计划 | `docs/plans/2026-03-12-browser-use-restart-impl.md` | 代码归档步骤 |
| 后端实现 | `docs/plans/2026-03-12-browser-use-backend-impl.md` | FastAPI 开发详情 |
| 多 LLM 配置 | `docs/plans/2026-03-12-multi-llm-config.md` | LLM 切换方案 |

### 归档文档
| 文档 | 路径 | 说明 |
|------|------|------|
| Phase 1-9 文档 | `docs/_archived/phase-1-9/` | 历史技术文档 |

### 外部参考
- [browser-use 官方文档](https://github.com/browser-use/browser-use)
- [langchain-openai 文档](https://python.langchain.com/docs/integrations/chat/openai/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)

---

## 📌 使用说明

### 如何更新本文档

1. **更新任务状态**：将 `⬜` 改为 `🔄`（进行中）或 `✅`（已完成）
2. **记录变更**：在变更日志中添加条目
3. **更新风险**：发现新风险或风险状态变化时更新

### 状态标记

| 标记 | 含义 |
|:----:|------|
| ⬜ | 未开始 |
| 🔄 | 进行中 |
| ✅ | 已完成 |
| ⚠️ | 有风险 |
| ❌ | 已阻塞 |

---

## ✅ 项目验收

### 最终验收清单

| # | 验收项 | 状态 | 备注 |
|---|--------|:----:|------|
| V1 | 后端服务启动正常 | ⬜ | `uvicorn backend.api.main:app` |
| V2 | 前端访问正常 | ⬜ | `http://localhost:11001` |
| V3 | 任务 CRUD 功能正常 | ⬜ | 创建、查看、编辑、删除 |
| V4 | SSE 实时推送正常 | ⬜ | 步骤、截图实时显示 |
| V5 | ERP 登录测试通过 | ⬜ | 端到端流程 |
| V6 | 双重断言通过 | ⬜ | AI + 代码断言 |
| V7 | 文档更新完成 | ⬜ | CLAUDE.md、主计划 |

### 交付物清单

- [ ] 可运行的后端服务
- [ ] 可运行的前端应用
- [ ] 完整的 API 文档（/docs）
- [ ] 更新的项目文档
- [ ] Git Tag（v0.1.0-browser-use-restart）
