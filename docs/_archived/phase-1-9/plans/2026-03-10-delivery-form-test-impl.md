# 发货单表单填写测试实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 创建发货单表单填写测试用例，验证 SimpleAgent 能否完成 ERP 系统复杂表单填写任务

**Architecture:** 使用 SimpleAgent + Playwright，在单个 pytest 测试用例中完成登录 → 导航 → 填写表单 → 提交 → 验证的完整流程

**Tech Stack:** Python, pytest, Playwright, SimpleAgent, QwenChat

---

## Task 1: 创建测试文件骨架

**Files:**
- Create: `backend/tests/test_delivery_form.py`

**Step 1: 创建测试文件骨架**

```python
"""发货单表单填写测试

测试 SimpleAgent 能否完成 ERP 系统复杂表单（发货单）的填写任务。
"""

import asyncio
import os
import random
import string

import pytest
from playwright.async_api import async_playwright

from backend.agent_simple.agent import SimpleAgent
from backend.llm.qwen import QwenChat


def generate_random_delivery_data():
    """生成随机发货单数据"""
    suffix = ''.join(random.choices(string.ascii_lowercase, k=6))
    return {
        'receiver': f'测试收货人_{suffix}',
        'phone': f'1{random.choice("3456789")}{random.randint(100000000, 999999999)}',
        'address': f'测试地址_{suffix}号',
    }


async def main():
    """主函数 - 直接运行测试"""
    print("\n=== 发货单表单填写测试 ===\n")

    # 检查 API Key
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("⚠️ DASHSCOPE_API_KEY 未配置，跳过测试")
        return

    test_data = generate_random_delivery_data()
    print(f"测试数据: {test_data}")

    # TODO: 实现测试逻辑

    print("\n✅ 测试完成")


if __name__ == "__main__":
    asyncio.run(main())
```

**Step 2: 验证文件创建成功**

Run: `python -c "from backend.tests.test_delivery_form import generate_random_delivery_data; print(generate_random_delivery_data())"`
Expected: 输出类似 `{'receiver': '测试收货人_xxx', 'phone': '1xxxxxxxxxx', 'address': '测试地址_xxx号'}`

**Step 3: Commit**

```bash
git add backend/tests/test_delivery_form.py
git commit -m "test: 添加发货单表单填写测试骨架"
```

---

## Task 2: 实现完整测试用例

**Files:**
- Modify: `backend/tests/test_delivery_form.py`

**Step 1: 添加 pytest 测试用例**

在 `main()` 函数之前添加：

```python
@pytest.mark.asyncio
async def test_delivery_form_fill():
    """测试发货单表单填写完整流程

    测试流程：
    1. 登录 ERP 系统
    2. 导航到：商品采购 → 采购管理 → 新增发货单
    3. 点击"+新增"打开表单弹窗
    4. 填写发货单信息
    5. 保存发货单
    6. 在列表中搜索确认发货单已创建
    """
    # 检查 API Key
    if not os.getenv("DASHSCOPE_API_KEY"):
        pytest.skip("DASHSCOPE_API_KEY 未配置")

    # 生成随机测试数据
    test_data = generate_random_delivery_data()

    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # 创建 Agent
        llm = QwenChat(model="qwen-vl-max")
        agent = SimpleAgent(
            task=f"""
            执行发货单填写任务：
            1. 打开 https://erptest.epbox.cn/
            2. 登录 ERP（用户名：Y59800075，密码：Aa123456）
            3. 导航到：侧边栏 商品采购 → 采购管理 → 新增发货单
            4. 点击"+新增"按钮打开表单弹窗
            5. 填写发货单信息：
               - 收货人：{test_data['receiver']}
               - 电话：{test_data['phone']}
               - 地址：{test_data['address']}
               - 添加至少一个商品明细（如果需要选择商品，选择第一个可用的）
            6. 点击保存按钮提交表单
            7. 在发货单列表中搜索 {test_data['receiver']}，确认发货单已创建
            8. 任务完成
            """,
            llm=llm,
            page=page,
            output_dir="outputs/tests/delivery_form",
            max_steps=30,  # 复杂场景需要更多步骤
            max_retries=3,
        )

        # 执行任务
        result = await agent.run()

        # 打印结果详情
        print(f"\n=== 执行结果 ===")
        print(f"成功: {result.success}")
        if result.result:
            print(f"结果: {result.result}")
        if result.error:
            print(f"错误: {result.error}")
        print(f"总步数: {len(result.steps)}")

        # 打印每一步
        print(f"\n=== 执行步骤 ===")
        for step in result.steps:
            status = "✅" if step.result.success else "❌"
            print(f"Step {step.step_num}: {step.action.action} -> {step.action.target or ''} {status}")

        await browser.close()

        # 断言
        assert result.success, f"测试失败: {result.error}"
```

**Step 2: 更新 main 函数调用测试用例**

```python
async def main():
    """主函数 - 直接运行测试"""
    await test_delivery_form_fill()
    print("\n=== 测试完成 ===")
```

**Step 3: 验证语法正确**

Run: `python -m py_compile backend/tests/test_delivery_form.py`
Expected: 无输出（编译成功）

**Step 4: Commit**

```bash
git add backend/tests/test_delivery_form.py
git commit -m "test: 实现发货单表单填写完整测试用例"
```

---

## Task 3: 添加结果报告生成

**Files:**
- Modify: `backend/tests/test_delivery_form.py`

**Step 1: 添加结果报告生成函数**

在 `generate_random_delivery_data()` 之后添加：

```python
def generate_test_report(result, test_data, output_dir="outputs/tests/delivery_form"):
    """生成测试报告"""
    import json
    from pathlib import Path
    from datetime import datetime

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    report = {
        "timestamp": datetime.now().isoformat(),
        "success": result.success,
        "result": result.result,
        "error": result.error,
        "total_steps": len(result.steps),
        "test_data": test_data,
        "steps": [
            {
                "step_num": step.step_num,
                "action": step.action.action,
                "target": step.action.target,
                "value": step.action.value,
                "thought": step.action.thought,
                "success": step.result.success,
                "error": step.result.error,
                "screenshot": step.result.screenshot_path,
            }
            for step in result.steps
        ],
    }

    report_path = output_path / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n📄 测试报告已保存: {report_path}")

    return report_path
```

**Step 2: 在测试用例中调用报告生成**

在 `await browser.close()` 之前添加：

```python
        # 生成测试报告
        generate_test_report(result, test_data)
```

**Step 3: 验证语法正确**

Run: `python -m py_compile backend/tests/test_delivery_form.py`
Expected: 无输出（编译成功）

**Step 4: Commit**

```bash
git add backend/tests/test_delivery_form.py
git commit -m "test: 添加发货单测试结果报告生成"
```

---

## Task 4: 运行测试验证

**Step 1: 运行测试（pytest 方式）**

Run: `pytest backend/tests/test_delivery_form.py -v --tb=short`
Expected: 测试运行，输出执行步骤

**Step 2: 或直接运行（调试模式）**

Run: `python -m backend.tests.test_delivery_form`
Expected: 测试运行，输出执行步骤

**Step 3: 检查输出目录**

Run: `ls -la outputs/tests/delivery_form/`
Expected: 包含截图文件和测试报告 JSON

---

## 验收清单

| 检查项 | 命令 |
|--------|------|
| 语法检查 | `python -m py_compile backend/tests/test_delivery_form.py` |
| pytest 运行 | `pytest backend/tests/test_delivery_form.py -v` |
| 直接运行 | `python -m backend.tests.test_delivery_form` |
| 截图生成 | `ls outputs/tests/delivery_form/*.jpg` |
| 报告生成 | `ls outputs/tests/delivery_form/*.json` |
