"""断言服务 - 验证执行结果"""

from typing import Any

from backend.api.schemas.index import Assertion


class AssertionService:
    """断言服务"""

    def check_url_contains(self, history: Any, expected: str) -> bool:
        """检查最终 URL 是否包含期望字符串"""
        try:
            if hasattr(history, "final_result") and history.final_result:
                url = getattr(history.final_result, "url", "")
                return expected in str(url)
        except Exception:
            pass
        return False

    def check_text_exists(self, history: Any, expected: str) -> bool:
        """检查页面是否包含期望文本"""
        try:
            if hasattr(history, "final_result") and history.final_result:
                text = getattr(history.final_result, "extracted_content", "")
                return expected in str(text)
        except Exception:
            pass
        return False

    def check_no_errors(self, history: Any) -> bool:
        """检查执行是否无错误"""
        try:
            if hasattr(history, "is_done"):
                return history.is_done
        except Exception:
            pass
        return False

    def run_all_assertions(
        self, history: Any, assertions: list[Assertion]
    ) -> dict[str, bool]:
        """运行所有断言"""
        results = {}
        for assertion in assertions:
            if assertion.type == "url_contains":
                results[assertion.name] = self.check_url_contains(
                    history, str(assertion.expected)
                )
            elif assertion.type == "text_exists":
                results[assertion.name] = self.check_text_exists(
                    history, str(assertion.expected)
                )
            elif assertion.type == "no_errors":
                results[assertion.name] = self.check_no_errors(history)
            else:
                results[assertion.name] = False
        return results
