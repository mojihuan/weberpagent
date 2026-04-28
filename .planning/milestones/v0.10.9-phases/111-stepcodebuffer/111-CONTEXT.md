# Phase 111: StepCodeBuffer 核心实现 - Context

**Gathered:** 2026-04-28
**Status:** Ready for planning

<domain>
## Phase Boundary

创建 StepCodeBuffer 数据结构，支持逐步累积翻译结果：同步/异步单步翻译、智能等待推导、组装完整测试文件。Buffer 可独立使用，不依赖 runs.py 集成（Phase 112 负责）。

覆盖 REQUIREMENTS: CODEGEN-01, CODEGEN-02, CODEGEN-03, CODEGEN-04, VAL-01。

不涉及：runs.py 改动、code_generator.py 简化、E2E 测试、前端改动。

</domain>

<decisions>
## Implementation Decisions

### 缓冲区数据结构
- **D-01:** 新建 `StepRecord` frozen dataclass，包装 `TranslatedAction` + `wait_before: str` + `step_index: int`。不修改现有 TranslatedAction，保持已有代码稳定
- Buffer 内部存储为 `list[StepRecord]`，step_index 自动递增

### 弱步骤修复模型
- **D-02:** Buffer 构造时接收 `base_dir` 和 `run_id`，`append_step_async()` 自己从磁盘读取 DOM 快照文件（`{base_dir}/{run_id}/dom/step_{n}.txt`），与现有 `_heal_weak_steps()` 模式一致
- **D-03:** LLM 修复采用同步阻塞模式 — `append_step_async()` 调用 `LLMHealer.heal()` 并等待结果，将修复后的定位器代码片段合并到 StepRecord。简单可靠，修复结果立即可用

### 等待推导与组装
- **D-04:** `_derive_wait()` 的操作耗时信息由调用方通过 `duration: float | None = None` 参数传入，不依赖 buffer 内部计时。调用方（step_callback）已有 step_stats 数据
- **D-05:** `assemble()` 委托给现有 `PlaywrightCodeGenerator.generate()` 组装完整测试文件。StepCodeBuffer 只负责将 StepRecord 展平为 `list[TranslatedAction]`，然后调用 generate()。最大化复用，减少重复代码
- **D-06:** `wait_before` 等待代码作为独立的 `TranslatedAction` 插入到主操作 action 之前。`_build_body()` 自然处理，不需要修改现有 body 构建逻辑

### Claude's Discretion
- StepRecord 的具体字段命名和默认值
- `_derive_wait()` 的 navigate 操作检测逻辑（action_type 判断）
- `append_step_async()` 内部错误处理和 fallback 策略
- Buffer 的构造函数签名细节（哪些参数必选 vs 可选）
- 单元测试文件组织和覆盖粒度
- LLM 配置传递方式（llm_config 参数 vs 全局配置）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 核心源码（依赖与修改目标）
- `backend/core/action_translator.py` — TranslatedAction frozen dataclass（line 21），translate() 和 translate_with_llm() 方法。StepCodeBuffer 的核心依赖
- `backend/core/code_generator.py` — PlaywrightCodeGenerator 类，generate() 方法（line 39），_heal_weak_steps()（line 181），_build_body()（line 294）。assemble() 委托目标
- `backend/core/llm_healer.py` — LLMHealer.heal() 方法（line 191），LLMHealResult frozen dataclass（line 89）。append_step_async() 的修复依赖
- `backend/core/locator_chain_builder.py` — LocatorChainBuilder.extract() 方法。弱步骤检测需要用它判断定位器数量

### 数据结构参考
- `backend/core/action_translator.py` line 21-28 — TranslatedAction 冻结数据类定义
- `backend/core/llm_healer.py` line ~89 — LLMHealResult 冻结数据类定义
- `backend/core/self_healing_runner.py` line 99-106 — HealingResult 冻结数据类（模式参考）

### 集成参考（Phase 112 使用，Phase 111 需了解接口）
- `backend/api/routes/runs.py` line 372 — on_step callback 签名，step_callback 上下文
- `backend/api/routes/runs.py` line 590-619 — 代码生成块，Phase 112 替换目标

### 测试参考
- `backend/tests/unit/test_code_api.py` — 现有 code_generator 单元测试模式
- `backend/tests/unit/test_dom_patch.py` — frozen dataclass 测试模式参考

### 需求定义
- `.planning/REQUIREMENTS.md` — CODEGEN-01~04 需求定义和 VAL-01 验收标准

### 代码规范参考
- `.planning/codebase/CONVENTIONS.md` — frozen dataclass、不可变模式、中文注释约定

### 前置阶段参考
- `.planning/phases/107-自愈修复增强E2E/107-CONTEXT.md` — LLMHealer 修复增强上下文

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `ActionTranslator.translate()` / `translate_with_llm()` — 核心翻译方法，append_step() 直接复用
- `TranslatedAction` — 已有 frozen dataclass，StepRecord 包装它
- `LLMHealer.heal()` — 弱步骤修复，append_step_async() 调用
- `LocatorChainBuilder.extract()` — 定位器链提取，弱步骤检测用
- `PlaywrightCodeGenerator.generate()` — 组装逻辑，assemble() 委托目标

### Established Patterns
- frozen dataclass 用于不可变数据对象（项目约定）
- `_heal_weak_steps()` 批量修复模式 → Phase 111 改为逐步即时修复
- DOM 快照存于 `{base_dir}/{run_id}/dom/step_{n}.txt`（1-indexed）
- `ast.parse()` 语法验证是已有模式
- LLM 配置通过 `create_llm()` 工厂创建

### Integration Points
- Buffer 被 runs.py step_callback 调用（Phase 112）
- Buffer 调用 ActionTranslator 进行翻译
- Buffer 调用 LLMHealer.heal() 进行弱步骤修复
- Buffer.assemble() 委托给 PlaywrightCodeGenerator.generate()
- DOM 快照文件系统是 buffer 获取 DOM 的来源

### 当前代码生成流程（Phase 111 改造的目标）
```
PlaywrightCodeGenerator.generate_and_save():
  1. result.model_actions() -> raw_actions  # 批量获取
  2. _heal_weak_steps() -> llm_snippets     # 批量修复
  3. translate_with_llm() -> TranslatedAction  # 逐个翻译
  4. generate() -> complete .py file        # 组装

# Phase 111 改为：
StepCodeBuffer:
  1. append_step(action_dict) / append_step_async(action_dict)  # 每步即时
  2. assemble() -> 委托 generate()                              # 最终组装
```

</code_context>

<specifics>
## Specific Ideas

- SUCCESS CRITERIA 来自 REQUIREMENTS.md：
  1. append_step() 接收 action_dict，通过 ActionTranslator 同步翻译为 TranslatedAction，存储翻译结果 + wait_before + step_index
  2. _derive_wait() 对 navigate 生成 wait_for_load_state("networkidle")，耗时 >800ms 用实际耗时，click 生成 300ms 等待
  3. append_step_async() 检测弱步骤（elem=None 或 <=1 locator），即时调用 LLMHealer 修复
  4. assemble(header, precondition, assertions) 组装完整测试文件，ast.parse 语法验证通过
  5. 单元测试覆盖 append 同步/异步、wait 推导 3 种策略、assemble 组装、空 buffer 边界、语法验证

- StepCodeBuffer 独立于 runs.py，可单独测试
- 弱步骤检测逻辑复用 LocatorChainBuilder.extract() 的返回值长度判断
- DOM 快照读取路径与现有 _heal_weak_steps() 一致

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---
*Phase: 111-stepcodebuffer*
*Context gathered: 2026-04-28*
