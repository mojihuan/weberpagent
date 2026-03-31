#!/bin/bash
# deploy.sh - 云端部署脚本（在服务器上运行）
# 用法: ./deploy.sh [--backend-only] [--frontend-only] [--skip-build]

set -euo pipefail

# ========== 配置 ==========
PROJECT_PATH="/root/project/weberpagent"
NGINX_ROOT="/var/www/aidriveuitest"

# ========== 参数解析 ==========
BACKEND_ONLY=false
FRONTEND_ONLY=false
SKIP_BUILD=false

for arg in "$@"; do
  case $arg in
    --backend-only)  BACKEND_ONLY=true ;;
    --frontend-only) FRONTEND_ONLY=true ;;
    --skip-build)    SKIP_BUILD=true ;;
    --help|-h)
      echo "用法: ./deploy.sh [选项]"
      echo ""
      echo "选项:"
      echo "  --backend-only   只部署后端"
      echo "  --frontend-only  只部署前端"
      echo "  --skip-build     跳过构建，只拉取代码和重启"
      echo "  --help           显示帮助"
      exit 0
      ;;
  esac
done

# ========== 颜色 ==========
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()  { echo -e "${GREEN}[DEPLOY]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err()  { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# ========== 拉取代码 ==========
log "拉取最新代码..."
cd "$PROJECT_PATH"
BEFORE=$(git rev-parse HEAD)
git pull
AFTER=$(git rev-parse HEAD)

if [ "$BEFORE" = "$AFTER" ]; then
  warn "代码没有变化"
else
  log "代码已更新: $(git log --oneline -1)"
fi

# ========== 安装依赖和构建 ==========
if [ "$SKIP_BUILD" = false ]; then
  if [ "$FRONTEND_ONLY" = false ]; then
    log "安装 Python 依赖..."
    uv sync 2>&1 | tail -3
  fi

  if [ "$BACKEND_ONLY" = false ]; then
    log "构建前端..."
    cd "$PROJECT_PATH/frontend"
    npm install --silent 2>&1 | tail -1
    npm run build
  fi
fi

# ========== 重启后端 ==========
if [ "$FRONTEND_ONLY" = false ]; then
  log "重启后端服务..."
  systemctl restart aidriveuitest
  sleep 2
  if systemctl is-active --quiet aidriveuitest; then
    log "后端服务启动成功"
  else
    err "后端服务启动失败，查看日志: journalctl -u aidriveuitest -n 20"
  fi
fi

# ========== 部署前端 ==========
if [ "$BACKEND_ONLY" = false ]; then
  log "部署前端到 Nginx..."
  rm -rf "$NGINX_ROOT"/*
  cp -r "$PROJECT_PATH/frontend/dist/"* "$NGINX_ROOT"/
  systemctl reload nginx
fi

# ========== 健康检查 ==========
log "健康检查..."
sleep 2
HEALTH=$(curl -s http://127.0.0.1/health 2>&1 || echo "FAIL")
echo "Health: $HEALTH"

echo ""
echo "========================================="
echo " 部署完成!"
echo " 前端: http://121.40.191.49"
echo " API:  http://121.40.191.49/api/tasks"
echo "========================================="
