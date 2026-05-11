# aiDriveUITest 部署指南

> **本文档是 aiDriveUITest 平台的完整部署指南。**
> 包含第 1 节（环境要求）、第 2 节（快速部署）、第 3 节（Docker 部署）、第 4 节（配置详解）、第 5 节（运维操作）。

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

---

## 3. Docker 部署（可选）

如果不想手动安装 Python、Node.js、nginx 等依赖，可以使用 Docker 一键部署。

### 前置条件

```bash
# 安装 Docker
curl -fsSL https://get.docker.com | sh

# 安装 Docker Compose（如果 Docker 未自带）
# Ubuntu 通常随 Docker 一起安装，可通过以下命令确认：
docker compose version
```

> Docker Compose V2 已集成到 Docker 中，无需单独安装。如果 `docker compose version` 能正常输出版本号，说明已就绪。

### 配置环境变量

与 systemd 部署模式相同，在项目根目录创建 `.env` 文件：

```bash
cp .env.example .env
nano .env
```

必填项参见 [Step 3 — 配置环境变量](#step-3--配置环境变量)。

### 一键启动

```bash
docker compose up -d
```

首次启动会自动完成：
1. 构建后端镜像（多阶段构建：安装 Python 依赖 + Playwright Chromium）
2. 构建前端并打包到 nginx 镜像
3. 启动 backend 和 nginx 容器

### 数据持久化

`docker-compose.yml` 通过卷挂载将数据持久化到宿主机：

| 容器路径 | 宿主机路径 | 用途 |
|---------|-----------|------|
| `/app/data` | `./data` | SQLite 数据库文件 |
| `/app/outputs` | `./outputs` | 测试报告、截图等输出文件 |

容器重建或更新时，这两个目录中的数据不会丢失。

### 常用命令

```bash
# 查看实时日志
docker compose logs -f

# 查看后端日志（仅 backend 服务）
docker compose logs -f backend

# 重启服务
docker compose restart

# 停止服务
docker compose down

# 重新构建并启动（代码更新后）
docker compose up -d --build

# 查看容器状态
docker compose ps
```

### 注意事项

- **共享内存**：Playwright Chromium 需要较大的共享内存，`docker-compose.yml` 已配置 `shm_size: 2gb`，请勿移除此配置。
- **首次构建较慢**：Dockerfile 需要下载 Playwright Chromium（约 150MB），首次构建可能需要 5-10 分钟。
- **数据库安全**：SQLite 数据文件位于 `./data/database.db`，容器重建不会丢失，但建议定期备份。
- **健康检查**：backend 容器配置了健康检查 `curl -f http://localhost:8080/health`，可通过 `docker compose ps` 查看健康状态。

---

## 4. 配置详解

### .env 环境变量

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `DASHSCOPE_API_KEY` | 是 | - | 阿里云 DashScope API Key，用于 LLM 调用 |
| `OPENAI_API_KEY` | 否 | - | OpenAI API Key（备用 LLM） |
| `LLM_MODEL` | 否 | `qwen3.5-plus` | LLM 模型名称 |
| `LLM_BASE_URL` | 否 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | LLM API 地址 |
| `LLM_TEMPERATURE` | 否 | `0.0` | LLM 温度参数 |
| `ERP_BASE_URL` | 是 | - | 目标 ERP 系统地址 |
| `ERP_USERNAME` | 是 | - | ERP 登录用户名 |
| `ERP_PASSWORD` | 是 | - | ERP 登录密码 |
| `WEBSERP_PATH` | 否 | - | 外部模块路径（webseleniumerp） |
| `DATABASE_URL` | 否 | `sqlite+aiosqlite:///./data/database.db` | 数据库连接字符串 |
| `LOG_LEVEL` | 否 | `INFO` | 日志级别 |

### systemd 服务参数

| 参数 | 说明 |
|------|------|
| `Type=exec` | 直接执行，不等待 notify（gunicorn 不支持 sd_notify） |
| `--workers N` | gunicorn worker 数量，建议与 CPU 核数相同（2 核 = 2 workers） |
| `--worker-class uvicorn.workers.UvicornWorker` | 使用 uvicorn worker 支持异步（FastAPI 依赖 async） |
| `--timeout 120` | worker 超时时间 120s，AI agent 执行时间较长，避免超时杀进程 |
| `--keep-alive 5` | 保持连接 5s |
| `ExecStart` 中的 uv 路径 | 需确认实际安装路径：snap 安装为 `/snap/bin/uv`，curl 安装为 `~/.local/bin/uv` |

### nginx 配置要点

| 配置项 | 说明 |
|-------|------|
| `proxy_buffering off` | **必须关闭**，否则 SSE 事件会被缓冲导致前端无法实时接收测试执行进度 |
| `proxy_read_timeout 86400s` | 24 小时超时，测试执行可能长达数小时，避免 SSE 连接被 nginx 断开 |
| `proxy_http_version 1.1` + `Connection ''` | 支持 HTTP 长连接，SSE 依赖此配置 |
| `try_files $uri $uri/ /index.html` | SPA 路由支持，所有未匹配的路径回退到 index.html 由前端路由处理 |
| `gzip on` | 压缩 JSON/JS/CSS 响应，减少传输量 |
| `expires 1y` + `immutable` | 静态资源（JS/CSS/图片等）设置 1 年缓存，利用文件名 hash 实现缓存失效 |

---

## 5. 运维操作

### 更新部署

使用 `deploy.sh` 脚本更新（推荐）：

```bash
# 完整更新（推荐）
./deploy.sh

# 只更新后端
./deploy.sh --backend-only

# 只更新前端
./deploy.sh --frontend-only

# Docker 模式更新
./deploy.sh --docker
```

也可以手动更新：

```bash
cd /root/project/weberpagent
git pull origin main
uv sync
sudo systemctl restart aidriveuitest
cd frontend && npm ci && npm run build && cd ..
sudo cp -r frontend/dist/* /var/www/aidriveuitest/
```

### 备份与恢复

手动备份：

```bash
BACKUP_NAME="backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p /root/backups
tar czf /root/backups/${BACKUP_NAME}.tar.gz data/ outputs/ .env
```

设置自动备份 cron 任务：

```bash
# 创建备份脚本
cat > /root/project/weberpagent/scripts/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/root/backups"
PROJECT_DIR="/root/project/weberpagent"
BACKUP_NAME="backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p $BACKUP_DIR
tar czf $BACKUP_DIR/${BACKUP_NAME}.tar.gz -C $PROJECT_DIR data outputs .env
# 保留最近 7 天的备份
find $BACKUP_DIR -name "backup-*.tar.gz" -mtime +7 -delete
EOF
chmod +x /root/project/weberpagent/scripts/backup.sh

# 添加 cron 任务（每天凌晨 2 点执行）
echo "0 2 * * * root /root/project/weberpagent/scripts/backup.sh >> /var/log/aidriveuitest-backup.log 2>&1" | sudo tee /etc/cron.d/aidriveuitest-backup
```

恢复步骤：

```bash
sudo systemctl stop aidriveuitest
cd /root/project/weberpagent
tar xzf /root/backups/backup-XXXXXXXX-XXXXXX.tar.gz
sudo systemctl start aidriveuitest
```

### 日志查看

```bash
# 后端服务日志（实时）
journalctl -u aidriveuitest -f

# 后端服务日志（最近 1 小时）
journalctl -u aidriveuitest --since "1 hour ago"

# 后端服务日志（最近 100 行）
journalctl -u aidriveuitest -n 100

# nginx 错误日志
tail -f /var/log/nginx/error.log

# nginx 访问日志
tail -f /var/log/nginx/access.log

# Docker 模式日志
docker compose logs -f backend
docker compose logs -f --tail 100 backend
```

### 常见问题排查

| 问题 | 排查命令 | 解决方案 |
|------|----------|----------|
| 端口被占用 | `sudo lsof -i :8080` 或 `sudo ss -tlnp \| grep 8080` | kill 占用进程或修改 systemd 服务端口 |
| 后端服务启动失败 | `journalctl -u aidriveuitest -n 50` | 检查 .env 配置、Python 依赖、uv 路径 |
| Playwright/Chromium 崩溃 | `journalctl -u aidriveuitest \| grep -i chromium` | 检查系统依赖库是否完整：`ldd $(which chromium)` |
| SQLite 数据库锁定 | `journalctl -u aidriveuitest \| grep -i locked` | 检查并发写入，必要时重启服务 |
| SSE 事件不推送 | 检查 nginx 配置中 `proxy_buffering` 是否为 `off` | 确认 nginx 配置正确后 `sudo nginx -t && sudo systemctl reload nginx` |
| 前端页面 404 | `ls /var/www/aidriveuitest/` | 重新构建前端并部署：`./deploy.sh --frontend-only` |
| git pull 冲突 | `git status` | 手动解决冲突后重新部署 |
| LLM API 调用失败 | `journalctl -u aidriveuitest \| grep -i error` | 检查 API Key、网络连通性、DashScope 配额 |
