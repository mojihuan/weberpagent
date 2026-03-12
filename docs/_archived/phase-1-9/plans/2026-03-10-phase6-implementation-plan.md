# Phase 6: 采购表单测试与优化 实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 让采购单场景连续 2 次运行通过，验证 Agent 的稳定性。

**Architecture:** 采用迭代策略，先通过 Prompt 优化解决问题，如果不行再分析原因针对性修复。复用 Phase 4 的测试框架，新增 Phase 6 专用运行脚本。

**Tech Stack:** Python, Playwright. 通义千问 qwen-vl-max. pytest

---

## Task 1: 分析 Phase 4 失败原因

> 目的： 了解采购单场景失败的具体原因，确定优化方向
> 输出: 失败原因分析报告

**文件:**
- 读取: `outputs/tests/phase4/phase4_report.json`
- 读取: `outputs/tests/phase4/purchase/` 目录下的日志（如有）
- 创建: `docs/plans/phase6-failure-analysis.md`

**Step 1: 读取 Phase 4 测试报告**

```python
import json
from pathlib import Path

report_path = Path("outputs/tests/phase4/phase4_report.json")
with open(report_path) as f:
    report = json.load(f)

# 分析采购单场景
purchase_result = report["results"][1]  # 第二个是采购单
print(f"场景: {purchase_result['scenario']}")
print(f"成功: {purchase_result['success']}")
print(f"步数: {purchase_result['steps']}")
print(f"错误: {purchase_result['error']}")
```

**Step 2: 分析失败原因**

根据报告数据，可能的失败原因：
1. 超过最大步数 25 步
2. 可能卡在侧边栏导航（多级菜单）
3. 可能卡在表单填写（复杂控件）

**Step 3: 记录分析结果**

创建文件记录分析结论，为后续优化提供方向。

---

## Task 2: Prompt 优化 - 添加侧边栏导航指导
> 目的: 在系统提示词中添加侧边栏多级导航的指导规则
> 输出: 更新后的 `prompts.py`

**文件:**
- 修改: `backend/agent_simple/prompts.py:156-156` (SYSTEM_PROMPT)

**Step 1: 在 SYSTEM_PROMPT 中添加侧边栏导航规则**

在 `## ⚠️ 登录场景特殊处理` 之前添加：

```python
## ⚠️ 侧边栏导航规则（非常重要！）
### 多级菜单导航
很多 ERP 系统使用多级侧边栏菜单进行导航。
**导航规则：**
1. **逐级点击**： 侧边栏菜单需要逐级展开
   - 示例： 商品采购 → 采购管理 → 新增采购单
   - 每次点击展开下一级菜单
2. **判断菜单状态**:
   - 如果菜单项旁边有 ▶ 箭头，表示有子菜单
   - 如果菜单已展开，再次点击会收起
3. **等待展开完成**:
   - 点击后等待子菜单出现
   - 不要连续快速点击多个菜单项
### 侧边栏导航示例
任务：点击"新增采购单"
页面元素：
- [0] <DIV> 文本: "商品采购"（一级菜单）
- [1] <DIV> 文本: "采购管理"（子菜单，需要先展开"商品采购"）
- [2] <DIV> 文本: "新增采购单"（目标菜单）
正确操作：
Step 1: {"thought": "首先点击一级菜单'商品采购'展开子菜单", "action": "click", "target": "商品采购", "done": false}
Step 2: {"thought": "子菜单已展开，点击'采购管理'", "action": "click", "target": "采购管理", "done": false}
Step 3: {"thought": "点击'新增采购单'进入表单页", "action": "click", "target": "新增采购单", "done": false}
```

**Step 2: 验证修改**

检查 SYSTEM_PROMPT 的完整性，确保：
- 格式正确（缩进、换行）
- 新增内容与现有内容协调
- 没有破坏现有规则

---

## Task 3: Prompt 优化 - 添加表单填写指导
> 目的: 在系统提示词中添加表单填写的指导规则
> 输出: 更新后的 `prompts.py`

**文件:**
- 修改: `backend/agent_simple/prompts.py` (继续 Task 2 的修改)

**Step 1: 在 SYSTEM_PROMPT 中添加表单填写规则**

在侧边栏导航规则之后添加.

```python
## ⚠️ 表单填写规则（非常重要！）
### 常见表单控件类型
| 控件类型 | 识别特征 | 操作方式 |
|----------|----------|----------|
| 文本输入框 | placeholder 属性 | 直接 input |
| 下拉选择器 | 有下拉箭头 ▼ | 先 click 展开，再 click 选项 |
| 日期选择器 | 日历图标 | 先 click 打开，再 click 日期 |
| 单选按钮 | radio 类型 | click 选中 |
| 复选框 | checkbox 类型 | click 勾选 |
### 表单填写流程
1. **识别必填字段**: 通常有 * 标记或红色边框
2. **逐个填写**: 按从上到下的顺序填写
3. **检查完整性**: 提交前确认所有必填项已填写
4. **点击提交**: 通常是"保存"、"提交"、"确定"等按钮
### 表单填写示例
任务：填写采购单表单
页面元素：
- [0] <SELECT> | placeholder: "请选择设备类型"
- [1] <INPUT> | placeholder: "请输入数量" | ID: "quantity"
- [2] <INPUT> | placeholder: "请选择日期" | 类型: date
- [3] <BUTTON> | 文本: "提交"
正确操作：
Step 1: {"thought": "点击下拉选择器展开选项", "action": "click", "target": "请选择设备类型", "done": false}
Step 2: {"thought": "从下拉选项中选择'手机'", "action": "click", "target": "手机", "done": false}
Step 3: {"thought": "在数量输入框输入 10", "action": "input", "target": "quantity", "value": "10", "done": false}
Step 4: {"thought": "点击日期选择器打开日历", "action": "click", "target": "请选择日期", "done": false}
Step 5: {"thought": "选择今天的日期", "action": "click", "target": "今天", "done": false}
Step 6: {"thought": "所有字段已填写，点击提交", "action": "click", "target": "提交", "done": false}
```

**Step 2: 验证修改**

确保新增内容格式正确，与现有规则协调。

---

## Task 4: 创建 Phase 6 运行脚本
> 目的: 创建专用的 Phase 6 测试运行脚本，支持多次迭代
> 输出: `backend/tests/run_phase6.py`

**文件:**
- 创建: `backend/tests/run_phase6.py`
- 参考: `backend/tests/run_phase4.py`

**Step 1: 创建运行脚本**

```python
"""Phase 6 采购表单测试与优化

迭代运行采购单场景测试，直到连续 2 次通过或达到最大轮次 3
"""

import asyncio
import os
import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from playwright.async_api import async_playwright

from backend.agent_simple.agent import SimpleAgent
from backend.llm.qwen import QwenChat
from backend.tests.reporter import TestResult, Phase4Report
import yaml


def load_config():
    """加载测试配置"""
    config_path = Path(__file__).parent.parent / "config" / "test_targets.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


async def run_purchase_test(page, llm, config, output_dir) -> TestResult:
    """运行采购单测试"""
    purchase_config = config["purchase"]
    login_config = config["login"]
    task_output = output_dir / "purchase"
    task_output.mkdir(parents=True, exist_ok=True)

    device_types = "、".join(purchase_config["device_types"])
    navigation = purchase_config["navigation"]

    task = f"""
    在 ERP 系统完成新增采购单操作：
    1. 打开 {config['base_url']}
    2. 在账号输入框输入 {login_config['account']}
    3. 在密码输入框输入 {login_config['password']}
    4. 点击登录按钮
    5. 登录成功后，逐级点击侧边栏菜单：
       - 点击"{navigation[0]}"
       - 等待子菜单展开后，点击"{navigation[1]}"
       - 点击"{navigation[2]}"
    6. 点击"{purchase_config['add_button']}"按钮
    7. 选择设备类型（可选： {device_types}）
    8. 填写表单中的必填字段（根据页面实际情况填写）
    9. 点击提交或保存按钮
    10. 确认成功（检测是否出现新记录或成功提示）
    """

    agent = SimpleAgent(
        task=task,
        llm=llm,
        page=page,
        output_dir=str(task_output),
        max_steps=25,
        max_retries=3,
    )

    start_time = time.time()
    result = await agent.run()
    duration = time.time() - start_time

    screenshots = [str(s) for s in task_output.glob("*.png")]

    return TestResult(
        scenario="新增采购单",
        success=result.success,
        steps=len(result.steps),
        duration=duration,
        error=result.error if not result.success else None,
        screenshots=screenshots,
    )


async def run_single_iteration(page, llm, config, output_dir, run_num: int) -> tuple[bool, TestResult]:
    """运行单次测试

    Returns:
        (是否通过, 测试结果)
    """
    print(f"\n{'='*50}")
    print(f"Phase 6 - 第 {run_num} 轮测试")
    print(f"{'='*50}")

    start_time = time.time()
    result = await run_purchase_test(page, llm, config, output_dir)
    duration = time.time() - start_time

    # 打印结果
    print(f"\n结果:")
    print(f"  场景: {result.scenario}")
    print(f"  成功: {'✅' if result.success else '❌'}")
    print(f"  步数: {result.steps}")
    print(f"  耗时: {result.duration:.1f}s")
    if result.error:
        print(f"  错误: {result.error}")

    return result.success, result


async def main():
    """Phase 6 主函数 - 迭代运行直到成功"""
    # 检查 API Key
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("❌ DASHSCOPE_API_KEY 未配置")
        return False

    print("=" * 50)
    print("Phase 6: 采购表单测试与优化")
    print("=" * 50)
    print("目标: 采购单场景连续 2 次通过")
    print("最大迭代轮次: 3")
    print()

    # 加载配置
    config = load_config()

    # 初始化 LLM
    llm = QwenChat(model="qwen-vl-max")

    # 创建输出目录
    output_base = Path("outputs/tests/phase6")
    output_base.mkdir(parents=True, exist_ok=True)

    # 追踪连续成功次数
    consecutive_success = 0
    max_iterations = 3
    all_results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        for iteration in range(1, max_iterations + 1):
            run_dir = output_base / f"run{iteration}"
            run_dir.mkdir(parents=True, exist_ok=True)

            success, result = await run_single_iteration(
                page, llm, config, run_dir, iteration
            )
            all_results.append(result)

            if success:
                consecutive_success += 1
                print(f"\n✅ 第 {iteration} 轮通过！连续成功: {consecutive_success}/2")

                if consecutive_success >= 2:
                    print("\n🎉 目标达成！连续 2 次通过！")
                    break
            else:
                consecutive_success = 0  # 重置连续成功计数
                print(f"\n❌ 第 {iteration} 轮失败，分析原因...")
                # 这里可以添加自动优化逻辑

        await browser.close()

    # 生成汇总报告
    summary = {
        "phase": "Phase 6",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target": "采购单场景连续 2 次通过",
        "max_iterations": max_iterations,
        "consecutive_success": consecutive_success,
        "target_achieved": consecutive_success >= 2,
        "results": [
            {
                "run": i + 1,
                "scenario": r.scenario,
                "success": r.success,
                "steps": r.steps,
                "duration": r.duration,
                "error": r.error,
            }
            for i, r in enumerate(all_results)
        ],
    }

    # 保存汇总报告
    summary_path = output_base / "phase6_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print("Phase 6 测试完成")
    print(f"{'='*50}")
    print(f"总轮次: {len(all_results)}")
    print(f"连续成功: {consecutive_success}/2")
    print(f"目标达成: {'✅' if consecutive_success >= 2 else '❌'}")
    print(f"报告已保存: {summary_path}")

    return consecutive_success >= 2


```

**Step 2: 验证脚本语法**

运行: `python -m py_compile backend/tests/run_phase6.py`
预期: 无输出（语法正确）

---

## Task 5: 第 1 轮测试
> 目的: 运行第 1 轮采购单测试，验证 Prompt 优化效果
> 输出: 测试结果（截图、报告）

**文件:**
- 运行: `backend/tests/run_phase6.py`

**Step 1: 运行第 1 轮测试**

```bash
cd /Users/huhu/project/weberpagent
source venv/bin/activate
python -m backend.tests.run_phase6
```

预期:
- 测试开始运行
- 观察浏览器操作
- 等待测试完成（可能需要 5-10 分钟）
- 记录结果

**Step 2: 分析第 1 轮结果**

如果成功:
- 记录：第 1 轮通过
- 准备第 2 轮验证
如果失败:
- 分析失败日志
- 确定是否需要进一步优化

---

## Task 6: 第 2 轮测试（稳定性验证）
> 目的: 验证采购单场景的稳定性
> 输出: 测试结果

**前提条件:**
- 第 1 轮测试已通过

**Step 1: 运行第 2 轮测试**

```bash
cd /Users/huhu/project/weberpagent
source venv/bin/activate
python -m backend.tests.run_phase6
```

注意： 如果第 1 轮失败，脚本会自动进入第 2 轮。

**Step 2: 分析结果**

如果连续 2 次通过:
- ✅ Phase 6 目标达成！
- 进入 Task 8 更新文档
如果未达成:
- 分析失败原因
- 决定是否进入第 3 轮

---

## Task 7: 第 3 轮测试（如需要）
> 目的: 针对性修复后最终验证
> 输出: 测试结果

**前提条件:**
- 前 2 轮未达成连续 2 次通过

**Step 1: 分析前 2 轮失败原因**

查看日志:
```bash
ls outputs/tests/phase6/run1/
ls outputs/tests/phase6/run2/
```

**Step 2: 针对性优化（如果需要）**

根据失败原因，可能需要:
- 调整 Prompt 中的具体规则
- 或跳过优化，直接运行第 3 轮

**Step 3: 运行第 3 轮测试**

```bash
python -m backend.tests.run_phase6
```

---

## Task 8: 更新进度文档
> 目的: 记录 Phase 6 完成情况
> 输出: 更新后的进度文档

**文件:**
- 修改: `docs/progress.md`
- 修改: `docs/1_后端主计划.md`

**Step 1: 更新 progress.md**

在 Phase 6 部分添加完成信息:

```markdown
### Phase 6: 采购表单测试与优化 ✅
- **开始日期**: 2026-03-10
- **完成日期**: 2026-03-10
- **测试结果**: 采购单场景连续 2 次通过
- **任务清单**:
  - [x] 6.1 分析失败原因 ✅
  - [x] 6.2 Prompt 优化（侧边栏导航、表单填写） ✅
  - [x] 6.3 运行采购单场景测试 ✅
  - [x] 6.4 验证稳定性 ✅
  - [x] 6.5 生成报告 ✅
```

**Step 2: 更新 1_后端主计划.md**

勾选 Phase 6 的所有任务.

**Step 3: 提交文档更新**

```bash
git add docs/progress.md docs/1_后端主计划.md
git commit -m "docs: Phase 6 采购表单测试与优化完成"
```

---

## 任务依赖关系
> 明确任务执行顺序
```
Task 1 (分析失败原因)
    │
    ▼
Task 2 (添加侧边栏导航规则)
    │
    ▼
Task 3 (添加表单填写规则)
    │
    ▼
Task 4 (创建运行脚本)
    │
    ▼
Task 5 (第 1 轮测试)
    │
    ├─ 成功 ──→ Task 6 (第 2 轮测试)
    │                   │
    │                   ├─ 成功 ──→ Task 8 (更新文档) ✅ 完成
    │                   │
    │                   └─ 失败 ──→ Task 7 (第 3 轮)
    │
    └─ 失败 ──→ 分析原因
                    │
                    ▼
                Task 7 (第 3 轮)
                    │
                    ▼
                Task 8 (更新文档)
```

## 验收标准

- [ ] 采购单场景连续 2 次运行通过
- [ ] Phase 6 测试报告已生成
- [ ] `docs/progress.md` 已更新
- [ ] `docs/1_后端主计划.md` 任务已勾选

## 预计时间

| 任务 | 预计时间 |
|------|----------|
| Task 1 | 10 分钟 |
| Task 2-3 | 15 分钟 |
| Task 4 | 10 分钟 |
| Task 5 | 10-15 分钟（测试运行） |
| Task 6 | 10-15 分钟（测试运行） |
| Task 7 | 10-15 分钟（如需要） |
| Task 8 | 5 分钟 |
| **总计** | **70-90 分钟** |
