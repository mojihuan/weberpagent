"""LLM 模块工具函数"""

import base64
from pathlib import Path


def encode_image_to_base64(image_path: str) -> str:
    """将图像文件编码为 base64 字符串

    Args:
        image_path: 图像文件路径

    Returns:
        base64 编码的字符串

    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 不支持的图像格式
    """
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"图像文件不存在: {image_path}")

    # 支持的格式
    supported_formats = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
    if path.suffix.lower() not in supported_formats:
        raise ValueError(f"不支持的图像格式: {path.suffix}")

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
