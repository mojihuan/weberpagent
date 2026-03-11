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

        # 生成测试报告
        generate_test_report(result, test_data)

        await browser.close()

        # 断言
        assert result.success, f"测试失败: {result.error}"


async def main():
    """主函数 - 直接运行测试"""
    await test_delivery_form_fill()
    print("\n=== 测试完成 ===")


if __name__ == "__main__":
    asyncio.run(main())
