# Requirements: v0.10.9 逐步代码生成

## Milestone Goal

将 Playwright 代码生成从"事后一次性翻译"改为"每步即时翻译"，提高生成代码的可运行率。

## Active Requirements

### CODEGEN: 代码生成核心

- [x] **CODEGEN-01**: StepCodeBuffer.append_step() 同步翻译单步操作，复用 ActionTranslator，存储 TranslatedAction + wait_before + step_index
- [x] **CODEGEN-02**: append_step_async() 检测弱步骤（elem=None 或 ≤1 locator），即时调用 LLMHealer 修复，DOM 上下文最新
- [x] **CODEGEN-03**: _derive_wait() 智能等待推导 — navigate 后 wait_for_load_state、耗时 >800ms 用实际耗时、click 后 300ms
- [x] **CODEGEN-04**: buffer.assemble(header, precondition, assertions) 组装完整测试文件内容

### INTEGRATION: 集成

- [x] **INTEG-01**: runs.py step_callback 传递 action_dict 给 buffer.append_step()，每步即时翻译
- [x] **INTEG-02**: runs.py 代码生成块替换为 buffer.assemble() + import/header 组装 + 文件写入
- [x] **INTEG-03**: code_generator.py 删除 generate_and_save 和 _heal_weak_steps 方法，runs.py 使用 buffer.assemble() + Path.write_text 写文件

### VALIDATION: 验证

- [x] **VAL-01**: StepCodeBuffer 单元测试 — append 同步/异步、wait 推导、assemble 组装、空 buffer、语法验证
- [x] **VAL-02**: 集成测试 — buffer 在 step_callback 上下文中累积步骤、弱步骤异步修复
- [x] **VAL-03**: 全量回归测试通过 + code_generator 现有测试更新以匹配新 API

## Future Requirements (Deferred)

(None)

## Out of Scope

- agent_service.py 重构 — 仅修改 step_callback 传递 action_dict
- self_healing_runner.py 修改 — 保持不变作为最终兜底
- action_translator.py 修改 — 完全复用现有翻译逻辑
- locator_chain_builder.py 修改 — 完全复用现有定位器构建

## Traceability

| REQ-ID | Phase | Status |
|--------|-------|--------|
| CODEGEN-01 | 111 | Complete |
| CODEGEN-02 | 111 | Complete |
| CODEGEN-03 | 111 | Complete |
| CODEGEN-04 | 111 | Complete |
| INTEG-01 | 112 | Complete |
| INTEG-02 | 112 | Complete |
| INTEG-03 | 112 | Complete |
| VAL-01 | 111 | Complete |
| VAL-02 | 112 | Complete |
| VAL-03 | 113 | Complete |

---
*Last updated: 2026-04-28 — v0.10.9 requirements mapped to phases*
