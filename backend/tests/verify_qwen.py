"""验证通义千问 API 连接"""
import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

load_dotenv()


def verify_qwen() -> bool:
    """验证通义千问 API 能正常调用"""
    print("正在验证通义千问 API...")

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key or api_key == "your_dashscope_api_key_here":
        print("❌ 未配置 DASHSCOPE_API_KEY")
        print("   请在 .env 文件中设置有效的 API Key")
        return False

    try:
        import dashscope
        from dashscope import Generation

        dashscope.api_key = api_key

        response = Generation.call(
            model="qwen-plus",
            prompt="你好，请回复'OK'",
            max_tokens=10,
        )

        if response.status_code == 200:
            print("✅ 通义千问 API 正常")
            print(f"   响应: {response.output.text.strip()}")
            return True
        else:
            print(f"❌ API 调用失败")
            print(f"   状态码: {response.status_code}")
            print(f"   错误信息: {response.message}")
            return False

    except Exception as e:
        print(f"❌ 通义千问验证失败: {e}")
        return False


if __name__ == "__main__":
    result = verify_qwen()
    sys.exit(0 if result else 1)
