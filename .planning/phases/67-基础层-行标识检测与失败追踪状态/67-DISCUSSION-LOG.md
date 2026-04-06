# Phase 67: 基础层 — 行标识检测与失败追踪状态 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-06
**Phase:** 67-基础层-行标识检测与失败追踪状态
**Areas discussed:** backend_node_id 键策略, FailureDetectionResult 结构, 检测集成方式, 测试验证范围

---

## backend_node_id 键策略

| Option | Description | Selected |
|--------|-------------|----------|
| 先用 backend_node_id | 与 browser-use _selector_map 一致，简单直接。Phase 68/69 集成时如果发现问题再切换 | ✓ |
| 直接用复合键 | (tag_name, placeholder, row_identity) 三元组。不依赖 browser-use 内部 ID，但实现复杂 | |
| 双重验证 | 主键 backend_node_id + 额外存储 tag_name+placeholder 校验。混合方案，复杂度中等 | |

**User's choice:** 先用 backend_node_id
**Notes:** STATE.md blocker 指出跨 step 稳定性未验证。决定先走简单路径，集成时如果发现实际问题再切换复合键。避免过早优化。

---

## FailureDetectionResult 结构设计

| Option | Description | Selected |
|--------|-------------|----------|
| 新 frozen dataclass | FailureDetectionResult(failure_mode: str \| None, details: dict)。与 StallResult 平级，由 detect_failure_mode() 返回 | ✓ |
| 扩展 StallResult | 给 StallResult 增加 failure_mode 字段。减少返回类型，但让 StallResult 更复杂 | |
| 枚举 + dataclass | 定义 FailureMode 枚举 + FailureDetectionResult。更类型安全，但增加定义 | |

**User's choice:** 新 frozen dataclass
**Notes:** 遵循 Phase 48 frozen=True 不可变模式。failure_mode 为 None 表示无失败模式检测到。details 因模式而异。

---

## dom_hash 传递与检测集成方式

| Option | Description | Selected |
|--------|-------------|----------|
| 独立方法 | StallDetector 新增 detect_failure_mode() 独立方法，与 check() 平级。签名接收 dom_hash_before 和 dom_hash_after | ✓ |
| 扩展 check() | 修改 check() 签名增加 dom_hash_before 参数，内部同时检测停滞和失败模式 | |
| 新检测器类 | 新增 FailureModeDetector 类，与 StallDetector 平级。完全解耦但增加文件管理 | |

**User's choice:** 独立方法
**Notes:** 职责分离——check() 检测停滞，detect_failure_mode() 检测失败模式。step_callback 每步先调用 check() 再调用 detect_failure_mode()。

---

## 测试验证范围

| Option | Description | Selected |
|--------|-------------|----------|
| 纯单元测试 (mock) | 与 Phase 48 一致，backend_node_id 在 mock 中假设稳定。覆盖 >= 80% | ✓ |
| 单元 + 可选集成 | 增加 Playwright fixture 级别集成测试验证 backend_node_id 稳定性 | |

**User's choice:** 纯单元测试
**Notes:** backend_node_id 稳定性验证留给 Phase 68/69 集成阶段。mock 测试快速可靠。

---

## Claude's Discretion

- _detect_row_identity() 的具体 DOM 遍历实现
- update_failure_tracker() 的参数签名
- FailureDetectionResult.details 的具体字段名
- 单元测试的 mock 数据设计
- 失败模式关键词列表的具体内容

## Deferred Ideas

None — discussion stayed within phase scope.
