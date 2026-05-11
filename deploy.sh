#!/usr/bin/env bash
set -euo pipefail

# ── Colors ──────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ── Defaults ────────────────────────────────────────────────────────────────
BACKEND=false
FRONTEND=false
SKIP_BUILD=false
DOCKER=false
DEPLOY_ALL=true

# ── Help ────────────────────────────────────────────────────────────────────
show_help() {
    cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Deploy aiDriveUITest to production server.

Options:
  --backend-only   Only update backend (git pull + uv sync + systemctl restart)
  --frontend-only  Only update frontend (git pull + npm ci + build + copy)
  --skip-build     Skip frontend build step
  --docker         Use Docker Compose mode (git pull + docker compose up)
  --help           Show this help message

Default (no flags): deploy both backend and frontend via systemd.

Examples:
  $(basename "$0")                    # Deploy everything (systemd)
  $(basename "$0") --backend-only     # Only backend
  $(basename "$0") --frontend-only    # Only frontend
  $(basename "$0") --docker           # Deploy via Docker Compose
  $(basename "$0") --skip-build       # Backend only, skip frontend build
EOF
    exit 0
}

# ── Parse arguments ─────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
    case "$1" in
        --backend-only)
            BACKEND=true
            DEPLOY_ALL=false
            shift
            ;;
        --frontend-only)
            FRONTEND=true
            DEPLOY_ALL=false
            shift
            ;;
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        --docker)
            DOCKER=true
            shift
            ;;
        --help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            show_help
            ;;
    esac
done

if [[ "$DEPLOY_ALL" == true ]]; then
    BACKEND=true
    FRONTEND=true
fi

# ── Utility functions ───────────────────────────────────────────────────────
info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $*"; exit 1; }

step() {
    echo ""
    echo -e "${CYAN}──────────────────────────────────────────────────${NC}"
    echo -e "${CYAN}  $*${NC}"
    echo -e "${CYAN}──────────────────────────────────────────────────${NC}"
}

# ── Pre-flight checks ───────────────────────────────────────────────────────
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

info "Project directory: $PROJECT_DIR"

if [[ "$DOCKER" == true ]]; then
    command -v docker >/dev/null 2>&1 || fail "docker is not installed"
fi

# ── Docker deployment ───────────────────────────────────────────────────────
if [[ "$DOCKER" == true ]]; then
    step "Docker Compose Deployment"

    info "Pulling latest code..."
    git pull origin main

    info "Building and starting containers..."
    docker compose up -d --build

    info "Waiting for services to become healthy..."
    sleep 5

    if docker compose ps | grep -q "running"; then
        ok "Containers are running"
        docker compose ps
    else
        fail "Containers failed to start. Check logs: docker compose logs"
    fi

    echo ""
    ok "Docker deployment complete!"
    info "App: http://121.40.191.49"
    exit 0
fi

# ── Systemd deployment ──────────────────────────────────────────────────────
step "Pulling latest code"
git pull origin main
ok "Code updated"

# ── Backend ─────────────────────────────────────────────────────────────────
if [[ "$BACKEND" == true ]]; then
    step "Backend Deployment"

    info "Syncing Python dependencies..."
    uv sync
    ok "Dependencies synced"

    info "Restarting backend service..."
    sudo systemctl restart aidriveuitest
    sleep 3

    if sudo systemctl is-active --quiet aidriveuitest; then
        ok "Backend service is active"
    else
        fail "Backend service failed to start. Check: sudo systemctl status aidriveuitest"
    fi
fi

# ── Frontend ────────────────────────────────────────────────────────────────
if [[ "$FRONTEND" == true && "$SKIP_BUILD" == false ]]; then
    step "Frontend Build"

    info "Installing frontend dependencies..."
    cd frontend
    npm ci
    ok "Dependencies installed"

    info "Building frontend..."
    npm run build
    cd "$PROJECT_DIR"
    ok "Frontend built"

    info "Deploying to /var/www/aidriveuitest/..."
    sudo rm -rf /var/www/aidriveuitest/*
    sudo cp -r frontend/dist/* /var/www/aidriveuitest/
    ok "Frontend deployed to /var/www/aidriveuitest/"

    if command -v systemctl >/dev/null 2>&1; then
        sudo systemctl reload nginx 2>/dev/null && ok "Nginx reloaded" || true
    fi
fi

if [[ "$FRONTEND" == true && "$SKIP_BUILD" == true ]]; then
    warn "Frontend build skipped (--skip-build)"
fi

# ── Summary ─────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN}  Deployment complete!${NC}"
echo -e "${GREEN}====================================================${NC}"

if [[ "$BACKEND" == true ]]; then
    info "Backend:  http://121.40.191.49:11002"
fi
if [[ "$FRONTEND" == true && "$SKIP_BUILD" == false ]]; then
    info "Frontend: http://121.40.191.49"
fi

echo ""
