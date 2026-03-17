"""时间计算工具模块

提供时间相关的辅助函数，用于在前置条件中生成动态时间数据。
"""

from datetime import datetime, timedelta


def time_now(offset_minutes: int = 0) -> str:
    """获取当前时间，支持分钟偏移

    Args:
        offset_minutes: 分钟偏移量，正数为未来时间，负数为过去时间

    Returns:
        时间字符串，格式为 "%Y-%m-%d %H:%M:%S"

    Examples:
        time_now()        # "2026-03-17 10:30:00"
        time_now(30)      # "2026-03-17 11:00:00" (30分钟后)
        time_now(-5)      # "2026-03-17 10:25:00" (5分钟前)
    """
    current = datetime.now()
    if offset_minutes != 0:
        current = current + timedelta(minutes=offset_minutes)
    return current.strftime("%Y-%m-%d %H:%M:%S")
