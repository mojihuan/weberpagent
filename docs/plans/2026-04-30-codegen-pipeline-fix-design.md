# 测试代码生成管道优化计划

日期: 2026-04-30
状态: 待实施

## 背景

通过调试 `outputs/eca850b4/generated/test_eca850b4.py`（销售出库-未收款测试），发现代码生成管道存在 3 个问题。手动修复测试文件后测试通过（returncode=0），验证了问题分析的正确性。

## 已完成的改动（commit fbf0aca）

- `locator_chain_builder.py`: CSS 选择器增加 `.filter(has_text="...")` 文本过滤（替代泛化的 `.first`）
- `action_translator.py`: 回退定位器增加 `wait_for(state='visible', timeout=3000)` 前置等待

## 待修复问题

### P1: CSS filter 需要追加 `.first`（1 行改动）

**问题**: `filter(has_text="添加")` 做子串匹配，匹配到 "添加"、"导入添加"、"手动添加" 共 4 个元素，触发 Playwright strict mode violation。

**文件**: `backend/core/locator_chain_builder.py` 第 170-171 行

**当前代码**:
```python
return f'{base}.filter(has_text="{escaped_name}")'
```

**改为**:
```python
return f'{base}.filter(has_text="{escaped_name}").first'
```

**影响范围**: 仅 `_build_class_selector` 方法，1 行改动

---

### P2: input 操作只生成了 click，没有生成 fill（核心 bug）

**问题**: agent 执行了 `input` 操作填入物品编号（如 "xxx123"），但代码生成管道只产生了 `click`（点击输入框），丢失了 `.fill()` 步骤。导致后续"添加"按钮点击后无数据行，"请输入销售价"等字段不存在。

**调试证据**: 页面上所有 input 的 placeholder 列表中没有 "请输入销售价"，因为需要先添加物品行才会出现。

**根因（已确认）**: 方向 4 — agent 通过 `evaluate` (JavaScript) 输入文字而非标准 `input` action。

流程: agent 先 `click` 输入框 → 再 `evaluate` 执行 JS 设置值。evaluate 无 `interacted_element`，
生成的 `page.evaluate("...")` 代码不可靠。

**修复方案**: evaluate 智能转换（StepCodeBuffer 层）

在 `StepCodeBuffer.append_step` 中新增 `_try_convert_evaluate_to_fill` 方法：

1. **检测 JS 模式**（正则匹配）：
   - `setter.call(..., "xxx")` — nativeInputValueSetter
   - `.value = "xxx"` 或 `.value = 'xxx'` — 直接赋值
2. **提取文本值**: 从 JS 代码中提取填入的字符串
3. **复用前一步定位器**: 从 `self._records[-1]` 获取前一个 click 步骤的定位器链
4. **生成 fill 代码**: 用前一步的定位器 + 提取的文本值生成 `.fill(value)` TranslatedAction
5. **降级处理**: 如果前一步不是 click，或提取不到值/定位器，保留原始 evaluate

**新增方法签名**:
```python
def _try_convert_evaluate_to_fill(
    self, action_dict: dict, translated: TranslatedAction,
) -> TranslatedAction | None
```
返回 `None` 表示无法转换，保留原始 evaluate。调用位置: `append_step` 中翻译完成后、创建 StepRecord 之前。

**不修改的文件**: `action_translator.py`, `agent_service.py`

---

### P3: 不可达字段的优雅降级（可选，低优先级）

**问题**: 当页面状态不符合预期（如前置步骤未正确执行导致目标字段不存在），测试直接 HealerError 失败。

**可能的方案**:
- 增加 `skip_on_missing` 配置项，定位器全部失败时记录 warning 并继续而非 raise
- 或在回退链中增加 evaluate-based 的 JavaScript 降级方案

**暂不实施**，等 P1/P2 修复后再评估是否需要。

## 测试验证方法

1. 修复后重新触发一次 "销售出库-未收款测试" 的代码生成
2. 验证生成代码中：
   - CSS filter 包含 `.first`
   - input 操作包含 `.fill("xxx")` 而非只有 `.click()`
3. 执行生成的测试代码，确认 returncode=0

## 相关记忆文件

- `memory/browser-use-cdp-limitations.md` — browser-use CDP 限制说明
- `memory/playwright-codegen-pipeline.md` — 代码生成管道详细说明
- `memory/table-input-visibility-fix.md` — 表格内 input 检测演进
