# Phase 68: DOM Patch 增强 — 行标识注入与策略标注 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-07
**Phase:** 68-DOM Patch 增强
**Areas discussed:** 序列化注入方式, 标注格式设计, 策略层级命名, backend_node_id 稳定性风险

---

## 序列化注入方式

| Option | Description | Selected |
|--------|-------------|----------|
| 两阶段注入（推荐） | 树构建设属性 + 序列化输出注入注释。职责分离，两部分分别在树构建和文本生成阶段工作 | ✓ |
| 纯文本后处理 | 全部在序列化后处理：生成 DOM dump 文本后，扫描模式插入注释。简单但脆弱 | |
| 纯 DOM 树属性 | 所有注入在 DOM 树构建阶段完成。最自然但受序列化器限制 | |

**User's choice:** 两阶段注入
**Notes:** 职责分离清晰，Patch 4 负责判定，Patch 6/7 负责文本注入

---

## 标注格式

| Option | Description | Selected |
|--------|-------------|----------|
| 统一注释格式（推荐） | HTML 注释：行标识、行归属+策略、失败标注统一 `<!-- ... -->` 格式 | ✓ |
| 属性键值格式 | HTML 属性 data-row-identity / data-strategy / data-failure | |

**User's choice:** 统一注释格式
**Notes:** 注释格式不干扰 DOM 结构，Agent 自然语言理解可识别

---

## 策略层级命名

| Option | Description | Selected |
|--------|-------------|----------|
| 描述性命名（推荐） | 策略1-原生 input、策略2-需先 click、策略3-evaluate JS。描述性强，Agent 看即懂 | ✓ |
| 简洁编号 | S1/S2/S3，简洁但不自解释 | |

**User's choice:** 描述性命名
**Notes:** Agent 无需额外规则即可理解各策略的操作方式

---

## backend_node_id 稳定性风险

| Option | Description | Selected |
|--------|-------------|----------|
| Phase 69 验证（推荐） | Phase 68 假设稳定，集成时验证。若不稳定 Phase 69 切换复合键 | ✓ |
| Phase 68 内验证 | Phase 68 增加集成测试验证稳定性 | |
| 预先实现复合键 | 直接在 Phase 68 实现复合键回退逻辑 | |

**User's choice:** Phase 69 验证
**Notes:** 避免过早优化，Phase 67/68 均用 mock 假设稳定

---

## Claude's Discretion

- Patch 4 wrapper 的具体扩展方式（如何设置临时属性）
- 序列化方法包裹的具体实现（哪个方法、注入位置）
- 策略判定的具体条件（snapshot_node 存在性检查）
- Patch 6 和 Patch 7 的注册顺序
- 单元测试的 mock 数据设计

## Deferred Ideas

None — discussion stayed within phase scope.
