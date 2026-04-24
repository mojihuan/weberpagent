# Requirements: v0.10.5 生成测试代码修复与优化

**Defined:** 2026-04-24
**Core Value:** 让 QA 用自然语言写测试用例，AI 自动执行并生成报告

## v1 Requirements

### 核心键名修复

- [x] **KEY-01**: ActionTranslator._CORE_TYPES 使用 browser-use 实际输出的键名 click/input（而非 click_element/input_text）
- [ ] **KEY-02**: translate() 和 translate_with_llm() 的 action_type 分派使用正确键名
- [x] **KEY-03**: _heal_weak_steps() 中 action_type 检查使用正确键名，LLM healing 对 click/input 生效
- [ ] **KEY-04**: _build_fallback_code / _build_llm_only_code 中 action_type 参数使用正确键名

### 常用操作翻译

- [ ] **TRANS-01**: wait → page.wait_for_timeout(seconds * 1000)，显示有意义的等待代码
- [ ] **TRANS-02**: select_dropdown → page.locator("xpath=...").select_option(text)，使用元素定位器
- [ ] **TRANS-03**: evaluate → page.evaluate(code)，显示 JavaScript 执行代码
- [ ] **TRANS-04**: upload_file → page.locator("xpath=...").set_input_files(path)，使用元素定位器而非注释

### 边缘操作翻译

- [ ] **EDGE-01**: switch → page.bring_to_front() 或 tab 切换注释
- [ ] **EDGE-02**: close → page.close() 或 tab 关闭注释
- [ ] **EDGE-03**: search_page / find_elements / find_text → 有意义的注释（非核心 Playwright 操作）
- [ ] **EDGE-04**: screenshot / save_as_pdf → 有意义的注释
- [ ] **EDGE-05**: done / write_file / read_file / replace_file → 有意义的注释
- [ ] **EDGE-06**: search → page.goto(search_url) 或有意义的注释
- [ ] **EDGE-07**: dropdown_options → page.locator(...).evaluate() 或有意义的注释
- [ ] **EDGE-08**: extract → 有意义的注释（数据提取非 Playwright 回放操作）

### 测试验证

- [ ] **TEST-01**: 单元测试使用 browser-use 实际输出的键名（click/input 而非 click_element/input_text）
- [ ] **TEST-02**: 新增 wait/select_dropdown/evaluate 翻译的单元测试
- [ ] **TEST-03**: _heal_weak_steps() 测试验证 click/input 的 LLM healing 路径可触发
- [ ] **TEST-04**: 端到端验证 — AI 执行任务后，生成的代码包含可执行的 Playwright click/input 调用

## Out of Scope

| Feature | Reason |
|---------|--------|
| 重构 action_translator 架构 | 本次只修 bug + 补翻译，不重构 |
| 新增 Playwright action 类型 | 只翻译 browser-use 已有的 action |
| 修改 browser-use 源码 | 不侵入上游代码 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| KEY-01 | Phase 99 | Complete |
| KEY-02 | Phase 99 | Pending |
| KEY-03 | Phase 99 | Complete |
| KEY-04 | Phase 99 | Pending |
| TRANS-01 | Phase 100 | Pending |
| TRANS-02 | Phase 100 | Pending |
| TRANS-03 | Phase 100 | Pending |
| TRANS-04 | Phase 100 | Pending |
| EDGE-01 | Phase 100 | Pending |
| EDGE-02 | Phase 100 | Pending |
| EDGE-03 | Phase 100 | Pending |
| EDGE-04 | Phase 100 | Pending |
| EDGE-05 | Phase 100 | Pending |
| EDGE-06 | Phase 100 | Pending |
| EDGE-07 | Phase 100 | Pending |
| EDGE-08 | Phase 100 | Pending |
| TEST-01 | Phase 101 | Pending |
| TEST-02 | Phase 101 | Pending |
| TEST-03 | Phase 101 | Pending |
| TEST-04 | Phase 101 | Pending |

**Coverage:**
- v1 requirements: 20 total
- Mapped to phases: 20
- Unmapped: 0

---
*Requirements defined: 2026-04-24*
*Last updated: 2026-04-24 — traceability updated after roadmap creation*
