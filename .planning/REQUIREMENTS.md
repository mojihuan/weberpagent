# Requirements: aiDriveUITest v0.10.6

**Defined:** 2026-04-24
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v0.10.6 Requirements

### 执行修复 (Execution Fixes)

- [x] **EXEC-01**: SelfHealingRunner 以正确的 headless 模式调用 pytest（移除无效的 `--headed=false` 参数）
- [x] **EXEC-02**: 生成的测试代码中 done action 的文本不包含未注释的换行符，不会导致 SyntaxError
- [x] **EXEC-03**: 开发环境 uvicorn 启动命令排除 outputs 目录，避免 conftest.py 触发服务器热重载

### 自愈改进 (Healing Improvement)

- [ ] **HEAL-01**: SelfHealingRunner 区分"执行环境错误"（pytest 退出码 2/4/5）和"代码错误"（退出码 1），环境错误直接跳过 LLM 修复

### 端到端验证 (E2E Verification)

- [ ] **E2E-01**: AI 执行完整任务后，生成的 Playwright 测试代码可被 pytest 成功执行并返回有意义的结果（pass 或 test-level fail）

## Future Requirements

### Deferred

- **HEAL-02**: 退出码 1 的细粒度子分类（CODE_SYNTAX / CODE_IMPORT / CODE_RUNTIME）— 需要更多真实失败样本
- **EXEC-04**: code_generator.py 中已有的 `validate_syntax()` 方法在写入前调用 — 防御性保障

## Out of Scope

| Feature | Reason |
|---------|--------|
| 输出目录移到 /tmp/ | 会破坏代码查看器、截图、DOM 快照路径，排除模式已足够 |
| 生产环境 WatchFiles 修复 | 生产已用 `reload=False`，无需修改 |
| LLM healer 支持修复执行参数 | 超出 LLM healer 职责范围，应由错误分类器前置拦截 |
| 新增依赖或架构变更 | 所有修复均为单行/近单行改动 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| EXEC-01 | Phase 102 | Complete |
| EXEC-02 | Phase 102 | Complete |
| EXEC-03 | Phase 102 | Complete |
| HEAL-01 | Phase 103 | Pending |
| E2E-01 | Phase 104 | Pending |

**Coverage:**
- v0.10.6 requirements: 5 total
- Mapped to phases: 5
- Unmapped: 0

---
*Requirements defined: 2026-04-24*
*Last updated: 2026-04-24 — traceability updated after roadmap creation*
