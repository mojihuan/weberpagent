# 部署指南 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 创建完整的通用部署指南文档 + Docker 部署文件 + 更新部署脚本，使团队成员能从零在任意 Ubuntu 服务器上部署 aiDriveUITest。

**Architecture:** 分层式文档结构 — 快速部署（systemd + nginx）为主路径，Docker Compose 为可选替代。同时产出 Dockerfile、docker-compose.yml 和 deploy.sh 三个可执行文件。

**Tech Stack:** systemd + gunicorn + nginx（传统部署），Docker + Docker Compose（容器部署），Playwright + Chromium（浏览器自动化）

---

### Task 1: 创建 Dockerfile

**Files:**
- Create: `Dockerfile`

**Step 1: 编写多阶段构建 Dockerfile**

```dockerfile
# ==============================
# Stage 1: 前端构建
# ==============================
FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# ==============================
# Stage 2: 后端 + 运行时
# ==============================
FROM python:3.11-slim

# 安装系统依赖（Playwright Chromium 需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    gnupg \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    libwayland-client0 \
    && rm -rf /var/lib/apt/lists/*

# 安装 uv
RUN pip install uv

WORKDIR /app

# 安装 Python 依赖
COPY pyproject.toml ./
RUN uv pip install --system -r pyproject.toml

# 安装 Playwright Chromium
RUN playwright install chromium --with-deps

# 复制后端代码
COPY backend/ ./backend/

# 复制前端构建产物
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# 创建数据目录
RUN mkdir -p data/templates data/filled data/screenshots data/test-files outputs

# 环境变量默认值
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

EXPOSE 8080

CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Step 2: 验证 Dockerfile 语法**

Run: `docker build --check .`（如果 Docker 可用）或人工检查语法。

**Step 3: Commit**

```bash
git add Dockerfile
git commit -m "feat: add multi-stage Dockerfile for deployment"
```

---

### Task 2: 创建 docker-compose.yml

**Files:**
- Create: `docker-compose.yml`

**Step 1: 编写 docker-compose.yml**

```yaml
services:
  backend:
    build: .
    container_name: aidriveuitest-backend
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
    env_file:
      - .env
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///./data/database.db
      - WEBSERP_PATH=/app/webseleniumerp
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s

  nginx:
    image: nginx:alpine
    container_name: aidriveuitest-nginx
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    depends_on:
      backend:
        condition: service_healthy
```

**Step 2: 创建 nginx.conf（Docker 用）**

**Files:**
- Create: `nginx.conf`

```nginx
server {
    listen 80;
    server_name _;

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;

    location /api {
        proxy_pass http://backend:8080;
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

    location /health {
        proxy_pass http://backend:8080/health;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
    }

    location / {
        # Docker 部署时前端由 nginx 直接提供
        # 需要从 backend 容器复制或使用共享卷
        proxy_pass http://backend:8080/;
    }
}
```

注意：Docker 部署的 nginx 配置与 systemd 部署不同 — 前端静态文件需要额外处理（可用多阶段构建复制到 nginx 容器，或通过 FastAPI 的 StaticFiles 挂载）。文档中会说明。

**Step 3: Commit**

```bash
git add docker-compose.yml nginx.conf
git commit -m "feat: add Docker Compose configuration with nginx proxy"
```

---

### Task 3: 创建 deploy.sh 更新部署脚本

**Files:**
- Create: `deploy.sh`

**Step 1: 编写 deploy.sh**

```bash
#!/usr/bin/env bash
set -euo pipefail

# ============================================
# aiDriveUITest 更新部署脚本
# 用法: ./deploy.sh [--backend-only] [--frontend-only] [--skip-build] [--docker]
# ============================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

BACKEND_ONLY=false
FRONTEND_ONLY=false
SKIP_BUILD=false
USE_DOCKER=false

for arg in "$@"; do
    case $arg in
        --backend-only)  BACKEND_ONLY=true ;;
        --frontend-only) FRONTEND_ONLY=true ;;
        --skip-build)    SKIP_BUILD=true ;;
        --docker)        USE_DOCKER=true ;;
        --help|-h)       echo "用法: ./deploy.sh [--backend-only] [--frontend-only] [--skip-build] [--docker]"
                         exit 0 ;;
    esac
done

echo "=== aiDriveUITest 部署 ==="
echo "目录: $SCRIPT_DIR"

# --- Docker 部署 ---
if [ "$USE_DOCKER" = true ]; then
    echo "[Docker] 拉取最新代码..."
    git pull origin main
    echo "[Docker] 重新构建并启动..."
    docker compose up -d --build
    echo "[Docker] 部署完成"
    exit 0
fi

# --- 拉取最新代码 ---
echo "[1/5] 拉取最新代码..."
git pull origin main

# --- 后端更新 ---
if [ "$FRONTEND_ONLY" = false ]; then
    echo "[2/5] 更新 Python 依赖..."
    uv sync

    echo "[3/5] 重启后端服务..."
    sudo systemctl restart aidriveuitest
    sleep 3
    if sudo systemctl is-active --quiet aidriveuitest; then
        echo "  ✓ 后端服务运行正常"
    else
        echo "  ✗ 后端服务启动失败，查看日志: journalctl -u aidriveuitest -n 50"
        exit 1
    fi
else
    echo "[2/5] 跳过后端 (--frontend-only)"
    echo "[3/5] 跳过后端 (--frontend-only)"
fi

# --- 前端更新 ---
if [ "$BACKEND_ONLY" = false ]; then
    if [ "$SKIP_BUILD" = false ]; then
        echo "[4/5] 构建前端..."
        cd frontend
        npm ci
        npm run build
        cd "$SCRIPT_DIR"
    else
        echo "[4/5] 跳过前端构建 (--skip-build)"
    fi

    echo "[5/5] 部署前端静态文件..."
    DEPLOY_DIR="/var/www/aidriveuitest"
    sudo rm -rf "$DEPLOY_DIR"/*
    sudo cp -r frontend/dist/* "$DEPLOY_DIR"/
    echo "  ✓ 前端已部署到 $DEPLOY_DIR"
else
    echo "[4/5] 跳过前端 (--backend-only)"
    echo "[5/5] 跳过前端 (--backend-only)"
fi

echo ""
echo "=== 部署完成 ==="
echo "前端: http://$(hostname -I | awk '{print $1}')"
echo "API:  http://$(hostname -I | awk '{print $1}')/api/tasks"
```

**Step 2: 设置执行权限并提交**

```bash
chmod +x deploy.sh
git add deploy.sh
git commit -m "feat: add deployment script with systemd and Docker support"
```

---

### Task 4: 编写 docs/deployment.md — 环境要求 + 快速部署

**Files:**
- Create: `docs/deployment.md`

**Step 1: 编写第 1-2 节（环境要求 + 快速部署）**

这是文档的核心部分，包含完整的从零部署步骤。内容要点：

**环境要求节：**
- 硬件：2 核 CPU、4GB 内存、20GB 磁盘
- OS：Ubuntu 22.04/24.04 LTS
- 软件版本：Python 3.11+、Node.js 20+、uv、nginx
- 网络：需访问 DashScope API（`https://dashscope.aliyuncs.com`）和目标 ERP 系统

**快速部署 10 步：**

Step 1 — 安装系统依赖：
```bash
sudo apt update && sudo apt install -y python3 python3-venv nodejs npm nginx curl git
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

Step 2 — 克隆项目：
```bash
git clone <repo-url> /root/project/weberpagent
cd /root/project/weberpagent
```

Step 3 — 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env，填写 DASHSCOPE_API_KEY、ERP_BASE_URL、ERP_USERNAME、ERP_PASSWORD
```

Step 4 — 安装 Python 依赖：
```bash
uv sync
```

Step 5 — 安装 Playwright 浏览器：
```bash
uv run playwright install chromium --with-deps
```

Step 6 — 数据库（首次启动自动初始化，无需手动操作）

Step 7 — 构建前端：
```bash
cd frontend && npm ci && npm run build && cd ..
```

Step 8 — 部署前端静态文件：
```bash
sudo mkdir -p /var/www/aidriveuitest
sudo cp -r frontend/dist/* /var/www/aidriveuitest/
```

Step 9 — 配置后端 systemd 服务，创建 `/etc/systemd/system/aidriveuitest.service`（内容来自 memory 中的部署记录），注意 `uv` 路径和 worker 数。

Step 10 — 配置 nginx 站点，创建 `/etc/nginx/sites-available/aidriveuitest`，注意 `proxy_buffering off` 用于 SSE。

验证：
```bash
curl http://localhost/health
# 浏览器访问 http://<server-ip>
```

**Step 2: Commit**

```bash
git add docs/deployment.md
git commit -m "docs: add deployment guide - environment and quick deploy sections"
```

---

### Task 5: 补充 docs/deployment.md — Docker 部署 + 配置详解

**Files:**
- Modify: `docs/deployment.md`

**Step 1: 添加 Docker 部署章节（第 3 节）**

内容要点：
- 前置条件：安装 Docker + Docker Compose
- 一键启动：`docker compose up -d`
- 数据卷说明：`./data`（数据库）、`./outputs`（测试输出）会自动持久化
- 环境变量：通过 `.env` 文件配置，与 systemd 部署使用同一份 `.env`
- 常用命令：`docker compose logs -f`、`docker compose restart`、`docker compose down`
- 注意事项：Docker 内 Playwright 的 Chromium 需要共享内存，建议 `--shm-size=2g`

**Step 2: 添加配置详解章节（第 4 节）**

内容要点：

**.env 变量表：**

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| DASHSCOPE_API_KEY | 是 | - | 阿里云 DashScope API Key |
| OPENAI_API_KEY | 否 | - | OpenAI API Key（备用） |
| LLM_MODEL | 否 | qwen3.5-plus | LLM 模型名称 |
| LLM_BASE_URL | 否 | https://dashscope.aliyuncs.com/compatible-mode/v1 | API 地址 |
| ERP_BASE_URL | 是 | - | 目标 ERP 系统地址 |
| ERP_USERNAME | 是 | - | ERP 登录用户名 |
| ERP_PASSWORD | 是 | - | ERP 登录密码 |
| WEBSERP_PATH | 否 | - | 外部模块路径 |
| DATABASE_URL | 否 | sqlite+aiosqlite:///./data/database.db | 数据库连接 |
| LOG_LEVEL | 否 | INFO | 日志级别 |

**systemd 关键参数：**
- `workers`：建议与 CPU 核数相同（2 核 = 2 workers）
- `timeout`：AI agent 执行时间较长，建议 120s
- `keep-alive`：5s，SSE 需要保持连接
- `uv` 路径：确认 `which uv`，snap 安装为 `/snap/bin/uv`

**nginx 关键配置：**
- `proxy_buffering off`：必须关闭，否则 SSE 事件会被缓冲
- `proxy_read_timeout 86400s`：测试执行可能很长，24h 超时
- `try_files $uri $uri/ /index.html`：SPA 路由支持
- `gzip`：压缩 JSON 和 JS 减少传输量

**Step 3: Commit**

```bash
git add docs/deployment.md
git commit -m "docs: add Docker deployment and configuration reference sections"
```

---

### Task 6: 补充 docs/deployment.md — 运维操作

**Files:**
- Modify: `docs/deployment.md`

**Step 1: 添加运维操作章节（第 5 节）**

内容要点：

**更新部署：**
```bash
# 完整更新
./deploy.sh

# 只更新后端
./deploy.sh --backend-only

# 只更新前端
./deploy.sh --frontend-only

# Docker 更新
./deploy.sh --docker
```

**备份与恢复：**
- 手动备份：`tar czf backup-$(date +%Y%m%d).tar.gz data/ outputs/ .env`
- 自动备份：设置 cron 任务（参考 memory 中的备份脚本配置）
- 恢复：解压备份文件覆盖对应目录

**日志查看：**
```bash
# 后端日志
journalctl -u aidriveuitest -f
journalctl -u aidriveuitest --since "1 hour ago"

# nginx 日志
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

# Docker 日志
docker compose logs -f backend
```

**常见问题排查：**

| 问题 | 排查命令 | 解决方案 |
|------|----------|----------|
| 端口占用 | `sudo lsof -i :8080` | kill 占用进程或修改端口 |
| Playwright 崩溃 | `journalctl -u aidriveuitest \| grep -i "chromium\|playwright"` | 检查共享内存、依赖库 |
| SQLite 锁定 | `journalctl -u aidriveuitest \| grep -i "locked"` | 检查并发写入，重启服务 |
| SSE 断连 | 检查 nginx `proxy_buffering` 是否 off | 确认 nginx 配置正确 |
| 前端 404 | `ls /var/www/aidriveuitest/` | 重新构建并部署前端 |

**Step 2: Commit**

```bash
git add docs/deployment.md
git commit -m "docs: add operations and troubleshooting section to deployment guide"
```

---

### Task 7: 最终验证 + 更新 .gitignore

**Files:**
- Modify: `.gitignore`
- Read: `docs/deployment.md` (验证完整内容)

**Step 1: 更新 .gitignore**

当前 `.gitignore` 包含 `deploy.sh`，需要移除这一行，因为我们现在要将 deploy.sh 纳入版本控制。

在 `.gitignore` 中找到 `deploy.sh` 所在行并删除。

**Step 2: 读取完整的 deployment.md 验证所有章节**

Run: 读取 `docs/deployment.md` 全文，确认包含 5 个主要章节且内容完整。

**Step 3: 最终 Commit**

```bash
git add .gitignore docs/deployment.md Dockerfile docker-compose.yml nginx.conf deploy.sh
git commit -m "docs: complete deployment guide with Docker and systemd support"
```
