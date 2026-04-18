"""HealerError -- 定位器全部失败时抛出的自定义异常。

包含操作类型、尝试过的定位器列表、原始错误信息。
Phase 84 LLM 修复可捕获此异常并处理。

遵循 TokenFetchError 模式 (auth_service.py)。
"""

from __future__ import annotations


class HealerError(Exception):
    """定位器全部失败时抛出的自定义异常。

    包含足够信息让 Phase 84 LLM 修复使用:
    - action_type: 失败的操作类型 (click_element / input_text)
    - locators: 尝试过的定位器表达式列表
    - original_error: 最后一个定位器的原始 Playwright 错误
    """

    def __init__(
        self,
        action_type: str,
        locators: tuple[str, ...],
        original_error: str,
    ) -> None:
        self.action_type = action_type
        self.locators = locators
        self.original_error = original_error
        super().__init__(
            f"定位器全部失败 [{action_type}]: 尝试过 {len(locators)} 个定位器"
        )

    def __str__(self) -> str:
        return (
            f"定位器全部失败 [{self.action_type}]: "
            f"{', '.join(self.locators)} — {self.original_error}"
        )
