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
from urllib.parse import urlparse

from backend.core.auth_service import TokenFetchError, auth_service
from backend.core.error_classifier import classify_pytest_error
from backend.core.llm_healer import LLMHealer

logger = logging.getLogger(__name__)

PYTEST_TIMEOUT_SECONDS = 120


def _build_storage_state(token: str) -> dict[str, Any]:
    """Construct Playwright storage_state dict from access_token.

    Creates a storage_state with empty cookies and localStorage entries
    for Admin-Token and Admin-Expires-In, targeting the ERP origin.
    """
    from backend.config.settings import get_settings

    settings = get_settings()
    parsed = urlparse(settings.erp_base_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    return {
        "cookies": [],
        "origins": [
            {
                "origin": origin,
                "localStorage": [
                    {"name": "Admin-Token", "value": token},
                    {"name": "Admin-Expires-In", "value": "720"},
                ],
            }
        ],
    }


async def _get_storage_state_for_role(role: str) -> dict[str, Any]:
    """Get storage_state for a role by resolving credentials and fetching token.

    Combines AccountService.resolve() to get credentials,
    auth_service.fetch_token() to get access_token, and _build_storage_state()
    to construct the Playwright storage_state dict.
    """
    from backend.core.account_service import account_service

    account_info = account_service.resolve(role)
    token = await auth_service.fetch_token(
        account_info.account, account_info.password, role=role,
    )
    return _build_storage_state(token)

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
    error_category: str = ""  # 分类结果 (ENV_INTERRUPT/ENV_PYTEST_ERROR/ENV_NO_TESTS/CODE_ERROR/CODE_RUNTIME)


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
            storage_state = await _get_storage_state_for_role(login_role)
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
        classification = None  # 错误分类结果
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
                        error_category="passed",
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

                # 错误分类: 环境错误直接终止, 不调 LLM
                classification = classify_pytest_error(
                    proc_result.returncode, last_error
                )
                if classification.skip_llm_healing:
                    self._logger.info(
                        f"[{run_id}] 环境错误, 跳过 LLM 修复: "
                        f"{classification.user_message}"
                    )
                    self._cleanup(output_dir)
                    return HealingResult(
                        final_status="failed",
                        attempts=iteration,
                        error_message=self._truncate_error(last_error),
                        repaired_code_path=test_file_path,
                        error_category=classification.category.value,
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
                error_category=(
                    classification.category.value if classification else ""
                ),
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
                error_category="",
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

        # 从代码中提取失败行 (用于 DOM 定位器映射)
        failing_line = ""
        if line_number is not None and 1 <= line_number <= len(current_code.splitlines()):
            failing_line = current_code.splitlines()[line_number - 1]

        # 读取 DOM snapshot (优先使用定位器文本搜索)
        dom_content = self._read_dom_snapshot(
            run_id, base_dir, error_output, failing_line,
        )

        # 调用 LLMHealer.repair_code (专用测试修复方法)
        healer = LLMHealer(self._llm_config)
        try:
            result = await healer.repair_code(
                test_code=current_code,
                error_line=line_number,
                error_message=error_output[:1000],
                dom_snapshot=dom_content,
            )
        except Exception as exc:
            self._logger.warning(f"[{run_id}] LLM repair 异常: {exc}")
            return False

        if not result.success:
            self._logger.warning(f"[{run_id}] LLM repair 返回失败")
            return False

        # 检查结构化修复字段
        if not result.target_snippet or not result.replacement:
            self._logger.warning(
                f"[{run_id}] LLM repair 返回空的 target_snippet/replacement"
            )
            return False

        # 用 LLM 修复的代码替换目标片段 (内容匹配, 内含 ast.parse 验证)
        repaired_code = self._apply_fix(
            current_code, result.target_snippet, result.replacement,
        )
        if repaired_code is None:
            self._logger.warning(f"[{run_id}] 无法应用 LLM 修复到测试文件")
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
        run_id: str,
        base_dir: str,
        error_output: str = "",
        failing_line: str = "",
    ) -> str:
        """读取 DOM 快照文件内容.

        Per D-04: 从失败行代码中提取定位器文本，搜索 DOM 快照.
        Per D-05: 独立实现轻量级 DOM 搜索，不复用 dom_patch.py.
        """
        # 1. 从失败行提取定位器文本
        locator_text = SelfHealingRunner._extract_locator_from_code(failing_line)

        # 2. 收集所有 DOM 快照文件
        dom_dir = Path(base_dir) / run_id / "dom"
        if not dom_dir.exists():
            return "(无 DOM 快照目录)"

        dom_files = sorted(dom_dir.glob("step_*.txt"))
        if not dom_files:
            return "(无 DOM 快照文件)"

        # 3. 如果有定位器文本，搜索匹配的 DOM 文件
        if locator_text:
            for dom_file in dom_files:
                content = dom_file.read_text(encoding="utf-8")
                if locator_text in content:
                    return SelfHealingRunner._search_dom_for_text(content, locator_text)
            # 定位器未找到: 返回最后一个 step 的截断内容
            last_content = dom_files[-1].read_text(encoding="utf-8")
            return last_content[:2000] if len(last_content) > 2000 else last_content

        # 4. 无定位器: 后备到 error_output 中的 step 号 (兼容旧路径)
        step_match = re.search(r"step[_\s](\d+)", error_output, re.IGNORECASE)
        step_num = int(step_match.group(1)) if step_match else 1

        dom_path = dom_dir / f"step_{step_num}.txt"
        if dom_path.exists():
            return dom_path.read_text(encoding="utf-8")

        # 最后手段: 第一个 DOM 文件
        fallback = dom_files[0].read_text(encoding="utf-8")
        return fallback[:2000] if len(fallback) > 2000 else fallback

    @staticmethod
    def _extract_locator_from_code(failing_line: str) -> str | None:
        """从失败行代码中提取定位器文本.

        Per D-04: 从代码行中提取定位器字符串，用于 DOM 搜索.
        """
        if not failing_line:
            return None
        # Pattern 1: get_by_text("xxx") -> "xxx"
        match = re.search(r'get_by_text\(["\']([^"\']+)["\']', failing_line)
        if match:
            return match.group(1)
        # Pattern 2: name="xxx" in get_by_role
        match = re.search(r'name=["\']([^"\']+)["\']', failing_line)
        if match:
            return match.group(1)
        # Pattern 3: locator("xxx") or locator('xxx')
        match = re.search(r'locator\(["\']([^"\']+)["\']', failing_line)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def _search_dom_for_text(dom_content: str, search_text: str) -> str:
        """从 DOM 快照中搜索包含指定文本的上下文 (前后各 5 行)."""
        lines = dom_content.splitlines()
        for i, line in enumerate(lines):
            if search_text in line:
                start = max(0, i - 5)
                end = min(len(lines), i + 6)
                return "\n".join(lines[start:end])
        # 后备: 截断的完整 DOM
        return dom_content[:2000] if len(dom_content) > 2000 else dom_content

    @staticmethod
    def _apply_fix(
        current_code: str,
        target_snippet: str,
        replacement: str,
    ) -> str | None:
        """将 LLM 修复代码应用到源代码中 (内容匹配多行替换).

        1. 在 current_code 中搜索 target_snippet
        2. 替换为 replacement (可多行)
        3. ast.parse 验证 -> 失败返回 None (回滚)

        Args:
            current_code: 完整源代码.
            target_snippet: 要替换的原始代码片段 (LLM 从源码中识别).
            replacement: 新代码 (可多行).

        Returns:
            修复后的代码, 或 None 如果无法应用.
        """
        # 防止过短的片段导致多处匹配 (最小 20 字符)
        if len(target_snippet) < 20:
            logger.warning(f"target_snippet 过短 ({len(target_snippet)} 字符), 跳过替换")
            return None

        # 1. 内容匹配: 精确子串搜索
        pos = current_code.find(target_snippet)
        if pos == -1:
            logger.warning("target_snippet 在源代码中未找到")
            return None

        # 2. 替换 (不可变: 返回新字符串)
        new_code = current_code[:pos] + replacement + current_code[pos + len(target_snippet):]

        # 3. ast.parse 验证 (HEAL-04, per D-03)
        try:
            ast.parse(new_code)
        except SyntaxError as e:
            logger.warning(f"修复后 ast.parse 验证失败, 回滚: {e}")
            return None

        return new_code
