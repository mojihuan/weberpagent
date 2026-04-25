# Requirements: v0.10.7 生成测试代码行为优化

## Problem Statement

AI 生成的 Playwright 测试代码质量极差，3 次自愈修复后仍然失败。分析了 64 个已生成文件，发现 8 个系统性根因导致代码无法运行。

## Root Causes

| # | 根因 | 影响 | 严重性 |
|---|------|------|--------|
| 1 | 操作翻译缺失 — write_file/replace_file 等生成 `# 未翻译的操作类型` | ~30% 文件为空操作 | CRITICAL |
| 2 | 代码缩进错误 — Playwright 语句出现在函数体外 | ~10% 文件 SyntaxError | CRITICAL |
| 3 | exact=True 脆弱匹配 — get_by_text 精确匹配 ERP 动态 DOM | ~40% 定位器首层失败 | HIGH |
| 4 | 绝对 XPath — html/body/div[1]/... 极度脆弱 | 任何 DOM 变化即失效 | HIGH |
| 5 | 自愈单行修复 — try-except 块修复破坏嵌套结构 | 修复后反而更糟 | HIGH |
| 6 | DOM 快照猜测 — 正则匹配 error_output 而非代码上下文 | 拿到错误页面的 DOM | MEDIUM |
| 7 | LLM prompt 上下文不足 — 只看 10 行上下文 | LLM 无法理解操作意图 | MEDIUM |
| 8 | icon font 字符污染 — \ue6d9 等私有区字符混入定位器 | 文本匹配必败 | MEDIUM-HIGH |

## Requirements

### TRANSLATE: 操作翻译完善

- **TRANSLATE-01**: 非核心操作（write_file/replace_file/find_elements 等）生成有意义的注释占位，包含参数摘要，而非 `# 未翻译的操作类型`
- **TRANSLATE-02**: 已有核心 10 种操作确保翻译质量（click/input/navigate/scroll/send_keys/go_back/wait/evaluate/select_dropdown/upload_file）

### INDENT: 代码结构正确性

- **INDENT-01**: `_build_body` 生成的所有 Playwright 语句必须包含 4 空格函数体缩进
- **INDENT-02**: 多行 try-except 回退代码的嵌套缩进必须正确对齐
- **INDENT-03**: `generate()` 输出必须通过 `ast.parse()` 语法验证

### LOCATOR: 定位器质量

- **LOCATOR-01**: `get_by_text` 默认使用模糊匹配（去掉 `exact=True`），仅对短文本（<=4 字符）使用精确匹配
- **LOCATOR-02**: XPath 定位器改为相对路径 — 优先使用 `//*[@data-testid="..."]`、`//button[contains(text(),"...")]` 等语义定位
- **LOCATOR-03**: 过滤 `ax_name` 中的 Unicode 私有使用区字符（U+E000-U+F8FF），这些是 icon font 渲染字符
- **LOCATOR-04**: 定位器链优先级调整：get_by_text(模糊) → get_by_role → get_by_placeholder → CSS ID → data-testid → 相对 XPath

### HEAL: 自愈修复增强

- **HEAL-01**: `_apply_fix` 支持多行替换 — 当修复代码跨多行时，正确替换目标行范围
- **HEAL-02**: DOM 快照精准匹配 — 从失败行的注释/代码中提取步骤信息，而非从 error_output 正则猜测
- **HEAL-03**: LLM 修复 prompt 上下文窗口从 10 行扩大到 20 行
- **HEAL-04**: 自愈修复后整体验证 — 替换后对完整函数体做 ast.parse 验证

### E2E: 端到端验证

- **E2E-01**: 销售出库场景 E2E 验证 — AI 执行后生成的代码至少通过首次 pytest 运行
- **E2E-02**: 回归测试 — 全量测试套件通过，新增代码无副作用

## Scope Boundaries

### In Scope
- code_generator.py, action_translator.py, locator_chain_builder.py 的修改
- llm_healer.py, self_healing_runner.py 的修复增强
- 对应单元测试更新

### Out of Scope
- 前端改动
- API 路由改动
- 新增 LLM 模型切换
- browser-use 源码修改

## Success Criteria

1. 生成的测试代码 ast.parse 通过率 100%（当前约 60%）
2. 销售出库场景 E2E 测试首次 pytest 通过
3. 全量测试套件通过（967+ tests）
4. 定位器链中无 icon font 私有区字符
5. 无绝对 XPath（html/body/...）出现在定位器链中
