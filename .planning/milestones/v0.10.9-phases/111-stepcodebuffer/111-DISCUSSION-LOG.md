# Phase 111: StepCodeBuffer 核心实现 - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-28
**Phase:** 111-StepCodeBuffer 核心实现
**Areas discussed:** 缓冲区数据结构, 弱步骤修复模型, 等待推导与组装

---

## 缓冲区数据结构

| Option | Description | Selected |
|--------|-------------|----------|
| 新建 StepRecord 包装类 | 新建 frozen dataclass StepRecord(TranslatedAction, wait_before, step_index)。不修改现有 TranslatedAction | ✓ |
| 扩展 TranslatedAction 字段 | 给现有 TranslatedAction 加 wait_before='' 和 step_index=-1 可选字段 | |
| Buffer 内部用 dict/tuple | Buffer 内部存 list[tuple[TranslatedAction, str, int]] | |

**User's choice:** 新建 StepRecord 包装类
**Notes:** 保持现有 TranslatedAction 不变，符合项目不可变模式约定

---

## 弱步骤修复模型 — DOM 上下文获取

| Option | Description | Selected |
|--------|-------------|----------|
| Buffer 自己读磁盘 | buffer 构造时接收 base_dir/run_id，append_step_async() 自己读取 DOM 快照文件 | ✓ |
| 调用方传入 DOM | append_step_async(action_dict, dom_content) 由调用方传入 | |
| 注入 DOM provider | buffer 构造时接收 dom_provider: Callable[[int], str] | |

**User's choice:** Buffer 自己读磁盘
**Notes:** 与现有 _heal_weak_steps() 模式一致，简单直接

---

## 弱步骤修复模型 — LLM 修复阻塞策略

| Option | Description | Selected |
|--------|-------------|----------|
| 同步阻塞等修复结果 | append_step_async() 立即调用 LLMHealer.heal() 并等待结果 | ✓ |
| 异步非阻塞后补结果 | 先存 placeholder，后台异步修复后替换 StepRecord | |
| 异步 fire-and-forget | 不阻塞，用 LLM 结果时直接取 | |

**User's choice:** 同步阻塞等修复结果
**Notes:** 简单可靠，修复结果立即可用。LLMHealer.heal() 有 180s 超时保护

---

## 等待推导 — 耗时信息来源

| Option | Description | Selected |
|--------|-------------|----------|
| 调用方传入 duration | step_callback 已有 step_stats 数据，append_step() 接收 duration 参数 | ✓ |
| Buffer 自己计时 | buffer 内部记录每步 append 的时间戳 | |

**User's choice:** 调用方传入 duration
**Notes:** 更精确，调用方已有 step_stats 数据

---

## 组装策略

| Option | Description | Selected |
|--------|-------------|----------|
| 委托给 generate() | assemble() 将 StepRecord 展平为 TranslatedAction 列表，委托给现有 PlaywrightCodeGenerator.generate() | ✓ |
| 独立实现组装 | StepCodeBuffer 完全独立实现组装逻辑 | |

**User's choice:** 委托给 generate()
**Notes:** 最大化复用现有代码，仅 Phase 112 小改 generate() 接口

---

## wait_before 输出表示

| Option | Description | Selected |
|--------|-------------|----------|
| 独立步骤插入 | wait_before 作为独立的 TranslatedAction 插入到 action 之前 | ✓ |
| 拼接到 code 字段 | wait_before 拼接到 TranslatedAction.code 前面 | |

**User's choice:** 独立步骤插入
**Notes:** _build_body() 自然处理，不需要修改现有 body 构建逻辑

---

## Claude's Discretion

- StepRecord 的具体字段命名和默认值
- _derive_wait() 的 navigate 操作检测逻辑
- append_step_async() 内部错误处理和 fallback 策略
- Buffer 的构造函数签名细节
- 单元测试文件组织和覆盖粒度
- LLM 配置传递方式

## Deferred Ideas

None — discussion stayed within phase scope
