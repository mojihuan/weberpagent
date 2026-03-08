# Phase 1: 环境搭建设计文档

## 概述

本文档描述 AI + Playwright UI 自动化测试 POC 项目的 Phase 1 环境搭建设计。

## 目标

完成开发环境搭建，为后续 Phase 2-5 的开发工作奠定基础。

## 技术选型

| 项目 | 选择 | 理由 |
|------|------|------|
| 包管理器 | uv | 现代、快速、兼容 pip |
| Python 版本 | 3.11+ | Browser-Use 和异步特性需要 |
| LLM 提供商 | 通义千问 (Qwen) | 用户已有 API Key |
| 浏览器自动化 | Playwright | Browser-Use 底层依赖 |

## 目录结构

```
jianzhi_ui_test/
├── pyproject.toml              # uv 项目配置
├── .python-version             # Python 版本锁定
├── .env.example                # 环境变量模板
├── .env                        # 实际配置（gitignore）
├── .gitignore
│
├── docs/
│   └── plans/                  # 设计文档目录
│
├── backend/
│   ├── __init__.py
│   ├── agent/                  # Browser-Use 改造
│   │   └── __init__.py
│   ├── llm/                    # 模型适配
│   │   └── __init__.py
│   ├── utils/                  # 工具函数
│   │   └── __init__.py
│   ├── config/                 # 配置
│   │   └── __init__.py
│   └── tests/                  # 测试用例
│       └── __init__.py
│
└── outputs/                    # 输出目录（gitignore）
    ├── screenshots/
    ├── traces/
    └── reports/
```

## 依赖管理

### pyproject.toml

```toml
[project]
name = "jianzhi-ui-test"
version = "0.1.0"
description = "AI + Playwright UI 自动化测试 POC"
requires-python = ">=3.11"
dependencies = [
    "browser-use>=0.1.0",
    "langchain-core>=0.3.0",
    "dashscope>=1.20.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "ruff>=0.4.0",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["backend/tests"]

[tool.ruff]
line-length = 100
target-version = "py311"
```

### 核心依赖说明

| 依赖 | 用途 |
|------|------|
| browser-use | AI 浏览器自动化框架 |
| langchain-core | Browser-Use 的 LLM 抽象层 |
| dashscope | 阿里云通义千问官方 SDK |
| python-dotenv | 环境变量管理 |
| pyyaml | YAML 配置文件解析 |
| pydantic | 数据验证 |

## 环境变量配置

### .env.example

```bash
# 通义千问 API
DASHSCOPE_API_KEY=your_dashscope_api_key_here

# 可选：智谱 GLM（备选）
ZHIPU_API_KEY=your_zhipu_api_key_here

# 可选：DeepSeek（备选）
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# 模型选择（默认 qwen）
LLM_PROVIDER=qwen

# 测试目标配置
TEST_BASE_URL=https://your-test-system.com
```

### .gitignore 新增

```gitignore
# 环境变量
.env

# Python
__pycache__/
*.py[cod]
.venv/

# 输出目录
outputs/

# IDE
.vscode/
.idea/
```

## 验证脚本

### verify_playwright.py

验证 Playwright 能正常启动浏览器并访问页面。

### verify_qwen.py

验证通义千问 API 能正常调用。

## 验收标准

| 任务 | 验收标准 |
|------|----------|
| 1.1 初始化项目结构 | 所有目录和 `__init__.py` 文件存在 |
| 1.2 安装依赖 | `uv sync` 成功，无报错 |
| 1.3 配置 API Key | `.env` 文件存在且包含有效 API Key |
| 1.4 验证 Playwright | 验证脚本运行成功，能访问百度首页 |
| 1.4 验证 Qwen | 验证脚本运行成功，API 返回正常响应 |

## 风险

| 风险 | 缓解措施 |
|------|----------|
| Playwright 浏览器未安装 | 提供安装命令 `playwright install chromium` |
| API Key 无效 | 验证脚本会明确报错，提示检查配置 |
| 网络问题 | 使用国内镜像源 |

## 里程碑

Phase 1 完成后达到 **M1: 环境就绪** - Browser-Use + 国内模型 API 调通。
