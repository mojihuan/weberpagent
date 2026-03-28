# Phase 49: 提示词优化与参数调优 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-03-28
**Phase:** 49-提示词优化与参数调优
**Areas discussed:** Prompt 内容细化, 参数配置方式, 测试策略

---

## Prompt 内容细化

| Option | Description | Selected |
|--------|-------------|----------|
| 精简指令式 | 每条规则一句话，不超过 60 行 | ✓ |
| 详细解释式 | 每条规则带解释和示例，60-120 行 | |
| 混合式 | 核心规则精简 + 关键场景举例，60-80 行 | |

**User's choice:** 精简指令式
**Notes:** Qwen 3.5 Plus 对长 prompt 指令遵守力有限，越简洁越好执行

---

| Option | Description | Selected |
|--------|-------------|----------|
| 合并替换 | 全部合并为一个 ENHANCED_SYSTEM_MESSAGE | ✓ |
| 分离拼接 | 保留 CHINESE_ENHANCEMENT，新建 ENHANCED_SYSTEM_MESSAGE | |

**User's choice:** 合并替换
**Notes:** 设计文档已定义"合并替代"

---

| Option | Description | Selected |
|--------|-------------|----------|
| 严格按设计文档 | 只包含 PRM-01~04 + 原有有价值内容 | |
| 允许 Claude 补充 ERP 场景经验 | 还可添加弹窗处理、列表选择器等 | ✓ |

**User's choice:** 允许 Claude 补充 ERP 场景经验
**Notes:** 基于 ERP 实际使用经验补充

---

| Option | Description | Selected |
|--------|-------------|----------|
| 中文 | 与 ERP 系统和 Phase 48 干预消息一致 | ✓ |
| 英文 | browser-use 内置 system_message 是英文 | |
| 混合 | 关键规则英文，ERP 场景举例中文 | |

**User's choice:** 中文
**Notes:** 与 ERP 系统语言和干预消息一致

---

## 参数配置方式

| Option | Description | Selected |
|--------|-------------|----------|
| 硬编码 | 直接在 agent_service.py Agent() 构造中写入 | ✓ |
| 集中配置文件 | 创建 backend/agent/config.py | |
| 与 prompt 同文件 | 在 prompts.py 中定义常量 | |

**User's choice:** 硬编码
**Notes:** 简单直接，Phase 50 重构时保留参数

---

| Option | Description | Selected |
|--------|-------------|----------|
| Phase 49 就注入 | 修改 agent_service.py，加入 extend_system_message 和参数 | ✓ |
| Phase 50 再注入 | Phase 49 只创建内容，注入留给 Phase 50 | |

**User's choice:** Phase 49 就注入
**Notes:** PRM-05 成功标准要求通过 extend_system_message 参数注入

---

## 测试策略

| Option | Description | Selected |
|--------|-------------|----------|
| 结构 + 参数检查 | 测试关键词存在和参数值，不检查具体措辞 | ✓ |
| 字面量匹配 | 检查每行具体内容 | |
| 最小化测试 | 只验证非空和参数传入 | |

**User's choice:** 结构 + 参数检查
**Notes:** Prompt 经常调整，字面量测试维护成本高

---

| Option | Description | Selected |
|--------|-------------|----------|
| 新建测试文件 | test_enhanced_prompt.py + test_agent_params.py | ✓ |
| 追加到现有测试 | 在 test_agent_service.py 中添加 | |

**User's choice:** 新建测试文件
**Notes:** 独立测试文件便于维护

---

## Claude's Discretion

- ENHANCED_SYSTEM_MESSAGE 各部分的具体措辞
- ERP 场景补充内容的具体范围
- 从 CHINESE_ENHANCEMENT 中保留哪些有价值内容
- 测试用例的具体关键词列表

## Deferred Ideas

None — discussion stayed within phase scope.
