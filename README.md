# aiDriveUITest

> AI 驱动的 UI 自动化测试平台，让 QA 用自然语言编写测试用例

基于 Browser-Use + 阿里云 Qwen 3.5 Plus 构建，实现「自然语言描述 -> AI 决策 -> Playwright 执行」的自动化测试流程。

## 核心功能

- **自然语言用例** - 用中文描述测试步骤，AI 自动理解并执行
- **Excel 导入** - 通过 Excel 模板批量导入测试用例，支持前置条件和断言配置
- **前置条件支持** - 执行 Python 代码准备测试环境，支持变量传递
- **实时执行监控** - SSE 推送执行进度，可视化每一步操作
- **自动生成报告** - 完整的测试报告，包含截图、断言结果、耗时统计
- **智能断言** - 支持 URL 检查、文本存在、无错误等多种断言类型

## 技术架构

```
┌──────────────────────────────────────────────────────────┐
│                    前端 (React 19 + Vite 7)               │
│   Dashboard │ 任务管理 │ 执行监控 │ 报告查看              │
└────────────────────────┬─────────────────────────────────┘
                         │ SSE (实时推送)
                         ▼
┌──────────────────────────────────────────────────────────┐
│                  后端 (FastAPI + Python 3.11+)             │
├──────────────────────────────────────────────────────────┤
│  API Routes     │  Agent Service  │  Code Generator       │
├──────────────────────────────────────────────────────────┤
│                   Browser-Use Agent                       │
│     ┌──────────┐    ┌──────────┐    ┌──────────┐        │
│     │  感知    │───▶│  决策    │───▶│  执行    │        │
│     │ Browser  │    │ Qwen 3.5 │    │Playwright│        │
│     └──────────┘    └──────────┘    └──────────┘        │
└──────────────────────────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│                  目标系统 (ERP/Web)                        │
└──────────────────────────────────────────────────────────┘
```

| 层级 | 技术 |
|------|------|
| 前端 | React 19.2, TypeScript 5.9, Vite 7.3, Tailwind CSS 4.2, TanStack Query 5.90 |
| 后端 | Python 3.11+, FastAPI, Pydantic, SQLAlchemy |
| AI 引擎 | Browser-Use 0.12+, Qwen 3.5 Plus (DashScope) |
| 浏览器自动化 | Playwright (Chromium) |
| 通信 | REST API + SSE (Server-Sent Events) |
| 数据库 | SQLite (aiosqlite, 异步) |
| 包管理 | uv (Python), npm (Node.js) |

## 快速开始

### 环境要求

- Python 3.11+
- Node.js 22+
- uv 包管理器

### 安装步骤

```bash
# 1. 克隆项目
git clone git@github.com:mojihuan/weberpagent.git
cd aiDriveUITest

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入 API Key 和 ERP 配置

# 3. 安装后端依赖
uv sync
uv run playwright install chromium

# 4. 安装前端依赖
cd frontend && npm install
```

### 启动服务

```bash
# 终端 1: 启动后端（端口 11002）
uv run uvicorn backend.api.main:app --reload --port 11002

# 终端 2: 启动前端（端口 11001）
cd frontend && npm run dev
```

Windows 用户必须使用专用启动脚本：

```bash
uv run python backend/run_server.py
```

### 验证安装

```bash
curl http://localhost:11002/health
# 预期: {"status": "healthy"}
```

访问 http://localhost:11001 进入应用。

## 使用指南

### 创建测试任务

1. 点击左侧导航「任务管理」
2. 点击「新建任务」按钮
3. 填写任务信息：
   - **任务名称**：如「ERP 登录测试」
   - **任务描述**：用自然语言描述测试步骤
   - **前置条件**（可选）：执行 Python 代码准备环境
   - **断言配置**（可选）：添加验证条件

**示例 - 带前置条件和变量引用：**

前置条件：
```python
import requests
resp = requests.post('https://erptest.example.com/api/login', json={
    'username': os.getenv('ERP_USERNAME'),
    'password': os.getenv('ERP_PASSWORD')
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

### Excel 导入

支持通过 Excel 模板批量导入测试用例：

1. **下载模板** - 项目提供标准 Excel 模板
2. **填写用例** - 按模板格式填写任务名、描述、前置条件、断言
3. **上传导入** - 上传 Excel 文件，预览后确认导入
4. **批量管理** - 一次导入多个测试用例，自动解析变量引用和断言配置

### 断言类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `url_contains` | URL 包含指定字符串 | `/dashboard` |
| `text_exists` | 页面包含指定文本 | `欢迎回来` |
| `no_errors` | 执行过程无错误 | `true` |

### 执行与监控

1. 在任务列表找到目标任务，点击「执行」
2. 进入实时监控页面，通过 SSE 查看每一步执行状态：
   - **步骤时间线** - 每一步的执行状态
   - **推理日志** - AI 的思考和决策过程
   - **截图面板** - 每一步操作的页面截图
3. 执行完成后自动跳转到报告页面

### 前置条件

前置条件允许在 UI 测试开始前执行 Python 代码，用于登录获取 token、准备测试数据等。

关键要点：
- 使用 `context['变量名']` 存储结果，用 `{{变量名}}` 在描述中引用
- 使用环境变量（`os.getenv`）而非硬编码凭据

```python
# 推荐：使用环境变量
import os
username = os.getenv('ERP_USERNAME')
password = os.getenv('ERP_PASSWORD')
```

## 配置参考

所有配置通过项目根目录 `.env` 文件管理，参考 `.env.example`。

### LLM 配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DASHSCOPE_API_KEY` | 阿里云 DashScope API Key | - |
| `OPENAI_API_KEY` | OpenAI 兼容 API Key | - |
| `LLM_MODEL` | 模型名称 | qwen3.5-plus |
| `LLM_BASE_URL` | API 基础 URL | DashScope 端点 |
| `LLM_TEMPERATURE` | 模型温度 | 0.0 |

### 目标系统配置

| 变量 | 说明 |
|------|------|
| `ERP_BASE_URL` | 目标系统地址 |
| `ERP_USERNAME` | 测试账号用户名 |
| `ERP_PASSWORD` | 测试账号密码 |
| `WEBSERP_PATH` | webseleniumerp 项目路径（可选） |

### 浏览器配置

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `BROWSER_HEADLESS` | 无头模式 | true |
| `BROWSER_MODE` | launch 或 cdp | launch |

## 开发指南

### 项目结构

```
aiDriveUITest/
├── backend/
│   ├── api/routes/       # API 路由（每个 domain 一个文件）
│   ├── agent/            # AI 浏览器自动化（MonitoredAgent, detectors）
│   ├── core/             # 业务服务（执行管道、代码生成、断言）
│   ├── llm/              # LLM 抽象层
│   ├── db/               # 数据库（models, repository, schemas）
│   ├── config/           # 配置管理
│   └── utils/            # 工具类（logger, excel_parser）
├── frontend/
│   ├── src/pages/        # 页面组件
│   ├── src/components/   # UI 组件（按功能分组）
│   ├── src/hooks/        # 自定义 Hooks
│   ├── src/api/          # API 客户端
│   └── src/types/        # TypeScript 类型
├── e2e/                  # E2E 测试
├── outputs/              # 执行产物（gitignored）
├── docs/                 # 文档
├── pyproject.toml        # Python 项目配置
├── deploy.sh             # 部署脚本
└── .env.example          # 环境变量模板
```

### 开发命令

**后端：**
```bash
uv run uvicorn backend.api.main:app --reload --port 11002   # 开发服务器
uv run pytest backend/tests/ -v                              # 运行测试
uv run ruff check backend/ && uv run ruff format backend/    # 代码规范
```

**前端：**
```bash
cd frontend && npm run dev     # 开发服务器
cd frontend && npm run build   # 生产构建
cd frontend && npm run lint    # 代码规范
```

### API 文档

启动服务后访问：
- Swagger UI: http://localhost:11002/docs
- ReDoc: http://localhost:11002/redoc

### 添加新端点

1. 在 `backend/api/routes/` 添加路由文件
2. 在 `backend/db/schemas.py` 添加 Pydantic 模型
3. 在 `backend/api/main.py` 注册路由

## 部署说明

### 服务器环境准备

```bash
# 1. 安装基础依赖（Ubuntu 24.04）
apt update && apt install -y git nginx

# 2. 安装 uv
snap install --classic astral-uv

# 3. 安装 Node.js 22+
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs

# 4. 克隆项目
git clone git@github.com:mojihuan/weberpagent.git /root/project/weberpagent
cd /root/project/weberpagent

# 5. 配置环境变量
cp .env.example .env
# 编辑 .env，填入 DASHSCOPE_API_KEY、ERP_BASE_URL 等

# 6. 安装依赖
uv sync
uv run playwright install chromium
cd frontend && npm install
```

### deploy.sh 一键部署

在服务器上执行：

```bash
cd /root/project/weberpagent
./deploy.sh                    # 完整部署（拉代码 + 装依赖 + 构建 + 重启）
./deploy.sh --backend-only     # 只部署后端
./deploy.sh --frontend-only    # 只部署前端
./deploy.sh --skip-build       # 跳过构建，只拉取代码和重启
./deploy.sh --stop             # 停止后端服务
```

部署流程：`git pull` → `uv sync` / `npm build` → nohup 启动 uvicorn → 复制 dist 到 Nginx 目录。

### Nginx 配置

```nginx
# /etc/nginx/sites-available/aidriveuitest
server {
    listen 80;
    server_name 121.40.191.49;

    root /var/www/aidriveuitest;
    index index.html;

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # 后端 API 反代（端口 8080，与 deploy.sh 一致）
    location /api {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Connection '';
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 86400s;   # SSE 长连接
    }

    # 健康检查
    location /health {
        proxy_pass http://127.0.0.1:8080/health;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }

    # SPA 路由
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# 启用站点
ln -sf /etc/nginx/sites-available/aidriveuitest /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl enable --now nginx
```

### 数据库优化

SQLite 生产环境建议启用 WAL 模式（项目已内置在 `backend/db/database.py`）：

```python
@event.listens_for(engine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.close()
```

### 验证部署

```bash
curl http://127.0.0.1/health
# 预期: {"status": "healthy"}
```

访问 http://121.40.191.49 进入应用。

### 服务管理

```bash
# 后端日志
tail -f /tmp/aidriveuitest.log

# 停止后端
./deploy.sh --stop

# 重启 Nginx
systemctl reload nginx
```

## FAQ

**Playwright 安装失败？**

网络问题导致下载失败时，使用 npmmirror 镜像：

```bash
uv run playwright install chromium --mirror https://npmmirror.com/mirrors/playwright
```

**Windows 上出现 NotImplementedError？**

Windows asyncio 子进程兼容性问题，必须使用专用启动脚本：

```bash
uv run python backend/run_server.py
```

**LLM 调用返回错误？**

检查：1) API Key 是否正确配置 2) API 余额是否充足 3) 网络是否可访问 API 端点

**SSE 连接断开？**

确保 Nginx 配置了正确的超时设置：

```nginx
proxy_read_timeout 86400s;
proxy_buffering off;
```

**AI 执行步骤太多或太少？**

调整任务的 `max_steps` 参数，默认为 10 步。

## License

MIT License
