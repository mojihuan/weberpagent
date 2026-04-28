# Phase 112: 集成接入 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-28
**Phase:** 112-集成接入
**Areas discussed:** Buffer 实例化位置, append_step 调用时机, code_generator 简化范围, 集成测试策略

---

## Buffer 实例化位置

| Option | Description | Selected |
|--------|-------------|----------|
| 方案 A: runs.py 创建 + 扩展回调签名 | 修改 on_step 回调签名，增加 action_dict 参数。runs.py 创建 buffer，在 on_step 中调用 append_step_async | ✓ |
| 方案 B: agent_service 内部集成 buffer | 新增 run_with_streaming 参数接收 buffer，agent_service 的 step_callback 内部直接调用 | |

**User's choice:** 方案 A — runs.py 创建 + 扩展回调签名
**Notes:** 改动最小，职责清晰。agent_service 只需在调用 on_step 时多传一个 action_dict 参数

---

## append_step 调用时机

| Option | Description | Selected |
|--------|-------------|----------|
| 统一用 append_step_async | 弱步骤修复与步翻译同步进行 | ✓ |
| 同步 append_step + 后续批量修复 | 减少步中延迟，但丧失即时修复优势 | |
| 根据配置动态选择 | 灵活但增加分支复杂度 | |

**User's choice:** 统一用 append_step_async
**Notes:** DOM 快照在 step_callback 前段已写入（run_logger.log_browser），on_step 调用时 DOM 文件已存在

---

## code_generator 简化范围

| Option | Description | Selected |
|--------|-------------|----------|
| 保留 generate_and_save，接受预翻译 | 兼容性最好 | |
| 删除 generate_and_save，runs.py 直接 assemble | 更干净 | ✓ |
| 新增并行接口，保留旧的 | 两种接口并存 | |

**User's choice:** 删除 generate_and_save，runs.py 直接 assemble
**Notes:** runs.py 用 buffer.assemble() + Path.write_text() 替代

---

## 集成测试策略

| Option | Description | Selected |
|--------|-------------|----------|
| Mock agent + 进程内 E2E | 复用项目已有的 E2E 测试模式 | |
| 单元级 buffer 集成测试 | 构造模拟 step_callback 上下文 | ✓ |

**User's choice:** 单元级 buffer 集成测试
**Notes:** 直接调用 buffer.append_step_async，验证累积和组装

---

## Claude's Discretion

- on_step 签名扩展的具体参数名和顺序
- action_dict 为空或 None 时的 fallback 处理
- duration 从 step_stats_json 解析的具体逻辑
- 文件写入目录创建逻辑
- 测试文件组织

## Deferred Ideas

None — discussion stayed within phase scope
