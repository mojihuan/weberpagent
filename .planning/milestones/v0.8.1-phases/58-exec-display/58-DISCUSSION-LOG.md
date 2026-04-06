# Phase 58: 执行步骤展示 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-02
**Phase:** 58-exec-display
**Areas discussed:** 统一时间线数据结构, 步骤外观与信息密度, 交错排序策略, 点击交互与详情展示

---

## 统一时间线数据结构

| Option | Description | Selected |
|--------|-------------|----------|
| 统一 TimelineItem 类型 | 新建联合类型（type: 'step' \| 'precondition' \| 'assertion' + 对应数据），SSE 接收时实时转换 | ✓ |
| 适配复用现有 Step 类型 | 把前置条件/断言映射成 Step 字段，额外信息放扩展字段 | |
| Claude 决定 | 让 Claude 根据代码情况选择 | |

**User's choice:** 统一 TimelineItem 类型
**Notes:** SSE 接收时实时转换为统一数组，不复用现有 Step 类型以保持语义精确

---

## 步骤外观与信息密度

### 内容展示

| Option | Description | Selected |
|--------|-------------|----------|
| 摘要式 | 前置条件显示前 N 个字符 + "..."，断言显示名称/索引标识 | ✓ |
| 完整代码 | 显示完整代码，需折叠 | |
| 极简式 | 只显示"前置条件 #1" | |

**User's choice:** 摘要式
**Notes:** 保持时间线紧凑，详情在展开面板中查看

### 图标与颜色区分

| Option | Description | Selected |
|--------|-------------|----------|
| 不同图标 + 不同颜色 | 前置条件黄色/橙色+文件图标，断言绿色/紫色+盾牌图标 | ✓ |
| 纯文本前缀区分 | 用"[前置]"、"[断言]"文本前缀 | |
| Claude 决定 | 让 Claude 决定具体方案 | |

**User's choice:** 不同图标 + 不同颜色
**Notes:** 与蓝色 UI 步骤形成明确视觉区分

---

## 交错排序策略

| Option | Description | Selected |
|--------|-------------|----------|
| 实时 append | SSE 接收时直接 append 到统一数组，利用后端已有的发送顺序 | ✓ |
| 渲染时合并排序 | 分别存储，渲染时按 index/时间戳排序 | |
| Claude 决定 | 让 Claude 决定 | |

**User's choice:** 实时 append
**Notes:** 后端已按执行顺序发送事件，无需额外排序

---

## 点击交互与详情展示

### 点击行为

| Option | Description | Selected |
|--------|-------------|----------|
| 展开详情面板 | 点击前置条件展开代码+变量输出，点击断言展开代码+结果详情 | ✓ |
| 统一跳转截图 | 所有步骤点击都跳截图面板 | |
| 不可点击 | 前置条件/断言步骤不可点击 | |

**User's choice:** 展开详情面板
**Notes:** UI 步骤保持现有跳转截图行为

### Reasoning 展示

| Option | Description | Selected |
|--------|-------------|----------|
| 不展示推理文本 | 前置条件/断言是代码执行，无 AI 推理过程 | ✓ |
| 预留位置但为空 | 保持统一展开结构 | |
| Claude 决定 | 让 Claude 决定 | |

**User's choice:** 不展示推理文本
**Notes:** 前置条件和断言是代码执行结果，没有 AI 推理过程

---

## Claude's Discretion

- 具体图标选择（Lucide React）
- Tailwind 颜色值
- TimelineItem 类型字段设计
- 代码摘要截取长度
- 展开面板动画

## Deferred Ideas

None — discussion stayed within phase scope
