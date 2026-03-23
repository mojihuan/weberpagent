# Roadmap: aiDriveUITest

## Milestones

- **v0.4.2 人工验证断言系统** - Phases 33-35 (shipped 2026-03-23)
- **v0.5.0 项目云端部署** - Phases 36-38 (in progress)

## Phases

<details>
<summary>v0.4.2 人工验证断言系统 (Phases 33-35) - SHIPPED 2026-03-23</summary>

### Phase 33: Bug 修复
**Goal**: 修复断言执行中发现的问题
**Plans**: 2 plans

Plans:
- [x] 33-01: 修复字段命名和 Headers 解析问题
- [x] 33-02: 修复时间偏移和 UI 优化

### Phase 34: 断言执行验证
**Goal**: 验证断言系统端到端可用
**Plans**: 1 plan

Plans:
- [x] 34-01: 执行 sell_sale_item_list_assert 验证

### Phase 35: 文档完善
**Goal**: 创建断言系统使用指南
**Plans**: 1 plan

Plans:
- [x] 35-01: 编写断言系统使用指南

</details>

### v0.5.0 项目云端部署 (In Progress)

**Milestone Goal:** 将 aiDriveUITest 项目部署到国产云端服务器，并完成 Git 仓库迁移

#### Phase 36: Git 仓库迁移
**Goal**: 项目代码迁移到用户自己的 Git 仓库，便于云端部署
**Depends on**: Nothing
**Requirements**: GIT-01, GIT-02
**Success Criteria** (what must be TRUE):
  1. 用户可在自己的 Git 仓库中看到 weberpagent 项目代码
  2. 用户可在项目中看到 webseleniumerp 目录并正常引用
  3. `git remote -v` 显示用户的新仓库地址
**Plans**: 2 plans

Plans:
- [ ] 36-01-PLAN.md - 将 Git remote 从当前仓库替换为用户自己的仓库
- [ ] 36-02-PLAN.md - 将 webseleniumerp 复制到项目中作为子目录管理

#### Phase 37: 云服务器选型
**Goal**: 选择并购买符合预算要求的云服务器
**Depends on**: Nothing (可与 Phase 36 并行)
**Requirements**: CLOUD-01, CLOUD-02
**Success Criteria** (what must be TRUE):
  1. 用户可查看调研报告，了解阿里云/腾讯云/华为云的性价比对比
  2. 用户已购买云服务器并可通过 SSH 登录
  3. 云服务器系统为 Ubuntu 22.04
**Plans**: TBD

Plans:
- [ ] 37-01: 调研云服务器方案
- [ ] 37-02: 购买并初始化服务器

#### Phase 38: 部署执行
**Goal**: 将项目完整部署到云端服务器
**Depends on**: Phase 36, Phase 37
**Requirements**: DEPLOY-01, DEPLOY-02, DEPLOY-03, DEPLOY-04
**Success Criteria** (what must be TRUE):
  1. 用户可通过 HTTPS 访问前端页面
  2. API 接口可正常响应（`/api/tasks` 等）
  3. 数据库文件存在且备份脚本配置完成
  4. `systemctl status aidriveuitest` 显示服务 active
**Plans**: TBD

Plans:
- [ ] 38-01: 部署后端服务
- [ ] 38-02: 部署前端服务
- [ ] 38-03: 配置数据库持久化
- [ ] 38-04: 配置 HTTPS 证书

## Progress

**Execution Order:**
Phases 36, 37 可并行执行 - Phase 38

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 36. Git 仓库迁移 | v0.5.0 | 0/2 | Complete    | 2026-03-23 |
| 37. 云服务器选型 | v0.5.0 | 0/2 | Not started | - |
| 38. 部署执行 | v0.5.0 | 0/4 | Not started | - |

---

*Roadmap updated: 2026-03-23 - Phase 36 plans created*
