# aiDriveUITest

> AI 驱动的 UI 自动化测试平台，让 QA 用自然语言编写测试用例

基于 Browser-Use + 阿里云 Qwen 3.5 Plus 构建，实现「自然语言描述 → AI 决策 → Playwright 执行」的自动化测试流程。

## ✨ 核心功能

- 🗣️ **自然语言用例** - 用中文描述测试步骤，AI 自动理解并执行
- 📋 **前置条件支持** - 执行 Python 代码准备测试环境，支持变量传递
- 📊 **实时执行监控** - SSE 推送执行进度，可视化每一步操作
- 📈 **自动生成报告** - 完整的测试报告，包含截图、断言结果、耗时统计
- 🎯 **智能断言** - 支持 URL 检查、文本存在、无错误等多种断言类型
- 🔄 **任务管理** - 创建、编辑、复制、批量管理测试任务

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        前端 (React + Vite)                        │
│   Dashboard │ 任务管理 │ 执行监控 │ 报告查看                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │ SSE (实时推送)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     后端 (FastAPI + Python)                       │
├─────────────────────────────────────────────────────────────────┤
│  API Routes     │  Agent Service  │  Assertion Service          │
├─────────────────────────────────────────────────────────────────┤
│                     Browser-Use Agent                             │
│         ┌──────────┐    ┌──────────┐    ┌──────────┐           │
│         │  感知    │───▶│  决策    │───▶│  执行    │           │
│         │ Browser  │    │ Qwen 3.5 │    │Playwright│           │
│         └──────────┘    └──────────┘    └──────────┘           │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     目标系统 (ERP/Web)                            │
└─────────────────────────────────────────────────────────────────┘
```

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React 18, TypeScript, Vite 5, Tailwind CSS, React Router 6 |
| 后端 | Python 3.11, FastAPI, Pydantic, SQLAlchemy |
| AI 引擎 | Browser-Use 0.12+, 阿里云 Qwen 3.5 Plus |
| 浏览器 | Playwright (Chromium) |
| 通信 | REST API + SSE (Server-Sent Events) |
| 存储 | SQLite (aiosqlite) |

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- Playwright Chromium 浏览器

### 安装步骤

**1. 克隆项目**
```bash
git clone https://github.com/your-org/aiDriveUITest.git
cd aiDriveUITest
```

**2. 配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，填入以下配置：
```

```env
# LLM 配置 (必填)
OPENAI_API_KEY=sk-xxx

# 目标系统配置 (必填)
ERP_BASE_URL=https://your-erp-url.com
ERP_USERNAME=your_username
ERP_PASSWORD=your_password
```

**3. 创建后端环境（三选一）**

<Tabs>
<Tab value="uv">

```bash
# 方式一：uv（推荐，自动创建 .venv 隔离环境）
uv sync                          # 创建虚拟环境并安装依赖
uv run playwright install chromium
```

> 💡 `uv sync` 会在项目目录创建 `.venv`，不会污染系统 Python 环境

</Tab>
<Tab value="pip">

```bash
# 方式二：pip + venv（手动管理虚拟环境）
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

</Tab>
<Tab value="conda">

```bash
# 方式三：Conda（独立环境管理）
conda create -n aidrive-ui-test python=3.11
conda activate aidrive-ui-test
pip install -r requirements.txt
playwright install chromium
```

</Tab>
</Tabs>

**4. 安装前端依赖**
```bash
cd frontend
npm install
```

**5. 启动服务**

<Tabs>
<Tab value="macos-linux">

```bash
# macOS / Linux
uv run uvicorn backend.api.main:app --reload --port 8080
```

</Tab>
<Tab value="windows">

```bash
# Windows（必须使用专用启动脚本）
uv run python backend/run_server.py
```

> ⚠️ **Windows 注意事项**：
> - 必须使用 `run_server.py` 启动，不能直接用 `uvicorn` 命令
> - 原因：browser-use 使用 asyncio 子进程启动浏览器，Windows 需要特殊的事件循环配置
> - 启动脚本会自动设置 `ProactorEventLoop`，确保子进程正常工作

</Tab>
</Tabs>

```bash
# 终端 2: 启动前端（所有系统）
cd frontend && npm run dev
```

**6. 访问应用**

打开浏览器访问 http://localhost:5173

### 验证安装

```bash
# 运行健康检查
curl http://localhost:8080/health
# 预期输出: {"status": "healthy"}

# 运行测试
uv run pytest backend/tests/ -v  # uv 方式
pytest backend/tests/ -v         # pip/conda 方式
```

## 📖 使用指南

### 创建测试任务

1. 点击左侧导航「任务管理」
2. 点击「新建任务」按钮
3. 填写任务信息：
   - **任务名称**：如「ERP 登录测试」
   - **任务描述**：用自然语言描述测试步骤
   - **前置条件**（可选）：执行 Python 代码准备环境
   - **断言配置**（可选）：添加验证条件

**示例任务描述**：
```
登录 ERP 系统：
1. 打开 https://erptest.example.com
2. 点击「密码登录」切换登录方式
3. 输入用户名 admin 和密码
4. 点击登录按钮
5. 确认跳转到首页
```

**带前置条件的示例**：

前置条件：
```python
import requests
resp = requests.post('https://erptest.example.com/api/login', json={
    'username': 'admin',
    'password': 'password123'
})
context['token'] = resp.json()['token']
context['order_no'] = 'ORD-2024-001'
```

任务描述：
```
验证订单详情页面：
1. 使用登录态访问订单页面
2. 搜索订单号 {{order_no}}
3. 确认订单状态为「已发货」
```

### 执行与监控

1. 在任务列表找到目标任务，点击「执行」
2. 进入实时监控页面：
   - **步骤时间线**：显示每一步的执行状态
   - **推理日志**：AI 的思考和决策过程
   - **截图面板**：每一步操作的页面截图
3. 执行完成后自动跳转到报告页面

### 查看报告

测试报告包含：
- **执行摘要**：成功/失败状态、总耗时、总步数
- **断言结果**：URL 检查、文本存在等断言的通过情况
- **步骤详情**：每一步的操作类型、AI 推理、截图
- **错误信息**：失败时的详细错误堆栈

### 前置条件（Preconditions）

前置条件允许你在 UI 测试开始前执行 Python 代码，用于：
- 登录获取 token
- 准备测试数据（创建订单、用户等）
- 调用现有项目的 API 封装方法
- 将执行结果传递给后续测试步骤

#### 基本用法

在任务表单的「前置条件」区域输入 Python 代码，使用 `context['变量名']` 存储结果：

```python
# 示例 1: 登录获取 token
import requests
resp = requests.post('https://api.example.com/login', json={
    'username': 'admin',
    'password': 'password123'
})
context['token'] = resp.json()['token']
context['user_id'] = resp.json()['user_id']
```

```python
# 示例 2: 准备测试数据
import time
context['order_no'] = f'TEST-{int(time.time())}'
context['timestamp'] = int(time.time() * 1000)
```

#### 在测试描述中使用变量

前置条件执行后，可以在任务描述中使用 `{{变量名}}` 语法引用变量：

```
登录系统后检查订单：
1. 使用 token {{token}} 访问订单页面
2. 搜索订单号 {{order_no}}
3. 确认订单详情正确
```

#### 复用现有项目的 API 封装

如果已有 ERP 项目的 API 封装代码，可以配置外部模块路径：

```env
# .env 配置
ERP_API_MODULE_PATH=/path/to/your/erp/api/module
```

然后在前置条件中直接导入使用：

```python
# 假设你的模块结构：/path/to/erp_api/auth.py
from erp_api.auth import login, get_user_info

token = login('admin', 'password')
context['token'] = token
context['user'] = get_user_info(token)
```

#### ⚠️ 重要注意事项

| 注意点 | 说明 |
|--------|------|
| **超时控制** | 每个前置条件默认 30 秒超时，超时会终止执行 |
| **执行顺序** | 多个前置条件按顺序执行，任一失败则停止 |
| **变量覆盖** | 后续前置条件可以覆盖之前设置的变量 |
| **安全性** | 代码在受限环境中执行，但请勿执行不可信代码 |
| **异常处理** | 代码中的异常会导致前置条件失败，请妥善处理 |

#### 最佳实践

```python
# ✅ 推荐：添加错误处理
import requests
try:
    resp = requests.post('https://api.example.com/login', json={
        'username': 'admin',
        'password': 'password123'
    }, timeout=10)
    resp.raise_for_status()
    context['token'] = resp.json()['token']
except Exception as e:
    raise Exception(f'登录失败: {e}')

# ❌ 不推荐：没有错误处理
import requests
resp = requests.post('https://api.example.com/login', json={...})
context['token'] = resp.json()['token']  # 可能因网络问题失败
```

```python
# ✅ 推荐：使用环境变量
import os
username = os.getenv('ERP_USERNAME')
password = os.getenv('ERP_PASSWORD')

# ❌ 不推荐：硬编码凭据
username = 'admin'
password = 'password123'
```

### 断言类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `url_contains` | 检查最终 URL 是否包含指定字符串 | `/dashboard` |
| `text_exists` | 检查页面是否包含指定文本 | `欢迎回来` |
| `no_errors` | 检查执行过程是否无错误 | `true` |

## ⚙️ 配置说明

### LLM 配置

支持多种 LLM 后端，通过 `.env` 文件配置：

**OpenAI / 兼容 API（默认）**
```env
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4o              # 可选，默认 gpt-4o
OPENAI_TEMPERATURE=0.1           # 可选，默认 0.1
```

**阿里云 DashScope（推荐国内使用）**
```env
LLM_PROVIDER=qwen
DASHSCOPE_API_KEY=sk-xxx
OPENAI_API_KEY=sk-xxx            # 兼容模式使用
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen3.5-plus
```

**DeepSeek（实验性）**
```env
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-xxx
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat
```

> ⚠️ DeepSeek 目前不支持 JSON 格式输出，可能导致解析错误

**Azure OpenAI（推荐用于 Browser-Use）**
```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=xxx
AZURE_OPENAI_DEPLOYMENT=gpt-4o
```

### 目标系统配置

```env
# 被测试系统的地址和凭据
ERP_BASE_URL=https://erp.example.com
ERP_USERNAME=test_user
ERP_PASSWORD=your_password

# 外部 API 模块路径（用于前置条件复用现有 API 封装）
ERP_API_MODULE_PATH=/path/to/your/erp/api/module
```

> 💡 `ERP_API_MODULE_PATH` 允许在前置条件中导入现有项目的 API 封装模块，避免重复编写认证、数据准备等代码。

### webseleniumerp Configuration

To use external precondition operations from the webseleniumerp project, you need to configure the project path and create a settings file.

#### 1. Configure Environment Variable

Add the path to your webseleniumerp project in `.env`:

```env
WEBSERP_PATH=/path/to/your/webseleniumerp
```

The path should point to the root directory of webseleniumerp containing `base_prerequisites.py`.

#### 2. Create config/settings.py

The webseleniumerp project requires a `config/settings.py` file. This file is in `.gitignore` and must be created manually.

Create `webseleniumerp/config/settings.py` with the following content:

```python
# webseleniumerp/config/settings.py

# Data paths for test data files
DATA_PATHS = {
    'test_data': '/path/to/your/test/data',
    'excel_files': '/path/to/your/excel/files',
    # Add other paths as needed by your precondition operations
}
```

> **Note**: The actual paths depend on your test environment. Update them to match your local setup.

#### 3. Verify Configuration

Start the server to verify your configuration:

```bash
uv run uvicorn backend.api.main:app --reload --port 8080
```

If configuration is invalid, you will see an error message with specific instructions for fixing the issue:

```
[CONFIG ERROR] WEBSERP_PATH directory not found: /invalid/path
  Solution: Verify the path in your .env file
```

#### Available Operations

Once configured, you can use operations from webseleniumerp in your precondition code:

| Operation Code | Description |
|----------------|-------------|
| FA1 | Finance - Create account |
| HC1 | Inventory - Create stock |
| ... | See webseleniumerp documentation for full list |

To use these operations in your precondition:

```python
# In task precondition
self.pre.operations(data=['FA1', 'HC1'])
```

### 浏览器配置

```env
# 浏览器模式
BROWSER_MODE=launch              # launch（自动启动）| cdp（连接已有浏览器）
BROWSER_HEADLESS=true            # 无头模式
BROWSER_START_URL=https://example.com

# Chrome CDP 配置（BROWSER_MODE=cdp 时需要）
CHROME_DEBUG_PORT=9222
CDP_ENDPOINT=http://localhost:9222
```

### 服务器配置

```env
PORT=3001                        # 后端服务端口
LOG_LEVEL=INFO                   # 日志级别
```

### 完整配置示例

参见项目根目录的 `.env.example` 文件。

## 🔧 开发指南

### 项目结构

```
aiDriveUITest/
├── backend/                 # 后端代码
│   ├── api/                 # FastAPI 路由
│   │   ├── routes/          # API 端点
│   │   │   ├── tasks.py     # 任务管理
│   │   │   ├── runs.py      # 执行管理 + SSE
│   │   │   ├── reports.py   # 报告查询
│   │   │   └── dashboard.py # 仪表盘数据
│   │   ├── schemas/         # Pydantic 模型
│   │   └── main.py          # FastAPI 入口
│   ├── core/                # 核心服务
│   │   ├── agent_service.py # Browser-Use 封装
│   │   ├── event_manager.py # SSE 事件管理
│   │   └── assertion_service.py
│   ├── llm/                 # LLM 适配器
│   │   ├── factory.py       # LLM 工厂
│   │   └── openai.py        # OpenAI 兼容实现
│   ├── db/                  # 数据库层
│   │   ├── models.py        # SQLAlchemy 模型
│   │   ├── schemas.py       # Pydantic DTO
│   │   └── repository.py    # 数据访问
│   ├── storage/             # 文件存储
│   └── tests/               # 测试用例
├── frontend/                # 前端代码
│   ├── src/
│   │   ├── pages/           # 页面组件
│   │   ├── components/      # 通用组件
│   │   ├── hooks/           # 自定义 Hooks
│   │   ├── api/             # API 客户端
│   │   └── types/           # TypeScript 类型
│   └── package.json
├── docs/                    # 文档
│   └── plans/               # 设计/实施计划
├── .env.example             # 环境变量模板
├── pyproject.toml           # Python 项目配置
└── CLAUDE.md                # 项目说明（Claude Code）
```

### 后端开发

**运行开发服务器**
```bash
uv run uvicorn backend.api.main:app --reload --port 8080
```

**运行测试**
```bash
uv run pytest backend/tests/ -v
```

**代码规范**
```bash
uv run ruff check backend/
uv run ruff format backend/
```

**API 文档**

启动服务后访问：
- Swagger UI: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

### 前端开发

**运行开发服务器**
```bash
cd frontend && npm run dev
```

**构建生产版本**
```bash
cd frontend && npm run build
```

**代码规范**
```bash
cd frontend && npm run lint
```

### 添加新的 API 端点

1. 在 `backend/api/schemas/` 添加数据模型
2. 在 `backend/api/routes/` 添加路由
3. 在 `backend/api/main.py` 注册路由
4. 编写测试用例

## 🚢 部署说明

### Docker 部署（推荐）

**构建镜像**
```bash
docker build -t aidrive-ui-test:latest .
```

**运行容器**
```bash
docker run -d \
  --name aidrive-ui-test \
  -p 8080:8080 \
  -e OPENAI_API_KEY=sk-xxx \
  -e ERP_BASE_URL=https://erp.example.com \
  -e ERP_USERNAME=test_user \
  -e ERP_PASSWORD=test_password \
  aidrive-ui-test:latest
```

**Docker Compose**
```bash
docker-compose up -d
```

### 手动部署

**后端**
```bash
# 1. 安装依赖
uv sync --no-dev

# 2. 使用 Gunicorn 运行
uv run gunicorn backend.api.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8080
```

**前端**
```bash
# 1. 构建生产版本
cd frontend && npm run build

# 2. 使用 Nginx 托管静态文件
# 将 dist/ 目录部署到 Nginx
```

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /var/www/aidrive-ui-test/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # SSE 支持
    location /api/runs {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_buffering off;
        proxy_cache off;
    }
}
```

### 环境变量清单

生产部署必需的环境变量：

| 变量 | 说明 | 必需 |
|------|------|------|
| `OPENAI_API_KEY` | LLM API 密钥 | ✅ |
| `ERP_BASE_URL` | 目标系统地址 | ✅ |
| `ERP_USERNAME` | 测试账号用户名 | ✅ |
| `ERP_PASSWORD` | 测试账号密码 | ✅ |
| `ERP_API_MODULE_PATH` | 外部 API 模块路径（前置条件） | ❌ |
| `LOG_LEVEL` | 日志级别 | ❌ |
| `DATA_DIR` | 数据存储目录 | ❌ |

## ❓ 常见问题

### 安装问题

**Q: Playwright 安装失败？**
```bash
# 手动安装浏览器
uv run playwright install chromium

# 如果网络问题，使用镜像
uv run playwright install chromium --mirror https://npmmirror.com/mirrors/playwright
```

**Q: 前端依赖安装失败？**
```bash
# 清除缓存重试
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 运行问题

**Q: Windows 上出现 `NotImplementedError` 错误？**

这是 Windows asyncio 子进程兼容性问题。解决方案：
```bash
# 必须使用专用启动脚本
uv run python backend/run_server.py

# 不要使用 uvicorn 命令直接启动
```

**Q: LLM 调用返回错误？**

检查以下几点：
1. API Key 是否正确配置
2. API 余额是否充足
3. 网络是否可以访问 API 端点

**Q: 浏览器启动失败？**
```bash
# 检查 Playwright 是否正确安装
uv run python -c "from playwright.sync_api import sync_playwright; print('OK')"

# 安装系统依赖
uv run playwright install-deps chromium
```

**Q: SSE 连接断开？**

确保 Nginx 配置了正确的超时和缓冲设置：
```nginx
proxy_read_timeout 86400s;
proxy_send_timeout 86400s;
proxy_buffering off;
```

### 使用问题

**Q: AI 执行步骤太多或太少？**

调整任务的 `max_steps` 参数，默认为 10 步。

**Q: 如何调试 AI 决策过程？**

查看后端日志，AI 的推理过程会输出到控制台：
```bash
LOG_LEVEL=DEBUG uv run uvicorn backend.api.main:app --reload
```

**Q: 断言总是失败？**

1. 检查断言类型是否正确
2. 确认目标系统的实际行为
3. 查看截图确认页面状态

### 其他问题

**Q: 如何添加新的断言类型？**

1. 在 `backend/core/assertion_service.py` 添加检查方法
2. 在 `backend/api/schemas/index.py` 的 `Assertion` 类型中添加新类型
3. 更新前端类型定义

**Q: 如何支持其他 LLM？**

参考 `backend/llm/factory.py`，实现新的 LLM 适配器。

## 📄 License

MIT License
