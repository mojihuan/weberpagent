"""表单填写编排器 - 协调多 Agent 工作流程"""

import logging

from playwright.async_api import Page

from backend.llm.base import BaseLLM
from backend.agent_simple.types import PageState
from backend.agent_simple.form_filler.types import FillResult, ReviewResult, GeneratedCode
from backend.agent_simple.form_filler.code_generator import CodeGenerator
from backend.agent_simple.form_filler.code_reviewer import CodeReviewer
from backend.agent_simple.form_filler.code_optimizer import CodeOptimizer
from backend.agent_simple.form_filler.sandbox import execute_code

logger = logging.getLogger(__name__)


class FormFiller:
    """表单填写编排器 - 协调 CodeGenerator、CodeReviewer、CodeOptimizer"""

    MAX_REVIEW_ROUNDS = 3

    def __init__(self, llm: BaseLLM, page: Page):
        self.llm = llm
        self.page = page
        self.code_generator = CodeGenerator(llm)
        self.code_reviewer = CodeReviewer()
        self.code_optimizer = CodeOptimizer(llm)

    async def fill_form(self, state: PageState, task: str) -> FillResult:
        """填写表单

        流程：
        1. 生成代码
        2. 审查循环（最多 3 轮）
        3. 执行代码
        4. 返回结果
        """
        logger.info(f"开始表单填写流程，任务: {task[:50]}...")

        # 1. 生成代码
        try:
            generated = await self.code_generator.generate(state, task)
        except Exception as e:
            logger.error(f"代码生成失败: {e}")
            return FillResult(success=False, error=f"代码生成失败: {str(e)}")

        code = generated.code

        # 2. 审查循环
        for round_num in range(self.MAX_REVIEW_ROUNDS):
            review_result = self.code_reviewer.review(code, state.elements)

            if review_result.approved:
                logger.info(f"代码审查通过（第 {round_num + 1} 轮）")
                break

            logger.info(f"代码审查未通过（第 {round_num + 1} 轮），尝试优化...")

            try:
                code = await self.code_optimizer.optimize(
                    code, state.elements, review_result.issues
                )
            except Exception as e:
                logger.error(f"代码优化失败: {e}")

        # 3. 执行代码
        try:
            await self._execute_code(code)
            logger.info("代码执行成功")
        except Exception as e:
            error_msg = str(e)
            logger.warning(f"代码执行失败: {error_msg}")

            # 尝试一次优化后重新执行
            try:
                optimized_code = await self.code_optimizer.optimize(
                    code, state.elements, execution_error=error_msg
                )
                await self._execute_code(optimized_code)
                code = optimized_code
                logger.info("优化后执行成功")
            except Exception as retry_error:
                return FillResult(
                    success=False,
                    error=f"执行失败: {error_msg}，重试失败: {str(retry_error)}",
                )

        return FillResult(success=True, code=code)

    async def _execute_code(self, code: str) -> None:
        """执行代码"""
        result = await execute_code(code, {"page": self.page})
        if not result["success"]:
            raise Exception(result.get("error", "未知执行错误"))