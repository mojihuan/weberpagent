# Phase 37: 云服务器选型 - Context

**Gathered:** 2026-03-23
**Status:** Ready for planning

<domain>
## Phase Boundary

调研、选择并购买符合预算要求的国产云服务器，为后续 Phase 38 部署做准备。

**Scope:**
- 云服务器厂商调研与对比
- 服务器配置选型
- 购买并完成基础初始化

**Out of Scope:**
- 应用部署 (Phase 38)
- 域名配置与 HTTPS (Phase 38)
- 数据库初始化 (Phase 38)

</domain>

<decisions>
## Implementation Decisions

### 云厂商选择
- **D-01:** 云厂商 → **阿里云**
  - 原因: 轻量应用服务器性价比高，新人优惠力度大，国内市场占有率第一

### 地域与网络
- **D-02:** 部署地域 → **华东/华南 (国内)**
  - 约束: 需要 ICP 备案 (约1-2周)
  - 优势: 延迟最低，适合正式生产环境

- **D-03:** 付费模式 → **按月付费**
  - 原因: 灵活度高，可随时停用

### 服务器配置
- **D-04:** 服务器规格 → **2核4G**
  - CPU: 2核
  - 内存: 4GB
  - 带宽: 4Mbps
  - 满足 Playwright 运行需求

- **D-05:** 存储容量 → **60GB SSD** (默认配置)
  - 足够存储测试数据和截图

- **D-06:** 安全组端口 → **SSH(22), HTTP(80), HTTPS(443), API(8080)**
  - 注: API(8080) 可通过 Nginx 反向代理后仅限内网访问

### 交付物
- **D-07:** Phase 交付物 → **调研报告**
  - 包含: 配置对比、价格分析、购买链接、初始化指南

### Claude's Discretion
- 具体购买步骤的详细操作指南
- SSH 登录后的基础环境检查命令
- 安全组规则的详细配置说明

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 项目约束
- `.planning/PROJECT.md` — 项目概述、技术栈、部署约束
- `.planning/REQUIREMENTS.md` — CLOUD-01, CLOUD-02 需求定义

### 已确定的技术决策
- `.planning/STATE.md` — 预算约束 (100元/月以下)、操作系统 (Ubuntu 22.04)、部署架构

</canonical_refs>

<code_context>
## Existing Code Insights

### 无现有代码相关
本阶段为纯调研和采购任务，不涉及代码修改。

### Phase 38 需要的信息
- 服务器 IP 地址
- SSH 登录凭据
- 操作系统版本确认 (Ubuntu 22.04)

</code_context>

<specifics>
## Specific Ideas

- 阿里云轻量应用服务器 2核4G 预计价格约 16.6-25 元/月
- 需要提前准备 ICP 备案材料 (如需使用国内域名)
- 首次购买可享受新人优惠

</specifics>

<deferred>
## Deferred Ideas

None — 讨论保持在阶段范围内。

</deferred>

---

*Phase: 37-cloud-server-selection*
*Context gathered: 2026-03-23*
