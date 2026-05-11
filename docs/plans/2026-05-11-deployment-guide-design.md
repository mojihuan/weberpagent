# 部署指南设计

## 目标

为团队成员编写通用部署指南，使其能从零在任意 Ubuntu 服务器上部署 aiDriveUITest 平台。

## 目标受众

团队成员（有 Linux 基础的开发者）

## 输出位置

`docs/deployment.md` — 项目文档的一部分，Git 追踪

## 方案

分层式部署指南：先快后深，兼顾效率和排查需求。

## 文档结构

### 1. 环境要求

- 硬件最低要求：2 核 CPU、4GB 内存、20GB 磁盘
- 操作系统：Ubuntu 22.04/24.04 LTS
- 软件依赖：Python 3.11+、Node.js 20+、uv、Playwright + Chromium、nginx
- 网络要求：需能访问 DashScope API 和目标 ERP 系统

### 2. 快速部署（systemd + nginx）

10 步完成从零部署：

1. 安装系统依赖（Python、Node.js、nginx、uv）
2. 克隆项目 + 子模块初始化
3. 配置环境变量（.env）
4. 安装 Python 依赖（uv sync）
5. 安装 Playwright 浏览器
6. 初始化数据库（首次启动自动执行）
7. 构建前端（npm ci && npm run build）
8. 部署前端静态文件到 /var/www/
9. 配置后端 systemd 服务
10. 配置 nginx 站点

每步包含完整命令和注意事项。

### 3. Docker 部署（可选）

- Dockerfile（多阶段构建）
- docker-compose.yml（后端 + nginx）
- 数据卷挂载（data/、outputs/）
- 环境变量配置
- 一键启动命令

### 4. 配置详解

- .env 环境变量分组说明
- systemd 配置关键参数（workers、timeout、keep-alive）
- nginx 配置（SSE、SPA 路由、静态缓存）
- 前端生产环境配置
- 外部模块集成（WEBSERP_PATH）

### 5. 运维操作

- 更新部署流程
- 备份与恢复
- 日志查看
- 常见问题排查（端口占用、Playwright 崩溃、SQLite 锁定、SSE 断连）

## 额外产出

除了 `docs/deployment.md` 文档外，实施阶段还需创建：

- `Dockerfile` — 项目根目录
- `docker-compose.yml` — 项目根目录
- `deploy.sh` — 项目根目录（简化的更新部署脚本）

## 依赖

- 现有 memory 中的部署记录（deployment-v0.5.0.md）提供参考配置
- 项目 .env.example 提供环境变量模板
