# 侧边栏导航优化设计文档

**创建日期**: 2026-03-10
**问题场景**: 采购单场景（Phase 6）
**目标**: 解决 Agent 在侧边栏导航阶段陷入循环的问题

---

## 1. 问题诊断

### 1.1 失败现象

从 Phase 6 测试日志分析：
- Run 1: 25 步，超过最大步数
- Run 2: 25 步，超过最大步数
- Run 3: API 调用失败

### 1.2 截图分析

| 步骤 | 页面状态 | 问题 |
|------|----------|------|
| Step 5 | 登录页面 | 正常 |
| Step 6 | 首页（登录成功） | 正常进入 |
| Step 7-25 | 首页（循环） | **陷入循环** |

### 1.3 根本原因

1. **子菜单未展开**: Agent 需要点击"商品采购"展开子菜单
2. **操作方式错误**: 侧边栏可能需要 hover 而非 click
3. **缺乏状态检测**: Agent 没有验证子菜单是否成功展开
4. **循环检测不足**: 虽然有循环检测，但没有有效的恢复策略

---

## 2. 优化方案

采用 **Prompt + 执行层组合优化**：

### 2.1 Prompt 层优化

**文件**: `backend/agent_simple/prompts.py`

#### 改进点 1: 增强 hover 动作说明

```python
## ⚠️ 侧边栏导航规则（更新版）

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

### 侧边栏导航示例（更新版）

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

#### 改进点 2: 添加循环避免规则

```python
### 循环避免规则

如果连续 3 步页面状态相同（URL 和主要内容未变）：
1. 立即停止当前操作
2. 分析：可能需要换一种操作方式（click → hover 或 hover → click）
3. 或者：可能需要滚动页面查找目标元素
4. 不要重复执行相同的动作
```

### 2.2 执行层优化

**文件**: `backend/agent_simple/executor.py`

#### 改进点 1: 增强 hover 动作

```python
async def _hover(
    self,
    target: str | None,
    elements: list[InteractiveElement],
) -> ActionResult:
    """悬停在目标元素上（用于菜单展开）"""
    if not target:
        return ActionResult(success=False, error="悬停目标不能为空")

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
            return ActionResult(success=False, error=f"无法找到元素: {target}")
```

#### 改进点 2: 添加菜单项智能检测

```python
async def _detect_menu_item(self, locator) -> bool:
    """检测元素是否是可展开的菜单项

    Returns:
        True 如果元素是可展开的菜单项
    """
    try:
        element = await locator.element_handle(timeout=3000)
        is_menu = await self.page.evaluate("""
            (el) => {
                // 检查是否有子菜单
                const has_submenu = el.querySelector('ul, .submenu, .sub-menu, .children');
                // 检查是否有展开箭头
                const text = el.textContent || '';
                const has_arrow = text.includes('▶') || text.includes('▼') || text.includes('▸') || text.includes('▾');
                // 检查是否在导航区域内
                const is_nav_item = el.closest('nav, .menu, .sidebar, .nav, .ant-menu, .el-menu') !== null;
                // 检查是否有下拉相关的 class
                const has_dropdown_class = el.classList.contains('dropdown') ||
                                           el.classList.contains('has-submenu') ||
                                           el.getAttribute('aria-haspopup') === 'true';

                return !!(has_submenu || has_arrow || (is_nav_item && has_dropdown_class));
            }
        """, element)
        return is_menu
    except Exception as e:
        logger.debug(f"菜单检测失败: {e}")
        return False
```

#### 改进点 3: 增强 click 动作的菜单处理

```python
async def _click(
    self,
    target: str | None,
    elements: list[InteractiveElement],
) -> ActionResult:
    """点击目标元素 - 增强菜单处理"""
    if not target:
        return ActionResult(success=False, error="点击目标不能为空")

    locator = await self._locate_element(target, elements)

    if locator:
        try:
            # 检测是否可能是菜单项
            is_menu_item = await self._detect_menu_item(locator)

            if is_menu_item:
                # 菜单项：先尝试 hover 展开子菜单
                try:
                    await locator.hover(timeout=self.timeout)
                    await self.page.wait_for_timeout(800)
                    logger.info(f"菜单项悬停成功: {target}")
                    # 不直接返回成功，继续执行 click（有些菜单需要 click）
                except Exception:
                    pass  # hover 失败，继续尝试 click

            # 执行正常点击
            await locator.click(timeout=self.timeout)
            logger.info(f"点击成功: {target}")
            return ActionResult(success=True)

        except Exception as e:
            # ... 现有的 fallback 逻辑保持不变
```

---

## 3. 预期效果

| 指标 | 优化前 | 优化后目标 |
|------|--------|------------|
| 采购单场景步数 | 25+ | ≤ 15 |
| 采购单场景成功率 | 0% | 100% |
| 侧边栏导航步数 | 10+ | ≤ 4 |

---

## 4. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| hover 导致误触发其他菜单 | 低概率 | 限制 hover 等待时间 |
| 菜单检测误判 | 中等 | 保留原有 click 逻辑作为 fallback |
| 特殊 UI 框架不兼容 | 中等 | 支持主流框架（Ant Design、Element UI）|

---

## 5. 测试计划

1. **单元测试**: 测试 `_detect_menu_item` 方法
2. **集成测试**: 运行采购单场景，验证导航步骤减少
3. **回归测试**: 确保登录场景仍然通过

---

## 6. 实施任务

1. 更新 `prompts.py` 中的侧边栏导航规则
2. 在 `executor.py` 中添加 `_detect_menu_item` 方法
3. 修改 `_click` 方法增加菜单智能处理
4. 运行采购单场景测试验证效果
