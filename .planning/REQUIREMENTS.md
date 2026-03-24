# Requirements: v0.5.0 项目云端部署

**Milestone:** v0.5.0
**Goal:** 将 aiDriveUITest 项目部署到国产云端服务器，并完成 Git 仓库迁移
**Created:** 2026-03-23

## Requirements

### GIT - Git 仓库迁移

- [ ] **GIT-01**: 将 weberpagent 项目 git remote 替换为用户自己的仓库
  - 验收标准: git remote -v 显示用户的新仓库地址

- [ ] **GIT-02**: 将 webseleniumerp 复制到项目中，作为一个项目上传
  - 验收标准: webseleniumerp 目录存在于项目中，代码可正常引用

### CLOUD - 云服务器选型

- [x] **CLOUD-01**: 调研国产云服务器性价比方案 (100元/月以下)
  - 验收标准: 输出调研报告，包含阿里云/腾讯云/华为云对比

- [x] **CLOUD-02**: 选择并购买云服务器
  - 验收标准: 云服务器可 SSH 登录，系统为 Ubuntu 22.04
  - 完成: 2026-03-24

### DEPLOY - 部署执行

- [x] **DEPLOY-01**: 部署后端服务 (FastAPI + Gunicorn + Systemd)
  - 验收标准: systemctl status aidriveuitest 显示 active，API 可访问
  - 完成: 2026-03-24

- [x] **DEPLOY-02**: 部署前端服务 (React + Nginx 静态文件)
  - 验收标准: 访问域名/IP 显示前端页面
  - 完成: 2026-03-24

- [x] **DEPLOY-03**: 配置数据库持久化 (SQLite WAL模式 + 备份)
  - 验收标准: 数据库文件存在，备份脚本配置完成
  - 完成: 2026-03-24

- [x] **DEPLOY-04**: ~~配置 HTTPS 证书~~ (跳过 - 无域名)
  - 原因: 当前无域名，使用 HTTP 访问
  - 未来: 有域名后可用 `certbot --nginx` 配置

## Future Requirements

(暂无)

## Out of Scope

- 用户认证/权限管理 — 单用户使用
- 高可用/负载均衡 — 单服务器足够
- 自动扩缩容 — 预算有限，固定配置
- 域名购买 — 用户自行准备
- 日志轮转 — 可选功能，暂不实施
- 监控告警 — 可选功能，暂不实施

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| GIT-01 | Phase 36 | Complete |
| GIT-02 | Phase 36 | Complete |
| CLOUD-01 | Phase 37 | Complete |
| CLOUD-02 | Phase 37 | Complete |
| DEPLOY-01 | Phase 38 | Complete |
| DEPLOY-02 | Phase 38 | Complete |
| DEPLOY-03 | Phase 38 | Complete |
| DEPLOY-04 | Phase 38 | Skipped (no domain) |

---
*Requirements defined: 2026-03-23*
