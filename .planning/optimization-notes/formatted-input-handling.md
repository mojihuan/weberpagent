# 格式化输入框处理策略

**发现日期**: 2026-03-19
**里程碑版本**: v0.3.2
**严重级别**: High (影响自动化成功率)

---

## 问题背景

在 ERP 系统自动化测试中，某些输入字段（特别是金额、数字类型）不是普通的文本输入框，而是带有前端格式化逻辑的受控组件。

### 典型表现

当 Agent 尝试使用普通 `input` 指令输入 `150` 时：

```
Step 16: input 150
结果: 0.15000  (输入被追加，且被格式化为小数)

Step 17: input 150 (重试)
结果: 0.15015  (继续追加)

Step 19: input 150
结果: 0.15150015  (值持续错乱)
```

**关键日志提示**:
```
Text field clearing failed, typing may append to existing text
```

### 根本原因

1. **清空失败**: 输入框的清空操作没有真正生效
2. **追加输入**: 键盘输入被当作在已有小数值上继续编辑
3. **自动格式化**: 组件持续按金额/数字格式自动处理输入值
4. **受控组件**: 很可能是表格内嵌的数字组件，受前端框架控制

---

## 尝试过的失败方案

### 方案 A: 普通输入 + clear 参数
```python
controller.input("150", clear=True)
```
**结果**: 失败，clear 没有真正清空

### 方案 B: 键盘快捷键强制清空
```python
controller.click(field)
controller.keyboard("Control+a")
controller.keyboard("Backspace")
controller.input("150")
controller.keyboard("Enter")
```
**结果**: 失败，即使选中+删除，输入框仍不接受纯文本输入

---

## 成功方案: JavaScript 直接赋值

### 关键转折

放弃模拟人工键盘输入，改为直接在页面执行 JavaScript：

```javascript
(function(){
  try {
    // 找到目标输入框
    const field = document.querySelector(
      'td[aria-label*="销售金额"] input, ' +
      'td input[type="text"], ' +
      'td input[role="spinbutton"]'
    );

    if (field) {
      // 设置值
      field.value = '150';

      // 触发事件，让前端框架感知变化
      field.dispatchEvent(new Event('input', { bubbles: true }));
      field.dispatchEvent(new Event('change', { bubbles: true }));
    }
  } catch(e) {
    console.error('JS evaluation failed:', e);
  }
})();
```

### 执行方式

```python
# 使用 browser-use 的 evaluate 动作
controller.evaluate(javascript_code)
```

### 成功证据

```
Step 22: 执行 JavaScript 赋值
Step 23: Successfully set the sales amount to 150 using JavaScript
        - Field now shows 150.00
        - Total sales price shows 150元
```

---

## 技术原理

### 为什么 JS 赋值能成功

1. **绕过输入拦截**: 不触发 keydown/keypress/keyup 事件序列
2. **直接修改 DOM**: 直接设置 `value` 属性
3. **手动触发事件**: 显式调用 `input` 和 `change` 事件，让 React/Vue 等框架感知状态变化
4. **避免格式化逻辑**: 跳过输入框的即时格式化处理

### 前端框架兼容性

| 框架 | 需要触发的事件 |
|------|---------------|
| React | `input` + `change` |
| Vue | `input` |
| Angular | `input` + `change` + `blur` |
| 原生 | `change` |

---

## 后续优化建议

### 1. 自动检测机制

在 Agent 执行输入前，自动检测输入框类型：

```javascript
// 检测是否为格式化输入框
const isFormattedInput = (element) => {
  // 检测常见特征
  const hasSpinner = element.getAttribute('role') === 'spinbutton';
  const hasMask = element.dataset.mask || element.dataset.format;
  const hasNumericPattern = element.type === 'number' || element.inputMode === 'numeric';
  const parentClasses = element.parentElement?.className || '';
  const isAmountField = parentClasses.includes('amount') ||
                        parentClasses.includes('money') ||
                        element.getAttribute('aria-label')?.includes('金额');

  return hasSpinner || hasMask || hasNumericPattern || isAmountField;
};
```

### 2. 智能回退策略

```python
async def smart_input(field, value):
    """智能输入，自动选择最佳方式"""

    # 1. 尝试普通输入
    result = await try_normal_input(field, value)
    if verify_input_success(field, value):
        return result

    # 2. 尝试 Ctrl+A + 输入
    result = await try_select_and_input(field, value)
    if verify_input_success(field, value):
        return result

    # 3. 回退到 JavaScript 赋值
    return await js_set_value(field, value)
```

### 3. Agent Prompt 增强

在系统提示词中添加：

```
对于金额、数字、日期等格式化输入框：
- 如果普通输入失败（值被追加或格式化错误）
- 立即切换到 JavaScript 赋值方式
- 不要在普通输入方式上重试超过 2 次
```

### 4. 输入验证

每次输入后增加验证步骤：

```python
def verify_input_value(field, expected):
    """验证输入是否成功"""
    actual = await get_field_value(field)
    # 处理格式化差异（如 150 vs 150.00）
    return normalize_value(actual) == normalize_value(expected)
```

---

## 适用场景

| 场景 | 推荐方式 |
|------|---------|
| 普通文本输入框 | `input` 指令 |
| 密码框 | `input` 指令 |
| 金额/数字输入框 | **JavaScript 赋值** |
| 日期选择器 | JavaScript 或 日期组件 API |
| 下拉选择框 | `select` 指令 或 JavaScript |
| 富文本编辑器 | JavaScript 设置 innerHTML |

---

## 相关 Issue

- VERIFICATION.md Issue #14: 格式化输入框处理优化

---

## 参考日志

完整日志位于: `playwright-report/` 目录

关键步骤:
- Step 16-21: 普通输入方式失败
- Step 22: JavaScript 赋值成功
- Step 23: 验证成功

---

*本文档记录了 aiDriveUITest 项目在自动化测试中的一个重要技术发现。*
