# aiDriveUITest 部署指南

> **两种部署方式：**
> - **快速启动** — 直接运行前后端，分别开放端口，适合开发/测试
> - **Docker 部署** — 容器化部署，适合生产环境持久化运行

---

## 1. 环境要求

### 硬件要求

| 资源 | 最低配置 | 推荐配置 |
|------|---------|---------|
| CPU | 2 核 | 4 核 |
| 内存 | 4 GB | 8 GB |
| 磁盘 | 20 GB | 40 GB SSD |

> 浏览器自动化（Playwright Chromium）会消耗较多内存，同时运行多个测试任务时建议 8 GB 以上。

### 软件依赖

| 软件 | 版本 | 用途 |
|------|------|------|
| Python | 3.11+ | 后端运行时 |
| Node.js | 20+ | 前端构建 |
| uv | 最新版 | Python 包管理（替代 pip） |
| git | 2.x | 代码拉取 |

### 网络要求

| 目标 | 用途 |
|------|------|
| `dashscope.aliyuncs.com` | 阿里云 DashScope API（LLM 调用） |
| 目标 ERP 系统 | 被测系统访问 |

> 后端启动时会自动清除环境变量中的代理设置（`http_proxy` 等），避免 LLM 调用超时。

---

## 2. 快速启动

前后端分别启动，各自开放端口：

| 服务 | 端口 | 说明 |
|------|------|------|
| 后端 (FastAPI) | 11002 | REST API + SSE |
| 前端 (Vite) | 11001 | Web 界面，自动代理 `/api` 到后端 |

### 2.1 安装依赖

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Python、Node.js、git
sudo apt install -y python3 python3-venp nodejs npm git curl

# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

### 2.2 克隆项目

```bash
cd /root/project
git clone <repository-url> weberpagent
cd weberpagent
```

### 2.3 配置环境变量

```bash
cp .env.example .env
nano .env
```

`.env` 配置示例：

```ini
# ============================================
# ERP 系统配置（必填）
# ============================================
ERP_BASE_URL=https://erp.example.com    # 被测 ERP 系统地址
ERP_USERNAME=test_user
ERP_PASSWORD=your_password

# 外部模块路径（按需配置）
ERP_API_MODULE_PATH=/path/to/webseleniumerp
WEBSERP_PATH=/path/to/webseleniumerp

# ============================================
# LLM 配置（必填）
# ============================================
DASHSCOPE_API_KEY=sk-xxx                          # 阿里云 DashScope API Key
LLM_MODEL=qwen3.5-plus                            # 模型名称
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_TEMPERATURE=0.0

# ============================================
# 代码生成 LLM（可选，不配置则使用上面的默认 LLM）
# ============================================
#CODE_GEN_MODEL=deepseek-v4-pro
#CODE_GEN_BASE_URL=https://api.deepseek.com
#CODE_GEN_API_KEY=sk-xxx
#CODE_GEN_TEMPERATURE=0.0

# ============================================
# 应用配置（可选）
# ============================================
#DATABASE_URL=sqlite+aiosqlite:///./data/database.db
#LOG_LEVEL=INFO
```

> `DASHSCOPE_API_KEY` 和 `ERP_*` 是必须的。代码生成 LLM 可单独配置不同模型，不配置则复用默认 LLM。

### 2.4 安装 Python 依赖 + Playwright

```bash
cd /root/project/weberpagent

# 安装 Python 依赖
uv sync

# 安装 Playwright Chromium 及系统依赖
uv run playwright install chromium --with-deps
```

### 2.5 安装前端依赖

```bash
cd frontend
npm ci
```

### 2.6 启动服务

**方式 A — 开发模式（推荐）**

两个终端分别启动：

```bash
# 终端 1：启动后端（端口 11002）
cd /root/project/weberpagent
uv run uvicorn backend.api.main:app --host 0.0.0.0 --port 11002
```

```bash
# 终端 2：启动前端（端口 11001）
cd /root/project/weberpagent/frontend
npm run dev
```

前端 Vite 已配置 proxy，访问 `http://<server-ip>:11001` 即可，`/api` 请求自动转发到后端 11002。

**方式 B — 生产模式（后台运行）**

```bash
# 后端：nohup 后台运行
cd /root/project/weberpagent
nohup uv run uvicorn backend.api.main:app --host 0.0.0.0 --port 11002 > backend.log 2>&1 &

# 前端：构建 + 静态文件服务
cd frontend
npm run build
nohup npx vite preview --host 0.0.0.0 --port 11001 > ../frontend.log 2>&1 &
```

### 2.7 验证

```bash
# 健康检查
curl http://localhost:11002/health
# 预期: {"status":"healthy"}

# 浏览器访问
# http://<server-ip>:11001
```

> 数据库首次启动时自动创建（SQLite），无需手动操作。

---

## 3. Docker 部署（生产环境）

适合需要持久化运行、开机自启的生产环境。

### 3.1 前置条件

```bash
# 安装 Docker
curl -fsSL https://get.docker.com | sh

# 确认 Docker Compose 可用
docker compose version
```

### 3.2 配置环境变量

```bash
cp .env.example .env
nano .env
```

必填项参见 [2.3 配置环境变量](#23-配置环境变量)。

**Docker 模式额外注意：**

如果需要使用外部 ERP 模块（`WEBSERP_PATH`），需要额外操作：

1. 在 `docker-compose.yml` 中取消注释 volume 挂载行：
   ```yaml
   volumes:
     - /path/to/webseleniumerp:/app/external/webseleniumerp:ro
   ```
2. 在 `.env` 中将路径改为容器内路径：
   ```
   ERP_API_MODULE_PATH=/app/external/webseleniumerp
   WEBSERP_PATH=/app/external/webseleniumerp
   ```

### 3.3 一键启动

```bash
docker compose up -d
```

首次启动会自动构建镜像（安装 Python 依赖 + Playwright Chromium + 前端构建），可能需要 5-10 分钟。

### 3.4 端口说明

| 端口 | 服务 | 说明 |
|------|------|------|
| 8080 | backend | FastAPI 服务，同时提供 API 和前端静态文件 |

> Backend 在检测到 `frontend/dist` 目录时自动提供前端静态文件服务，无需额外的 web 服务器。

### 3.5 数据持久化

| 容器路径 | 宿主机路径 | 用途 |
|---------|-----------|------|
| `/app/data` | `./data` | SQLite 数据库 |
| `/app/outputs` | `./outputs` | 测试报告、截图 |

容器重建不会丢失这两个目录的数据。

### 3.6 验证

```bash
# 健康检查
curl http://localhost:8080/health
# 预期: {"status":"healthy"}

# 浏览器访问
# http://<server-ip>:8080
```

### 3.7 常用命令

```bash
docker compose logs -f              # 实时日志
docker compose logs -f backend      # 仅后端日志
docker compose restart              # 重启
docker compose down                 # 停止
docker compose up -d --build        # 代码更新后重建
docker compose ps                   # 容器状态
```

### 3.8 注意事项

- **共享内存**：`docker-compose.yml` 已配置 `shm_size: 2gb`，Playwright Chromium 需要，请勿移除
- **前端服务**：Backend 通过 FastAPI StaticFiles 自动服务前端静态文件，无需 nginx
- **备份**：定期备份 `./data/` 和 `./outputs/` 目录即可

---

## 4. 配置详解

### .env 环境变量

#### ERP 系统配置

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `ERP_BASE_URL` | 是 | - | 被测 ERP 系统地址，AI agent 会自动登录此系统 |
| `ERP_USERNAME` | 是 | - | ERP 登录用户名 |
| `ERP_PASSWORD` | 是 | - | ERP 登录密码 |
| `ERP_API_MODULE_PATH` | 否 | - | 外部 API 模块路径，用于前置条件中复用现有项目的 API 封装 |
| `WEBSERP_PATH` | 否 | - | webseleniumerp 项目路径，用于导入外部前置条件操作（FA1、HC1 等） |

#### LLM 配置

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `DASHSCOPE_API_KEY` | 是 | - | 阿里云 DashScope API Key，AI agent 依赖此 Key 调用 Qwen 模型 |
| `LLM_MODEL` | 否 | `qwen3.5-plus` | LLM 模型名称 |
| `LLM_BASE_URL` | 否 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | LLM API 地址 |
| `LLM_TEMPERATURE` | 否 | `0.0` | LLM 温度参数，0.0 = 确定性输出 |

#### 代码生成 LLM（可选）

代码生成使用独立的 LLM 配置，可选用不同模型。不配置则复用上面的默认 LLM。

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `CODE_GEN_MODEL` | 否 | 复用 `LLM_MODEL` | 代码生成模型，如 `deepseek-v4-pro` |
| `CODE_GEN_BASE_URL` | 否 | 复用 `LLM_BASE_URL` | 代码生成 API 地址 |
| `CODE_GEN_API_KEY` | 否 | 复用 `DASHSCOPE_API_KEY` | 代码生成 API Key |
| `CODE_GEN_TEMPERATURE` | 否 | `0.0` | 代码生成温度参数 |

#### 应用配置

| 变量 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `DATABASE_URL` | 否 | `sqlite+aiosqlite:///./data/database.db` | 数据库连接字符串 |
| `LOG_LEVEL` | 否 | `INFO` | 日志级别 |

### 端口说明

**快速启动模式：**

| 端口 | 服务 | 说明 |
|------|------|------|
| 11002 | 后端 (uvicorn) | FastAPI 服务，直接暴露 API |
| 11001 | 前端 (Vite) | Web 界面，`/api` 代理到 11002 |

**Docker 模式：**

| 端口 | 服务 | 说明 |
|------|------|------|
| 8080 | backend | FastAPI 统一服务，同时提供 API 和前端静态文件 |

> 快速启动模式前端 Vite 配置了 `proxy`，将 `/api` 请求自动转发到后端。如需修改后端端口，在 `frontend/vite.config.ts` 中调整 `proxy.target`。

---

## 5. 运维操作

### 更新部署

**快速启动模式：**

```bash
cd /root/project/weberpagent
git pull origin main
uv sync

# 重启后端（先 kill 旧进程）
pkill -f "uvicorn backend.api.main"
uv run uvicorn backend.api.main:app --host 0.0.0.0 --port 11002 &

# 重启前端
cd frontend && npm ci && npm run dev
```

**Docker 模式：**

```bash
cd /root/project/weberpagent
git pull origin main
docker compose up -d --build
```

### 备份与恢复

```bash
# 手动备份
tar czf backup-$(date +%Y%m%d).tar.gz data/ outputs/ .env

# 恢复
tar xzf backup-XXXXXXXX.tar.gz
```

### 日志查看

```bash
# 快速启动模式 — 查看日志文件
tail -f backend.log
tail -f frontend.log

# Docker 模式
docker compose logs -f backend
docker compose logs -f --tail 100 backend
```

### 常见问题

| 问题 | 排查 | 解决 |
|------|------|------|
| 端口被占用 | `lsof -i :11002` 或 `lsof -i :11001` | kill 占用进程 |
| 后端启动失败 | 查看终端错误输出 | 检查 .env、Python 依赖 |
| Playwright 崩溃 | 检查系统依赖 | `playwright install chromium --with-deps` |
| 前端无法连后端 | 检查 11002 端口 | 确认后端已启动、Vite proxy 配置 |
| LLM 调用失败 | 查看后端日志 | 检查 API Key、网络、配额 |
| Docker 前端白屏 | 检查后端日志 | 确认 frontend/dist 存在于镜像中（`docker compose up -d --build` 重建） |
