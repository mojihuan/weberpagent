"""Per-run structured file logger (JSONL format).

Provides RunLogger that creates a per-run output directory structure
and writes structured JSONL log entries for post-mortem analysis.

Directory structure created per run:
    outputs/{run_id}/logs/run.jsonl
    outputs/{run_id}/dom/step_{N}.txt
    outputs/{run_id}/screenshots/step_{N}.png
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class RunLogger:
    """Per-run structured file logger writing JSONL entries."""

    def __init__(self, run_id: str, base_dir: str = "outputs") -> None:
        self.run_id = run_id
        self.base_dir = Path(base_dir)

        # Create directory structure
        self.run_dir = self.base_dir / run_id
        self.logs_dir = self.run_dir / "logs"
        self.dom_dir = self.run_dir / "dom"
        self.screenshots_dir = self.run_dir / "screenshots"

        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.dom_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)

        # Open JSONL file
        self._log_file_path = self.logs_dir / "run.jsonl"
        self._file_handle = open(
            self._log_file_path, "a", encoding="utf-8"
        )

    @property
    def log_file_path(self) -> str:
        return str(self._log_file_path)

    def log(
        self,
        level: str,
        category: str,
        message: str,
        **extra: Any,
    ) -> None:
        """Write one JSONL log entry.

        Args:
            level: Log level (info, warning, error, debug).
            category: Log category (step, browser, agent, system).
            message: Human-readable message.
            **extra: Additional fields merged into the entry.
        """
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "category": category,
            "message": message,
            "run_id": self.run_id,
            **extra,
        }
        self._write_entry(entry)

    def log_browser(
        self,
        url: str,
        dom_content: str,
        step: int,
        element_count: int,
    ) -> str:
        """Log browser state and save DOM snapshot to file.

        Args:
            url: Current browser URL.
            dom_content: Full DOM text content.
            step: Step number.
            element_count: Number of elements in DOM.

        Returns:
            Relative path to the saved DOM file.
        """
        # Save DOM to file
        dom_filename = f"step_{step}.txt"
        dom_path = self.dom_dir / dom_filename
        dom_path.write_text(dom_content, encoding="utf-8")
        dom_relative = f"{self.run_id}/dom/{dom_filename}"

        # Write JSONL entry
        self.log(
            level="info",
            category="browser",
            message=f"Browser state at step {step}",
            url=url,
            dom_length=len(dom_content),
            step=step,
            element_count=element_count,
            dom_file=dom_relative,
        )

        return dom_relative

    def log_agent(
        self,
        action_name: str,
        action_params: dict,
        reasoning: str,
        step: int,
    ) -> None:
        """Log an agent action with reasoning.

        Args:
            action_name: Name of the action (e.g. click, type, navigate).
            action_params: Parameters of the action.
            reasoning: AI reasoning text.
            step: Step number.
        """
        self.log(
            level="info",
            category="agent",
            message=f"Agent action: {action_name}",
            action_name=action_name,
            action_params=action_params,
            reasoning=reasoning,
            step=step,
        )

    def _write_entry(self, entry: dict) -> None:
        """Append a JSONL entry to the log file."""
        line = json.dumps(entry, ensure_ascii=False)
        self._file_handle.write(line + "\n")
        self._file_handle.flush()

    def close(self) -> None:
        """Close the log file handle."""
        if self._file_handle and not self._file_handle.closed:
            self._file_handle.close()

    def __enter__(self) -> "RunLogger":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()
