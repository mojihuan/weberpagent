# CLAUDE.md

## 项目概述

aiDriveUITest - AI 驱动的 UI 自动化测试平台。

**目标用户**: QA 测试人员
**核心价值**: 自然语言写用例 → AI 自动执行 → 自动生成报告

## 技术架构

详见 README.md 第 35-70 行（架构图 + 技术栈）。

## 模块职责

详见 README.md 第 140-175 行（项目结构）。

## LLM 配置

**推荐**: 阿里云 DashScope + Qwen 3.5 Plus

```bash
DASHSCOPE_API_KEY=sk-xxx
ERP_BASE_URL=https://your-erp-url.com
ERP_USERNAME=xxx
ERP_PASSWORD=xxx
```

## Key Commands

```bash
# 后端
uv sync && uv run playwright install chromium
uv run uvicorn backend.api.main:app --reload --port 8080
uv run pytest backend/tests/ -v

# 前端
cd frontend && npm install && npm run dev
cd frontend && npm run build
```

## Documentation

- `docs/plans/` - 设计与实施计划
- `docs/_archived/` - 历史文档归档
