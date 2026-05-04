# Phase 129: 测试规划 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-03
**Phase:** 129-测试规划
**Areas discussed:** 测试优先级策略, 测试分层与范围, 输出格式与可操作性

---

## 测试优先级策略

| Option | Description | Selected |
|--------|-------------|----------|
| 严重程度驱动 | 按 Phase 125-128 发现的 Critical > High > Medium > Low 排序 | ✓ |
| 业务影响驱动 | 按核心执行管道优先，工具类后补 | |
| 复合分数 | 修复频率 × 严重度复合得分 | |
| Claude's Discretion | Claude 决定优先级策略 | |

**User's choice:** 严重程度驱动 (Recommended)
**Notes:** 直接保护最高风险区域，与 Phase 125-128 的分级体系一致

---

## 场景输出深度

| Option | Description | Selected |
|--------|-------------|----------|
| 仅输出清单 | review-only，不写代码，不设计 fixtures/mocks | ✓ |
| 清单 + fixture 设计 | 附加 fixture/mock 设计建议 | |
| 清单 + 示例代码模板 | 附带 1-2 个 P0 场景的示例测试代码 | |

**User's choice:** 仅输出清单 (Recommended)
**Notes:** 与 Phase 125-128 保持 review-only 一致性，后续里程碑再实施

---

## 测试分层

| Option | Description | Selected |
|--------|-------------|----------|
| 后端优先 | 单元测试 → 集成测试 → 前端组件测试 → E2E 补充 | ✓ |
| 按业务域分组 | 按管道/Agent/API/前端分组，不区分层级 | |
| 仅单元 + E2E | 只聚焦两层，跳过集成和前端组件测试 | |
| Claude's Discretion | Claude 决定分层策略 | |

**User's choice:** 后端优先 (Recommended)
**Notes:** 后端无测试保护、风险最高，优先建立基线

---

## 场景识别方法

| Option | Description | Selected |
|--------|-------------|----------|
| 从发现推导 | 从 390 条审查发现中筛选可测试验证的部分 | ✓ |
| 边界分析 + 审查交叉 | 独立边界分析再与审查发现交叉验证 | |
| 两者结合 | 先从发现推导，再边界分析补充 | |

**User's choice:** 从发现推导 (Recommended)
**Notes:** 不需要覆盖全部 390 条发现，只识别有回归保护价值的场景

---

## 输出格式

| Option | Description | Selected |
|--------|-------------|----------|
| FINDINGS 格式 | 延续 Phase 125-128 格式，按严重程度分级 | ✓ |
| 测试规格格式 (GWT) | Given-When-Then 描述风格 | |
| Claude's Discretion | Claude 决定格式 | |

**User's choice:** FINDINGS 格式 (Recommended)
**Notes:** 与 Phase 125-128 保持一致，每个场景含名称、描述、发现引用、测试类型、优先级

---

## Claude's Discretion

- 每条发现是否「适合写测试」的判断标准
- 后端单元测试与集成测试的边界划分
- E2E 缺失场景的具体优先级排序
- 最终统计数据和分组方式

## Deferred Ideas

None — discussion stayed within phase scope
