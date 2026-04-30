# 定位器策略改进设计

日期: 2026-04-30

## 问题

生成测试代码在 ERP 系统执行时失败。具体案例：
1. "销售出库" 菜单点击回退到泛化 CSS 选择器 `li.el-menu-item`，点了错误元素
2. 后续 "请选择客户" 因页面未正确加载而找不到
3. 级联失败导致整个测试用例失败

## 根因

1. **CSS class 选择器太泛化**：`_build_class_selector` 生成的 `tag.className.first` 在 Element UI 应用中匹配所有同类组件
2. **无前置等待**：回退定位器直接执行操作，不验证元素是否已在 DOM 中渲染

## 方案

### 改动 1：CSS 选择器增加文本过滤

文件：`backend/core/locator_chain_builder.py`

修改 `_build_class_selector` 方法：
- 增加 `ax_name` 参数
- 当 `ax_name` 存在时：`page.locator("tag.className").filter(has_text="文本")`
- 当 `ax_name` 不存在时：仍用 `.first`（兜底）

改动范围：
- `_build_class_selector` 签名增加参数
- `extract` 方法调用处传入 `ax_name`

### 改动 2：回退链前置等待

文件：`backend/core/action_translator.py`

修改 `_build_fallback_code` 方法：
- 回退定位器（第 2、3 个）在操作前先 `wait_for(state="visible", timeout=3000)`
- 首定位器不额外等待（Playwright actionability check 已覆盖）

改动范围：
- `_build_fallback_code` 中 locators[1] 和 locators[2] 的代码生成逻辑

## 不变

- 定位器优先级顺序不变（role → text → placeholder → ID → CSS → XPath）
- 最多 3 个定位器的限制不变
- 单定位器代码生成不变（已有 wait_for 重试）
- 其他操作类型（navigate, scroll, send_keys 等）不变
