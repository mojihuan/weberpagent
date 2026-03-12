# 侧边栏导航优化 实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 优化 Agent 的侧边栏导航能力，解决采购单场景陷入循环的问题

**Architecture:** Prompt 层增强 hover 动作说明 + 执行层添加菜单智能检测。当检测到可展开菜单项时，优先使用 hover 展开子菜单。

**Tech Stack:** Python, Playwright, 通义千问 qwen-vl-max

---

## Task 1: Prompt 层 - 增强侧边栏导航规则

**Files:**
- Modify: `backend/agent_simple/prompts.py:85-112`

**Step 1: 更新侧边栏导航规则**

在 `SYSTEM_PROMPT` 中找到 `## ⚠️ 侧边栏导航规则（非常重要！）` 部分，替换为：

```python
## ⚠️ 侧边栏导航规则（非常重要！）

### 菜单操作优先级

1. **检测菜单类型**:
   - 如果菜单项右侧有 ▶ 或 ▼ 箭头，表示有子菜单
   - 有子菜单的项优先使用 `hover` 动作悬停展开

2. **操作策略**:
   - **优先 hover**: 对有子菜单的项，先用 hover 悬停等待展开
   - **hover 失败再 click**: 如果 hover 后子菜单未出现，尝试 click
   - **验证展开成功**: 操作后必须检查子菜单是否出现

3. **展开成功判断**:
   - 等待 1-2 秒
   - 检查是否有新的菜单项出现
   - 如果没有新项出现，尝试另一种操作

### 循环避免规则

如果连续 3 步页面状态相同（URL 和主要内容未变）：
1. 立即停止当前操作
2. 分析：可能需要换一种操作方式（click → hover 或 hover → click）
3. 或者：可能需要滚动页面查找目标元素
4. 不要重复执行相同的动作

### 多级菜单导航
很多 ERP 系统使用多级侧边栏菜单进行导航。

**导航规则：**
1. **逐级展开**： 侧边栏菜单需要逐级展开
   - 示例： 商品采购 → 采购管理 → 新增采购单
   - 每次操作后等待子菜单出现
2. **判断菜单状态**:
   - 如果菜单项旁边有 ▶ 箭头，表示有子菜单
   - 如果菜单已展开，再次点击会收起
3. **等待展开完成**:
   - 操作后等待子菜单出现
   - 不要连续快速点击多个菜单项

### 侧边栏导航示例
任务：点击"新增采购单"

页面元素：
- [0] <DIV> 文本: "商品采购"（一级菜单，有 ▶ 箭头）
- [1] <DIV> 文本: "采购管理"（子菜单，需要先展开"商品采购"）
- [2] <DIV> 文本: "新增采购单"（目标菜单）

正确操作：
Step 1: {"thought": "一级菜单'商品采购'有子菜单箭头，使用 hover 悬停展开", "action": "hover", "target": "商品采购", "done": false}
Step 2: {"thought": "子菜单已展开，点击'采购管理'", "action": "click", "target": "采购管理", "done": false}
Step 3: {"thought": "点击'新增采购单'进入表单页", "action": "click", "target": "新增采购单", "done": false}
```

**Step 2: 验证语法**

Run: `python -m py_compile backend/agent_simple/prompts.py`
Expected: 无输出（语法正确）

**Step 3: Commit**

```bash
git add backend/agent_simple/prompts.py
git commit -m "feat(agent): 增强侧边栏导航 Prompt 规则 - 添加 hover 优先策略和循环避免规则"
```

---

## Task 2: 执行层 - 添加菜单项检测方法

**Files:**
- Modify: `backend/agent_simple/executor.py`

**Step 1: 添加 _detect_menu_item 方法**

在 `Executor` 类中，`_hover` 方法之前添加：

```python
    async def _detect_menu_item(self, locator) -> bool:
        """检测元素是否是可展开的菜单项

        通过检查 DOM 结构判断元素是否是可展开的菜单：
        - 是否有子菜单元素（ul, .submenu 等）
        - 是否有展开箭头（▶, ▼ 等）
        - 是否有下拉相关的 class 或属性

        Args:
            locator: Playwright Locator 对象

        Returns:
            True 如果元素是可展开的菜单项
        """
        try:
            element = await locator.element_handle(timeout=3000)
            is_menu = await self.page.evaluate(
                """
                (el) => {
                    // 检查是否有子菜单
                    const has_submenu = el.querySelector('ul, .submenu, .sub-menu, .children, .ant-menu-sub, .el-submenu__title');
                    // 检查是否有展开箭头
                    const text = el.textContent || '';
                    const has_arrow = text.includes('▶') || text.includes('▼') ||
                                     text.includes('▸') || text.includes('▾') ||
                                     text.includes('►') || text.includes('▽');
                    // 检查是否在导航区域内
                    const is_nav_item = el.closest('nav, .menu, .sidebar, .nav, .ant-menu, .el-menu, .aside') !== null;
                    // 检查是否有下拉相关的 class 或属性
                    const has_dropdown_class = el.classList.contains('dropdown') ||
                                              el.classList.contains('has-submenu') ||
                                              el.classList.contains('ant-menu-submenu') ||
                                              el.classList.contains('el-submenu') ||
                                              el.getAttribute('aria-haspopup') === 'true';

                    return !!(has_submenu || has_arrow || (is_nav_item && has_dropdown_class));
                }
            """,
                element,
            )
            if is_menu:
                logger.debug(f"检测到可展开菜单项")
            return is_menu
        except Exception as e:
            logger.debug(f"菜单检测失败: {e}")
            return False
```

**Step 2: 验证语法**

Run: `python -m py_compile backend/agent_simple/executor.py`
Expected: 无输出（语法正确）

**Step 3: Commit**

```bash
git add backend/agent_simple/executor.py
git commit -m "feat(agent): 添加菜单项智能检测方法 _detect_menu_item"
```

---

## Task 3: 执行层 - 增强 hover 动作

**Files:**
- Modify: `backend/agent_simple/executor.py:240-278`

**Step 1: 更新 _hover 方法**

找到 `_hover` 方法，替换为：

```python
    async def _hover(
        self,
        target: str | None,
        elements: list[InteractiveElement],
    ) -> ActionResult:
        """悬停在目标元素上（用于菜单展开）

        Args:
            target: 目标元素描述
            elements: 可交互元素列表

        Returns:
            ActionResult: 执行结果
        """
        if not target:
            return ActionResult(success=False, error="悬停目标不能为空")

        # 尝试定位元素
        locator = await self._locate_element(target, elements)

        if locator:
            try:
                await locator.hover(timeout=self.timeout)
                # 增加等待时间，确保子菜单展开
                await self.page.wait_for_timeout(1000)
                logger.info(f"悬停成功: {target}")
                return ActionResult(success=True)
            except Exception as e:
                logger.warning(f"悬停失败: {target}, 错误: {e}")
                return ActionResult(success=False, error=f"悬停失败: {str(e)[:100]}")
        else:
            # 直接尝试通过文本悬停
            try:
                await self.page.get_by_text(target).hover(timeout=self.timeout)
                await self.page.wait_for_timeout(1000)
                logger.info(f"通过文本悬停成功: {target}")
                return ActionResult(success=True)
            except Exception as e:
                logger.warning(f"悬停失败: {target}, 错误: {e}")
                return ActionResult(success=False, error=f"无法找到元素: {target}")
```

**Step 2: 验证语法**

Run: `python -m py_compile backend/agent_simple/executor.py`
Expected: 无输出（语法正确）

**Step 3: Commit**

```bash
git add backend/agent_simple/executor.py
git commit -m "feat(agent): 增强 hover 动作 - 增加等待时间确保子菜单展开"
```

---

## Task 4: 执行层 - 增强 click 动作的菜单处理

**Files:**
- Modify: `backend/agent_simple/executor.py:106-159`

**Step 1: 更新 _click 方法**

找到 `_click` 方法，在 `if locator:` 块的开头添加菜单检测逻辑：

```python
    async def _click(
        self,
        target: str | None,
        elements: list[InteractiveElement],
    ) -> ActionResult:
        """点击目标元素"""
        if not target:
            return ActionResult(success=False, error="点击目标不能为空")

        # 尝试定位元素
        locator = await self._locate_element(target, elements)

        if locator:
            try:
                # 检测是否可能是菜单项（有子菜单）
                is_menu_item = await self._detect_menu_item(locator)

                if is_menu_item:
                    # 菜单项：先尝试 hover 展开子菜单
                    try:
                        await locator.hover(timeout=self.timeout)
                        await self.page.wait_for_timeout(800)
                        logger.info(f"菜单项悬停成功: {target}")
                        # 继续执行 click（有些菜单需要 click 才能展开）
                    except Exception as hover_error:
                        logger.debug(f"菜单项 hover 失败: {hover_error}")
                        # hover 失败，继续尝试 click

                # 策略 1: 正常点击
                await locator.click(timeout=self.timeout)
                logger.info(f"点击成功: {target}")
                return ActionResult(success=True)
            except Exception as e:
                error_str = str(e).lower()

                # 策略 2: force 点击（跳过可见性检查）
                if "not visible" in error_str or "covered" in error_str:
                    try:
                        await locator.click(force=True, timeout=self.timeout)
                        logger.info(f"Force 点击成功: {target}")
                        return ActionResult(success=True)
                    except Exception as force_error:
                        pass

                # 策略 3: JavaScript 点击
                try:
                    element_handle = await locator.element_handle(timeout=5000)
                    await self.page.evaluate("el => el.click()", element_handle)
                    logger.info(f"JavaScript 点击成功: {target}")
                    return ActionResult(success=True)
                except Exception as js_error:
                    logger.warning(f"所有点击策略都失败: {target}")

                return ActionResult(success=False, error=f"点击失败: {str(e)[:100]}")
        else:
            # 策略 4: 直接通过文本点击
            try:
                await self.page.get_by_text(target).click(timeout=self.timeout)
                logger.info(f"通过文本点击成功: {target}")
                return ActionResult(success=True)
            except Exception as e:
                # 策略 5: 通过 role 点击
                try:
                    await self.page.get_by_role("button", name=target).click(timeout=self.timeout)
                    logger.info(f"通过 role 点击成功: {target}")
                    return ActionResult(success=True)
                except Exception:
                    return ActionResult(success=False, error=f"无法找到元素: {target}")
```

**Step 2: 验证语法**

Run: `python -m py_compile backend/agent_simple/executor.py`
Expected: 无输出（语法正确）

**Step 3: Commit**

```bash
git add backend/agent_simple/executor.py
git commit -m "feat(agent): 增强 click 动作 - 菜单项智能 hover + click 组合"
```

---

## Task 5: 运行采购单场景测试

**Files:**
- Run: `backend/tests/run_phase6.py`

**Step 1: 运行测试**

Run: `cd /Users/huhu/project/weberpagent && source venv/bin/activate && python -m backend.tests.run_phase6`

Expected:
- 采购单场景成功通过
- 步数 ≤ 15
- 无循环现象

**Step 2: 分析结果**

如果成功：
- 记录测试结果
- 进入 Task 6 更新文档

如果失败：
- 查看截图分析失败点
- 检查是否需要进一步优化

---

## Task 6: 更新进度文档

**Files:**
- Modify: `docs/progress.md`
- Modify: `docs/1_后端主计划.md`

**Step 1: 更新 progress.md**

添加 Phase 6.5 完成记录：

```markdown
### Phase 6.5: 侧边栏导航优化 ✅
- **完成日期**: 2026-03-10
- **更新内容**:
  - 增强 Prompt 侧边栏导航规则（hover 优先策略）
  - 添加菜单项智能检测方法 `_detect_menu_item`
  - 增强 click 动作的菜单处理（hover + click 组合）
  - 采购单场景测试通过
```

**Step 2: Commit**

```bash
git add docs/progress.md docs/1_后端主计划.md
git commit -m "docs: 记录 Phase 6.5 侧边栏导航优化完成"
```

---

## 任务依赖关系

```
Task 1 (Prompt 优化)
    │
    ▼
Task 2 (添加菜单检测方法)
    │
    ▼
Task 3 (增强 hover 动作)
    │
    ▼
Task 4 (增强 click 动作)
    │
    ▼
Task 5 (运行测试)
    │
    ├─ 成功 ──→ Task 6 (更新文档) ✅ 完成
    │
    └─ 失败 ──→ 分析原因 → 针对性修复 → 重新运行 Task 5
```

## 验收标准

- [ ] Prompt 中添加了 hover 优先策略和循环避免规则
- [ ] `_detect_menu_item` 方法添加成功
- [ ] `_hover` 方法等待时间增加到 1000ms
- [ ] `_click` 方法增加了菜单智能处理
- [ ] 采购单场景测试通过（步数 ≤ 15）
- [ ] `docs/progress.md` 已更新

## 预计时间

| 任务 | 预计时间 |
|------|----------|
| Task 1 | 5 分钟 |
| Task 2 | 5 分钟 |
| Task 3 | 5 分钟 |
| Task 4 | 10 分钟 |
| Task 5 | 15-20 分钟（测试运行）|
| Task 6 | 5 分钟 |
| **总计** | **45-50 分钟** |
