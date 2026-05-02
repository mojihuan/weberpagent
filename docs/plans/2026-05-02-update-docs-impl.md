# 文档更新实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 全面重写 CLAUDE.md 和 README.md，修正过时信息，精简结构，补充缺失内容

**Architecture:** 纯文档更新任务，无代码变更。基于 codebase map 最新分析结果，按设计文档的结构逐段编写

**Tech Stack:** Markdown, 信息来源为 .planning/codebase/ 下的 7 个分析文档

---

### Task 1: 重写 CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

**Step 1: 编写 CLAUDE.md 内容**

用 Write 工具覆盖 CLAUDE.md，内容结构：
1. 项目概述（一句话描述 + 核心流程图 + 技术栈速览表）
2. 架构关键决策（browser-use CDP 限制、多阶段管道、SSE、外部集成）
3. 目录结构约定（backend/ 各子目录职责、frontend/ 各子目录职责）
4. 代码规范（Python ruff/TS strict/API 响应格式/异步优先）
5. 开发命令（启动/测试/lint/部署）
6. 已知陷阱（exec() 安全、monkey-patch、UUID 碰撞、LLM 双配置）

关键数据来源：
- 技术栈版本：`.planning/codebase/STACK.md`
- 目录结构：`.planning/codebase/STRUCTURE.md`
- 编码规范：`.planning/codebase/CONVENTIONS.md`
- 已知陷阱：`.planning/codebase/CONCERNS.md`
- 架构决策：`.planning/codebase/ARCHITECTURE.md`

注意事项：
- 全中文（技术术语保留英文）
- 目标 ~120-150 行
- 不要重复内容（当前文件重复了两遍）
- 不含通用 LLM 行为规范（由 ~/.claude/rules/ 覆盖）

**Step 2: 验证 CLAUDE.md**

Run: `wc -l CLAUDE.md`
Expected: 120-150 行

**Step 3: 提交**

```bash
git add CLAUDE.md
git commit -m "docs: rewrite CLAUDE.md with project-specific context"
```

---

### Task 2: 重写 README.md — 项目描述与架构

**Files:**
- Modify: `README.md`

**Step 1: 编写 README.md 前 3 个段落**

覆盖 README.md，写入：
1. **项目标题与描述**（一句话 + 核心流程："自然语言 → AI 决策 → Playwright 执行"）
2. **核心功能**（6 条，使用 emoji 列表，与当前类似但精简描述）
3. **技术架构**（简化 ASCII 架构图 + 修正后的技术栈表格）

技术栈表格修正清单（来自 STACK.md）：
| 层级 | 技术 |
|------|------|
| 前端 | React 19.2, TypeScript 5.9, Vite 7.3, Tailwind CSS 4.2 |
| 后端 | Python 3.11+, FastAPI, Pydantic, SQLAlchemy |
| AI 引擎 | Browser-Use 0.12+, Qwen 3.5 Plus (DashScope) |
| 浏览器 | Playwright (Chromium) |
| 通信 | REST API + SSE |
| 存储 | SQLite (aiosqlite) |
| 包管理 | uv (Python), npm (Node.js) |

**Step 2: 验证**

Run: `wc -l README.md`
Expected: ~50 行（前 3 段）

---

### Task 3: 追加快速开始段落

**Files:**
- Modify: `README.md`

**Step 1: 追加快速开始段落**

使用 Edit 工具在 README.md 末尾追加：
4. **快速开始**
   - 环境要求：Python 3.11+, Node.js 22+, uv
   - 安装步骤（统一为 uv 流程，移除 Tabs 标签）：
     ```bash
     git clone <repo>
     cd weberpagent
     cp .env.example .env
     uv sync
     uv run playwright install chromium
     cd frontend && npm install
     ```
   - 启动服务（端口修正为 11002/11001）
   - Windows 特殊说明（run_server.py）
   - 验证安装

注意事项：
- 不使用 `<Tabs>` 标签（GitHub 不支持）
- 统一用 uv 流程，pip/conda 作为备选简述
- 端口：后端 11002，前端 11001

**Step 2: 验证**

Run: `wc -l README.md`
Expected: ~100 行

---

### Task 4: 追加使用指南段落

**Files:**
- Modify: `README.md`

**Step 1: 追加使用指南段落**

使用 Edit 追加：
5. **使用指南**
   - 创建测试任务（一个完整示例，带前置条件 + 变量引用）
   - Excel 导入（新增段落：模板下载 → 上传 → 预览 → 确认导入）
   - 断言类型（保留表格：url_contains / text_exists / no_errors）
   - 执行与监控（简要说明 SSE 实时监控）
   - 前置条件最佳实践（精简为 2 个要点：错误处理 + 环境变量）

注意事项：
- 前置条件代码示例精简为一个（当前有 4 个重复示例）
- 新增 Excel 导入段落（参考 backend/utils/excel_parser.py 和前端 ImportModal/）
- 移除 webseleniumerp 配置段落（过于项目特定，放到开发指南即可）

**Step 2: 验证**

Run: `wc -l README.md`
Expected: ~200 行

---

### Task 5: 追加配置参考与开发指南

**Files:**
- Modify: `README.md`

**Step 1: 追加配置参考段落**

使用 Edit 追加：
6. **配置参考**
   - 环境变量表格（合并当前分散的配置段落）
   - 关键变量：DASHSCOPE_API_KEY, OPENAI_API_KEY, LLM_MODEL, ERP_BASE_URL 等
   - LLM 配置：只保留 DashScope 和通用 OpenAI 兼容模式，移除实验性 DeepSeek
   - 浏览器配置：BROWSER_MODE, BROWSER_HEADLESS
   - 注意：移除 Azure OpenAI（未实际使用）

**Step 2: 追加开发指南段落**

7. **开发指南**
   - 项目结构树（更新为实际目录，基于 STRUCTURE.md）
   - 后端开发命令（uvicorn, pytest, ruff）
   - 前端开发命令（npm run dev, npm run build, npm run lint）
   - API 文档（Swagger/ReDoc 地址）
   - 添加新端点步骤（精简为 3 步）

注意事项：
- 项目结构树基于 STRUCTURE.md 的 Directory Layout，精简到 2 级深度
- 移除当前分散的 Nginx 配置示例段落（放到部署段落）

**Step 3: 验证**

Run: `wc -l README.md`
Expected: ~330 行

---

### Task 6: 追加部署与 FAQ 段落，完成 README.md

**Files:**
- Modify: `README.md`

**Step 1: 追加部署段落**

使用 Edit 追加：
8. **部署说明**
   - 手动部署（uv sync --no-dev + gunicorn）
   - deploy.sh 脚本（支持 --backend-only, --frontend-only, --skip-build）
   - Nginx 配置（简化为一个精简的 server block）
   - SSE 代理注意事项（proxy_buffering off）
   - 环境变量清单表格（~8 个变量）
   - 移除 Docker 部署（项目未实际使用 Docker）

**Step 2: 追加 FAQ 段落**

9. **FAQ**（精简到 5 个高频问题）
   - Playwright 安装失败（网络问题 → npmmirror）
   - Windows NotImplementedError（使用 run_server.py）
   - LLM 调用返回错误（API Key/余额/网络）
   - SSE 连接断开（Nginx 超时配置）
   - AI 步骤太多/太少（调整 max_steps）

**Step 3: 追加 License**

10. **License** — MIT License

**Step 4: 最终验证**

Run: `wc -l README.md`
Expected: ~400 行（目标范围 350-450）

验证清单：
- [ ] 所有版本号正确（React 19, Vite 7, Node 22）
- [ ] 端口号正确（11002 后端，11001 前端）
- [ ] 无 `<Tabs>` / HTML 标签
- [ ] 无 Docker 段落
- [ ] 无实验性 DeepSeek 配置
- [ ] 包含 Excel 导入说明
- [ ] 全中文

**Step 5: 提交**

```bash
git add README.md
git commit -m "docs: rewrite README.md with corrected info and streamlined structure"
```

---

### Task 7: 最终审查与提交

**Files:**
- Verify: `CLAUDE.md`
- Verify: `README.md`

**Step 1: 检查 CLAUDE.md 质量**

- 无重复段落
- 包含项目概述、架构决策、目录约定、代码规范、开发命令、已知陷阱
- 行数 120-150

**Step 2: 检查 README.md 质量**

- 行数 350-450
- 所有版本号/端口号正确
- 无 HTML/XML 标签
- 全中文
- 包含 Excel 导入说明

**Step 3: 推送提交（如用户确认）**

```bash
git log --oneline -3
# 确认两个 commit 存在
```

---
