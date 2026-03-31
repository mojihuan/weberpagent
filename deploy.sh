#!/bin/bash
# deploy.sh - 云端部署脚本（在服务器上运行）
# 用法: ./deploy.sh [--backend-only] [--frontend-only] [--skip-build]

set -euo pipefail

# ========== 配置 ==========
PROJECT_PATH="/root/project/weberpagent"
NGINX_ROOT="/var/www/aidriveuitest"
BACKEND_PID_FILE="/tmp/aidriveuitest.pid"
BACKEND_LOG="/tmp/aidriveuitest.log"

# ========== 参数解析 ==========
BACKEND_ONLY=false
FRONTEND_ONLY=false
SKIP_BUILD=false

for arg in "$@"; do
  case $arg in
    --backend-only)  BACKEND_ONLY=true ;;
    --frontend-only) FRONTEND_ONLY=true ;;
    --skip-build)    SKIP_BUILD=true ;;
    --stop)          stop_backend; exit 0 ;;
    --help|-h)
      echo "用法: ./deploy.sh [选项]"
      echo ""
      echo "选项:"
      echo "  --backend-only   只部署后端"
      echo "  --frontend-only  只部署前端"
      echo "  --skip-build     跳过构建，只拉取代码和重启"
      echo "  --stop           停止后端服务"
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

# ========== 后端管理 ==========
stop_backend() {
  if [ -f "$BACKEND_PID_FILE" ]; then
    local pid
    pid=$(cat "$BACKEND_PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
      log "停止后端服务 (PID: $pid)..."
      kill "$pid"
      sleep 1
      if kill -0 "$pid" 2>/dev/null; then
        kill -9 "$pid" 2>/dev/null || true
      fi
      log "后端已停止"
    else
      warn "后端进程不存在，清理 PID 文件"
    fi
    rm -f "$BACKEND_PID_FILE"
  else
    warn "后端未运行"
  fi

  # 同时停掉 systemd 服务（如果存在）
  if systemctl is-active --quiet aidriveuitest 2>/dev/null; then
    log "停止 systemd 服务..."
    systemctl stop aidriveuitest
    systemctl disable aidriveuitest 2>/dev/null || true
  fi
}

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

# ========== 重启后端（uvicorn 直接启动） ==========
if [ "$FRONTEND_ONLY" = false ]; then
  log "重启后端服务..."
  stop_backend

  cd "$PROJECT_PATH"
  nohup uv run uvicorn backend.api.main:app \
    --host 0.0.0.0 \
    --port 8080 \
    > "$BACKEND_LOG" 2>&1 &

  echo $! > "$BACKEND_PID_FILE"
  BACKEND_PID=$(cat "$BACKEND_PID_FILE")

  sleep 3
  if kill -0 "$BACKEND_PID" 2>/dev/null; then
    log "后端服务启动成功 (PID: $BACKEND_PID)"
  else
    err "后端服务启动失败，查看日志: $BACKEND_LOG"
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
sleep 1
HEALTH=$(curl -s http://127.0.0.1/health 2>&1 || echo "FAIL")
echo "Health: $HEALTH"

echo ""
echo "========================================="
echo " 部署完成!"
echo " 前端: http://121.40.191.49"
echo " API:  http://121.40.191.49/api/tasks"
echo " 后端日志: tail -f $BACKEND_LOG"
echo " 停止服务: ./deploy.sh --stop"
echo "========================================="
