# Phase 112: 集成接入 - Context

**Gathered:** 2026-04-28
**Status:** Ready for planning

<domain>
## Phase Boundary

将 StepCodeBuffer 接入 runs.py step_callback（每步即时翻译）和代码生成块（buffer.assemble 替代 generate_and_save），简化 code_generator.py 去掉 _heal_weak_steps。

覆盖 REQUIREMENTS: INTEG-01, INTEG-02, INTEG-03, VAL-02。

不涉及：E2E 全量回归（Phase 113）、前端改动。

</domain>

<decisions>
## Implementation Decisions

### Buffer 实例化与传递
- **D-01:** runs.py 中 on_step 闭包外创建 StepCodeBuffer 实例，通过闭包捕获传给 on_step。扩展 on_step 回调签名，增加 `action_dict: dict | None = None` 参数。agent_service 的 step_callback 调用 on_step 时传递 action_dict
- Buffer 构造参数：`base_dir="outputs"`, `run_id=run_id`, `llm_config=get_code_gen_llm_config()`

### 调用策略
- **D-02:** 统一使用 `append_step_async`（含弱步骤即时 LLM 修复）。DOM 快照在 step_callback 前段已写入（run_logger.log_browser），on_step 调用时 DOM 文件已存在，append_step_async 可正常读取
- duration 参数从 step_stats 中提取（agent_service 已有 step_stats_data）

### code_generator 简化
- **D-03:** 删除 `generate_and_save()` 方法和 `_heal_weak_steps()` 方法。runs.py 代码生成块改为 `buffer.assemble()` + 手动写文件（`Path.write_text`）。`generate()` 方法保留不变（assemble 内部委托调用）
- 现有 `generate_and_save` 测试更新：移除或改为测试 assemble + write 流程

### 集成测试策略
- **D-04:** 单元级 buffer 集成测试 — 构造模拟 step_callback 上下文直接调用 buffer.append_step_async，验证累积和组装。不启动真实 HTTP 服务器

### Claude's Discretion
- on_step 签名扩展的具体参数名和顺序
- action_dict 为空或 None 时的 fallback 处理
- duration 从 step_stats_json 解析的具体逻辑
- 文件写入目录创建逻辑
- 测试文件组织

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### 核心源码（修改目标）
- `backend/api/routes/runs.py` line 370-418 — on_step 回调定义和调用
- `backend/api/routes/runs.py` line 590-619 — 代码生成块（Phase 112 替换目标）
- `backend/core/code_generator.py` — PlaywrightCodeGenerator，generate_and_save (line 125) 和 _heal_weak_steps (line 181) 删除目标
- `backend/core/step_code_buffer.py` — StepCodeBuffer 已实现，Phase 112 的集成对象

### 依赖与接口
- `backend/core/agent_service.py` line 393-590 — step_callback 定义，action_dict 解析 (line 456)，on_step 调用 (line 587-590)
- `backend/core/agent_service.py` line 340-350 — run_with_streaming 签名，on_step 回调类型
- `backend/utils/run_logger.py` line 86-91 — DOM 快照写入逻辑，step_{N}.txt 路径

### 前置阶段
- `.planning/phases/111-stepcodebuffer/111-CONTEXT.md` — Phase 111 决策，StepCodeBuffer 接口定义

### 数据结构参考
- `backend/core/action_translator.py` line 21-28 — TranslatedAction 冻结数据类

### 测试参考
- `backend/tests/unit/test_step_code_buffer.py` — 现有 buffer 单元测试
- `backend/tests/unit/test_code_generator.py` — 现有 code_generator 测试（需更新）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `StepCodeBuffer` — Phase 111 已实现，append_step / append_step_async / assemble 接口完整
- `PlaywrightCodeGenerator.generate()` — assemble 委托目标，无需修改
- `ActionTranslator` — buffer 内部已集成
- `LLMHealer` — buffer 内部已集成
- `get_code_gen_llm_config()` — runs.py 已有的 LLM 配置获取函数

### Established Patterns
- frozen dataclass 不可变数据对象
- on_step 闭包捕获 run_id, global_seq 等变量
- 代码生成非阻塞（try-except 包裹）
- httpx + ASGITransport 进程内测试模式
- DOM 快照存于 outputs/{run_id}/dom/step_{n}.txt（1-indexed）

### Integration Points
- `runs.py on_step` — 新增 action_dict 参数，调用 buffer.append_step_async
- `runs.py 代码生成块` — 用 buffer.assemble() + write 替换 generate_and_save
- `agent_service.step_callback` — 传递 action_dict 给 on_step
- `code_generator.py` — 删除 generate_and_save 和 _heal_weak_steps

### 关键时序
```
agent_service.step_callback 执行顺序：
1. DOM 快照保存 (run_logger.log_browser) ← DOM 已写入
2. action_dict 解析 (first_action.model_dump)
3. step_stats 构建
4. 检测器调用 (stall/failure/progress)
5. on_step 调用 ← 此时 DOM 已存在，action_dict 已解析
```

</code_context>

<specifics>
## Specific Ideas

- SUCCESS CRITERIA 来自 ROADMAP.md：
  1. runs.py step_callback 中每步操作即时调用 buffer.append_step()，action_dict 正确传递
  2. runs.py 代码生成块使用 buffer.assemble() + import/header 组装替代旧 generate_and_save()
  3. code_generator.py 去掉 _heal_weak_steps，generate_and_save 接受 list[TranslatedAction] 预翻译结果直接组装输出
  4. 集成测试验证 buffer 在 step_callback 上下文中累积步骤，弱步骤异步修复正常触发

- generate_and_save 删除后，runs.py 直接 `buffer.assemble()` 得到代码内容，`Path(output_dir).write_text(content)` 写文件
- 现有 test_code_generator.py 中 generate_and_save 相关测试需更新

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---
*Phase: 112-集成接入*
*Context gathered: 2026-04-28*
