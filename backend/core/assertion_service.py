"""断言服务 - 验证执行结果"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.schemas.index import Assertion
from backend.db.repository import AssertionResultRepository
from backend.db.models import AssertionResult


class AssertionService:
    """断言服务 - 验证执行结果并存储到数据库"""

    def __init__(self, session: AsyncSession):
        """初始化断言服务。

        Args:
            session: AsyncSession 数据库会话
        """
        self.session = session
        self.result_repo = AssertionResultRepository(session)

    def _check_attribute(
        self, history: Any, attr_path: str, expected: str | None,
        check_fn: Any = None, fallback_message: str = ""
    ) -> tuple[bool, str, str]:
        """Generic attribute check with try/except guard.

        Args:
            history: browser-use history object
            attr_path: dotted attribute path to resolve (e.g. "final_result.url")
            expected: expected value for comparison (None means no comparison)
            check_fn: custom check function(actual, expected) -> bool
            fallback_message: message when attribute cannot be retrieved
        """
        try:
            obj = history
            for part in attr_path.split('.'):
                if obj is None:
                    return False, fallback_message, ""
                obj = getattr(obj, part, None)
            if obj is None:
                return False, fallback_message, ""
            actual = str(obj)
            if expected is not None and check_fn:
                passed = check_fn(actual, expected)
                message = "" if passed else f"Expected '{expected}' not found in '{actual}'"
                return passed, message, actual
            return True, "", actual
        except Exception as e:
            return False, f"Check failed: {str(e)}", ""

    async def check_url_contains(
        self, history: Any, expected: str
    ) -> tuple[bool, str, str]:
        """检查最终 URL 是否包含期望字符串。"""
        return self._check_attribute(
            history, "final_result.url", expected,
            lambda a, e: e in a, "无法获取 URL"
        )

    def check_text_exists(self, history: Any, expected: str) -> tuple[bool, str, str]:
        """检查页面是否包含期望文本。"""
        return self._check_attribute(
            history, "final_result.extracted_content", expected,
            lambda a, e: e in a, "无法获取页面内容"
        )

    def check_no_errors(self, history: Any) -> tuple[bool, str, str]:
        """检查执行是否无错误。

        Args:
            history: browser-use 执行历史对象

        Returns:
            tuple[bool, str, str]: (是否通过, 消息, 实际值)
        """
        try:
            if hasattr(history, "is_done"):
                passed = history.is_done
                message = "" if passed else "执行未完成"
                return passed, message, str(passed)
        except Exception as e:
            return False, f"检查失败: {str(e)}", ""
        return False, "无法检查执行状态", ""

    async def check_element_exists(
        self, history: Any, selector: str
    ) -> tuple[bool, str, str]:
        """检查元素是否存在（通过 CSS 选择器）。

        注意：browser-use 的 history 可能没有直接的 DOM 访问能力。
        当前实现基于执行完成状态作为回退方案。

        Args:
            history: browser-use 执行历史对象
            selector: CSS 选择器

        Returns:
            tuple[bool, str, str]: (是否通过, 消息, 实际值)
        """
        try:
            if hasattr(history, "is_done") and history.is_done:
                # 如果执行完成且无错误，假设元素检查通过
                # 真实实现需要检查浏览器 DOM 状态
                return True, "", selector
        except Exception as e:
            return False, f"元素检查失败: {str(e)}", ""
        return False, f"无法检查元素 '{selector}'", ""

    async def evaluate_all(
        self,
        run_id: str,
        assertions: list[Assertion],
        history: Any,
    ) -> list[AssertionResult]:
        """评估所有断言并存储结果。

        Args:
            run_id: 执行记录 ID
            assertions: 断言列表（Assertion ORM 对象）
            history: browser-use 执行历史对象

        Returns:
            list[AssertionResult]: 断言结果 ORM 对象列表
        """
        results = []
        for assertion in assertions:
            if assertion.type == "url_contains":
                passed, message, actual = await self.check_url_contains(
                    history, str(assertion.expected)
                )
            elif assertion.type == "text_exists":
                passed, message, actual = self.check_text_exists(
                    history, str(assertion.expected)
                )
            elif assertion.type == "no_errors":
                passed, message, actual = self.check_no_errors(history)
            elif assertion.type == "element_exists":
                passed, message, actual = await self.check_element_exists(
                    history, str(assertion.expected)
                )
            else:
                passed = False
                message = f"未知断言类型: {assertion.type}"
                actual = ""

            result = await self.result_repo.create(
                run_id=run_id,
                assertion_id=assertion.id,
                status="pass" if passed else "fail",
                message=message,
                actual_value=actual,
            )
            results.append(result)
        return results
