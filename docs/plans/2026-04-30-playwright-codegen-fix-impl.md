# Playwright 测试代码生成修复 — 实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 修复 interacted_element 数据管道断裂问题，使生成的 Playwright 测试代码包含真实定位器而非占位符；优化定位器优先级策略。

**Architecture:** 在 step_callback 中从 browser_state.dom_state.selector_map 提取 DOMInteractedElement 并注入 action_dict，下游 ActionTranslator 和 LocatorChainBuilder 无需修改。

**Tech Stack:** Python 3.11, browser-use (DOMInteractedElement, SerializedDOMState), 现有 ActionTranslator/LocatorChainBuilder

---

## 关键数据结构参考

```
browser_state: BrowserStateSummary
  .dom_state: SerializedDOMState
    .selector_map: dict[int, EnhancedDOMTreeNode]  # index → DOM node

agent_output: AgentOutput
  .action: list[ActionModel]
    [0].get_index() → int | None  # 获取目标元素的 index

DOMInteractedElement.load_from_enhanced_dom_tree(EnhancedDOMTreeNode) → DOMInteractedElement
  属性: x_path, node_name, attributes, ax_name, bounds, ...
```

---

### Task 1: 修复 interacted_element 数据管道

**Files:**
- Modify: `backend/core/agent_service.py:441-477` (step_callback)

**Step 1: 在 step_callback 中注入 interacted_element**

在 `agent_service.py` 的 `_create_step_callback` 方法中，`step_callback` 函数体内，紧接在 `_extract_agent_output` 调用之后（当前 line 444），添加 interacted_element 提取逻辑：

```python
# 当前代码 (line 444):
action, action_name, action_params, action_dict, reasoning = svc._extract_agent_output(run_id, agent_output)

# 在其后添加:
# 从 browser_state 提取 interacted_element 并注入 action_dict
if action_dict and browser_state and hasattr(browser_state, 'dom_state'):
    try:
        from browser_use.dom.views import DOMInteractedElement
        selector_map = browser_state.dom_state.selector_map
        first_action = agent_output.action[0]
        index = first_action.get_index()
        if index is not None and index in selector_map:
            action_dict["interacted_element"] = DOMInteractedElement.load_from_enhanced_dom_tree(
                selector_map[index]
            )
        else:
            action_dict["interacted_element"] = None
    except Exception as e:
        logger.warning(f"[{run_id}] 提取 interacted_element 失败: {e}")
        action_dict["interacted_element"] = None
```

**设计说明：**
- 复用 `AgentHistory.get_interacted_element()` 的相同逻辑（browser_use/agent/views.py:499-508）
- 数据来源（selector_map、agent_output.action）在回调中均已可用
- 异常不中断主流程，降级为 None（等同于当前行为）
- import 放在条件块内，避免循环依赖

**Step 2: 验证修改**

Run: `cd /Users/huhu/project/weberpagent && uv run python -c "from backend.core.agent_service import AgentService; print('import OK')"`

**Step 3: 提交**

```bash
git add backend/core/agent_service.py
git commit -m "fix: inject interacted_element into action_dict in step_callback"
```

---

### Task 2: 优化定位器优先级 — 提升 get_by_role

**Files:**
- Modify: `backend/core/locator_chain_builder.py:62-83`

**Step 1: 调整 LocatorChainBuilder.extract() 中的定位器顺序**

当前顺序：text → role → placeholder → ID → data-testid → XPath
调整为：**text + role 并列第一**（因为 role 定位器基于 ARIA 语义，比 CSS 定位器更稳定）

修改 `locator_chain_builder.py` 的 `extract()` 方法（当前 line 62-82），将 get_by_text 和 get_by_role 的生成逻辑合并到同一个判断块中：

```python
# 替换当前的 # 1. get_by_text 和 # 2. get_by_role 块为:
# 1. 语义定位器 — text 和 role 并列优先
if ax_name:
    escaped_name = _escape_string(ax_name)
    role = _NODE_TO_ROLE.get(elem.node_name)

    if role:
        # 有映射 role 时，role+name 最稳定（语义锚定 ARIA）
        locators.append(
            f'page.get_by_role("{role}", name="{escaped_name}")'
        )

    # text 定位器作为第二选择
    if len(ax_name) <= 4:
        locators.append(
            f'page.get_by_text("{escaped_name}", exact=True)'
        )
    else:
        locators.append(
            f'page.get_by_text("{escaped_name}")'
        )
```

**设计说明：**
- 有 `ax_name` 且有映射 role 时，`get_by_role("button", name="提交")` 优先于 `get_by_text("提交")`
- role 定位器锚定在 ARIA 语义上，比纯文本匹配更精确（区分同文本不同角色）
- 无映射 role 的元素（如 `<div>`）仍然优先使用 text 定位器
- 保留 <= 4 字符精确匹配策略

**Step 2: 验证修改**

Run: `cd /Users/huhu/project/weberpagent && uv run python -c "from backend.core.locator_chain_builder import LocatorChainBuilder; b = LocatorChainBuilder(); print('import OK')"`

**Step 3: 提交**

```bash
git add backend/core/locator_chain_builder.py
git commit -m "refactor: prioritize get_by_role over get_by_text in locator chain"
```

---

### Task 3: 端到端验证

**Step 1: 手动触发一次 agent 运行**

通过前端或 API 触发一个测试任务（如 "销售出库-未收款测试"），观察生成的代码。

**Step 2: 检查生成代码质量**

验证生成代码中：
- click 操作有真实的定位器（如 `page.get_by_role("button", name="提交")`）
- input 操作有真实定位器（如 `page.get_by_placeholder("请输入")`）
- 不再出现 `TODO: 定位器缺失`
- 定位器 fallback 链（最多 3 层 try-except）正确生成

**Step 3: 记录结果**

将生成代码样本保存到 `outputs/` 目录，记录修复前后对比。
