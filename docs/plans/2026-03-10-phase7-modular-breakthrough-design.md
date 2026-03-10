# Phase 7 设计：采购单场景分模块突破

> 设计日期：2026-03-10
> 维护者：Claude

## 1. 背景与目标

### 1.1 背景

Phase 6 采购单场景测试 3 轮全部失败：
- 第 1 轮：25 步，超时
- 第 2 轮：25 步，超时
- 第 3 轮：API 错误

核心失败原因：
1. 侧边栏导航循环 - Agent 在"商品采购"菜单上陷入循环
2. 子菜单未展开 - 点击后子菜单没有出现
3. 循环恢复机制无效

### 1.2 目标

**核心目标**：采购单场景端到端成功（从登录到表单提交完成）

**策略**：分模块突破 - 将复杂场景拆分为 5 个独立模块，逐个验证通过

**成功标准**：
- 5 个模块全部通过
- 最终整合测试连续 2 次通过

---

## 2. 模块拆分

| 模块 | 名称 | 任务描述 | 成功标准 |
|------|------|----------|----------|
| M1 | 登录验证 | 打开首页 → 输入账号密码 → 点击登录 → 验证登录成功 | 单次通过 |
| M2 | 侧边栏一级菜单 | 点击"采购管理" → 验证菜单展开/子菜单出现 | 连续 2 次通过 |
| M3 | 侧边栏二级菜单 | 点击"采购订单" → 点击"商品采购" → 验证页面跳转 | 连续 2 次通过 |
| M4 | 表单填写 | 点击"新增" → 填写设备类型 → 填写必填字段 | 连续 2 次通过 |
| M5 | 提交验证 | 点击提交/保存 → 验证成功提示或列表出现新记录 | 连续 2 次通过 |

**整合测试**：M1→M2→M3→M4→M5 完整流程，连续 2 次通过

**阻塞策略**：不设轮次上限，每个模块必须通过才能进入下一个

---

## 3. 测试架构

### 3.1 目录结构

```
backend/tests/
├── modules/                          # 模块测试目录
│   ├── __init__.py
│   ├── test_m1_login.py              # M1: 登录验证
│   ├── test_m2_sidebar_l1.py         # M2: 侧边栏一级菜单
│   ├── test_m3_sidebar_l2.py         # M3: 侧边栏二级菜单
│   ├── test_m4_form.py               # M4: 表单填写
│   ├── test_m5_submit.py             # M5: 提交验证
│   └── test_integration.py           # 整合测试
├── conftest.py                       # 共享 fixtures（复用 Phase 4）
└── run_phase7.py                     # 统一运行入口
```

### 3.2 运行方式

```bash
# 运行单个模块
python -m backend.tests.run_phase7 --module m1

# 运行所有模块（顺序执行）
python -m backend.tests.run_phase7 --all

# 运行整合测试
python -m backend.tests.run_phase7 --integration
```

---

## 4. 输出目录结构

```
outputs/tests/phase7/
├── m1_login/
│   ├── screenshots/
│   └── report.json
├── m2_sidebar_l1/
│   ├── run1/
│   ├── run2/
│   └── summary.json
├── m3_sidebar_l2/
│   ├── run1/
│   ├── run2/
│   └── summary.json
├── m4_form/
│   ├── run1/
│   ├── run2/
│   └── summary.json
├── m5_submit/
│   ├── run1/
│   ├── run2/
│   └── summary.json
├── integration/
│   ├── run1/
│   ├── run2/
│   └── summary.json
└── phase7_final_report.json         # 最终汇总报告
```

---

## 5. 各模块详细设计

### 5.1 M1: 登录验证

```python
# test_m1_login.py
任务: "登录系统"
验证点:
  - URL 变为首页/仪表盘
  - 页面包含用户名或退出按钮
复用: Phase 5 已验证成功，直接复用
```

### 5.2 M2: 侧边栏一级菜单（重点）

```python
# test_m2_sidebar_l1.py
任务: "点击侧边栏'采购管理'菜单"
起点: 登录成功后的首页
验证点:
  - "采购管理"菜单展开
  - 子菜单项可见（如"采购订单"）

关键优化:
  1. Prompt: 添加"等待菜单展开"指导
  2. 执行器: 点击后等待 1-2 秒，检测子元素变化
  3. 反思: 如果子菜单未出现，尝试悬停(hover)
```

### 5.3 M3: 侧边栏二级菜单（重点）

```python
# test_m3_sidebar_l2.py
任务: "依次点击'采购订单' → '商品采购'"
起点: M2 完成后的状态（采购管理已展开）
验证点:
  - URL 变为商品采购页面
  - 页面包含"新增"按钮或采购列表

关键优化:
  1. 感知: 增强子菜单元素识别
  2. 执行器: 支持连续菜单点击的链式操作
```

### 5.4 M4: 表单填写

```python
# test_m4_form.py
任务: "点击新增按钮，填写采购表单"
起点: M3 完成后的商品采购页面
验证点:
  - 表单页面打开
  - 必填字段已填写

关键优化:
  1. Prompt: 下拉框操作指导（先展开再选择）
  2. 执行器: 增强下拉框处理逻辑
```

### 5.5 M5: 提交验证

```python
# test_m5_submit.py
任务: "提交表单并验证成功"
起点: M4 完成后的表单页面
验证点:
  - 成功提示出现，或
  - 列表页出现新记录

关键优化:
  1. Prompt: 添加"提交成功判断"指导
  2. 反思: 检测 toast 通知、页面跳转等成功信号
```

---

## 6. 核心优化项

基于 Phase 6 失败分析，本阶段需要重点实现：

| 优化项 | 位置 | 说明 |
|--------|------|------|
| **悬停支持** | `executor.py` | 新增 `hover` 动作类型，用于菜单展开 |
| **菜单展开检测** | `perception.py` | 点击后检测子元素是否出现 |
| **等待子菜单** | `agent.py` | 点击菜单后增加智能等待 |
| **侧边栏 Prompt** | `prompts.py` | 添加侧边栏导航专门指导 |

### 6.1 悬停支持实现

```python
# executor.py
async def _hover(
    self,
    target: str,
    elements: list[InteractiveElement],
) -> ActionResult:
    """悬停在元素上（用于菜单展开）"""
    locator = await self._locate_element(target, elements)
    if locator:
        await locator.hover(timeout=5000)
        # 等待子菜单出现
        await self.page.wait_for_timeout(500)
        return ActionResult(success=True, message=f"悬停在 '{target}' 上")
    return ActionResult(success=False, error=f"未找到元素: {target}")
```

### 6.2 菜单展开检测

```python
# perception.py
async def detect_menu_expanded(
    self,
    menu_text: str,
    before_elements: list[InteractiveElement],
) -> bool:
    """检测菜单是否展开（子元素数量增加）"""
    current_elements = await self.get_interactive_elements()
    before_count = len([e for e in before_elements if menu_text in e.text])
    current_count = len([e for e in current_elements if menu_text in e.text])
    return current_count > before_count
```

### 6.3 侧边栏导航 Prompt

```python
# prompts.py - 添加到系统提示词
SIDEBAR_NAVIGATION_RULES = """
## 侧边栏导航规则

1. **菜单展开方式**
   - 首先尝试点击菜单项
   - 如果子菜单未出现，尝试悬停(hover)在菜单上
   - 等待 1-2 秒让子菜单展开

2. **多级菜单处理**
   - 一级菜单 → 等待展开 → 二级菜单 → 等待展开 → 三级菜单
   - 每次只操作一个菜单层级

3. **菜单状态判断**
   - 如果菜单已展开，直接点击子菜单
   - 如果菜单未展开，先展开再点击子菜单

4. **示例**
   任务：导航到"采购管理 → 采购订单 → 商品采购"

   Step 1: {"thought": "点击'采购管理'展开菜单", "action": "click", "target": "采购管理"}
   Step 2: {"thought": "等待菜单展开后，点击'采购订单'", "action": "click", "target": "采购订单"}
   Step 3: {"thought": "点击'商品采购'进入页面", "action": "click", "target": "商品采购"}
"""
```

---

## 7. 实施计划

| 步骤 | 任务 | 预计耗时 |
|------|------|----------|
| 7.1 | 创建测试目录结构和运行脚本 | 0.5h |
| 7.2 | 实现 hover 动作支持 (`executor.py`) | 0.5h |
| 7.3 | 增强菜单展开检测 (`perception.py`) | 0.5h |
| 7.4 | 更新侧边栏导航 Prompt (`prompts.py`) | 0.5h |
| 7.5 | 编写 M1 测试脚本（复用 Phase 5） | 0.25h |
| 7.6 | 编写 M2 测试脚本并验证 | 1h |
| 7.7 | 编写 M3 测试脚本并验证 | 1h |
| 7.8 | 编写 M4 测试脚本并验证 | 1h |
| 7.9 | 编写 M5 测试脚本并验证 | 1h |
| 7.10 | 编写整合测试并验证 | 1h |
| 7.11 | 生成最终报告，更新文档 | 0.5h |

**总计**：约 8-9 小时

---

## 8. 完成标准

- [ ] M1 登录验证：单次通过
- [ ] M2 侧边栏一级菜单：连续 2 次通过
- [ ] M3 侧边栏二级菜单：连续 2 次通过
- [ ] M4 表单填写：连续 2 次通过
- [ ] M5 提交验证：连续 2 次通过
- [ ] 整合测试：连续 2 次通过
- [ ] 生成 Phase 7 测试报告
- [ ] 更新 `docs/progress.md`
- [ ] 更新 `docs/1_后端主计划.md`

---

## 9. 风险与应对

| 风险 | 可能性 | 应对措施 |
|------|--------|----------|
| 悬停无法展开菜单 | 中 | 尝试点击 + 等待组合策略 |
| 子菜单元素识别困难 | 中 | 增强 DOM 提取，添加更多选择器 |
| 表单字段动态变化 | 低 | 增加页面状态检测 |
| 提交成功信号不稳定 | 中 | 多种成功信号检测（toast、URL、列表） |
