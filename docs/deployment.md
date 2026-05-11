# aiDriveUITest 部署指南

> **本文档是 aiDriveUITest 平台的完整部署指南。**
> 目前包含第 1 节（环境要求）和第 2 节（快速部署），后续将追加 Docker 部署、配置详解、运维操作等章节。

---

## 1. 环境要求

### 1.1 硬件最低要求

| 资源 | 最低配置 | 推荐配置 |
|------|---------|---------|
| CPU | 2 核 | 4 核 |
| 内存 | 4 GB | 8 GB |
| 磁盘 | 20 GB | 40 GB SSD |
| 网络 | 需访问公网 | 稳定公网连接 |

> 浏览器自动化（Playwright Chromium）会消耗较多内存，同时运行多个测试任务时建议 8 GB 以上内存。
> gunicorn worker 数量应与 CPU 核数匹配，2 核建议 `--workers 2`，4 核建议 `--workers 4`。

### 1.2 操作系统

| 系统 | 版本要求 |
|------|---------|
| Ubuntu | 22.04 LTS / 24.04 LTS |
| Debian | 12 (Bookworm) 及以上 |

> 本指南以 Ubuntu 22.04/24.04 为基准编写，其他 Linux 发行版可参考调整包管理命令。

### 1.3 软件依赖

| 软件 | 版本要求 | 用途 |
|------|---------|------|
| Python | 3.11+ | 后端运行时 |
| Node.js | 20+ | 前端构建 |
| npm | 随 Node.js 安装 | 前端包管理 |
| uv | 最新版 | Python 包管理（替代 pip） |
| nginx | 1.18+ | 反向代理 + 静态文件服务 |
| git | 2.x | 代码拉取 |
| curl | 任意 | 下载工具、健康检查 |

### 1.4 网络要求

| 目标 | 用途 |
|------|------|
| `dashscope.aliyuncs.com` | 阿里云 DashScope API（LLM 调用） |
| 目标 ERP 系统 | 被测系统访问 |
| Ubuntu/PyPI 软件源 | 系统包、Python 依赖安装 |

> 如果服务器在内网环境，需配置代理或确保以上域名可达。后端启动时会自动清除环境变量中的代理设置（`http_proxy` 等），避免 LLM 调用超时。

---

## 2. 快速部署（systemd + nginx）

以下 10 步从零开始完成部署，以 Ubuntu 22.04/24.04 为例。

### Step 1 — 安装系统依赖

```bash
# 更新软件源
sudo apt update && sudo apt upgrade -y

# 安装基础依赖
sudo apt install -y python3 python3-venv nodejs npm nginx curl git

# 安装 uv（Python 包管理器）
# 方式一：snap（推荐，Ubuntu 默认支持）
sudo snap install astral-uv

# 方式二：curl（适用于无 snap 的环境）
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> 安装完成后，确认 uv 路径：
> ```bash
> which uv
> # snap 安装: /snap/bin/uv
> # curl 安装: /root/.local/bin/uv
> ```
> 后续 systemd 服务文件中的 `ExecStart` 路径需与此一致。

### Step 2 — 克隆项目

```bash
# 创建项目目录（按实际路径调整）
cd /root/project

# 克隆代码仓库
git clone <repository-url> weberpagent
cd weberpagent
```

### Step 3 — 配置环境变量

```bash
# 从示例文件创建 .env
cp .env.example .env

# 编辑 .env，填写实际配置
nano .env
```

`.env` 必填项说明：

```ini
# LLM 配置 — 必填，用于 AI 驱动浏览器
DASHSCOPE_API_KEY=sk-xxx          # 阿里云 DashScope API Key
LLM_MODEL=qwen3.5-plus            # 模型名称
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# ERP 系统配置 — 必填，用于自动登录被测系统
ERP_BASE_URL=https://erp.example.com
ERP_USERNAME=test_user
ERP_PASSWORD=your_password

# 外部模块路径 — 按需配置
WEBSERP_PATH=./webseleniumerp
```

> `OPENAI_API_KEY` 可选，仅在同时使用 OpenAI 兼容接口时填写。
> `DASHSCOPE_API_KEY` 是必须的，AI agent 依赖此 Key 调用 Qwen 模型。

### Step 4 — 安装 Python 依赖

```bash
cd /root/project/weberpagent

# uv 自动创建虚拟环境并安装所有依赖
uv sync
```

> `uv sync` 会根据 `pyproject.toml` 和 `uv.lock` 安装精确版本的依赖，确保环境可复现。

### Step 5 — 安装 Playwright 浏览器

```bash
# 安装 Chromium 及其系统依赖（libglib、libnss 等）
uv run playwright install chromium --with-deps
```

> `--with-deps` 会自动安装 Chromium 运行所需的系统库（如 libglib2.0-0、libnss3、libatk1.0-0 等）。
> 若无 `--with-deps`，需手动执行 `sudo npx playwright install-deps chromium`。

### Step 6 — 数据库初始化

数据库会在后端首次启动时自动创建，**无需手动操作**。

后端启动时 `init_db()` 会自动完成：
- 创建 `backend/data/database.db`（SQLite）
- 创建所有业务表
- 检查并补充新版本新增的列（兼容旧数据库）

> 数据库使用 SQLite，数据文件位于 `backend/data/database.db`。生产环境建议定期备份此文件。

### Step 7 — 构建前端

```bash
cd /root/project/weberpagent/frontend

# 安装前端依赖
npm ci

# 构建生产版本
npm run build
```

构建产物在 `frontend/dist/` 目录下。

> `npm ci` 严格按照 `package-lock.json` 安装，比 `npm install` 更适合 CI/CD 和生产部署。

### Step 8 — 部署前端静态文件

```bash
# 创建部署目录
sudo mkdir -p /var/www/aidriveuitest

# 复制构建产物到部署目录
sudo cp -r /root/project/weberpagent/frontend/dist/* /var/www/aidriveuitest/

# 设置权限
sudo chown -R www-data:www-data /var/www/aidriveuitest
```

> 每次更新前端后需重新执行此步骤。可编写脚本简化流程。

### Step 9 — 配置后端 systemd 服务

创建 systemd 服务文件：

```bash
sudo nano /etc/systemd/system/aidriveuitest.service
```

写入以下内容：

```ini
[Unit]
Description=aiDriveUITest FastAPI Backend
After=network.target

[Service]
Type=exec
User=root
WorkingDirectory=/root/project/weberpagent
Environment=PATH=/snap/bin:/usr/bin:/bin
ExecStart=/snap/bin/uv run gunicorn backend.api.main:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8080 \
    --timeout 120 \
    --keep-alive 5
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

> **注意 `ExecStart` 中 uv 的路径**：
> - snap 安装：`/snap/bin/uv`
> - curl 安装：`/root/.local/bin/uv`
>
> 请根据 Step 1 中 `which uv` 的结果调整 `ExecStart` 和 `Environment=PATH`。
>
> `--workers` 数量建议与 CPU 核数一致，`--timeout 120` 保证长时间运行的测试任务不会超时。

启用并启动服务：

```bash
# 重载 systemd 配置
sudo systemctl daemon-reload

# 设置开机自启
sudo systemctl enable aidriveuitest

# 启动服务
sudo systemctl start aidriveuitest

# 查看运行状态
sudo systemctl status aidriveuitest
```

常用管理命令：

```bash
# 查看实时日志
sudo journalctl -u aidriveuitest -f

# 重启服务
sudo systemctl restart aidriveuitest

# 停止服务
sudo systemctl stop aidriveuitest
```

### Step 10 — 配置 nginx 反向代理

创建 nginx 站点配置：

```bash
sudo nano /etc/nginx/sites-available/aidriveuitest
```

写入以下内容（将 `<server-ip>` 替换为实际服务器 IP 或域名）：

```nginx
server {
    listen 80;
    server_name <server-ip>;

    root /var/www/aidriveuitest;
    index index.html;

    # 开启 gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    # API 反向代理
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
        proxy_read_timeout 86400s;
    }

    # 健康检查端点
    location /health {
        proxy_pass http://127.0.0.1:8080/health;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }

    # 前端路由（SPA fallback）
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

> `proxy_read_timeout 86400s`（24 小时）确保 SSE（Server-Sent Events）长连接不会被 nginx 超时断开，这对于实时推送测试执行进度至关重要。
>
> `proxy_buffering off` 和 `proxy_cache off` 确保 SSE 事件即时推送到前端。

启用站点并重载 nginx：

```bash
# 创建软链接启用站点
sudo ln -sf /etc/nginx/sites-available/aidriveuitest /etc/nginx/sites-enabled/

# 移除默认站点（可选）
sudo rm -f /etc/nginx/sites-enabled/default

# 测试配置是否正确
sudo nginx -t

# 重载 nginx
sudo systemctl reload nginx
```

### 验证部署

**1. 健康检查**

```bash
# 检查后端 API
curl http://localhost/health
# 预期返回: {"status":"healthy"}

# 检查 API 文档
curl http://localhost/api/tasks
# 预期返回: {"success":true,"data":[]}
```

**2. 浏览器访问**

打开浏览器，访问 `http://<server-ip>`，应看到 aiDriveUITest 前端界面。

**3. 检查服务状态**

```bash
# 后端服务状态
sudo systemctl status aidriveuitest

# nginx 状态
sudo systemctl status nginx
```

> 如果遇到问题，优先检查：
> 1. 后端日志：`sudo journalctl -u aidriveuitest -f`
> 2. nginx 错误日志：`sudo tail -f /var/log/nginx/error.log`
> 3. `.env` 配置是否正确（特别是 `DASHSCOPE_API_KEY`）
> 4. uv 路径是否与 systemd 服务文件一致
