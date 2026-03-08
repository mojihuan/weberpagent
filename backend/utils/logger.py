"""结构化日志工具"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class StructuredLogger:
    """结构化日志记录器，输出 JSONL 格式"""

    def __init__(self, output_dir: str, task_id: str):
        """初始化日志记录器

        Args:
            output_dir: 输出根目录
            task_id: 任务 ID，用于创建日志文件名
        """
        self.log_dir = Path(output_dir) / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"{task_id}.jsonl"

    def log_step(
        self,
        step: int,
        action: str,
        selector: str | None,
        reasoning: str,
        success: bool,
        screenshot_path: str | None = None,
        error: str | None = None,
        **extra: Any,
    ) -> None:
        """记录执行步骤

        Args:
            step: 步骤编号
            action: 执行的动作类型
            selector: 目标元素选择器
            reasoning: AI 的推理说明
            success: 是否成功
            screenshot_path: 截图文件路径
            error: 错误信息（如果有）
            **extra: 其他额外字段
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "action": action,
            "selector": selector,
            "reasoning": reasoning,
            "success": success,
            "screenshot": screenshot_path,
            "error": error,
            **extra,
        }
        self._write_entry(entry)

    def log_error(self, step: int, error: str, **extra: Any) -> None:
        """记录错误信息"""
        self.log_step(
            step=step,
            action="error",
            selector=None,
            reasoning="",
            success=False,
            error=error,
            **extra,
        )

    def log_summary(
        self,
        total_steps: int,
        success: bool,
        duration_seconds: float,
        **extra: Any,
    ) -> None:
        """记录执行摘要"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "summary",
            "total_steps": total_steps,
            "success": success,
            "duration_seconds": duration_seconds,
            **extra,
        }
        self._write_entry(entry)

    def _write_entry(self, entry: dict) -> None:
        """写入日志条目"""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def get_log_file(self) -> str:
        """获取日志文件路径"""
        return str(self.log_file)
