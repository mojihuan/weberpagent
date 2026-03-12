"""任务存储服务 - JSON 文件实现"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.api.schemas.index import Task


class TaskStore:
    """任务存储"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.data_dir / "tasks.json"
        self._ensure_file()

    def _ensure_file(self) -> None:
        """确保文件存在"""
        if not self.file_path.exists():
            self._save([])

    def _load(self) -> list[dict]:
        """加载所有任务"""
        with open(self.file_path, encoding="utf-8") as f:
            return json.load(f)

    def _save(self, tasks: list[dict]) -> None:
        """保存所有任务"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2, default=str)

    def create(
        self,
        name: str,
        description: str,
        target_url: str = "",
        max_steps: int = 10,
        status: str = "draft",
        assertions: list | None = None,
    ):
        """创建任务"""
        from backend.api.schemas.index import Task

        tasks = self._load()
        now = datetime.now()
        task_data = {
            "id": str(uuid.uuid4())[:8],
            "name": name,
            "description": description,
            "target_url": target_url,
            "max_steps": max_steps,
            "status": status,
            "assertions": [a.model_dump() for a in assertions] if assertions else [],
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }
        tasks.append(task_data)
        self._save(tasks)
        return Task(**task_data)

    def get(self, task_id: str):
        """获取单个任务"""
        from backend.api.schemas.index import Task

        for task in self._load():
            if task["id"] == task_id:
                return Task(**task)
        return None

    def list(self):
        """列出所有任务"""
        from backend.api.schemas.index import Task

        return [Task(**t) for t in self._load()]

    def update(self, task_id: str, **kwargs):
        """更新任务"""
        from backend.api.schemas.index import Task

        tasks = self._load()
        for i, task in enumerate(tasks):
            if task["id"] == task_id:
                task.update(kwargs)
                task["updated_at"] = datetime.now().isoformat()
                tasks[i] = task
                self._save(tasks)
                return Task(**task)
        return None

    def delete(self, task_id: str) -> bool:
        """删除任务"""
        tasks = self._load()
        original_len = len(tasks)
        tasks = [t for t in tasks if t["id"] != task_id]
        if len(tasks) < original_len:
            self._save(tasks)
            return True
        return False
