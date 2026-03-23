# Phase 37: 云服务器选型 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-23
**Phase:** 37-cloud-server-selection
**Areas discussed:** 厂商选择, 地域选择, 付费模式, 存储配置, 安全组配置, 服务器规格, 带宽配置, 交付物

---

## 云厂商选择

| Option | Description | Selected |
|--------|-------------|----------|
| 阿里云 | 轻量应用服务器 2核4G 约 16.6元/月，新人优惠力度大，国内市场占有率第一 | ✓ |
| 腾讯云 | 轻量云 2核4G 约 19元/月，微信集成方便，但价格略高 | |
| 华为云 | HECS云耀 2核4G 约 21元/月，政企客户较多，价格偏高 | |
| 三家都调研 | 调研报告同时对比三家，最终由您决定 | |

**User's choice:** 阿里云
**Notes:** 无

---

## 地域选择

| Option | Description | Selected |
|--------|-------------|----------|
| 华东/华南 (国内) | 延迟最低，但需要完成 ICP 备案（约1-2周），适合正式生产环境 | ✓ |
| 香港/新加坡 (海外) | 无需 ICP 备案，可直接使用，但延迟略高（50-100ms），适合测试/开发 | |
| 华北2 (北京) | 延迟和备案均可接受，面向全国用户 | |

**User's choice:** 华东/华南 (国内)
**Notes:** 需要完成 ICP 备案

---

## 付费模式

| Option | Description | Selected |
|--------|-------------|----------|
| 包年 | 新人优惠价更低，但需要一次性支付，适合确定长期使用的场景 | |
| 按月付费 | 灵活度高，可随时停用，但单价略高，适合试水或不确定的场景 | ✓ |

**User's choice:** 按月付费
**Notes:** 灵活度优先

---

## 存储配置

| Option | Description | Selected |
|--------|-------------|----------|
| 60GB (默认) | 轻量应用服务器默认 60GB SSD，足够测试数据存储 | ✓ |
| 100GB+ | 数据量较大或需要保留更多测试记录/截图 | |
| 系统盘 + 数据盘分离 | 系统盘 60GB + 数据盘，便于数据迁移和备份 | |

**User's choice:** 60GB (默认)
**Notes:** 无

---

## 安全组配置

| Option | Description | Selected |
|--------|-------------|----------|
| SSH (22) | 远程管理服务器必须开放 | ✓ |
| HTTP (80) | HTTP 访问，用于前端页面 | ✓ |
| HTTPS (443) | HTTPS 访问，配置 SSL 证书后使用 | ✓ |
| API (8080) | 后端 API 端口，通过 Nginx 代理则无需开放 | ✓ |

**User's choice:** 全部开放 (SSH/HTTP/HTTPS/API)
**Notes:** API(8080) 可通过 Nginx 反向代理后仅限内网访问以提高安全性

---

## 服务器规格

| Option | Description | Selected |
|--------|-------------|----------|
| 2核4G (推荐) | 2核 CPU + 4GB 内存 + 4Mbps 带宽，满足 Playwright 运行需求 | ✓ |
| 2核2G (经济型) | 2核 CPU + 2GB 内存，可运行但内存紧张，不推荐 | |
| 4核8G (高性能) | 4核 CPU + 8GB 内存，性能充裕但超预算 (约60元/月) | |

**User's choice:** 2核4G (推荐)
**Notes:** 无

---

## 带宽配置

| Option | Description | Selected |
|--------|-------------|----------|
| 4Mbps (默认) | 轻量服务器默认带宽，足够测试平台使用 | ✓ |
| 6-10Mbps | 需要上传大量截图或测试视频时考虑 | |

**User's choice:** 4Mbps (默认)
**Notes:** 无

---

## 交付物

| Option | Description | Selected |
|--------|-------------|----------|
| 调研报告 | 输出详细调研报告，包含配置、价格、购买链接 | ✓ |
| 调研报告 + 初始化脚本 | 调研报告 + 服务器初始化 Shell 脚本 | |

**User's choice:** 调研报告
**Notes:** 无

---

## Claude's Discretion

- 具体购买步骤的详细操作指南
- SSH 登录后的基础环境检查命令
- 安全组规则的详细配置说明

## Deferred Ideas

None — 讨论保持在阶段范围内。
