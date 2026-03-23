# Phase 31: E2E 测试 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in 31-CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-22
**Phase:** 31-e2e
**Areas discussed:** Mock 策略 + 测试范围, field_params 测试, 与现有测试的关系

---

## Mock 策略

| Option | Description | Selected |
|--------|-------------|----------|
| 环境变量 + 后端 Mock 模式 | E2E 测试设置环境变量，后端检测到 Mock 模式后返回预设数据 | |
| Playwright route 拦截 | 通过 page.route() 拦截 HTTP 请求，但只能 Mock 前端请求 | |
| Python unittest.mock | 在测试中 patch 外部模块，需要修改后端代码 | ✓ |

**User's choice:** 环境变量 + 后端 Mock 模式
**Notes:** 后续讨论中用户更改为使用真实 ERP 环境

---

## Mock 范围

| Option | Description | Selected |
|--------|-------------|----------|
| 仅 Mock headers | 仅 Mock LoginApi.headers 返回测试 token，断言方法仍调用真实 ERP | ✓ |
| Mock 整个断言执行 | Mock 整个断言方法执行，返回预设结果（完全隔离） | |
| 可配置两种模式 | 同时 Mock headers 和断言执行，通过配置选择 | |

**User's choice:** 仅 Mock headers
**Notes:** 最终改为真实 ERP，不需要 Mock

---

## 测试场景

| Option | Description | Selected |
|--------|-------------|----------|
| 断言成功场景 | 所有字段通过，返回 passed: true | ✓ |
| 断言失败场景 | 部分字段失败，展示 expected/actual | |
| 'now' 时间转换 | 验证 'now' 转换为实际时间字符串 | ✓ |
| 三层参数结构 | 验证 data/api_params/field_params 三层结构正确传递 | ✓ |

**User's choice:** 断言成功场景, 'now' 时间转换, 三层参数结构
**Notes:** 断言失败场景已有测试覆盖（Phase 26）

---

## 'now' 时间转换验证方式

| Option | Description | Selected |
|--------|-------------|----------|
| 验证请求体转换 | 检查请求体中 'now' 字段被替换为实际时间字符串 | |
| 验证后端日志 | 直接验证后端日志中的转换结果 | |
| 验证断言结果 | 验证最终断言结果中时间字段通过 | ✓ |

**User's choice:** 我想所有的测试使用真实的场景
**Notes:** 用户希望使用真实 ERP 环境进行测试

---

## 三层参数验证方式

| Option | Description | Selected |
|--------|-------------|----------|
| 通过 UI 填写并验证 | 在前端表单填写三层参数，执行后验证结果 | ✓ |
| 直接调用后端 API | 直接构造 API 请求体，绕过前端 UI | |
| 两者结合 | 两种方式都测试 | |

**User's choice:** 通过 UI 填写并验证
**Notes:** 端到端测试，覆盖完整用户流程

---

## 测试环境

| Option | Description | Selected |
|--------|-------------|----------|
| 真实 ERP | 使用真实 ERP 环境（需要 ERP_BASE_URL） | ✓ |
| Mock ERP | 完全 Mock ERP，不需要真实环境 | |

**User's choice:** 真实 ERP
**Notes:** 与 ROADMAP.md 原计划不同，改为使用真实 ERP

---

## 与现有测试的关系

| Option | Description | Selected |
|--------|-------------|----------|
| 扩展现有文件 | 在 assertion-flow.spec.ts 中添加新测试用例 | ✓ |
| 新建专用文件 | 创建新文件如 assertion-three-layer.spec.ts | |

**User's choice:** 扩展现有文件
**Notes:** 复用现有测试模式和基础设施

---

## Mock ERP 需求（最终确认）

| Option | Description | Selected |
|--------|-------------|----------|
| 移除 Mock 要求（真实 ERP） | 使用真实 ERP，依赖 ERP_BASE_URL 环境变量 | ✓ |
| 同时支持 Mock + 真实 ERP | 保持 ROADMAP 的 Mock 策略，但添加真实 ERP 作为备选 | |

**User's choice:** 移除 Mock 要求（真实 ERP）
**Notes:** 与 Phase 26 一致，使用真实 ERP 环境

---

## 验证方式

| Option | Description | Selected |
|--------|-------------|----------|
| 通过 UI 验证结果 | 在报告页面验证断言结果卡片显示正确 | ✓ |
| 检查 API 响应 | 检查后端 API 响应中的 fields 数组 | |
| 两者结合 | 同时验证 UI 和 API 响应 | |

**User's choice:** 通过 UI 验证结果
**Notes:** 端到端验证，检查报告页面断言结果卡片

---

## Claude's Discretion

- 具体选择哪个断言方法进行测试
- 测试用例的具体实现细节
- 超时设置（建议 5 分钟，与现有测试一致）
- 失败诊断信息格式

## Deferred Ideas

- Mock ERP 模式 — 使用真实 ERP 替代
- 断言失败场景测试 — 已有测试覆盖
- API 响应验证 — 仅通过 UI 验证
