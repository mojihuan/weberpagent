"""执行记录存储服务 - JSON 文件实现"""

import json
import uuid
from datetime import datetime
from pathlib import Path

from backend.api.schemas.index import Run, Step, RunResult


class RunStore:
    """执行记录存储"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.data_dir / "runs.json"
        self._ensure_file()

    def _ensure_file(self) -> None:
        """确保文件存在"""
        if not self.file_path.exists():
            self._save([])

    def _load(self) -> list[dict]:
        """加载所有执行记录"""
        with open(self.file_path, encoding="utf-8") as f:
            return json.load(f)

    def _save(self, runs: list[dict]) -> None:
        """保存所有执行记录"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(runs, f, ensure_ascii=False, indent=2, default=str)

    def create(self, task_id: str) -> Run:
        """创建执行记录"""
        runs = self._load()
        run_data = {
            "id": str(uuid.uuid4())[:8],
            "task_id": task_id,
            "status": "pending",
            "steps": [],
            "result": None,
            "created_at": datetime.now(),
            "started_at": None,
            "completed_at": None,
        }
        runs.append(run_data)
        self._save(runs)
        return Run(**run_data)

    def get(self, run_id: str) -> Run | None:
        """获取单个执行记录"""
        for run in self._load():
            if run["id"] == run_id:
                return Run(**run)
        return None

    def list(self) -> list[Run]:
        """列出所有执行记录"""
        return [Run(**r) for r in self._load()]

    def list_by_task(self, task_id: str) -> list[Run]:
        """按任务 ID 列出执行记录"""
        return [Run(**r) for r in self._load() if r["task_id"] == task_id]

    def update_status(self, run_id: str, status: str) -> Run | None:
        """更新执行状态"""
        runs = self._load()
        for i, run in enumerate(runs):
            if run["id"] == run_id:
                run["status"] = status
                if status == "running":
                    run["started_at"] = datetime.now().isoformat()
                elif status in ("completed", "failed"):
                    run["completed_at"] = datetime.now().isoformat()
                runs[i] = run
                self._save(runs)
                return Run(**run)
        return None

    def add_step(self, run_id: str, step: Step) -> Run | None:
        """添加执行步骤"""
        runs = self._load()
        for i, run in enumerate(runs):
            if run["id"] == run_id:
                run["steps"].append(step.model_dump())
                runs[i] = run
                self._save(runs)
                return Run(**run)
        return None

    def set_result(self, run_id: str, result: RunResult) -> Run | None:
        """设置执行结果"""
        runs = self._load()
        for i, run in enumerate(runs):
            if run["id"] == run_id:
                run["result"] = result.model_dump()
                runs[i] = run
                self._save(runs)
                return Run(**run)
        return None

    def delete(self, run_id: str) -> bool:
        """删除执行记录"""
        runs = self._load()
        original_len = len(runs)
        runs = [r for r in runs if r["id"] != run_id]
        if len(runs) < original_len:
            self._save(runs)
            return True
        return False
