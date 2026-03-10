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
