# Phase 61: E2E 验证 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-02
**Phase:** 61-e2e
**Areas discussed:** 测试用例设计, 验证方法与环境, 通过标准与结果记录, 预检查

---

## 测试用例设计

| Option | Description | Selected |
|--------|-------------|----------|
| 一个综合用例 | 创建一个包含前置条件+断言的测试任务，执行一次覆盖 Phase 57-60 全部功能 | ✓ |
| 多个专项用例 | 创建多个分别针对每个 Phase 功能的测试用例 | |
| 复用已有用例 | 复用 Phase 56 的已有 ERP 测试用例，加前置条件+断言 | |

**User's choice:** 一个综合用例
**Notes:** 采购场景（如采购入库），配置前置条件（查询供应商信息）+ 业务断言（验证入库数量）

## 验证方法与环境

| Option | Description | Selected |
|--------|-------------|----------|
| 本地开发机 | 方便查看日志和调试，与 Phase 56 一致 | ✓ |
| 云服务器 | 在线上环境验证，更接近真实场景 | |

| Option | Description | Selected |
|--------|-------------|----------|
| 手动 UI 验证 | 通过平台 UI 创建/执行任务，人工判断 | ✓ |
| 自动化+手动结合 | 先跑自动化测试再手动验证 | |

**User's choice:** 本地开发机 + 手动 UI 验证
**Notes:** 与 Phase 51/56 验证模式一致

## 通过标准与结果记录

| Option | Description | Selected |
|--------|-------------|----------|
| 按 Success Criteria 逐条验证 | 对应 ROADMAP 的 4 条 Success Criteria 逐条检查 | ✓ |
| 粗粒度验证 | 只看核心流程能否跑通 | |

| Option | Description | Selected |
|--------|-------------|----------|
| 验证结果文档 | 在 docs/test-steps/ 下新建文档记录 | ✓ |
| 仅 VERIFICATION.md | 只用结构化验证文件 | |

**User's choice:** 按 Success Criteria 逐条验证 + 验证结果文档

## 预检查

| Option | Description | Selected |
|--------|-------------|----------|
| 先跑自动化检查 | pytest + 前端 build 确保代码层面无回归 | ✓ |
| 跳过，直接 E2E | 直接开始手动验证 | |

**User's choice:** 先跑自动化检查

## Claude's Discretion

- 综合测试用例的具体测试步骤描述
- 验证结果文档的具体格式
- 失败原因分析的具体深度

## Deferred Ideas

None — discussion stayed within phase scope
