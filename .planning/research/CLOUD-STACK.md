# Stack Research: 云端部署基础设施

**Domain:** Cloud Server Deployment (国产云服务器)
**Researched:** 2026-03-23
**Confidence:** HIGH (Multiple official sources + community verification)

## Executive Summary

为 aiDriveUITest 项目在 100元/月 预算下实现云端部署，推荐使用 **阿里云轻量应用服务器 2核4G** (约16.6元/月) 配合 **Ubuntu 22.04 LTS**。此配置可稳定运行 Playwright Chromium 单实例，满足项目需求。

## Recommended Stack

### Core Infrastructure

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| **阿里云轻量应用服务器** | 2核4G | 云服务器 | 新用户首购9.9元/月或199元/年，流量不限量，性价比最高 |
| **Ubuntu Server** | 22.04 LTS | 操作系统 | Playwright官方明确支持，`install-deps`兼容性最佳 |
| **Python** | 3.11+ | 运行时 | 与项目当前版本一致，Playwright支持良好 |
| **Gunicorn** | 21.x+ | WSGI进程管理 | 生产级进程管理，支持UvicornWorker异步模式 |
| **Nginx** | 1.24+ | 反向代理 | SSE支持（需关闭buffering），静态文件服务，SSL终止 |

### Supporting Components

| Component | Version | Purpose | When to Use |
|-----------|---------|---------|-------------|
| **uvicorn[standard]** | 0.27+ | ASGI服务器 | 配合Gunicorn使用，支持热重载 |
| **systemd** | 内置 | 服务管理 | 开机自启、故障自动恢复、日志管理 |
| **playwright** | 1.40+ | 浏览器自动化 | 项目核心依赖，需安装Chromium |

### Optional Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| **certbot** | HTTPS证书 | Let's Encrypt免费证书 |
| **logrotate** | 日志轮转 | 防止日志文件过大 |
| **cron** | 定时备份 | SQLite数据库备份 |

## Server Specifications

### Minimum Configuration (100元/月以下)

| 厂商 | 配置 | 价格 | 带宽 | 流量 | 推荐度 |
|------|------|------|------|------|--------|
| **阿里云轻量** | 2核2G | 38-68元/年 | 200M | 不限量 | 低内存不推荐 |
| **阿里云轻量** | 2核4G | 199元/年 (约16.6元/月) | 5-6M | 不限量 | **推荐** |
| **腾讯云轻量** | 2核4G | 约199元/年 | 6M | 300G/月限制 | 备选 |
| **华为云** | 2核4G | 约100-200元/年 | 一般 | 视套餐 | 安全优先选 |

### Resource Requirements for Playwright

| 资源 | 最低配置 | 推荐配置 | 说明 |
|------|---------|---------|------|
| CPU | 2核 | 2核+ | 单任务足够，并发需更多 |
| 内存 | 4GB | 8GB+ | 每个Chromium实例约500MB-1GB |
| 存储 | 40GB | 50GB+ | 系统+Playwright浏览器约2-3GB |
| 带宽 | 5Mbps | 10Mbps+ | 影响页面加载速度 |

### Concurrency Limits (2核4G)

| 场景 | 并发数 | 状态 |
|------|--------|------|
| 单任务执行 | 1 | 完全OK |
| 低并发 | 3-5实例 | 勉强够用 |
| 高并发 | 10+ | 不推荐，需升级8G |

## Installation

### 1. 系统依赖 (Ubuntu 22.04)

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装基础工具
sudo apt install -y curl git build-essential

# 安装 Python 3.11+
sudo apt install -y python3.11 python3.11-venv python3-pip

# 安装 Playwright 浏览器依赖
sudo apt install -y \
  libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
  libcups2 libdrm2 libxkbcommon0 libxcomposite1 \
  libxdamage1 libxfixes3 libxrandr2 libgbm1 \
  libasound2 libpango-1.0-0 libcairo2

# 或使用 Playwright 自动安装
# uv run playwright install-deps chromium
```

### 2. 项目部署

```bash
# 克隆项目
git clone <your-repo> /opt/aidriveuitest
cd /opt/aidriveuitest

# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装依赖
uv sync

# 安装 Playwright Chromium
uv run playwright install chromium
```

### 3. Gunicorn 配置

```python
# /opt/aidriveuitest/gunicorn.conf.py
import multiprocessing

bind = "127.0.0.1:8080"
workers = 2  # 2核CPU建议2-4个worker
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120  # Playwright执行可能较慢
keepalive = 5
max_requests = 1000  # 防止内存泄漏
max_requests_jitter = 50
```

### 4. Systemd 服务配置

```ini
# /etc/systemd/system/aidriveuitest.service
[Unit]
Description=aiDriveUITest API Server
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/aidriveuitest
Environment="PATH=/opt/aidriveuitest/.venv/bin"
Environment="DASHSCOPE_API_KEY=sk-xxx"
Environment="ERP_BASE_URL=https://your-erp.com"
Environment="ERP_USERNAME=xxx"
Environment="ERP_PASSWORD=xxx"
ExecStart=/opt/aidriveuitest/.venv/bin/gunicorn \
  -c gunicorn.conf.py \
  backend.api.main:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
# 启用服务
sudo systemctl daemon-reload
sudo systemctl enable aidriveuitest
sudo systemctl start aidriveuitest
```

### 5. Nginx 配置 (支持SSE)

```nginx
# /etc/nginx/sites-available/aidriveuitest
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /opt/aidriveuitest/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API 反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:8080/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # SSE 端点 (关键配置)
    location ~ ^/api/.*stream|/api/.*events {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Connection '';
        proxy_buffering off;       # 关键：关闭缓冲
        proxy_cache off;           # 关键：关闭缓存
        proxy_read_timeout 86400s; # 长连接超时
        proxy_send_timeout 86400s;
        chunked_transfer_encoding on;
    }
}
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| 阿里云轻量 | 腾讯云轻量 | 音视频业务、需要腾讯生态集成 |
| 阿里云轻量 | 华为云 | 政企项目、安全合规要求高 |
| Ubuntu 22.04 | Rocky Linux 9 | 必须用RHEL系，愿意自行解决Playwright依赖 |
| systemd | Supervisor | 更简单的进程管理需求 |
| SQLite | PostgreSQL | 数据量超过500GB、需要高并发写入 |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| **CentOS 7/8** | Playwright依赖缺失，官方不推荐 | Ubuntu 22.04 LTS |
| **1核1G配置** | Chromium启动即崩溃 | 2核4G起 |
| **2核2G配置** | 内存不足，Chromium+后端+系统会OOM | 2核4G起 |
| **Windows Server** | Playwright部署复杂，依赖问题多 | Ubuntu 22.04 |
| **共享主机/VPS低配** | 无法安装浏览器依赖 | 独立云服务器 |

## Budget Allocation (100元/月)

| 项目 | 月费用 | 年费用 | 说明 |
|------|--------|--------|------|
| 阿里云轻量2核4G | ~16.6元 | 199元 | 新用户首购年付 |
| 域名 (.com) | ~5元 | 55-60元 | 可选，阿里云优惠 |
| HTTPS证书 | 0 | 0 | Let's Encrypt免费 |
| **总计** | **~22元** | **~260元** | 远低于100元/月预算 |

**省钱技巧:**
1. 选择年付享受新用户优惠
2. 关注阿里云双11、618等大促活动
3. 使用免费HTTPS证书(Let's Encrypt)

## Stack Patterns by Variant

**If 预算极度紧张 (<50元/年):**
- 使用阿里云2核2G (38-68元/年)
- 限制单任务执行，禁用并发
- 风险: 内存可能不足，需密切监控

**If 需要高可用 (生产环境):**
- 升级到2核8G配置
- 配置自动备份策略
- 考虑负载均衡+多实例

**If 需要更高并发:**
- 升级到4核16G
- 使用Redis缓存会话
- 实现任务队列(如Celery)

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| Python 3.11 | Playwright 1.40+ | 项目当前配置 |
| Playwright 1.40+ | Chromium 最新版 | 自动下载对应版本 |
| Gunicorn 21+ | Uvicorn 0.27+ | UvicornWorker模式 |
| Nginx 1.24+ | SSE/WebSocket | 需关闭proxy_buffering |

## SQLite Persistence Strategy

### Backup Configuration

```bash
# /etc/cron.daily/sqlite-backup
#!/bin/bash
BACKUP_DIR="/var/backups/aidriveuitest"
DB_FILE="/opt/aidriveuitest/backend/data/database.db"
DATE=$(date +%Y%m%d)

mkdir -p $BACKUP_DIR

# 使用 sqlite3 在线备份
sqlite3 $DB_FILE ".backup '$BACKUP_DIR/database_$DATE.db'"

# 保留最近7天备份
find $BACKUP_DIR -name "database_*.db" -mtime +7 -delete
```

### WAL Mode Configuration

```python
# 在数据库初始化时启用 WAL 模式
from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()
```

## Pre-Deployment Checklist

- [ ] 云服务器购买并配置安全组(开放80/443/22端口)
- [ ] Ubuntu 22.04 系统更新完成
- [ ] Python 3.11+ 安装验证
- [ ] Playwright Chromium 依赖安装完成
- [ ] 项目代码部署并依赖安装
- [ ] 环境变量配置(DASHSCOPE_API_KEY等)
- [ ] Gunicorn + Systemd 服务配置
- [ ] Nginx 反向代理配置(含SSE支持)
- [ ] 前端静态文件构建(npm run build)
- [ ] SQLite数据库目录权限配置
- [ ] 日志轮转配置
- [ ] 备份策略配置

## Security Configuration

### Firewall (ufw)

```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### File Permissions

```bash
# 设置项目目录权限
sudo chown -R www-data:www-data /opt/aidriveuitest
sudo chmod 750 /opt/aidriveuitest/backend/data
sudo chmod 640 /opt/aidriveuitest/backend/data/database.db
```

## Sources

- [阿里云2026年新人优惠政策](https://developer.aliyun.com/article/1716986) - 价格信息 (HIGH confidence)
- [阿里云2核4G服务器2026年活动价](http://www.aliyunminisite.com/16046.html) - 价格信息 (HIGH confidence)
- [Playwright官方文档 - Browsers](https://playwright.dev/docs/browsers) - 系统依赖 (HIGH confidence)
- [Playwright中文文档 - 版本说明](https://playwright.net.cn/docs/release-notes) - Chrome for Testing变更 (HIGH confidence)
- [Nginx反代导致SSE延迟变高的问题与解决方法](https://jia.je/devops/2026/03/05/nginx-sse-buffering/) - SSE配置 (HIGH confidence)
- [Gunicorn部署FastAPI生产环境实践](https://comate.baidu.com/zh/page/zj148cdtlws) - 部署方案 (MEDIUM confidence)
- [CentOS不推荐使用说明](https://blog.csdn.net/YYSonic407/article/details/139422632) - 系统选择 (MEDIUM confidence)
- [SQLite云服务器选型指南](https://cloud.baidu.com/article/4115232) - 持久化策略 (MEDIUM confidence)

---
*Stack research for: 云端部署基础设施*
*Researched: 2026-03-23*
