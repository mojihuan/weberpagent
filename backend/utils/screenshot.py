"""截图文件管理"""

from pathlib import Path
from datetime import datetime


class ScreenshotManager:
    """截图文件管理器"""

    def __init__(self, output_dir: str, task_id: str):
        """初始化截图管理器

        Args:
            output_dir: 输出根目录
            task_id: 任务 ID，用于创建子目录
        """
        self.screenshot_dir = Path(output_dir) / "screenshots" / task_id
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def get_path(self, step: int, suffix: str = "") -> str:
        """生成截图文件路径

        Args:
            step: 步骤编号
            suffix: 文件名后缀（可选）

        Returns:
            截图文件的完整路径
        """
        filename = f"step_{step:03d}{suffix}.png"
        return str(self.screenshot_dir / filename)

    def get_dir(self) -> str:
        """获取截图目录路径"""
        return str(self.screenshot_dir)
