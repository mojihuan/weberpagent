# Phase 51: 端到端验证 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-28
**Phase:** 51-e2e-verification
**Areas discussed:** 单元测试验证范围, E2E 测试执行方式

---

## 单元测试验证范围

| Option | Description | Selected |
|--------|-------------|----------|
| 全量测试 | 运行所有测试（包括已有），确保回归安全 | ✓ |
| 只跑新增模块 | 只跑 Phase 48-50 新增的 6 个测试文件 | |

**User's choice:** 全量测试
**Notes:** 确保回归安全，不只跑新增模块

### 覆盖率统计范围

| Option | Description | Selected |
|--------|-------------|----------|
| 只看新增模块 | 覆盖率只统计 Phase 48-50 新增的 6 个模块 | ✓ |
| 全 backend 覆盖率 | 统计整个 backend 的覆盖率 | |

**User's choice:** 只看新增模块
**Notes:** REQUIREMENTS.md VAL-01 要求“所有新增模块单元测试覆盖率 >= 80%”

---

## E2E 测试执行方式

| Option | Description | Selected |
|--------|-------------|----------|
| 平台 UI 手动执行 | 通过平台 UI 创建/执行任务，人工判断 | ✓ |
| 脚本直接调用 AgentService | 写 Python 脚本调用 run_with_streaming() | |
| API 自动化脚本 | 前端+后端都测试，自动化断言日志 | |

**User's choice:** 平台 UI 手动执行
**Notes:** 与真实用户使用场景一致

### 测试用例选择

| Option | Description | Selected |
|--------|-------------|----------|
| 复用原测试用例 | 使用 outputs/7fcea593 同一销售出库用例 | ✓ |
| 新建简化测试用例 | 专门为验证创建简化用例 | |
| 用现有任意用例 | 库中现有的任意销售出库用例 | |

**User's choice:** 复用原测试用例
**Notes:** 直接对比改善效果

---

## Claude's Discretion

- 验证成功标准（VAL-02~04）的具体判读方式
- 覆盖率报告生成方式
- 全量测试运行命令

## Deferred Ideas

None — discussion stayed within phase scope.
