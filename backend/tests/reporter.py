"""Phase 4 测试报告模块"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class TestResult:
    """单个测试结果"""
    scenario: str
    success: bool
    steps: int
    duration: float
    error: Optional[str]
    screenshots: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Phase4Report:
    """Phase 4 测试报告"""
    date: str
    results: list[TestResult]

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.success)

    @property
    def failed(self) -> int:
        return self.total - self.passed

    @property
    def pass_rate(self) -> float:
        return self.passed / self.total if self.total > 0 else 0

    @property
    def avg_steps(self) -> float:
        return sum(r.steps for r in self.results) / self.total if self.total > 0 else 0

    @property
    def avg_duration(self) -> float:
        return sum(r.duration for r in self.results) / self.total if self.total > 0 else 0

    def print_summary(self):
        """打印报告摘要"""
        print("\n" + "=" * 50)
        print("Phase 4 测试报告")
        print("=" * 50)
        print()
        print(f"{'场景':<20} {'成功':<6} {'步数':<6} {'耗时':<8}")
        print("-" * 50)

        for r in self.results:
            status = "✅" if r.success else "❌"
            print(f"{r.scenario:<20} {status:<6} {r.steps:<6} {r.duration:.1f}s")

        print("-" * 50)
        print(f"总计通过率: {self.pass_rate:.0%} ({self.passed}/{self.total})")
        print(f"平均步数: {self.avg_steps:.1f}")
        print(f"平均耗时: {self.avg_duration:.1f}s")
        print("=" * 50)

    def to_json(self) -> dict:
        """转换为 JSON 格式"""
        return {
            "phase": "Phase 4",
            "date": self.date,
            "results": [r.to_dict() for r in self.results],
            "summary": {
                "total": self.total,
                "passed": self.passed,
                "failed": self.failed,
                "pass_rate": self.pass_rate,
                "avg_steps": self.avg_steps,
                "avg_duration": self.avg_duration,
            }
        }

    def save(self, path: Path):
        """保存报告到文件"""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_json(), f, ensure_ascii=False, indent=2)
        print(f"\n报告已保存: {path}")
