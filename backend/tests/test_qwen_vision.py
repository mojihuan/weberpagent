"""验证通义千问视觉能力"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

load_dotenv()


async def test_basic_chat():
    """测试基础文本对话"""
    from backend.llm import QwenChat

    llm = QwenChat()

    response = await llm.chat_with_vision(
        messages=[{"role": "user", "content": "你好，请回复'OK'"}],
        images=[],
    )

    assert response.content, "响应内容不应为空"
    print(f"✅ 基础对话测试通过: {response.content}")
    return True


async def test_vision_with_url():
    """测试图像 URL 理解能力"""
    from backend.llm import QwenChat

    llm = QwenChat()

    # 使用公开测试图片（阿里云官方示例图片）
    test_image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg"

    response = await llm.chat_with_vision(
        messages=[{"role": "user", "content": "请描述这张图片的内容"}],
        images=[test_image],
    )

    assert response.content, "响应内容不应为空"
    print(f"✅ 图像 URL 测试通过: {response.content[:100]}...")
    return True


async def test_action_parsing():
    """测试动作解析能力"""
    from backend.llm import QwenChat

    llm = QwenChat()

    # 模拟包含动作的响应
    test_response = '''
    根据页面内容，我需要点击登录按钮。
    {"action": "click", "selector": "#login-btn", "reasoning": "用户需要登录"}
    '''

    result = llm.parse_action(test_response)

    assert result is not None, "应该能解析出动作"
    assert result.action == "click"
    assert result.selector == "#login-btn"
    print(f"✅ 动作解析测试通过: {result}")
    return True


async def test_vision_with_local_file():
    """测试本地图像文件理解能力"""
    from backend.llm import QwenChat

    llm = QwenChat()

    # 使用 screenshots 目录中的测试图片（如果存在）
    screenshot_dir = Path(__file__).parent.parent.parent / "outputs" / "screenshots"
    test_images = list(screenshot_dir.glob("*.png")) if screenshot_dir.exists() else []

    if not test_images:
        print("⏭️ 跳过本地图像测试（无测试图片）")
        return True

    response = await llm.chat_with_vision(
        messages=[{"role": "user", "content": "请描述这个页面的主要元素"}],
        images=[str(test_images[0])],
    )

    assert response.content, "响应内容不应为空"
    print(f"✅ 本地图像测试通过: {response.content[:100]}...")
    return True


async def main():
    """运行所有验证测试"""
    print("=" * 50)
    print("通义千问视觉能力验证")
    print("=" * 50)

    # 检查 API Key
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key or api_key == "your_dashscope_api_key_here":
        print("❌ 未配置 DASHSCOPE_API_KEY")
        return False

    tests = [
        ("基础对话", test_basic_chat),
        ("图像 URL", test_vision_with_url),
        ("动作解析", test_action_parsing),
        ("本地图像", test_vision_with_local_file),
    ]

    results = []
    for name, test in tests:
        print(f"\n测试: {name}")
        try:
            result = await test()
            results.append((name, result))
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            results.append((name, False))

    print("\n" + "=" * 50)
    print("测试结果汇总:")
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"  {status} {name}")

    all_passed = all(r[1] for r in results)
    print("=" * 50)
    return all_passed


if __name__ == "__main__":
    import asyncio

    success = asyncio.run(main())
    sys.exit(0 if success else 1)
