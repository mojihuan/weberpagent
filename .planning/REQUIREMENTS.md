# Requirements: v0.10.8 生成测试代码前置条件与断言步骤

## Milestone Goal

生成的 Playwright 测试代码从「仅操作步骤」升级为「完整的可执行测试」：包含前置条件（page.goto + 认证状态）和断言验证（expect 语句）。

## Problem Statement

当前生成的测试代码有三个结构性缺陷：

1. **无 page.goto()** — 浏览器停留在 about:blank，所有定位器超时
2. **无断言 expect()** — 操作完成后没有任何验证，测试永远"通过"
3. **SelfHealingRunner 的 storage_state 缺少导航** — 注入了 localStorage token 但页面未加载

## Root Causes (from debug analysis)

- `code_generator.py:112` 只处理 `model_actions()` 输出，不含 `pre_navigate()` 的导航步骤
- `runs.py:594` 调用代码生成时，`effective_target_url` 和任务断言在作用域内但未传递
- `code_generator.py` 无断言意识 — 不接受断言定义，无 expect() 生成逻辑

## Requirements

### ~~PREC-01: page.goto() 前置条件注入~~ -- DONE (Phase 108)

**Priority:** P0 (阻塞所有后续功能)

`code_generator.generate()` 接受可选的 `precondition_config` 参数。当提供 `target_url` 时，在测试函数体首行注入：

```python
page.goto("https://erp.example.com")
page.wait_for_load_state("networkidle")
```

**Acceptance Criteria:**
- generate_and_save() 新增 `precondition_config: dict | None = None` 参数
- generate() 新增同参数
- 当 `precondition_config["target_url"]` 存在时，在函数体首行注入 page.goto() + wait_for_load_state()
- 注入的代码正确缩进（4 空格）
- 当 precondition_config 为 None 或无 target_url 时，行为不变

### ~~PREC-02: runs.py 传递 target_url~~ -- DONE (Phase 108)

**Priority:** P0

`runs.py:594` 处将 `effective_target_url` 传递给 `generate_and_save()`。

**Acceptance Criteria:**
- runs.py 构造 `precondition_config = {"target_url": effective_target_url}` 传递给代码生成器
- effective_target_url 为 None 时不传 precondition_config（保持向后兼容）
- 现有测试不受影响

### ~~PREC-03: SelfHealingRunner 页面导航验证~~ -- DONE (Phase 108)

**Priority:** P0

确认 SelfHealingRunner 的 storage_state + 生成的 page.goto() 组合能正常工作。

**Acceptance Criteria:**
- SelfHealingRunner conftest.py 注入 storage_state（已有）
- 生成的代码中 page.goto() 加载 ERP 页面后，localStorage token 生效
- 页面加载后后续操作不再超时

### ~~ASRT-01: 断言 → Playwright expect() 翻译~~ -- DONE (Phase 109)

**Priority:** P1

将 4 种现有断言类型映射为 Playwright expect() 语句，追加到测试函数体末尾。

**映射规则：**

| Assertion Type | Playwright Code |
|---------------|-----------------|
| `url_contains("x")` | `expect(page).to_have_url(re.compile(".*x.*"))` |
| `text_exists("y")` | `expect(page.locator("body")).to_contain_text("y")` |
| `no_errors` | `expect(page.locator(".ant-message-error")).to_have_count(0)` |
| `element_exists("selector")` | `expect(page.locator("selector")).to_be_visible()` |

**Acceptance Criteria:**
- code_generator 新增 `assertions: list | None = None` 参数
- 当有断言时，生成对应的 expect() 语句
- 添加必要的 import: `from playwright.sync_api import expect` + `import re`（按需）
- 断言语句追加在操作步骤之后，用空行分隔
- 未知断言类型生成注释 `# unknown assertion: {type}`

### ~~ASRT-02: runs.py 传递任务断言~~ -- DONE (Phase 109)

**Priority:** P1

`runs.py:594` 处将 `run.task.assertions` 传递给 `generate_and_save()`。

**Acceptance Criteria:**
- runs.py 在代码生成调用时读取 task.assertions 并传递
- 无断言时传 None（向后兼容）
- 断言数据在 agent 执行完成后可用（在 assertion_service.evaluate_all() 之后）

### ~~ASRT-03: 断言翻译单元测试~~ -- DONE (Phase 109)

**Priority:** P1

4 种断言类型的翻译测试 + 边界情况。

**Acceptance Criteria:**
- url_contains → expect(page).to_have_url(re.compile(".*expected.*"))
- text_exists → expect(page.locator("body")).to_contain_text("expected")
- no_errors → expect(page.locator(".ant-message-error")).to_have_count(0)
- element_exists → expect(page.locator("selector")).to_be_visible()
- 无断言时不生成 expect 语句
- 未知类型生成注释

### E2E-01: 完整生成代码 E2E 验证

**Priority:** P0

验证生成的测试包含 page.goto() + 操作步骤 + expect() 语句，语法正确。

**Acceptance Criteria:**
- 生成的代码通过 ast.parse 验证
- 代码包含 page.goto(target_url) 作为首行
- 代码包含 expect() 语句在末尾（当有断言时）
- import 包含必要的 `expect` 和 `re`
- 回归测试全量通过

## Out of Scope

- 运行时断言评估（已有 AssertionService，不修改）
- SelfHealingRunner 断言修复（future scope）
- 数据驱动测试参数化
- 前端 UI 修改（断言已在前端显示）

## File Impact

| File | Change Type |
|------|-------------|
| `backend/core/code_generator.py` | 修改 — 新增 precondition_config + assertions 参数 |
| `backend/api/routes/runs.py` | 修改 — 传递 target_url 和 assertions |
| `backend/tests/unit/test_code_generator.py` | 新增/修改 — 前置条件和断言翻译测试 |
| `backend/tests/unit/test_assertion_translation.py` | 新增 — 断言翻译专项测试 |

## Dependencies

- v0.10.7 已交付的代码生成管道（code_generator, action_translator, locator_chain_builder）
- SelfHealingRunner 已有的 storage_state + conftest 机制
