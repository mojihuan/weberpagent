#!/bin/bash
# deploy.sh - 一键部署到云端服务器
# 用法: ./deploy.sh [--backend-only] [--frontend-only] [--skip-build]

set -euo pipefail

# ========== 配置 ==========
SERVER="serverAli"
REMOTE_PATH="/root/project/weberpagent"
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
      echo "  --skip-build     跳过构建，只同步代码和重启"
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

# ========== 检查 SSH 连接 ==========
log "检查 SSH 连接..."
if ! ssh -o ConnectTimeout=5 -o BatchMode=yes "$SERVER" "echo ok" &>/dev/null; then
  err "无法连接到 $SERVER。请先运行: ssh-copy-id $SERVER"
fi
log "SSH 连接正常"

# ========== 同步代码 ==========
log "同步代码到服务器..."

RSYNC_EXCLUDES=(
  --exclude '.git'
  --exclude '.env'
  --exclude 'node_modules'
  --exclude '__pycache__'
  --exclude '.venv'
  --exclude 'data/'
  --exclude '.planning/'
  --exclude '.claude/'
  --exclude 'screenshots/'
  --exclude 'test-results/'
  --exclude '.mcp.json'
  --exclude 'outputs/'
  --exclude '_backup/'
  --exclude '_documents/'
  --exclude '*.egg-info'
)

rsync -avz --delete "${RSYNC_EXCLUDES[@]}" \
  "${PWD}/" "${SERVER}:${REMOTE_PATH}/"

log "代码同步完成"

# ========== 远程构建和部署 ==========
REMOTE_SCRIPT='set -e'

if [ "$SKIP_BUILD" = false ]; then
  if [ "$FRONTEND_ONLY" = false ]; then
    REMOTE_SCRIPT+='
echo "[DEPLOY] 安装 Python 依赖..."
cd '"$REMOTE_PATH"'
uv sync 2>&1 | tail -1'
  fi

  if [ "$BACKEND_ONLY" = false ]; then
    REMOTE_SCRIPT+='
echo "[DEPLOY] 构建前端..."
cd '"$REMOTE_PATH"'/frontend
npm install --silent 2>&1 | tail -1
npm run build'
  fi
fi

if [ "$FRONTEND_ONLY" = false ]; then
  REMOTE_SCRIPT+='
echo "[DEPLOY] 重启后端服务..."
systemctl restart aidriveuitest
sleep 2
if systemctl is-active --quiet aidriveuitest; then
  echo "[DEPLOY] 后端服务启动成功"
else
  echo "[ERROR] 后端服务启动失败，查看日志: journalctl -u aidriveuitest -n 20"
  exit 1
fi'
fi

if [ "$BACKEND_ONLY" = false ]; then
  REMOTE_SCRIPT+='
echo "[DEPLOY] 部署前端到 Nginx..."
rm -rf '"$NGINX_ROOT"'/*
cp -r '"$REMOTE_PATH"'/frontend/dist/* '"$NGINX_ROOT"'/
systemctl reload nginx'
fi

REMOTE_SCRIPT+='
echo "[DEPLOY] 健康检查..."
sleep 2
HEALTH=$(curl -s http://127.0.0.1/health || echo "FAIL")
echo "Health: $HEALTH"

echo ""
echo "========================================="
echo " 部署完成!"
echo " 前端: http://121.40.191.49"
echo " API:  http://121.40.191.49/api/tasks"
echo "========================================="'

log "执行远程部署..."
ssh "$SERVER" "$REMOTE_SCRIPT"

log "部署完成!"
