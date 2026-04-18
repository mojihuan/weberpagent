"""SelfHealingRunner -- pytest re-execution orchestrator with LLM retry loop.

Implements the final layer of the three-tier self-healing pipeline:
  1. Locator fallback (80%) - LocatorChainBuilder
  2. LLM repair (15%) - LLMHealer
  3. Agent re-execution (5%) - SelfHealingRunner (this module)

Orchestrates:
  - Running generated Playwright code via subprocess pytest
  - Retrying with LLM feedback on failure (max 2 retries)
  - Persisting healing status to the database

Per D-01: subprocess pytest execution
Per D-04: skip when AuthService fails or no login_role
Per D-06: LLM repair on pytest failure
Per D-07: max 2 retries (3 total iterations)
Per D-08: replace code in DB on success
"""

import ast
import asyncio
import dataclasses
import json
import logging
import re
import subprocess
from pathlib import Path
from typing import Any

from backend.core.auth_service import TokenFetchError, auth_service
from backend.core.llm_healer import LLMHealer

logger = logging.getLogger(__name__)

PYTEST_TIMEOUT_SECONDS = 120

CONFTEST_TEMPLATE = '''"""Auto-generated conftest for Playwright storage_state injection."""
import json
from pathlib import Path

import pytest
from playwright.sync_api import BrowserContext


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Inject storage_state from .storage_state.json in the test file directory."""
    state_file = Path(__file__).parent / ".storage_state.json"
    if state_file.exists():
        with open(state_file, encoding="utf-8") as f:
            return {**browser_context_args, "storage_state": json.load(f)}
    return browser_context_args
'''


@dataclasses.dataclass(frozen=True)
class HealingResult:
    """Immutable result from the self-healing re-execution pipeline.

    Attributes:
        final_status: "passed", "failed", or "skipped"
        attempts: Number of pytest execution attempts (0 for skipped)
        error_message: Error output from the last failed attempt (empty on pass/skip)
        repaired_code_path: Path to the final test file (may differ if LLM repaired)
    """

    final_status: str
    attempts: int
    error_message: str
    repaired_code_path: str


class SelfHealingRunner:
    """Orchestrates pytest re-execution with LLM repair retry loop.

    Takes a generated Playwright test file, runs it via subprocess pytest,
    and retries with LLM-based repair on failure.
    """

    def __init__(self, llm_config: dict) -> None:
        self._llm_config = llm_config
        self._logger = logging.getLogger(__name__)

    async def run(
        self,
        run_id: str,
        test_file_path: str,
        login_role: str | None,
        base_dir: str = "outputs",
    ) -> HealingResult:
        """Execute the self-healing re-execution pipeline.

        Args:
            run_id: Execution record ID.
            test_file_path: Path to the generated pytest test file.
            login_role: ERP login role (e.g. "main"). None = skip.
            base_dir: Base output directory.

        Returns:
            HealingResult with final status and attempt count.
        """
        # D-04: 无 login_role 时跳过
        if not login_role:
            self._logger.info(f"[{run_id}] 无 login_role, 跳过自愈重执行")
            return HealingResult(
                final_status="skipped",
                attempts=0,
                error_message="",
                repaired_code_path=test_file_path,
            )

        # D-04: AuthService 失败时跳过
        try:
            storage_state = await auth_service.get_storage_state_for_role(login_role)
        except TokenFetchError as exc:
            self._logger.warning(
                f"[{run_id}] AuthService 失败, 跳过自愈重执行: {exc}"
            )
            return HealingResult(
                final_status="skipped",
                attempts=0,
                error_message=str(exc),
                repaired_code_path=test_file_path,
            )

        output_dir = Path(test_file_path).parent

        # 写入 storage state 和 conftest
        state_path = output_dir / ".storage_state.json"
        state_path.write_text(
            json.dumps(storage_state, ensure_ascii=False), encoding="utf-8"
        )
        self._generate_conftest(output_dir)

        last_error = ""
        max_iterations = 3  # 1 initial + 2 retries (per D-07)

        try:
            for iteration in range(1, max_iterations + 1):
                self._logger.info(
                    f"[{run_id}] 自愈重执行第 {iteration}/{max_iterations} 次"
                )

                # D-01: subprocess pytest 执行
                try:
                    proc_result = await asyncio.to_thread(
                        subprocess.run,
                        [
                            "uv", "run", "pytest",
                            test_file_path,
                            "--headed=false",
                            "--timeout=60",
                            "-v",
                        ],
                        capture_output=True,
                        text=True,
                        timeout=PYTEST_TIMEOUT_SECONDS,
                    )
                except subprocess.TimeoutExpired:
                    self._logger.warning(
                        f"[{run_id}] pytest 超时 ({PYTEST_TIMEOUT_SECONDS}s)"
                    )
                    last_error = f"pytest 执行超时 ({PYTEST_TIMEOUT_SECONDS}s)"
                    if iteration < max_iterations:
                        repair_ok = await self._llm_repair(
                            run_id, test_file_path, last_error, base_dir
                        )
                        if not repair_ok:
                            self._logger.warning(
                                f"[{run_id}] LLM 修复失败, 继续重试"
                            )
                    continue

                # D-08: pytest 通过
                if proc_result.returncode == 0:
                    self._logger.info(
                        f"[{run_id}] 自愈重执行通过 (第 {iteration} 次)"
                    )
                    self._cleanup(output_dir)
                    return HealingResult(
                        final_status="passed",
                        attempts=iteration,
                        error_message="",
                        repaired_code_path=test_file_path,
                    )

                # pytest 失败: 提取错误输出
                last_error = (
                    proc_result.stderr.strip()
                    if proc_result.stderr.strip()
                    else proc_result.stdout.strip()
                )
                self._logger.warning(
                    f"[{run_id}] pytest 失败 (第 {iteration} 次): "
                    f"{last_error[:200]}"
                )

                # D-06: 非最后一次迭代时调用 LLM 修复
                if iteration < max_iterations:
                    repair_ok = await self._llm_repair(
                        run_id, test_file_path, last_error, base_dir
                    )
                    if not repair_ok:
                        self._logger.warning(
                            f"[{run_id}] LLM 修复失败, 继续重试"
                        )

            # D-07: 超过最大重试次数
            self._logger.warning(
                f"[{run_id}] 自愈重执行失败 (共 {max_iterations} 次)"
            )
            self._cleanup(output_dir)
            return HealingResult(
                final_status="failed",
                attempts=max_iterations,
                error_message=self._truncate_error(last_error),
                repaired_code_path=test_file_path,
            )
        except Exception as exc:
            self._logger.error(
                f"[{run_id}] 自愈重执行异常: {exc}", exc_info=True
            )
            self._cleanup(output_dir)
            return HealingResult(
                final_status="failed",
                attempts=0,
                error_message=str(exc),
                repaired_code_path=test_file_path,
            )

    async def _llm_repair(
        self,
        run_id: str,
        test_file_path: str,
        error_output: str,
        base_dir: str,
    ) -> bool:
        """尝试用 LLM 修复失败的测试文件.

        Args:
            run_id: 执行记录 ID.
            test_file_path: 测试文件路径.
            error_output: pytest 输出的错误信息.
            base_dir: 输出基础目录.

        Returns:
            True if repair was applied, False otherwise.
        """
        test_path = Path(test_file_path)
        if not test_path.exists():
            self._logger.warning(f"[{run_id}] 测试文件不存在: {test_file_path}")
            return False

        current_code = test_path.read_text(encoding="utf-8")

        # 尝试从 pytest traceback 中提取行号
        line_number = self._extract_error_line(error_output)

        # 读取 DOM snapshot (优先 step_1, 后备 step_1)
        dom_content = self._read_dom_snapshot(run_id, base_dir, error_output)

        # 调用 LLMHealer
        healer = LLMHealer(self._llm_config)
        try:
            result = await healer.heal(
                action_type="fix_test",
                failed_locators=(error_output[:500],),
                dom_snapshot=dom_content,
                action_params={},
            )
        except Exception as exc:
            self._logger.warning(f"[{run_id}] LLM heal 异常: {exc}")
            return False

        if not result.success:
            self._logger.warning(f"[{run_id}] LLM heal 返回失败")
            return False

        # 用 LLM 修复的代码替换失败行
        repaired_code = self._apply_fix(
            current_code, result.code_snippet, line_number
        )
        if repaired_code is None:
            self._logger.warning(f"[{run_id}] 无法应用 LLM 修复到测试文件")
            return False

        # ast.parse 验证
        try:
            ast.parse(repaired_code)
        except SyntaxError:
            self._logger.warning(f"[{run_id}] LLM 修复后语法验证失败")
            return False

        test_path.write_text(repaired_code, encoding="utf-8")
        self._logger.info(f"[{run_id}] LLM 修复已应用到测试文件")
        return True

    def _generate_conftest(self, output_dir: Path) -> None:
        """在输出目录生成 conftest.py 文件."""
        conftest_path = output_dir / "conftest.py"
        conftest_path.write_text(CONFTEST_TEMPLATE, encoding="utf-8")

    def _cleanup(self, output_dir: Path) -> None:
        """清理临时文件 (storage state + conftest).

        Non-blocking: errors are logged but not raised.
        """
        for filename in (".storage_state.json", "conftest.py"):
            try:
                file_path = output_dir / filename
                if file_path.exists():
                    file_path.unlink()
            except OSError as exc:
                self._logger.warning(
                    f"清理文件失败 {output_dir / filename}: {exc}"
                )

    @staticmethod
    def _truncate_error(error: str, max_length: int = 2000) -> str:
        """截断错误信息, 保留尾部 (最近 traceback 在末尾)."""
        if len(error) <= max_length:
            return error
        return "..." + error[-(max_length - 3):]

    @staticmethod
    def _extract_error_line(error_output: str) -> int | None:
        """从 pytest traceback 提取失败行号."""
        # 匹配 "test_xxx.py:42" 或 "test_xxx.py:42: Error" 模式
        match = re.search(r"test_\w+\.py:(\d+)", error_output)
        if match:
            return int(match.group(1))
        # 匹配 "line 42" 模式
        match = re.search(r"line (\d+)", error_output)
        if match:
            return int(match.group(1))
        return None

    @staticmethod
    def _read_dom_snapshot(
        run_id: str, base_dir: str, error_output: str
    ) -> str:
        """读取 DOM 快照文件内容.

        优先从错误输出中提取步骤号, 否则使用 step_1 作为后备.
        """
        # 尝试从错误输出中提取步骤号
        step_match = re.search(r"step[_\s](\d+)", error_output, re.IGNORECASE)
        step_num = int(step_match.group(1)) if step_match else 1

        dom_path = Path(base_dir) / run_id / "dom" / f"step_{step_num}.txt"
        if dom_path.exists():
            return dom_path.read_text(encoding="utf-8")

        # 后备: step_1
        fallback_path = Path(base_dir) / run_id / "dom" / "step_1.txt"
        if fallback_path.exists():
            return fallback_path.read_text(encoding="utf-8")

        return f"(无 DOM 快照: step_{step_num})"

    @staticmethod
    def _apply_fix(
        current_code: str,
        fix_snippet: str,
        line_number: int | None,
    ) -> str | None:
        """将 LLM 修复代码应用到源代码中.

        如果有行号, 替换该行. 否则追加到文件末尾的函数体内.

        Returns:
            修复后的代码, 或 None 如果无法应用.
        """
        lines = current_code.splitlines()

        if line_number is not None and 1 <= line_number <= len(lines):
            # 替换指定行 (1-indexed)
            new_lines = [
                *lines[: line_number - 1],
                fix_snippet,
                *lines[line_number:],
            ]
            return "\n".join(new_lines)

        # 无行号: 在最后一个非空行之前插入
        # 找到最后一个包含 "page." 的行并替换
        for i in range(len(lines) - 1, -1, -1):
            if "page." in lines[i]:
                new_lines = [
                    *lines[:i],
                    fix_snippet,
                    *lines[i + 1:],
                ]
                return "\n".join(new_lines)

        # 最后手段: 追加到末尾
        return current_code + "\n" + fix_snippet + "\n"
