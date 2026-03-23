# Phase 28: 后端字段发现 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-21
**Phase:** 28-backend-field-discovery
**Areas discussed:** AST解析策略, 字段分组规则, Description生成逻辑, 时间字段识别

---

## AST 解析策略

| Option | Description | Selected |
|--------|-------------|----------|
| 扩展现有 Bridge (推荐) | 在 external_precondition_bridge.py 中新增 parse_assertions_field() 函数 | ✓ |
| 新建独立模块 | 创建新的 backend/core/assertions_field_parser.py 文件 | |

**User's choice:** 扩展现有 Bridge (推荐)
**Notes:** 与现有模式保持一致，减少文件数量

---

## 字段分组规则

| Option | Description | Selected |
|--------|-------------|----------|
| 命名模式推断 (推荐) | sale* → 销售相关，purchase* → 采购相关，*Time/*time → 时间字段，其他 → 通用 | ✓ |
| 不分组 | 全部字段放在一个组，前端自行搜索过滤 | |
| 手动配置分组 | 维护一个 JSON 配置文件定义分组规则 | |

**User's choice:** 命名模式推断 (推荐)
**Notes:** 自动化程度高，维护成本低

---

## Description 生成逻辑

| Option | Description | Selected |
|--------|-------------|----------|
| 关键词映射表 (推荐) | 维护 ~50 个关键词映射，createTime → "创建时间" | ✓ |
| AI 生成 | 调用 LLM 生成中文描述 | |

**User's choice:** 关键词映射表 (推荐)
**Notes:** 确定性输出，无额外 API 成本

---

## 时间字段识别

| Option | Description | Selected |
|--------|-------------|----------|
| 后缀匹配 (推荐) | 字段名以 Time/time/date/Date 结尾的字段视为时间字段 | ✓ |
| 白名单 | 维护一个已知时间字段列表 | |

**User's choice:** 后缀匹配 (推荐)
**Notes:** 简单可靠，覆盖大多数情况

---

## Claude's Discretion

- 关键词映射表的具体条目（约 50 个，可在实现时补充）
- 嵌套字段 path 的具体格式
- 边界情况处理

## Deferred Ideas

None — discussion stayed within phase scope
