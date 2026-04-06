# Phase 66: 优化方案设计 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-06
**Phase:** 66-优化方案设计
**Areas discussed:** 文档格式与深度, 优化方案实施层级, 按行定位策略, 反重复与失败恢复策略

---

## 设计文档格式与深度

| Option | Description | Selected |
|--------|-------------|----------|
| 规则表 + 任务清单 | 每项优化用统一模板：目标 → 规则表（条件/动作/示例）→ 集成点 → 任务清单 | ✓ |
| 流程图 + 伪代码 | 流程描述 + 决策树 + 关键代码伪代码 | |
| 文字描述 + 判定表 | 类似 Phase 65 分析报告风格 | |

**User's choice:** 规则表 + 任务清单
**Notes:** 表格驱动格式，直接可映射为代码任务

### 文档位置

| Option | Description | Selected |
|--------|-------------|----------|
| .planning/phases/66/ | 与 Phase 65 报告平级，分析类产物统一在 .planning/ | ✓ |
| docs/ 正式文档 | 放在 docs/ 下作为正式设计文档 | |
| .planning/ + docs/ 双版本 | 详细设计在 .planning/，摘要版在 docs/ | |

**User's choice:** .planning/phases/66/

### 文档粒度

| Option | Description | Selected |
|--------|-------------|----------|
| 单文件统一设计 | 四项优化统一放在一个 66-OPTIMIZE-DESIGN.md | ✓ |
| 每项优化单独文件 | 每项优化一个文件 | |
| 按相关性分两个文件 | 定位+策略 和 防护+恢复 分开 | |

**User's choice:** 单文件统一设计

---

## 优化方案实施层级

| Option | Description | Selected |
|--------|-------------|----------|
| DOM Patch + Prompt 两层 | 不新增模块，在现有两层上增强 | ✓ |
| 新增独立中间层模块 | 新模块在 AgentService 和 browser-use 之间 | |
| 扩展现有监控模块 | 在 StallDetector 框架上扩展 | |

**User's choice:** DOM Patch + Prompt 两层

### DOM Patch 文件位置

| Option | Description | Selected |
|--------|-------------|----------|
| 融入现有 dom_patch.py | 新增 patch 函数，保持单文件 | ✓ |
| 新建 erp_table_optimizer.py | 与 dom_patch.py 并行，关注点分离 | |

**User's choice:** 融入现有 dom_patch.py

### Prompt 调整方式

| Option | Description | Selected |
|--------|-------------|----------|
| 追加新规则到 Section 9 | 保留现有内容，追加优化指导 | ✓ |
| 重写 Section 9 | 整合现有指导和新规则 | |

**User's choice:** 追加新规则到 Section 9

---

## 按行定位策略

| Option | Description | Selected |
|--------|-------------|----------|
| DOM Patch 标记行标识 | 为每个 <tr> 添加商品标识，类似 Patch 5 | ✓ |
| 纯 Prompt 指导识别 | Prompt 指导 Agent 通过文本自行识别行 | |
| DOM Patch 结构化 + Prompt 引导 | 双层协作 | |

**User's choice:** DOM Patch 标记行标识

### 行标识符选择

| Option | Description | Selected |
|--------|-------------|----------|
| 商品编号/IMEI 文本 | 唯一标识，出现在特定 <td> 中 | ✓ |
| 行序号 | 给 <tr> 分配序号，语义弱 | |
| 行内全文本摘要 | 拼接所有 <td> 文本，信息量大 | |

**User's choice:** 商品编号/IMEI 文本

### 行内 input 匹配

| Option | Description | Selected |
|--------|-------------|----------|
| 行内 placeholder 匹配 | 在指定行内查找目标 placeholder 的 input | ✓ |
| 行内列序号定位 | 按固定列序号，依赖固定布局 | |
| 行内 input 语义标注 | 查找行内所有 input 并标注字段名 | |

**User's choice:** 行内 placeholder 匹配

---

## 反重复与失败恢复策略

### 反重复检测层级

| Option | Description | Selected |
|--------|-------------|----------|
| DOM Patch 层检测 | 序列化时动态调整，Agent 无感知 | ✓ |
| Prompt 层指导 Agent 自检 | Section 9 追加规则，依赖 LLM | |
| 监控层新增检测器 | 类似 StallDetector，增加复杂度 | |

**User's choice:** DOM Patch 层检测

### DOM Patch 反重复机制

| Option | Description | Selected |
|--------|-------------|----------|
| 序列化时动态调整 | 根据失败历史改变元素优先级/可见性/标注 | ✓ |
| 标记状态 + Prompt 引导 | Patch 标记，Prompt 指导 Agent 避让 | |

**User's choice:** 序列化时动态调整

### 失败恢复设计结构

| Option | Description | Selected |
|--------|-------------|----------|
| 统一规则表 | 失败模式 → 检测条件 → 切换动作 | ✓ |
| 分层决策树 | 更精细但复杂度高 | |

**User's choice:** 统一规则表

### 策略优先级实现

| Option | Description | Selected |
|--------|-------------|----------|
| DOM Patch 标注策略层级 | 通过 DOM dump 标注自然切换 | ✓ |
| Prompt 层优先级指导 | Section 9 追加规则 | |

**User's choice:** DOM Patch 标注策略层级

---

## Claude's Discretion

- 规则表中示例的具体文字表述
- 文档中的图表/流程图使用
- 与 Phase 65 结论的引用格式

## Deferred Ideas

None — discussion stayed within phase scope.
